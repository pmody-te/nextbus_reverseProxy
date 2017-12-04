"""Reverse proxy for Next Bus server"""
import requests

##API ENDPOINTS##
API_ENDPOINTS = {
    "useShortTitles": "&useShortTitles=True",
    "agencyList": ["agencyList"],
    "routeList": ["routeList&a="],
    "routeConfig": ["routeConfig&a=", "&r="],
    "messages": ["messages&a=", "&r="],
    "predictByStop": ["predictions&a=", "&r=", "&s="],
    "predictByStopId": ["predictions&a=", "&stopId=", "&routeTag="],
    "predictionsForMultiStops": ["predictionsForMultiStops&a=", "&stops="],
    "vehicleLocations": ["vehicleLocations&a=", "&r=", "&t="],
    "schedule": ["schedule&a=", "&r="],
    "stats": ["stats"]
}

def createURL(config, endpoint):
	url = config['proxy_config']['target_url'] + "/service/publicXMLFeed?command=" + API_ENDPOINTS[endpoint][0]
	return url

if __name__ == '__main__':
	print load_config("../config.ini")
#	config_dict  = load_config(path)
	print http_request("http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList") 
