import flask 
from flask import Response
import reverseProxy
import tools 
import logging 
import time 


APP = flask.Flask(__name__)
config = tools.load_config("../config.ini")

@APP.route('/api/v1/agencyList')
def agencyList():
	url = reverseProxy.createURL(config,"agencyList")
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

@APP.route('/api/v1/routeList/<agency>/')
def routeList(agency):
	url = reverseProxy.createURL(config,"routeList") + agency
	xml = tools.http_request(url)
	return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
    APP.debug=True
#    print config['proxy_config']['target_url']
    APP.run()
