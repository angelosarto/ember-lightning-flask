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

    index_key = request.args.get('index_key', None)

    if config.lightning_app_automatic:
        app_name = app_url
        redis_key = None

    elif config.lightning_app_map.get(app_url, False):
        app_name = config.lightning_app_map.get(app_url)['app_name']
        redis_key = config.lightning_app_map.get(app_url).get('redis_key', None)

    else:
        return "No such Application Configured", 404

    if redis_key is None:
        redis_key = config.redis_prefix+app_name+config.redis_suffix

    redis_conn = redis.StrictRedis(host=config.redis_host, port=config.redis_port, password=config.redis_secret,decode_responses=True)
    if index_key is None:
        index_key = redis_conn.get(redis_key+":current")
        if index_key is None:
            if redis_conn.exists(redis_key+":revisions"):
                return "No such Application - App is deployed, no active deployment", 404
            else:
                return "No such Application - that application does not exist", 404

    # index_key is now set, check for requested revision
    if not redis_conn.exists(redis_key+":"+index_key):
        if redis_conn.exists(redis_key+":revisions"):
            return "No such Application - App is deployed, that revision does not exist", 404
        else:
            return "No such Application - that application does not exist", 404

    page = redis_conn.get(redis_key+":"+index_key)

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
