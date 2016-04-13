**Authentication**

Guide to performing Authentication for REST API.

Authentication is required for all requests for the Logentries REST API. This usually involves adding a 'key' to the Header of your request, in the case of Resources that are only accessible by Owners of the Account a signature will need to be generated to authenticate.

The following doc will outline how to Authenticate for all requests.

***Obtaining API Keys*** 

To obtain your API key log in to your Logentries Account. Go to Accounts page and modify the URL by appending `apikey` to the URL. Your URL should look like the following.

`
https://logentries.com/app/#ACCOUNT-KEY/user-account/apikey
`

You should now be on the API Keys page. On your first visit to this page you should generate a Owner and Read/Write API Key. Keep these keys say as they will be used later for authenticating.

*Please note that these keys will only be displayed once on creation, if the key is lost then you will be required to generate a new key within the UI.*

Account Resource ID is also displayed here, this will be used when performing requests against your Account. This Account Resource ID will be displayed on the Account Summary page which is accessible via the following URL.

`
https://logentries.com/app/#ACCOUNT-KEY/user-account/
`

***Authentication Read/Write credentials***

For Resources which only require Read/Write credentials i.e any reqest other then Account or User, your authentication will only involve you adding a Header to your request called 'x-api-key' where the value is your Read/Write key. An example of this can be shown below

```
headers = {'x-api-key': '7f7c461f-2e71-4d50-8cdf-06c11ee67789'}'
```

***Generating Authentication Signature***

Account and User Resources are only accessible using the Owner rights of the account. Users must authenticate these requests by generating a signature and passing it through as a Header. 

*Note* Do NOT pass in the Owner Key in the header. 


The following is an example of generating the signature which is passed into the 'authorization-api-key' header as 'api-key-id:signature'.

```Python
import sys
import hashlib, hmac
import base64
import datetime
import requests

if (len(sys.argv) < 6):
    print "Usage: "
    print "gen_signature <api_key> <api_key_id> <method> <uri> <body>"
    exit()

def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())

    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()

print 'Usage is: api_key apikeyid method path body'
date_h = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
content_type_h = "application/json"

method = sys.argv[3]
uri = sys.argv[4]
body = sys.argv[5]

url = "https://staging-lerest.logentries.net/" + uri

# Remove the query parameters
action = uri.split("?")[0]
signature = gensignature(sys.argv[1], date_h, content_type_h, method, action, body)

headers = {
    "Date": date_h,
    "Content-Type": content_type_h,
    "authorization-api-key": "%s:%s" % (sys.argv[2].encode('utf8'), base64.b64encode(signature))
}

print "Sending %s request to %s with body='%s'" % (method, url, body)
print "headers = '%s'" % headers


r = requests.request(method, url, data=body, headers=headers)
print r.status_code, r.content
```

Note:
* Content-type is not required
* There should be no trailing / at the end of the query_path

