**GET User**
----
  Request used to get a specific user for a given account

* **URL**

  https://rest.logentries.com/management/accounts/:accountid/users/:userid

* **Method:**
  

  `GET`
  
* **Authentication:**

  Owner key is required.
  
*  **URL Params**
  
  `accountid=[UUID]`
  Example Value: de305d54-75b4-431b-adb2-eb6b9e546014

  `userid=[UUID]`
  Example Value: de305d54-75b4-431b-adb2-eb6b9e546014

* **Data Params**

  None

* **Success Response:**
  

  * **Code:** 200 <br />
    **Content:** 
    
    ```
    {
      'id':'UserID',
      'user_name':'UserName',
      'login_name':'LoginName',
      'email':'Email',
      'first_name':'FirstName',
      'last_name':'LastName',
    }
    ```
 
* **Error Response:**

  If a request other then GET is made.
  * **Code:** 405 UNAUTHORIZED <br />

  If the Account or User can not be found
  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ``` python
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
    action = 'management/accounts/%s/user/%s' % (resource_id, user_id)
    signature = gensignature(api_key_id, date_h, content_type_h, method, action, '')
    headers = {
        "Date": date_h,
        "Content-Type": content_type_h,
        "authorization-api-key": "%s:%s" % (api_key_id.encode('utf8'), base64.b64encode(signature))
    }
    print headers
    return headers


def get_account(users):
    uri = 'https://rest.logentries.com/management/accounts/%s/user/%s' % (resource_id, user_id)
    r = requests.request('GET', uri, headers=headers)
    print r.status_code, r.content

  ```

* **Notes:**
