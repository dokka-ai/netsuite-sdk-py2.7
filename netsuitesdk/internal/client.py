u"""
    :class:`NetSuiteClient`: client proxy class which uses the python library
    Zeep to connect to a NetSuite account and make requests.
"""

from __future__ import absolute_import
import base64
import hashlib
import hmac
import logging
import os.path
import random
import time

import oauthlib.oauth1
import requests
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.exceptions import LookupError as ZeepLookupError

from .constants import *
from .exceptions import *
from .netsuite_types import *
from .utils import PaginatedSearch


class NetSuiteClient(object):
    u"""The Netsuite client class providing access to the Netsuite
    SOAP/WSDL web service"""

    WSDL_URL_TEMPLATE = u'https://{account}.suitetalk.api.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl'
    DATACENTER_URL_TEMPLATE = u'https://{account}.suitetalk.api.netsuite.com/services/NetSuitePort_2020_1'

    _search_preferences = None
    _passport = None
    _account = None

    # Used by TBA
    _consumer_key = None
    _consumer_secret = None
    _token_key = None
    _token_secret = None
    _app_id = None



    def __init__(self, account=None, caching=True, caching_timeout=2592000):
        u"""
        Initialize the Zeep SOAP client, parse the xsd specifications
        of Netsuite and store the complex types as attributes of this
        instance.

        :param str account_id: Account ID to connect to
        :param str caching: If caching = 'sqlite', setup Sqlite caching
        :param int caching_timeout: Timeout in seconds for caching.
                            If None, defaults to 30 days
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        assert account, u'Invalid account'
        assert u'-' not in account, u'Account cannot have hyphens, it is likely an underscore'
        self._account = account

        self._wsdl_url = self.WSDL_URL_TEMPLATE.format(account=account.replace(u'_', u'-'))
        self._datacenter_url = self.DATACENTER_URL_TEMPLATE.format(account=account.replace(u'_', u'-'))

        if caching:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), u'cache.db')
            timeout = caching_timeout
            cache = SqliteCache(path=path, timeout=timeout)
            transport = Transport(cache=cache)
        else:
            transport = None

        # Initialize the Zeep Client
        self._client = Client(self._wsdl_url, transport=transport)

        # default service points to wrong data center. need to create a new service proxy and replace the default one
        self._service_proxy = self._client.create_service(u'{urn:platform_2020_1.webservices.netsuite.com}NetSuiteBinding', self._datacenter_url)

        # Parse all complex types specified in :const:`~netsuitesdk.netsuite_types.COMPLEX_TYPES`
        # and store them as attributes of this instance. Same for simple types.
        self._namespaces = {}
        self._init_complex_types()
        self._init_simple_types()

        self._app_info = None
        self._is_authenticated = False
        self.set_search_preferences()

    def set_search_preferences(self, page_size = 100, return_search_columns = False):
        self._search_preferences = self.SearchPreferences(
            bodyFieldsOnly=False,
            pageSize=page_size,
            returnSearchColumns=return_search_columns
        )

    def _init_complex_types(self):
        self._complex_types = {}
        for namespace, complex_types in COMPLEX_TYPES.items():
            if not namespace in self._namespaces:
                self._namespaces[namespace] = []
            for type_name in complex_types:
                try:
                    verbose_type_name = u'{namespace}:{type_name}'.format(
                        namespace=namespace,
                        type_name=type_name
                    )
                    complex_type = self._client.get_type(verbose_type_name)
                except ZeepLookupError:
                    self.logger.warning(u'LookupError: Did not find complex type {}'.format(verbose_type_name))
                else:
                    setattr(self, type_name, complex_type)
                    self._complex_types[type_name] = complex_type
                    self._namespaces[namespace].append(complex_type)

    def _init_simple_types(self):
        self._simple_types = {}
        for namespace, simple_types in SIMPLE_TYPES.items():
            if not namespace in self._namespaces:
                self._namespaces[namespace] = []
            for type_name in simple_types:
                try:
                    verbose_type_name = u'{namespace}:{type_name}'.format(
                        namespace=namespace,
                        type_name=type_name
                    )
                    simple_type = self._client.get_type(verbose_type_name)
                except ZeepLookupError:
                    self.logger.warning(u'LookupError: Did not find simple type {}'.format(type_name))
                else:
                    setattr(self, type_name, simple_type)
                    self._simple_types[type_name] = simple_type
                    self._namespaces[namespace].append(simple_type)

    def get_complex_type(self, type_name):
        # if ':' in type_name:
        #     namespace, type_name = type_name.split(':')
            # namespace_index = namespace[2:]
        return self._complex_types[type_name]

    def get_simple_type(self, type_name):
        return self._simple_types[type_name]

    def get_complex_type_attributes(self, complex_type):
        if isinstance(complex_type, unicode):
            complex_type = self.get_complex_type(complex_type)
        try:
            return [(attribute.name, attribute.type.name) for attribute in complex_type._attributes]
        except AttributeError:
            return []

    def get_complex_type_elements(self, complex_type):
        if isinstance(complex_type, unicode):
            complex_type = self.get_complex_type(complex_type)
        try:
            return [(attr_name, element.type.name) for attr_name, element in complex_type.elements]
        except AttributeError:
            return []

    def get_complex_type_info(self, complex_type):
        if isinstance(complex_type, unicode):
            complex_type = self.get_complex_type(complex_type)
            label = complex_type
        else:
            if hasattr(complex_type, u'name'):
                label = complex_type.name
            else:
                label = unicode(complex_type)
        attributes = self.get_complex_type_attributes(complex_type)
        elements = self.get_complex_type_elements(complex_type)
        yield u'complexType {}:'.format(label)
        if attributes:
            yield u'Attributes:'
            for name, type_name in attributes:
                yield u'\t{}: {}'.format(name, type_name)
        else:
            yield u'No attributes'
        if elements:
            yield u'Elements:'
            for name, type_name in elements:
                yield u'\t{}: {}'.format(name, type_name)
        else:
            yield u'No elements'

    def login(self, email, password, role, application_id):
        u"""
        Authenticate and login user for a Netsuite session. The passport argument is
        of type Passport(email, password, role and account) which holds the credentials
        and can be created with NetSuiteClient.create_password.

        :param int applicationId: All requests done in this session will be identified
            with this application id.
        :param Passport passport: holds the credentials to authenticate the user.
        :return: the login response which contains the response status and user roles
        :rtype: LoginResponse
        :raises :class:`~netsuitesdk.exceptions.NetSuiteLoginError`: if login was not successful. Possible codes
            are: InsufficientPermissionFault, InvalidAccountFault, InvalidSessionFault,
            InvalidCredentialsFault and UnexpectedErrorFault
        """

        role = self.RecordRef(internalId=role)
        self._passport = self.Passport(email=email, password=password, role=role, account=self._account)

        if self._is_authenticated:
            self.logout()
        try:
            self._app_info = self.ApplicationInfo(applicationId=application_id)
            response = self._service_proxy.login(
                                self._passport,
                                _soapheaders={u'applicationInfo': self._app_info}
            )
            if response.status.isSuccess:
                self._is_authenticated = True
                return response
            else:
                statusDetail = response.status[u'statusDetail'][0]
                exc = self._request_error(u'login',
                                          detail=statusDetail,
                                          error_cls=NetSuiteLoginError)
                raise exc
        except Fault, fault:
            exc = NetSuiteLoginError(unicode(fault), code=fault.code)
            raise exc

    def _generate_token_passport(self):
        def compute_nonce(length=20):
            u"""pseudo-random generated numeric string"""
            return u''.join([unicode(random.randint(0, 9)) for i in xrange(length)])

        nonce = compute_nonce(length=20)
        timestamp = int(time.time())
        key = u'{}&{}'.format(self._consumer_secret, self._token_secret)
        base_string = u'&'.join([self._account, self._consumer_key, self._token_key, nonce, unicode(timestamp)])
        key_bytes = key.encode(encoding=u'ascii')
        message_bytes = base_string.encode(encoding=u'ascii')
        # compute the signature
        if self._signature_algorithm == u'HMAC-SHA256':
            # hash
            hashed_value = hmac.new(key_bytes, msg=message_bytes, digestmod=hashlib.sha256)
        elif self._signature_algorithm == u'HMAC-SHA1':
            hashed_value = hmac.new(key_bytes, msg=message_bytes, digestmod=hashlib.sha1)
        else:
            raise NetSuiteError(u"signature_algorithm needs to be one of 'HMAC-SHA256', 'HMAC-SHA1'")

        dig = hashed_value.digest()
        # convert dig (a byte sequence) to a base 64 string
        value = base64.b64encode(dig).decode()

        signature = self.TokenPassportSignature(value, algorithm=self._signature_algorithm)
        return self.TokenPassport(account=self._account, consumerKey=self._consumer_key, token=self._token_key,
                                  nonce=nonce, timestamp=timestamp, signature=signature)

    def connect_tba(self, consumer_key, consumer_secret, token_key, token_secret, signature_algorithm=u'HMAC-SHA256'):
        u"""
        Create a TokenPassport object holding credentials for Token based
        authentication which will be passed to NetSuiteClient.login

        :param str account: the NetSuite account ID
        :param str consumer_key: the consumer key for the integration record
        :param str consumer_secret: the consumer secret
        :param str token_key: a string identifier of a token representing a
                        unique combination of a user, a role and an integration record
        :param str token_secret: the token secret
        :param str signature_algorithm: algorithm to compute the signature value (a hashed value),
                        choices are 'HMAC-SHA256' or 'HMAC-SHA1'
        """
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._token_key = token_key
        self._token_secret = token_secret
        self._signature_algorithm = signature_algorithm

    @property
    def logged_in(self):
        return self._is_authenticated

    def logout(self):
        if not self._is_authenticated:
            return
        response = self._service_proxy.logout()
        self._is_authenticated = False
        self._consumer_key = None
        self._consumer_secret = None
        self._token_key = None
        self._token_secret = None
        return response.status

    def _request_error(self, service_name, detail, error_cls=None):
        if error_cls is None:
            error_cls = NetSuiteRequestError
        exc = error_cls(
                u"An error occured in a {service_name} request: {msg}".format(
                                                    service_name=service_name,
                                                    msg=detail[u'message']),
                code=detail[u'code']
        )
#        self.logger.error(str(exc))
        return exc

    def _build_soap_headers(self, include_search_preferences = False):
        u"""
        Generate soap headers dictionary to send with a request

        :param Passport passport: holds the authentication credentials
        :param TokenPassport tokenPassport: holds the token based authentication details
        :param ApplicationInfo applicationInfo: contains the application Id
        :return: the dictionary representing the headers
        :rtype: dict
        :raises :class:`~netsuitesdk.exceptions.NetSuiteError`: if user is neither logged in nor a passport or tokenPassport was passed
        """

        soapheaders = {}

        if self._is_authenticated:
            # User is already logged in, so there is no
            # need to pass authentication details in the header
            pass
        elif self._consumer_key is not None:
            soapheaders[u'tokenPassport'] = self._generate_token_passport()
        elif self._passport is not None:
            soapheaders[u'passport'] = self._passport
        else:
            raise NetSuiteError(u'Must either login first or pass passport or tokenPassport to request header.')
        if include_search_preferences:
            soapheaders[u'searchPreferences'] = self._search_preferences

        return soapheaders

    def request(self, name, *args, **kwargs):
        u"""
        Make a NetSuite web service request

        :param str name: the name of the request service ('get', 'search', ...)
        :return: the request response object
        :rtype: the exact type depends on the request
        """
        method = getattr(self._service_proxy, name)
        # call the service:
        include_search_preferences = (name == u'search')
        response = method(*args,
                _soapheaders=self._build_soap_headers(include_search_preferences=include_search_preferences)
                , **kwargs)
        return response

    def get(self, recordType, internalId=None, externalId=None):
        u"""
        Make a get request to retrieve an object of type recordType
        specified by either internalId or externalId

        :param str recordType: the complex type (e.g. 'vendor')
        :param int internalId: id specifying the record to be retrieved
        :param str externalId: str specifying the record to be retrieved
        :return: the matching record in case of success
        :rtype: Record
        :raises ValueError: if neither internalId nor externalId was passed
        """

        recordType = recordType[0].lower() + recordType[1:]
        if internalId is not None:
            record_ref = self.RecordRef(type=recordType, internalId=internalId)
        elif externalId is not None:
            record_ref = self.RecordRef(type=recordType, externalId=externalId)
        else:
            raise ValueError(u'Either internalId or externalId is necessary to make a get request.')

        response = self.request(u'get', baseRef=record_ref)
        response = response.body.readResponse

        status = response.status
        if status.isSuccess:
            record = response[u'record']
            return record
        else:
            exc = self._request_error(u'get', detail=status[u'statusDetail'][0])
            raise exc

    def getAll(self, recordType):
        u"""
        Make a getAll request to retrieve all objects of type recordType.
        All NetSuite types available for a search
        are listed under :const:`constants.GET_ALL_RECORD_TYPES`.

        :param str recordType: the complex type (e.g. 'vendor')
        :param int internalId: id specifying the record to be retrieved
        :param str externalId: str specifying the record to be retrieved
        :return: the matching record in case of success
        :rtype: Record
        """

        recordType = recordType[0].lower() + recordType[1:]
        record = self.GetAllRecord(recordType=recordType)
        response = self.request(u'getAll', record=record)
        response = response.body.getAllResult

        status = response.status
        if status.isSuccess:
            records = response[u'recordList'][u'record']
            return records
        else:
            exc = self._request_error(u'getAll', detail=status[u'statusDetail'][0])
            raise exc

    def _search_factory(self, search_type, type_name, **kwargs):
        _type_name = type_name[0].lower() + type_name[1:]
        if _type_name not in SEARCH_RECORD_TYPES:
            raise NetSuiteTypeError(u'{} is not a searchable NetSuite type!'.format(type_name))
        _search_cls_name = u'{}{}'.format(type_name, search_type)
        _search_cls = self.get_complex_type(_search_cls_name)
        _search = _search_cls(**kwargs)
        return _search

    def search_factory(self, type_name, **kwargs):
        _type_name = type_name[0].lower() + type_name[1:]
        if not _type_name in SEARCH_RECORD_TYPES:
            raise NetSuiteTypeError(u'{} is not a searchable NetSuite type!'.format(type_name))
        search_cls_name = u'{}Search'.format(type_name)
        search_cls = self.get_complex_type(search_cls_name)
        search_record = search_cls(**kwargs)
        return search_record

    def basic_search_factory(self, type_name, **kwargs):
        _type_name = type_name[0].lower() + type_name[1:]
        if not _type_name in SEARCH_RECORD_TYPES:
            raise NetSuiteTypeError(u'{} is not a searchable NetSuite type!'.format(type_name))
        basic_search_cls_name = u'{}SearchBasic'.format(type_name)
        basic_search_cls = self.get_complex_type(basic_search_cls_name)
        basic_search = basic_search_cls()
        for key, value in kwargs.items():
            setattr(basic_search, key, value)
        return basic_search

    def advanced_search_factory(self, type_name, **kwargs):
        return self._search_factory('SearchAdvanced', type_name, **kwargs)

    def search_row_factory(self, type_name, **kwargs):
        return self._search_factory('SearchRow', type_name, **kwargs)

    def search_row_basic_factory(self, type_name, **kwargs):
        return self._search_factory('SearchRowBasic', type_name, **kwargs)

    def row_basic_search_factory(self, type_name, **kwargs):
        _type_name = type_name[0].lower() + type_name[1:]
        if not _type_name in SEARCH_RECORD_TYPES:
            raise NetSuiteTypeError(u'{} is not a searchable NetSuite type!'.format(type_name))
        basic_search_cls_name = u'{}SearchRowBasic'.format(type_name)
        basic_search_cls = self.get_complex_type(basic_search_cls_name)
        basic_search = basic_search_cls()
        for key, value in kwargs.items():
            setattr(basic_search, key, value)
        return basic_search

    def search(self, searchRecord):
        u"""
        Make a search request to retrieve an object of type recordType
        specified by internalId. All NetSuite types available for a search
        are listed under :const:`constants.SEARCH_RECORD_TYPES`.

        :param Record searchRecord: data object holding all parameters for the search.
                    The utility function `search_factory` can be used to create one.
        :return: result records and meta data about search result
        :rtype: SearchResult(type):
                    int totalRecords: total number of records
                    int pageSize: number of records per page
                    int totalPages: number of pages
                    int pageIndex: index of actual returned result page
                    str searchId: identifier for the search
                    list records: the actual records found
        """
        response = self.request(u'search',
                                searchRecord=searchRecord)

        result = response.body.searchResult
        status = result.status
        success = status.isSuccess
        if success:
            if hasattr(result.recordList, u'record'):
                result.records = result.recordList.record
                return result
            elif hasattr(result.searchRowList, 'searchRow'):
                result.records = result.searchRowList.searchRow
                return result
            else:
                # Did not find anything
                result.records = None
                return result
        else:
            exc = self._request_error(u'search', detail=status[u'statusDetail'][0])
            raise exc

    def searchMoreWithId(self, searchId, pageIndex):
        response = self.request(u'searchMoreWithId',
                                searchId=searchId,
                                pageIndex=pageIndex)

        result = response.body.searchResult
        status = result.status
        success = status.isSuccess
        if success:
            if hasattr(result.recordList, u'record'):
                result.records = result.recordList.record
                return result
            elif hasattr(result.searchRowList, 'searchRow'):
                result.records = result.searchRowList.searchRow
                return result
            else:
                # Did not find anything
                result.records = None
                return result
        else:
            exc = self._request_error(u'searchMoreWithId', detail=status[u'statusDetail'][0])
            raise exc

    def upsert(self, record):
        u"""
        Add an object of type recordType with given externalId..
        If a record of specified type with matching externalId already
        exists, it is updated.

        Usage example:
            customer = self.Customer()
            customer.externalId = 'customer_id'
            customer.companyName = 'Test Inc.'
            customer.email = 'test@example.com'
            self.upsert(record=customer)

        :param str recordType: the complex type (e.g. either 'Customer' or 'vendors')
        :param str externalId: str specifying the record to be retrieved
        :return: a reference to the newly created or updated record (in case of success)
        :rtype: RecordRef
        """

        response = self.request(u'upsert', record=record)
        response = response.body.writeResponse
        status = response.status
        if status.isSuccess:
            record_ref = response[u'baseRef']
            self.logger.debug(u'Successfully updated record of type {type}, internalId: {internalId}, externalId: {externalId}'.format(
                    type=record_ref[u'type'], internalId=record_ref[u'internalId'], externalId=record_ref[u'externalId']))
            return record_ref
        else:
            exc = self._request_error(u'upsert', detail=status[u'statusDetail'][0])
            raise exc

    def add(self, record):
        u"""
        Add an object of type recordType with given externalId..
        If a record of specified type with matching externalId already
        exists, it is updated.

        Usage example:
            customer = self.Customer()
            customer.externalId = 'customer_id'
            customer.companyName = 'Test Inc.'
            customer.email = 'test@example.com'
            self.upsert(record=customer)

        :param str recordType: the complex type (e.g. either 'Customer' or 'vendors')
        :param str externalId: str specifying the record to be retrieved
        :return: a reference to the newly created or updated record (in case of success)
        :rtype: RecordRef
        """

        response = self.request(u'add', record=record)
        response = response.body.writeResponse
        status = response.status
        if status.isSuccess:
            record_ref = response[u'baseRef']
            self.logger.debug(u'Successfully updated record of type {type}, internalId: {internalId}, externalId: {externalId}'.format(
                    type=record_ref[u'type'], internalId=record_ref[u'internalId'], externalId=record_ref[u'externalId']))
            return record_ref
        else:
            exc = self._request_error(u'add', detail=status[u'statusDetail'][0])
            raise exc

    def initialize(self, record):
        u"""
        Initialize an object of type recordType with given externalId..
        If a record of specified type with matching externalId already
        exists, it is updated.

        Usage example:
            customer = self.Customer()
            customer.externalId = 'customer_id'
            customer.companyName = 'Test Inc.'
            customer.email = 'test@example.com'
            self.upsert(record=customer)

        :param str recordType: the complex type (e.g. either 'Customer' or 'vendors')
        :param str externalId: str specifying the record to be retrieved
        :return: a reference to the newly created or updated record (in case of success)
        :rtype: RecordRef
        """

        response = self.request(u'initialize', initializeRecord=record)
        response = response.body.readResponse
        status = response.status
        if status.isSuccess:
            record_ref = response.record
            # self.logger.debug(u'Successfully updated record of type {type}, internalId: {internalId}, externalId: {externalId}'.format(
            #         internalId=record_ref[u'internalId'], externalId=record_ref[u'externalId']))
            return record_ref
        else:
            exc = self._request_error(u'initialize', detail=status[u'statusDetail'][0])
            raise exc

    def attach(self, record):
        u"""
        Initialize an object of type recordType with given externalId..
        If a record of specified type with matching externalId already
        exists, it is updated.

        Usage example:
            customer = self.Customer()
            customer.externalId = 'customer_id'
            customer.companyName = 'Test Inc.'
            customer.email = 'test@example.com'
            self.upsert(record=customer)

        :param str recordType: the complex type (e.g. either 'Customer' or 'vendors')
        :param str externalId: str specifying the record to be retrieved
        :return: a reference to the newly created or updated record (in case of success)
        :rtype: RecordRef
        """

        response = self.request(u'attach', attachReference=record)
        response = response.body.writeResponse
        status = response.status
        if status.isSuccess:
            record_ref = response
            # self.logger.debug(u'Successfully updated record of type {type}, internalId: {internalId}, externalId: {externalId}'.format(
            #         internalId=record_ref[u'internalId'], externalId=record_ref[u'externalId']))
            return record_ref
        else:
            exc = self._request_error(u'attach', detail=status[u'statusDetail'][0])
            raise exc

    def call_get_restlet(self, script, deploy, integration_type):
        oauth1_client = oauthlib.oauth1.Client(
            self._consumer_key,
            client_secret=self._consumer_secret,
            resource_owner_key=self._token_key,
            resource_owner_secret=self._token_secret,
            signature_method=oauthlib.oauth1.SIGNATURE_HMAC_SHA1,
            realm=self._account
        )
        main_url = "https://{}.restlets.api.netsuite.com/app/site/hosting/restlet.nl".format(self._account)
        rest_url = "{}?script={}&deploy={}&integrationType={}".format(
            main_url,
            script,
            deploy,
            integration_type
        )

        url, headers, _ = oauth1_client.sign(rest_url)
        headers['Content-Type'] = 'application/json'
        response = requests.get(rest_url, headers=headers)
        return response.json()

    # def upsertList(self, records):
    #     """
    #     Add objects of type recordType with given externalId..
    #     If a record of specified type with matching externalId already
    #     exists, it is updated.

    #     Usage example:
    #         customer1 = self.Customer(externalId='customer', email='test1@example.com')
    #         customer2 = self.Customer(externalId='another_customer', email='test2@example.com')
    #         self.upsertList(records=[customer1, customer2])

    #     :param list[CompoundValue] records: the records to be created or updated
    #     :return: a reference to the newly created or updated records
    #     :rtype: list[CompoundValue]
    #     """

    #     response = self.request('upsertList', record=records)
    #     responses = response.body.writeResponse
    #     record_refs = []
    #     for response in responses:
    #         status = response.status
    #         if status.isSuccess:
    #             record_ref = response['baseRef']
    #             self.logger.debug('Successfully updated record of type {type}, internalId: {internalId}, externalId: {externalId}'.format(
    #                     type=record_ref['type'], internalId=record_ref['internalId'], externalId=record_ref['externalId']))
    #             record_refs.append(record_ref)
    #         else:
    #             exc = self._request_error('upsertList', detail=status['statusDetail'][0])
    #             has_failures = True
    #             raise exc
    #     return record_refs
