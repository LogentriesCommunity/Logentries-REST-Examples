**PUT User (Replace User)**
----
  Request used to replace the attributes for a specific user for a given account

* **URL**

  https://logentries.com/management/accounts/:accountid/users/:userid

* **Method:**
  

  `PUT`

* **Authentication:**

  Read/Write key or above is required.
  
*  **URL Params**
  
  `accountid=[UUID]`
  Example Value: de305d54-75b4-431b-adb2-eb6b9e546014

  `userid=[UUID]`
  Example Value: de305d54-75b4-431b-adb2-eb6b9e546014

* **Data Params**

    ```
    {
      'user_name':'UserName',
      'login_name':'LoginName',
      'email':'Email',
      'first_name':'FirstName',
      'last_name':'LastName',
    }
    ```

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


* **Notes:**
* Full object must be used when performing this request otherwise it will fail with a 401 error.

* Only the Owner of a given account can perform a PUT request on their own user, otherwise a response will return 404.
