import flask
import flask_limiter
import markdown
import pathlib
import requests
import validators
import urllib

app = flask.Flask(__name__)
limiter = flask_limiter.Limiter(app,
                                key_func=flask_limiter.util.get_remote_address,
                                default_limits=['200 per day', '50 per hour'])

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
    md = pathlib.Path('README.md').read_text()
    html = markdown.markdown(md)

    return html


@app.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):
    if not validators.url(url):
        flask.abort(404)

    request_function = method_requests_mapping[flask.request.method]

    request_headers = dict(flask.request.headers)
    request_headers['Host'] = urllib.parse.urlparse(url).netloc
    request_headers['User-Agent'] = 'cors.pub'

    request = request_function(url,
                               stream=True,
                               params=flask.request.args,
                               data=flask.request.data,
                               headers=request_headers)

    response = flask.Response(request.iter_content(),
                              status=request.status_code,
                              headers=dict(request.headers))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response


if __name__ == '__main__':
    app.run(debug=True)
