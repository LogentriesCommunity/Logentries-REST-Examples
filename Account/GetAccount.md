**GET Account**
----
  Request used to get account details for a specified account

* **URL**

  https://rest.logentries.com/management/accounts/:accountid

* **Method:**
  

  `GET`

* **Authentication:**
  
  Owner key is required.
  
*  **URL Params**

  `accountid=[UUID]`
  Example Value: de305d54-75b4-431b-adb2-eb6b9e546014

* **Data Params**

  None

* **Success Response:**
  

  * **Code:** 200 <br />
    **Content:** 
    
    ```
    {
        "id": "",
        "email": "foo@bar.com",
        "name": "Foo Bar",
        "organization": "Foo Bar INC",
        "max_retention_period": 100000,
        "retention_period": 100000
    }
    ```
 
* **Error Response:**

  If a request other then GET is made.
  * **Code:** 405 UNAUTHORIZED <br />

  If the Account ID can not be found
  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ``` python
  import requests

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
    action = 'management/accounts/%s/' % resource_id
    signature = gensignature(api_key_id, date_h, content_type_h, method, action, '')
    headers = {
        "Date": date_h,
        "Content-Type": content_type_h,
        "authorization-api-key": "%s:%s" % (api_key_id.encode('utf8'), base64.b64encode(signature))
    }
    print headers
    return headers


def get_account(users):
    uri = 'https://rest.logentries.com/management/accounts/%s' % resource_id
    r = requests.request('GET', uri, headers=headers)
    print r.status_code, r.content

  ```

* **Notes:**
