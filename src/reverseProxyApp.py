""" Reverse proxy for Next Bus server using flask """

import flask 
from flask import Response,g,request
import reverseProxy
import tools 
import time 
import json
from flask_caching import Cache
from redis import ConnectionError
from redis import Redis
import logging 

config 	= 	tools.load_config("config.ini")

##Setup Logging 
logging.basicConfig()
logger = logging.getLogger('reverseProxyApp')

""" Initializing the flask app with redis caching """
APP 	= 	flask.Flask(__name__)
redis_host = config['proxy_config']['redis_host']
redis_port = config['proxy_config']['redis_port']
cache 	=	 Cache(APP, config={'CACHE_TYPE': 'redis',
	'CACHE_REDIS_HOST': redis_host,
	'CACHE_REDIS_PORT': redis_port,
	'CACHE_DEFAULT_TIMEOUT':config['proxy_config']['cache_timeout']})
slow_requests_threshold = float (config['proxy_config']['slow_requests_threshold'])
redis	=	Redis( host=redis_host , port=redis_port )
try:
	redis.ping()
except ConnectionError:
	logger.error("Redis isn't available, check the server %s:%s and try again"%(redis_host,redis_port))
	exit(0)



@APP.before_request
def before_request():
	"""Start request timer for metrics"""
	g.start = time.time()

@APP.route('/api/v1/agencyList')
@cache.cached()
def agencyList():
	url = reverseProxy.createURL(config,"agencyList")
	redis.incr('agencyList')
	xml = tools.http_request(url)
	redis.incr(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/routeList/<agency>')
@cache.cached()
def routeList(agency):
	url = reverseProxy.createURL(config,"routeList") %(agency)
	redis.incr('routeList')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/routeConfig/<agency>/<route>')
@cache.cached()
def routeConfig(agency,route):
	url = reverseProxy.createURL(config,"routeConfig") %(agency,route)
	redis.incr('routeConfig')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/messages/<agency>/<route>')
@cache.cached()
def messages(agency,route):
	url = reverseProxy.createURL(config,"messages") %(agency,route)
	redis.incr('messages')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/schedule/<agency>/<route>')
@cache.cached()
def schedule(agency,route):
	url = reverseProxy.createURL(config,"schedule") %(agency,route)
	redis.incr('schedule')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/predictByStop/<agency>/<route>/<stop>')
@cache.cached()
def predictByStop(agency,route,stop):
	url = reverseProxy.createURL(config,"predictByStop") %(agency,route,stop)
	redis.incr('predictByStop')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/predictByStopId/<agency>/<stopId>/<routeTag>')
@cache.cached()
def predictByStopIdrt(agency,stopId,routeTag=False):
	url = reverseProxy.createURL(config,"predictByStopIdrt") %(agency,stopId,routeTag)
	redis.incr('predictByStopId')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/predictByStopId/<agency>/<stopId>')
@cache.cached()
def predictByStopId(agency,stopId):
	url = reverseProxy.createURL(config,"predictByStopId") %(agency,stopId)
	redis.incr('predictByStopId')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/vehicleLocations/<agency>/<route>/<time>')
@cache.cached()
def vehicleLocations(agency,route,time):
	url = reverseProxy.createURL(config,"vehicleLocations") %(agency,route,time)
	redis.incr('vehicleLocations')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')


@APP.route('/api/v1/predictionsForMultiStops/<agency>/<stops>')
@cache.cached()
def predictionsForMultiStops(agency,stops):
	url = reverseProxy.createURL(config,"predictionsForMultiStops") %(agency)
	for stop in stops.split("&"):
		url = url + "&stops=%s"%stop
	redis.incr('predictionsForMultiStops')
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/stats/')
def metrics():
	metrics = {"queries":redis.hgetall('queries'),"slow_requests":redis.hgetall('slow_requests')}
	return Response(json.dumps(metrics,indent=2), mimetype='application/json')

@APP.route('/api/v1/stats/reset')
def reset():
	"""Flushes all the keys from the redis db"""
	redis.flushall()
	return Response("Database has been flushed\n", mimetype='text') 

@APP.after_request
def after_request(response):
	""" Calculates the request time and checks for slow requests """
	request_time = time.time() - g.start
	logger.debug("Exec time: %ss" % str(request_time))
	request_time = round(request_time*1000)/1000
	if request_time > slow_requests_threshold :
		redis.hset('slow_requests',request.path,str(request_time)+"s")
	if request.path != "/api/v1/stats/reset" :
		logger.debug("Requested Path: "+request.path)
		redis.hincrby('queries', request.path,1)
	return response

if __name__ == '__main__':
	APP.debug=True
	try:
		app_port = int(config['proxy_config']['app_port'])
	except Exception as e:
		logger.error("Bad configuration file, enter a valid PORT number %s %s" % (config['proxy_config']['app_port'], e))
	APP.run(host ='0.0.0.0' , port = app_port)
