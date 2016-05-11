**GET Query**
---
Request used to Query your Logentries Logs using a LEQL query.

* **URL**

  https://rest.logentries.com/query/logs/:log_id

* **Method:**
  

  `GET`

* **Authentication:**
  
  Read Only key or above is required.
  
*  **URL Params**


  | Param  | About | Required  | Example |
  | :-----:|:-----|:---------:| -------|
  | log_id| Logentries log key  | True | /logs/f9c6e2c1-ac7a-4a29-8faa-a8d70f96df71 |
  | query  | a valid LEQL query to run against the log; url-encoded string | True      | query=where(foo=bar) |
  | from   | lower bound of the time range you want to query against; UNIX timestamp in milliseconds     | True      | from=1450557604000  |
  | to     | lower bound of the time range you want to query against; UNIX timestamp in milliseconds      | True      | to=1460557604000 |
  | per_page | number of log entries to return per page. Default of 50 | False | per_page=50
  | sequence_number | the earlier sequence number of a log entry to start searching from | False | sequence_number=10


**Success Response:**

 * **Code:** `200` for a successful query
    
    **Content:** 
    
    ```json
    {
      "logs": ["f9c6e2c1-ac7a-4a29-8faa-a8d70f96df70"],
      "statistics": {...},
      "leql": {
        "statement": "where(something) calculate(count)",
        "during": {
          "from": 1,
          "to": 10000
        }
      }
    }  
    ```
 
 * **Code:** `202` for a query that successfully started but has not yet finished
    
    **Content:** 
    
    ```json
    {
      "logs": [
        "f9c6e2c1-ac7a-4a29-8faa-a8d70f96df70"
      ],
      "id": "deace1fd-e605-41cd-a45c-5bf1ff0c3402-1",
      "query": {
        "statement": "where(foo) calculate(count:x)",
        "during": {
          "to": 100000,
          "from": 100
        }
      },
      "links": [{
        "rel": "self",
        "href": "https://lerest-api-example.com/query/deace1fd-e605-41cd-a45c-5bf1ff0c3402-1"
      }]
    }  
    ```

**Error Response:**
 
 * **Code:** `400` for bad user input
    **Content:** 
    
 * **Code:** `404` for bad user input
    **Content:** 

 * **Code:** `500` for bad user input
    **Content:** 

**Sample Call:**

``` Python
import requests
import json
import time

API_KEY = 'YOUR API KEY GOES HERE'

def continue_request(req):
    if 'links' in req.json():
        continue_url = req.json()['links'][0]['href']
        new_response = make_request(continue_url)
        handle_response(new_response)


def handle_response(resp):
    response = resp
    time.sleep(5)
    if response.status_code == 200:
        print json.dumps(resp.json(), indent=4)
        return
    if response.status_code == 202:
        continue_request(resp)
        return
    if response.status_code > 202:
        print 'Error status code ' + str(response.status_code)
        return


def make_request(provided_url=None):
    headers = {'x-api-key': API_KEY}

    url = "https://rest.logentries.com/query/logs/f9c6e2c1-ac7a-4a29-8faa-a8d70f96df71?query=where(foo=bar)from=1450557604000&to=1460557604000"
    if provided_url:
        url = provided_url
    req = requests.get(url, headers=headers)
    return req


def print_query():
    req = make_request()
    handle_response(req)

def start():
    print_query()


if __name__ == '__main__':
    start()
```    

* **Notes:**

* The maximum supported length of the URL is 8192 characters
* Pagination is only supported with 'where' queries only
* The maximum page size is currently limited to 500 log entries
