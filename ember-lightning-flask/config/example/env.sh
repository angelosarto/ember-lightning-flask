#!/bin/sh

export PORT=5500
export INSTANCE=0
export REDIS_HOST=127.0.0.1
export REDIS_PORT=6379
export REDIS_SECRET

# url defaults to root if not set
#export APP_URL="mla"
# for a single app deploy (this app serves one ember lighting deployed project set app name
#export APP_NAME="my-lightning-app"
# prefixes the app name and adds :index on the end of the app_name, to override the key completely use REDIS_KEY
#export REDIS_PREFIX="my-pre:"
export REDIS_SUFFIX=":index"
#export REDIS_KEY="my-pre:my-lightning-app:index"

# or to serve any matched app name as a URL you can use auto - the appname must be a valid URL prefix
# whatever the url request contains as its first url will be used as the app-name e.g.
# /my-lightning-app will attempt to load my-lightning-app from redis respecting the redis_prefix and redis_suffix
export APP_NAME="AUTO"

# to host multiple ember apps in the same service set up a mapping of a url to an app name and optionally a redis_key.
# If redis_key is ommited it will use redis_prefix + app_name + redis_suffix

#export APP_MAP='
#{
#    "some-url":{
#        "app_name" : "my-lightning-app",
#        "redis_key": "my-pre:my-lightning-app:index"
#    },
#    "some-other-url":{
#        "app_name" : "my-lightning-app2"
#    }
#}'
