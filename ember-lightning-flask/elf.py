from flask import Flask, Response, request
import redis


from configuration import ConfigSource, Configuration
config = Configuration()
if not config.load():
    print("No configuration")
    exit(-1)

app = Flask(__name__)

@app.route('/', defaults={'app_url': ''})
@app.route('/<app_url>')
def lightning(app_url):

    app_name = None
    if config.lightning_app_map is not None:
        app_name = config.lightning_app_map.get(app_url)
    elif config.lightning_app_automatic:
        if app_url != '':
            app_name = app_url
    elif app_url == config.lightning_url:
        app_name = config.lightning_app_name

    if app_name is None:
        return "No such Application Configured", 404

    redis_conn = redis.StrictRedis(host=config.redis_host, port=config.redis_port, password=config.redis_secret)

    index_key = request.args.get('index_key', None)
    requested_default = False
    if index_key is None:
        index_key = redis_conn.get(app_name + ':current')
        requested_default = True
    else:
        index_key = app_name + ':' + index_key

    if not redis_conn.exists(index_key):
        if redis_conn.exists(app_name):
            if requested_default:
                return "No such Application - App is deployed, no active deployment", 404
            else:
                return "No such Application Version - That App Version is not deployed", 404
        else:
            return "No such Application - that application does not exist", 404

    page = redis_conn.get(index_key)

    if page is None or len(page) == 0:
        return "No such Application - that application has no content", 404

    resp = Response(page)
    resp.headers['X-UI-APP-NAME'] = app_name
    resp.headers['X-UI-APP-VERSION'] = index_key
    resp.status_code = 200

    return resp

if __name__ == '__main__':
    app.debug = False # this shows errors in the browser if True
    app.run(host='0.0.0.0', port=config.application_port, use_reloader=False)
