import flask
import requests
import validators

app = flask.Flask(__name__)

method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
    'OPTIONS': requests.options,
}


@app.route('/')
def index():
    return ""


@app.route('/ping')
def ping():
    return "pong"


@app.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):
    if not validators.url(url):
        flask.abort(404)

    request_function = method_requests_mapping[flask.request.method]

    request_headers = filter(lambda tuple: tuple[0] != "Host",
                             flask.request.headers)
    request_headers = dict(request_headers)

    request = request_function(url,
                               stream=True,
                               params=flask.request.args,
                               headers=request_headers)

    response_content = flask.stream_with_context(request.iter_content())

    response = flask.Response(response_content,
                              content_type=request.headers['content-type'],
                              status=request.status_code)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response


if __name__ == '__main__':
    app.run(debug=True)
