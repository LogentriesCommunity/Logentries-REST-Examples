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
    params['api-key-id'] = config.get('AddUser', 'api-key-id')
    params['api-key'] = config.get('AddUser', 'api-key')
    params['resource-id'] = config.get('AddUser', 'resource-id')

    params['users-map'] = config.get('Misc', 'json-file')


def get_users_from_map():
    try:
        json_file = open(params.get('users-map'), 'rb')
    except IOError:
        print 'Error while reading users-map file: ', params.get('users-map')
    json_data = json.load(json_file)
    return json_data


def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()


def create_headers(uri):
    date_h = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type_h = "application/json"
    method = 'POST'
    action = uri.split("com/")[1]
    signature = gensignature(params.get('api-key'), date_h, content_type_h, method, action, '')
    headers = {
        "Date": date_h,
        "Content-Type": content_type_h,
        "authorization-api-key": "%s:%s" % (params.get('api-key-id').encode('utf8'), base64.b64encode(signature))
    }
    return headers


def add_users_to_account(users):
    for user in users:
        uri = 'https://rest.logentries.com/management/accounts/%s/users/%s' % (params.get('resource-id'), user['id'])
        headers = create_headers(uri)
        r = requests.request('POST', uri, data='', headers=headers)
        print r.status_code, r.content


def start():
    load_config()
    get_params()
    users = get_users_from_map()
    add_users_to_account(users)


if __name__ == '__main__':
    start()
