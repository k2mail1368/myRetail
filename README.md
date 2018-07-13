# myRetail API Service

The goal is to create an end-to-end Proof-of-Concept for a products API, which will aggregate product data from multiple sources and return it as JSON to the caller. 

## What this solution does ?

This API service responds to HTTP GET request and delivers aggregated product data from multiple sources (redsky.target.com and NoSQL data store) as a JSON. 
Also, service accepts an HTTP PUT request at the same path, containing a JSON request body similar to the GET response, and updates the product’s price in the data store.

Note: MongoDB holds the product’s price details which includes the price and currency code. redsky.target.com provides the name of the product.

### Prerequisites

Download the latest version of the following softwares and run it locally. 
•	Python 3 - https://www.python.org/downloads/
•	Flask - https://pypi.org/project/Flask/
•	PyCharm (IDE for Python) - https://www.jetbrains.com/pycharm/download
•	MongoDB - https://www.mongodb.com/download-center#atlas
•	Postman - https://www.getpostman.com/apps 

### Installing and Getting Started

To run this application locally, Python 3, flask, and MongoDB must be installed locally. Currently, the application assumes that MongoDB is running on localhost:27017. 
1. Clone The Repository from Git Hub to a local workstation -- git clone
2. Open Command Prompt/Terminal and Change Directory Location to the project directory -- cd /Users/karthik/PycharmProjects/myRetail/venv
3. run command -- python app.py
4. Open another Terminal and run command to start mongo admin shell -- mongo 
5. Open another Terminal and run command to start mongo daemon -- mongod
Note: By default, MongoDB listens for connections from clients on port 27017, and stores data in the /data/db directory.
6. Load MongoDB with few Product ID’s along with price and currency code as individual documents under a collection name “product”, using the below command for these product_id's: 13860421, 13860424, 13860425, 13860428, 13860429.
 ```
db.product.insert ({"product_id": 13860421, "current_price": {"value": 16.42, "currency_code": "USD"}});
```
7. Launch Postman
8. Access the product details from URI - http://localhost:5000/api/products/13860421
9. Update product details by a PUT request to the URI http://localhost:8080/api/products/13860428 with the request body in the format below. { "value": 23.22, "currency_code": "USD" }
Note: Product_id will be picked from the query string 

### Get Method:

To make a Get Request, use below shown URL and pass the product_id 

```
http://localhost:5000/api/products/{}
Example: http://localhost:5000/api/products/13860421
```
Response:

```
{"id":,"name":"":{"value":,"currency_code":""}}
Example: {"id":13860421,"name":"The Big Lebowski (Blu-ray)","current_price":{"value":17.44,"currency_code":"USD"}}
```

### PUT Method:

To perform a PUT request at the same path. Use Postman - type the url in the address bar, select the PUT menthod from the dropdown, hit text "Body" just underneath the address bar, select raw and select JSON(application/json) from the drop down. 
Now, udpate the new value in the request body and hit send blue button on right top corner.
Note: product_id will be picked from the query string and hence user doesn't have supply product_id in the request body.

Request
```
Example: {"id":13860421,"name":"The Big Lebowski (Blu-ray) ","current_price":{"value": 17.44,"currency_code":"USD"}} 
key in the new value 40.44 (was 17.44) and execute it.

```
Response:

```
Example: {"id":13860421,"name":"The Big Lebowski (Blu-ray)","current_price":{"value":17.44,"currency_code":"USD"}}
```


