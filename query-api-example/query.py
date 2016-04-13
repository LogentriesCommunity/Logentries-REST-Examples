import requests
import json
import ConfigParser
import time
config = ConfigParser.ConfigParser()
params = {}


def continue_request(req):
    if 'links' in req.json():
        continue_url = req.json()['links'][0]['href']
        new_response = make_request(continue_url)
        handle_response(new_response)


def handle_response(resp):
    response = resp
    time.sleep(5)
    if response.status_code == 200:
        print json.dumps(resp.json(), indent=4, separators={':', ';'})
        return
    if response.status_code == 202:
        continue_request(resp)
        return
    if response.status_code > 202:
        print 'Error status code ' + str(response.status_code)
        return


def make_request(provided_url=None):
    headers = {'x-api-key': params['api-key']}

    url = "https://rest.logentries.com/query/logs/"+ params['log-key'] + "/?query=" \
          + params['query'] + "&from=" + params['from'] + '&to=' + params['to']
    if provided_url:
        url = provided_url
    req = requests.get(url, headers=headers)
    return req


def print_stats():
    req = make_request()
    handle_response(req)


def load_config():
    config.read('query.ini')


def get_params():

    params['api-key'] = config.get('Auth', 'api-key')
    params['log-key'] = config.get('Auth', 'log-key')

    params['query'] = config.get('Search', 'query')
    params['from'] = config.get('Search', 'from')
    params['to'] = config.get('Search', 'to')

    return params


def start():
    load_config()
    get_params()
    print_stats()


if __name__ == '__main__':
    start()