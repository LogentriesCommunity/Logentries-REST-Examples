import sys
import hashlib, hmac
import base64
import datetime
import requests
import ConfigParser
import csv
import json

config = ConfigParser.ConfigParser()
params = {}


def load_config():
    config.read('settings.ini')


def get_params():
    params['api-key-id'] = config.get('AddUser', 'api-key-id')
    params['api-key'] = config.get('AddUser', 'api-key')
    params['resource-id'] = config.get('AddUser', 'resource-id')

    params['users-file'] = config.get('Misc', 'users-file')


def get_users_from_csv():
    try:
        f = open(params.get('users-file'), 'rb')
    except IOError:
        print 'Error while reading Users file: ', params.get('users-file')
    reader = csv.reader(f)
    return list(reader)


def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()


def create_headers(body):
    date_h = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type_h = "application/json"
    method = 'POST'
    action = 'management/accounts/%s/users' % params.get('resource-id')
    signature = gensignature(params.get('api-key'), date_h, content_type_h, method, action, body)
    headers = {
        "Date": date_h,
        "Content-Type": content_type_h,
        "authorization-api-key": "%s:%s" % (params.get('api-key-id').encode('utf8'), base64.b64encode(signature))
    }
    return headers


def add_users_to_account(users):
    uri = 'https://rest.logentries.com/management/accounts/%s/users' % params.get('resource-id')
    for user in users[0]:
        body = {
            "email":user,
            "first_name":"tmp",
            "last_name":"tmp"
        }
        body = json.dumps(body, separators=(',', ':'))
        headers = create_headers(body)
        r = requests.request('POST', uri, data=body, headers=headers)
        print r.status_code, r.content

def start():
    load_config()
    get_params()
    users = get_users_from_csv()
    add_users_to_account(users)

if __name__ == '__main__':
    start()