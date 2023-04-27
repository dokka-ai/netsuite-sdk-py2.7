import zeep
import logging
from collections import OrderedDict
from ..internal.utils import PaginatedSearch
from typing import List

logger = logging.getLogger(__name__)

 # TODO: introduce arg and return types
class ApiBase:
    def __init__(self, ns_client, type_name):
        self.ns_client = ns_client
        self.type_name = type_name

    def search(self):
        pass
        # self.ns_client.

    def get_all(self, page_size=1000):
        return list(self.get_all_generator(page_size=page_size))

    def get_all_generator(self, page_size=1000):
        """
        Returns a generator which is more efficient memory-wise
        """
        return self._search_all_generator(page_size=page_size)

    def get(self, internalId=None, externalId=None):
        return self._get(internalId=internalId, externalId=externalId)

    def get_ref(self, internalId=None, externalId=None):
        return self._serialize(self.ns_client.RecordRef(type=self.type_name.lower(), internalId=internalId, externalId=externalId))

    def post(self, data):
        raise NotImplementedError('post method not implemented')

    def _serialize(self, record):
        """
        record: single record
        Returns a dict
        """
        return zeep.helpers.serialize_object(record, target_cls=dict)

    def _serialize_array(self, records):
        """
        records: a list of records
        Returns an array of dicts
        """
        return zeep.helpers.serialize_object(records, target_cls=dict)

    def _paginated_search_to_generator(self, paginated_search):
        if paginated_search.num_records == 0:
            return

        num_pages = paginated_search.total_pages
        logger.debug('total pages = %d, records in page = %d', paginated_search.total_pages, paginated_search.num_records)
        logger.debug(u'current page index {}'.format(paginated_search.page_index))
        logger.debug('going to page %d', 0)

        num_records = paginated_search.num_records
        for r in range(0, num_records):
            record = paginated_search.records[r]
            yield self._serialize(record=record)

        for p in range(2, num_pages + 1):
            logger.debug('going to page %d', p)
            paginated_search.goto_page(p)
            logger.debug(u'current page index {}'.format(paginated_search.page_index))
            num_records = paginated_search.num_records
            for r in range(0, num_records):
                record = paginated_search.records[r]
                yield self._serialize(record=record)

    def _search_all_generator(self, page_size):
        ps = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=page_size)
        return self._paginated_search_to_generator(paginated_search=ps)

    def advanced_search_by_id(self, page_size, search_id, *basic_columns):
        search_record = self.ns_client.advanced_search_factory(self.type_name)
        search_record.savedSearchId = search_id

        ps = PaginatedSearch(client=self.ns_client,
                             search_record=search_record,
                             type_name=self.type_name,
                             pageSize=page_size)
        for result_search_record in self._paginated_search_to_generator(paginated_search=ps):
            pass

    def advanced_search(self, page_size, basic_columns, search_criteria=None, joins=None):
        """
        :param page_size:
        :param list basic_columns:
        :param list search_criteria:
            list of tuples where
                (('searchField', 'operator', 'value'),)
                Example:
                    (('transactionNumber', 'startsWith', 'PURCHORD'),)
        :param list joins:
        """
        if not joins:
            joins = []

        search_record = self.ns_client.advanced_search_factory(self.type_name)
        search_row = self.ns_client.search_row_factory(self.type_name)
        search_row.basic = self.ns_client.search_row_basic_factory(self.type_name)

        # build list of columns which we want to get in response
        columns_types = dict(search_row.basic.__class__._xsd_type.elements)
        for column in basic_columns:
            if isinstance(column, tuple):
                column, _column_type = column
            column_type = columns_types[column].type()
            setattr(search_row.basic, column, column_type)

        # extra search criteria
        if search_criteria:
            search = self.ns_client.search_factory(self.type_name)
            search.basic = self.ns_client.basic_search_factory(self.type_name)
            search_columns_types = dict(search.basic.__class__._xsd_type.elements)
            for search_field, operator, value in search_criteria:
                if operator is None:
                    # boolean and other types
                    _f = search_columns_types[search_field](searchValue=value)
                else:
                    _f = search_columns_types[search_field](searchValue=value, operator=operator)
                setattr(search.basic, search_field, _f)

            search_record.criteria = search

        # join_types = dict(search_row.__class__._xsd_type.elements)
        # for join, join_fields in joins:
        #     join_type = join_types[join].type
        #     join_type_dict = dict(join_type.elements)
        #     join_instance = join_type()
        #     for join_field in join_fields:
        #         join_field_type = join_type_dict[join_field]
        #         setattr(join_instance, join_field, join_field_type())
        #
        #     setattr(search_row, join, join_instance)

        search_record.columns = search_row

        ps = PaginatedSearch(client=self.ns_client,
                             search_record=search_record,
                             type_name=self.type_name,
                             pageSize=page_size)
        for result_search_record in self._paginated_search_to_generator(paginated_search=ps):
            record = {}
            for column in basic_columns:
                _column_type = None
                if isinstance(column, tuple):
                    column, _column_type = column

                if not result_search_record['basic']:
                    continue

                column_result = result_search_record['basic'][column]
                len_column_result = len(column_result)
                if _column_type == 'as_list' or len_column_result > 1:
                    result_list = []
                    for iter_column_result in column_result:
                        result_list.append(self._serialize_advanced(
                            iter_column_result['searchValue']
                        ))
                    record[column] = result_list
                elif len_column_result == 1:
                    record[column] = self._serialize_advanced(
                        column_result[0]['searchValue']
                    )
                else:
                    record[column] = None

                # for join, join_fields in joins:
                #     if not result_search_record[join]:
                #         continue
                #     join_columns = {}
                #     for join_field in join_fields:
                #         if len(result_search_record[join][join_field]):
                #             join_columns[join_field] = self._serialize_advanced(
                #                 result_search_record[join][join_field][0]['searchValue']
                #             )
                #         else:
                #             join_columns[join_field] = None
                #     record[join] = join_columns

            yield record

    def _serialize_advanced(self, search_result):
        if isinstance(search_result, dict):
            # if it is nested object then take internalId
            return search_result['internalId']
        else:
            return search_result

    def _get_all(self):
        records = self.ns_client.getAll(recordType=self.type_name)
        return self._serialize_array(records)

    def _get_all_generator(self):
        res = self._get_all()
        for r in res:
            yield r

    def _get(self, internalId=None, externalId=None):
        record = self.ns_client.get(recordType=self.type_name, internalId=internalId, externalId=externalId)
        return self._serialize(record=record)
