import flask 
from flask import Response,g,request
import reverseProxy
import tools 
import logging 
import time 
import json
from flask_caching import Cache
from redis import Redis

APP 	= 	flask.Flask(__name__)
config 	= 	tools.load_config("/Users/pranoymody/Desktop/Code/reverseProxy/config.ini")
cache 	=	 Cache(APP, config={'CACHE_TYPE': 'redis',
	'CACHE_REDIS_HOST': config['proxy_config']['redis_host'],
	'CACHE_REDIS_PORT':config['proxy_config']['redis_port'],
	'CACHE_DEFAULT_TIMEOUT':config['proxy_config']['cache_timeout']})
redis	=	Redis( host=config['proxy_config']['redis_host'] , port=config['proxy_config']['redis_port'])

@APP.before_request
def before_request():
	g.start = time.time()

@APP.route('/api/v1/agencyList')
@cache.cached()
def agencyList():
	url = reverseProxy.createURL(config,"agencyList")
	redis.incr('agencyList')
	xml = tools.http_request(url)
	redis.incr(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/routeList/<agency>/')
@cache.cached()
def routeList(agency):
	url = reverseProxy.createURL(config,"routeList") + agency
	redis.incr('routeList')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/stats/')
def metrics():
	metrics = {"queries":redis.hgetall('queries'),"slow_requests":redis.hgetall('slow_requests')}
	return Response(json.dumps(metrics,indent=2), mimetype='application/json') 

@APP.route('/api/v1/stats/reset')
def reset():
	redis.flushall()
	return Response("Database has been flushed", mimetype='text') 

@APP.after_request
def after_request(response):
    diff = time.time() - g.start
    if diff > 0.01 :
    	redis.hset('slow_requests',request.path,str(diff)+"s")
    if request.path != "/api/v1/stats/reset" :
    	print request.path
    	redis.hincrby('queries', request.path,1)
    print "Exec time: %ss" % str(diff)
 #   if (response.response):
 #       response.response[0] = response.response[0].replace('__EXECUTION_TIME__', str(diff))
    return response

if __name__ == '__main__':
    APP.debug=True
    APP.run()
