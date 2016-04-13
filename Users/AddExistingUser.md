**POST User (Add Existing User)**
----
  Request used to add an existing user to a given account.

* **URL**

  https://rest.logentries.com/management/accounts/:accountid/users/:userid

* **Method:**
  

  `POST`

* **Authentication:**
  
  Owner Key is required.
  
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
      "id": "1d27d3c7-2e86-4edb-bea3-bc82a2049452",
      "last_login": 1460143586,
      "first_name": "tmp",
      "last_name": "tmp",
      "email": "foo@bar.com",
      "login_name": "foo@bar.com"
    }   
    ```
 
* **Error Response:**

  If a request other then GET is made.
  * **Code:** 405 UNAUTHORIZED <br />

  If the Account ID can not be found
  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ``` python
def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    print request_body
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    print type(api_key)
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
    print action
    signature = gensignature(api_key), date_h, content_type_h, method, action, '')
    headers = {
        "Date": date_h,
        "Content-Type": content_type_h,
        "authorization-api-key": "%s:%s" % (api_key_id).encode('utf8'), base64.b64encode(signature))
    }
    print headers
    return headers


def add_users_to_account(users):
      uri = 'https://rest.logentries.com/management/accounts/%s/users/%s' % (resource_id, user_id)
      headers = create_headers(uri)
      r = requests.request('POST', uri, data='', headers=headers)
      print r.status_code, r.content
  ```

* **Notes:**
*No Invitation email is sent, instead a password will be automatically created for the Users. To login Users will first have to retrieve their password via the [Password Reset Page](https://logentries.com/user/password-reset/)

*You can only add Users to an Account of which you are the Owner of and of which you have the Owner API Key.
