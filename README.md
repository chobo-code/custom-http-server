# The server implementation which supports both HTTP/1 and HTTP/2
- This server supports HTTP/1 + HTTP/2.
- This server is async server framework.


## Requirements
- Python > 3.11
- pytest>=8.3.2
- pyassert>=0.4.2
- hpack==4.0.0
- hyperframe==6.0.1


## HTTP/2 Server spec.
```shell
$ brew install h2spec
$ cd http_h2
$ python main.py
...

$ h2spec -p 8080 -h localhost 
>>
Generic tests for HTTP/2 server
  1. Starting HTTP/2
    ✔ 1: Sends a client connection preface
    ...

Hypertext Transfer Protocol Version 2 (HTTP/2)
  3. Starting HTTP/2
    3.5. HTTP/2 Connection Preface
      ✔ 1: Sends client connection preface
      ✔ 2: Sends invalid connection preface
    ...

HPACK: Header Compression for HTTP/2
  2. Compression Process Overview
    ...

Finished in 0.2501 seconds
146 tests, 145 passed, 1 skipped, 0 failed
```



## How to use.
```python
import asyncio
from server import Dispatcher, Server
from generic_http_object import GenericHttpRequest, GenericHttpResponse
from status_code import StatusCode


@Dispatcher.request_mapping(path='/')
async def path_default(http_request: GenericHttpRequest, http_response: GenericHttpResponse):
  print('default_path function called.')
  http_response.status_code = StatusCode.OK
  http_response.body = 3
  return http_response


@Dispatcher.route(path='/200', methods=['POST', 'GET'])
async def path_200(http_request: GenericHttpRequest, http_response: GenericHttpResponse):
  print('path_200 called.')
  http_response.status_code = StatusCode.OK
  http_response.body = 2
  return http_response


@Dispatcher.get_mapping(path='/200/test')
async def path_200_test(http_request: GenericHttpRequest, http_response: GenericHttpResponse):

  print('path_200_test called.')
  http_response.status_code = StatusCode.OK
  return http_response


async def main():
  server = Server(host='0.0.0.0', port=8080)
  await server.serve_forever()

if __name__ == '__main__':
  asyncio.run(main())

```


## Performance `HTTP/1`
- HTTP/1 Condition
    - Local M1 Mac.
    - `Locust` load test.
    - `FastAPI` with `uvicorn`.
    - Custom Server.
    - Using `keep-alive`.

RPS

| Server Type   | Type | Name | # Requests | # Fails | Average (ms) | Min (ms) | Max (ms) | Average size (bytes) | RPS    | Failures/s |
|---------------|------|------|------------|---------|--------------|----------|----------|----------------------|--------|------------|
| CUSTOM SERVER | GET  | /200 | 659853     | 0       | 69.16        | 0        | 1189     | 1                    | 1461.36| 0          |
| FAST API      | GET  | /200 | 552122     | 0       | 244.37       | 0        | 6732     | 1                    | 1220.07|            |


Response Time

| Server Type   | Method | Name | 50%ile (ms) | 60%ile (ms) | 70%ile (ms) | 80%ile (ms) | 90%ile (ms) | 95%ile (ms) | 99%ile (ms) | 100%ile (ms) |
|---------------|--------|------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|
| CUSTOM SERVER | GET    | /200 | 35          | 49          | 69          | 100         | 160         | 230         | 640         | 1200         |
| FAST API      | GET    | /200 | 93          | 190         | 310         | 440         | 650         | 820         | 1300        | 6700         |


## Performance `HTTP/2`
- HTTP/2 Condition
    - Local M1 Mac.
    - `Locust` load test. (h2 client was integrated to `locust`).
    - `FastAPI` with `hypercorn` (Note that `uvicorn` seems to have not HTTP/2 compatibility.
    - Custom Server

RPS

| Server Type   | Type | Name | # Requests | # Fails | Average (ms) | Min (ms) | Max (ms) | Average size (bytes) | RPS    | Failures/s |
|---------------|------|------|------------|---------|--------------|----------|----------|----------------------|--------|------------|
| Custom Server | GET  | /200 | 705092     | 0       | 15.71        | 0        | 290      | 0                    | 1564.11| 0          |
| FAST API      | GET  | /200 | 500745     | 0       | 429.87       | 0        | 3893     | 0                    | 1111.84| 0          |

Response Time

| Server Type   | Method | Name | 50%ile (ms) | 60%ile (ms) | 70%ile (ms) | 80%ile (ms) | 90%ile (ms) | 95%ile (ms) | 99%ile (ms) | 100%ile (ms) |
|---------------|--------|------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|
| Custom Server | GET    | /200 | 9           | 12          | 16          | 21          | 33          | 56          | 120         | 290          |
| FAST API      | GET    | /200 | 200         | 360         | 730         | 960         | 1200        | 1300        | 1400        | 3900         |
