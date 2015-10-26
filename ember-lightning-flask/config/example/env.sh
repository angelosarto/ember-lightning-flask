#!/bin/sh

export PORT=5500
export INSTANCE=0
export REDIS_HOST=127.0.0.1
export REDIS_PORT=6379
export REDIS_SECRET

# url defaults to root if not set
export URL_PREFIX="/mla"
# for a single app deploy (this app serves one ember lighting deployed project set app name
export APP_NAME="my-lightning-app"

# to host multiple ember apps in the same service set up a mapping of url to app name using JSON
#export APP_MAP='{"url":"my-app-name", "mla":"my-lightning-app"}'

# or to serve any matched app name as a URL you can use auto - the appname must be a valid URL prefix
# whatever the url request contains as its first url will be used as the app-name e.g.
# /my-lightning-app will attempt to load my-lightning-app from redis.
#export APP_NAME="AUTO"

