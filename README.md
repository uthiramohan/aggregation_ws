# Setting UP
1. git clone FILL

## Starting the git@github.com:uthiramohan/aggregation_ws.git

make start_server


The server access logs will showup in the current directory, server.access.log file

## Submitting POST request
Open a new Terminal, and submit post requests

curl -X 'POST' \
  'http://127.0.0.1:8080/flows' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d@data.json

For your convenience, the test_data1.json contains some flow data and post_request.sh submits that to the database.

## Submitting GET request
Open a new terminal, and submit GET Request with query parameter of hour and value is integer

curl -X 'POST' \
  'http://127.0.0.1:8080/flows&hour=2' \


you will get a response like 

{"items":[{"src_app":"baz","dest_app":"qux","vpc_id":"vpc-0","hour":2,"bytes_rx":500,"bytes_tx":100},{"src_app":"baz","dest_app":"qux","vpc_id":"vpc-1","hour":2,"bytes_rx":500,"bytes_tx":100}],"total":2,"page":1,"size":50}


Note:
1. The response for a GET request is *paginated* and the actual results would showup inside the `items` key with additional information like `"total":2,"page":1,"size":50`.
2. All the events posted are *persisted across several server restarts/crashes*. If you want to clear the database, run `make purge_db`

## Running the tests and get coverage metrics

make run_test


## Shutdown and cleanup

make shutdown


# API Spec
## Supported Methods

### GET request
A Schema of json response. 

Response: Json Object

{
"items": JSON Array of Flow Objects,
"total":2,
"page":1,
"size":50
}

Flow Object:
● src_app - string
● dest_app - string
● vpc_id - string 
● bytes_tx - int
● bytes_rx - int
● hour - int


if successful, returns 200 http response code

if unsuccessful,returns 500 http response code and json response with message containing more information about 
error

any issues with query parameters return HTTP_422_UNPROCESSABLE_ENTITY response code

### POST request
message_payload - JSON Array of flow objects

if successful, returns 201 response code

if unsuccessful, returns 500  response code and a json response with message containing more information about 
error

Note that a check is enforced to ensure that the number of items in the message payload does not exceed a configured 
value. If this happens json response contains a status code of 406 and message Too many flow objects are being registered
is displayed (`{'error_message': 'Too many flow objects are being registered', 'status_code': 406}`)

## Unsupported Methods
The API returns HTTP 405 response code for any HTTP methods other than GET or POST
