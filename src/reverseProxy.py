"""Reverse proxy for Next Bus server"""
import requests
##API ENDPOINTS##
API_ENDPOINTS = {
    "useShortTitles": "&useShortTitles=True",
    "agencyList": ["agencyList"],
    "routeList": ["routeList&a=%s"],
    "routeConfig": ["routeConfig&a=%s&r=%s"],
    "messages": ["messages&a=%s&r=%s"],
    "predictByStop": ["predictions&a=%s&r=%s&s=%s"],
    "predictByStopIdrt": ["predictions&a=%s&stopId=%s&routeTag=%s"],
    "predictByStopId": ["predictions&a=%s&stopId=%s"],
    "predictionsForMultiStops": ["predictionsForMultiStops&a=%s"],
    "vehicleLocations": ["vehicleLocations&a=%s&r=%s&t=%s"],
    "schedule": ["schedule&a=%s&r=%s"],
    "stats": ["stats"]
}

def createURL(config, endpoint):
	"""creates the query url using the API endpoints and the target url for the API """
	url = config['proxy_config']['target_url'] + "/service/publicXMLFeed?command=" + API_ENDPOINTS[endpoint][0]
	return url

if __name__ == '__main__':
	print API_ENDPOINTS
