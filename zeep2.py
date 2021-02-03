import oauth2 as oauth
import requests
from requests import Session
import time
from zeep import Client
from zeep.transports import Transport
import hmac
import base64
import hashlib
NS_ACCOUNT = "6758546"
NS_CONSUMER_KEY = "f0fbdf22d73942afd2433de153a84c19dcd408a4c2d54aac6ecf83f84ee763b0"
NS_CONSUMER_SECRET = "90369bc8c290ac61fb12b43e57f13fdbd0394b9f868622cf7924173755a15ac3"
NS_TOKEN_KEY = "fdf42bd9aeb7366b79d97654f0f0c30a3ab3192ae4d1180e2749ac59d8d188bf"
NS_TOKEN_SECRET = "339c8b3c2b0bef4b904ef30595e9dd2e234249f949e7baee35c372766fb1f354"

url = "https://6758546.suitetalk.api.netsuite.com"
token = oauth.Token(key=NS_TOKEN_KEY, secret=NS_TOKEN_SECRET)
consumer = oauth.Consumer(key=NS_CONSUMER_KEY, secret=NS_CONSUMER_SECRET)

http_method = "GET"
realm = NS_ACCOUNT

params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': str(int(time.time())),
    'oauth_token': token.key,
    'oauth_consumer_key': consumer.key,
   # 'oauth_signature_method': 'HMAC-SHA256'
    # 'exclude_oauth_signature': True
}
# OAuth realm="6758546",\
# oauth_consumer_key="f0fbdf22d73942afd2433de153a84c19dcd408a4c2d54aac6ecf83f84ee763b0",\
# oauth_token="95b8f09376e7aa736dffbddadd98ca26d6e2e9f04748a01dad94762e11e59a4a",\
# oauth_signature_method="HMAC-SHA256",\
# oauth_timestamp="1612260072",\

# oauth_nonce="BrtqX8HFhtB",\
# oauth_version="1.0",\
# oauth_signature="q8rLEO0raYAiFPc%2FHL2PWh77msDtvvEGoIgmglCVLgw%3D"

# OAuth realm="6758546",\
# oauth_consumer_key="f0fbdf22d73942afd2433de153a84c19dcd408a4c2d54aac6ecf83f84ee763b0",\
# oauth_token="fdf42bd9aeb7366b79d97654f0f0c30a3ab3192ae4d1180e2749ac59d8d188bf",\
# oauth_signature_method="HMAC-SHA256",\
# oauth_timestamp="1612262041",\

# oauth_nonce="QoPRzi5A4oD",\
# oauth_version="1.0",\
# oauth_signature="mx84ZvVhOrNSBs4v9m%2Bhh96uUR7U9NKR4lYkMaNWIaE%3D"

# OAuth realm="6758546"
#  oauth_consumer_key="f0fbdf22d73942afd2433de153a84c19dcd408a4c2d54aac6ecf83f84ee763b0"
#  oauth_token="fdf42bd9aeb7366b79d97654f0f0c30a3ab3192ae4d1180e2749ac59d8d188bf"
#  oauth_signature_method="HMAC-SHA1"
#  oauth_timestamp="1612262820"


#  oauth_nonce="68599147"
#  oauth_version="1.0"
#  oauth_body_hash="2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D"



def create_signature(secret_key, signature_base_string):
    encoded_string = signature_base_string.encode()
    encoded_key = secret_key.encode()
    temp = hmac.new(encoded_key, encoded_string, hashlib.sha256).hexdigest()
    byte_array = b64encode(binascii.unhexlify(temp))
    return byte_array.decode()

oauth_signature = create_signature(signing_key, encoded_base_string)

encoded_oauth_signature = urllib.parse.quote(oauth_signature, safe='')

class SignatureMethod_HMAC_SHA256(SignatureMethod):
    name = 'HMAC-SHA1'

    def signing_base(self, request, consumer, token):
        if (not hasattr(request, 'normalized_url') or request.normalized_url is None):
            raise ValueError("Base URL for request is not set.")

        sig = (
            escape(request.method),
            escape(request.normalized_url),
            escape(request.get_normalized_parameters()),
        )

        key = '%s&' % escape(consumer.secret)
        if token:
            key += escape(token.secret)
        raw = '&'.join(sig)
        return key.encode('ascii'), raw.encode('ascii')

    def sign(self, request, consumer, token):
        encoded_string = signature_base_string.encode()
        encoded_key = secret_key.encode()
        temp = hmac.new(encoded_key, encoded_string, hashlib.sha256).hexdigest()
        byte_array = b64encode(binascii.unhexlify(temp))
        return byte_array.decode()

#  oauth_signature="ex0o8l5tEvxVqJ3TYrkp8xN2iCY%3D"
class SignatureMethod_HMAC_SHA256():
    name = 'HmacSHA256'
    version = '2'

    def build_signature_base_string(self, request):
        sig = '\n'.join((
            request.get_normalized_http_method(),
            request.get_normalized_http_host(),
            request.get_normalized_http_path(),
            request.get_normalized_parameters(),
        ))
        return sig

    def build_signature(self, request, aws_secret):
        base = self.build_signature_base_string(request)
        hashed = hmac.new(aws_secret, base, hashlib.sha256)
        return base64.b64encode(hashed.digest())

req = oauth.Request(method=http_method, url=url, parameters=params)

signature_method = oauth.SignatureMethod_HMAC_SHA1()
req.sign_request(signature_method, consumer, token)
header = req.to_header(realm)
header_y = header['Authorization'].encode('ascii', 'ignore')
#header_auth = 'OAuth realm="6758546",oauth_consumer_key="-f0fbdf22d73942afd2433de153a84c19dcd408a4c2d54aac6ecf83f84ee763b0",oauth_token="fdf42bd9aeb7366b79d97654f0f0c30a3ab3192ae4d1180e2749ac59d8d188bf",oauth_signature_method="HMAC-SHA256",oauth_timestamp="1612273346",oauth_nonce="bIXmnksad46",oauth_version="1.0",oauth_signature="uduiwFAACCl0GZY4Va55muSNnODXWrKPTEAA2Nlfkqg%3D"'
header_x = {"Authorization": header_y, "Content-Type": "application/json"}
conn = requests.get(url, headers=header_x)
session = Session()
session.headers = header_x
#print header['Authorization']
#print header_x
#exit(1)
for header in header_x:
    if "," in header_x[header]:
        subh = header_x[header].split(",")
        for h in subh:
            print h
    else:
        print header, header_x[header]
WSDL_URL = "https://webservices.netsuite.com/wsdl/v2020_2_0/netsuite.wsdl"
client = Client(WSDL_URL, transport=Transport(session=session))
client.set_ns_prefix('urn','')
client.
print client.get_type(u"urn:StatusDetail")

# for ns in client.namespaces:
#     print ns, client.namespaces[ns]
# client.set_ns_prefix('ns1', '')
# service = client.create_service('urn:types.relationships_2020_1.lists.webservices.netsuite.com',
#                                 'urn:types.relationships_2020_1.lists.webservices.netsuite.com')
# print service
# # print client.get_type('urn:core_2020_1.platform.webservices.netsuite.com')
