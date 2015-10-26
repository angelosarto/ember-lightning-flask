from flask import Flask
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
    index_key = redis_conn.get(app_name + ':current')

    if index_key is None:
        if redis_conn.exists(app_name):
            return "No such Application - App is deployed, no active deployment", 404
        else:
            return "No such Application - App is not deployed", 404

    page = redis_conn.get(index_key)

    if page is None or len(page) == 0:
        return "No such Application - missing content", 404

    return page, 202

if __name__ == '__main__':
    app.run(port=config.application_port)
