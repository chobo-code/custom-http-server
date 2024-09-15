import asyncio
from server import Dispatcher, Server
from generic_http_object import GenericHttpRequest, GenericHttpResponse
from status_code import StatusCode


@Dispatcher.route(path='/200', methods=['POST', 'GET'])
async def path_200(http_request: GenericHttpRequest, http_response: GenericHttpResponse):
    print('path_200 called.')
    http_response.status_code = StatusCode.OK
    http_response.body = 2
    return http_response


@Dispatcher.request_mapping(path='/')
async def path_default(http_request: GenericHttpRequest, http_response: GenericHttpResponse):
    print('default_path function called.')
    http_response.status_code = StatusCode.OK
    http_response.body = 3
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
