import flask 
from flask import Response,g
import reverseProxy
import tools 
import logging 
import time 
from flask_caching import Cache

APP = flask.Flask(__name__)
cache = Cache(APP, config={'CACHE_TYPE': 'redis','CACHE_REDIS_HOST': 'localhost','CACHE_REDIS_PORT':'6379','CACHE_DEFAULT_TIMEOUT':'5'})
config = tools.load_config("/Users/pranoymody/Desktop/Code/reverseProxy/config.ini")


@APP.before_request
def before_request():
	g.start = time.time()

@APP.route('/api/v1/agencyList')
@cache.cached()
def agencyList():
	url = reverseProxy.createURL(config,"agencyList")
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/routeList/<agency>/')
@cache.cached()
def routeList(agency):
	url = reverseProxy.createURL(config,"routeList") + agency
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.after_request
def after_request(response):
    diff = time.time() - g.start
    print "Exec time: %s" % str(diff)
    if (response.response):
        response.response[0] = response.response[0].replace('__EXECUTION_TIME__', str(diff))
    return response

if __name__ == '__main__':
    APP.debug=True
#    print config['proxy_config']['target_url']
    APP.run()
