import ConfigParser
import base64
import datetime
import hashlib
import hmac
import json

import requests

config = ConfigParser.ConfigParser()
params = {}


def load_config():
    config.read('settings.ini')


def get_params():
    params['api-key-id'] = config.get('Map', 'api-key-id')
    params['api-key'] = config.get('Map', 'api-key')
    params['resource-id'] = config.get('Map', 'resource-id')


def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()


def create_headers():
    date_h = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type_h = "application/json"
    method = 'GET'
    action = 'management/accounts/%s/users' % params.get('resource-id')
    signature = gensignature(params.get('api-key'), date_h, content_type_h, method, action, '')
    headers = {
        "Date": date_h,
        "Content-Type": content_type_h,
        "authorization-api-key": "%s:%s" % (params.get('api-key-id').encode('utf8'), base64.b64encode(signature))
    }
    return headers


def write_map_to_file(response_data):
    try:
        user_map_file = open('user-map.json', 'w')
    except IOError:
        print 'Error writing to file'
    user_map_file.write(json.dumps(response_data, separators=(',', ':')))
    user_map_file.close()


def build_users_map():
    uri = 'https://rest.logentries.com/management/accounts/%s/users' % params.get('resource-id')
    headers = create_headers()
    r = requests.request('GET', uri, headers=headers)
    response_data = r.json()
    if r.status_code == 200:
        write_map_to_file(response_data)


def start():
    load_config()
    get_params()
    build_users_map()


if __name__ == '__main__':
    start()
