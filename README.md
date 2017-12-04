NextBus Reverse Proxy
===

A simple reverse proxy for San Francisco's public transportation powered by NextBus's XML feed.   


## Usage run locally 

```bash
# run reverseProxy server
$> ./run.sh
# test for common things 
$> ./test.sh
```

## Demo using docker-compose 
1. [Install docker-compose](https://docs.docker.com/v1.5/compose/install/)
2. docker-compose up 
3. curl localhost:8080/api/v1/agencyList

## Dependencies
- **Used Python Flask, the micro web framework as the reverse proxy broker because it is lightweight and easy to implement
- **Redis for caching the responses of NextBus XML feed and storing the api metrics** 
- **Python 2.7**
	- redis
	- requests
	- flask 
	- flask_caching

## Design Specification

**Design Choices**
1. Redis was the choice for caching, it supports `key:value` mappings
	* Redis gives one a scalable cache infrastructure as well as rich representations to cache objects.
2. Flask as it is a light micro web framework, which is easy to impliment.
	* Flask implements the most commonly-used core components of a web application framework, like URL routing, request and response objects, and templates which encompasses all that is required. 


**Configuration Settings**
You can configure reverseProxy in  `config.ini`
	- "redis_host" & "redis_port" for caching and storing metrics 
	- "slow_requests_threshold"  
	- "cache_timeout" 

## Reverseproxy API Endpoints 

The application address is, by default, `127.0.0.1:8080/`. A brief description of all the end points are given below. 
The `api/v1/stats` endpoint is particular to the state of reverse proxy

|*api/v1/stats*| Exposes Reverseproxy statistics |
|:---:|:---|
|*slow_requests*| Lists the endpoints which had response time higher a certain threshold along with the time taken.|
|*queries*|List all the endpoints queried by the user along with the number of requests for each.|

|*/api/v1/stats/reset*| Reset stats |
|:---|:---|

|End points| Description | 
|:---|:---|
|*api/v1/agencyList*| Lists all agencies.|
|*api/v1/routeList/{agency}*| Lists all the routes for the agency tag supplied.
|*api/v1/routeConfig/{agency}/{route}*| Lists all the stops for the route tag supplied.
|*api/v1/predictByStopId/{agency}/{stopId}*| Lists arrival/departure predictions for a stop.|
|*api/v1/predictByStop/{agency}/{route}/{stop}*| Same as predictByStopId but using the *{stop}* tag instead *{route}* tag is required because *{stop}* tag is associated with a route.  
|*api/v1/predictionsForMultiStops/{agency}/{stops}*| Lists arrival/departure predictions for multi-stops. The format of the *{stops}* tag is *route or stop* . Append more stops using "&" for more stops .|
|*api/v1/schedule/{agency}/{route}*| Obtain the schedule information for a given *{agency}* and *{route}* tags
|*api/v1/messages/{agency}/{route}*| List the active messages for the selected route. Append *{/route}*for more routes.
|*api/v1/vehicleLocations/{agency}/{route}/{time}*| Lists vehicle locations for the selected *{route}*. *{time}* tag is in msec since the 1970 epoch time. If you specify a time of 0, then data for the last 15 minutes is provided.

	Get {agency} tags using `agencyList`
	Get {route} tags using `routeList`, 
    Get {stop} and {stopId} tags using `routeConfig`.
    A /{route} tag  can be appended if predictions for only one route 
    are desired.
    Append `&useShortTitles=true` to return short titles intended for display
    devices with small screens.

### Examples
   
1. `api/v1/agencyList`
2. `api/v1/routeList/sf-muni`
2. `api/v1/routeConfig/sf-muni/E`
3. `api/v1/predictByStopId/sf-muni/15184`
4. `api/v1/predictByStop/sf-muni/E/5184&useShortTitles=True`
5. `api/v1/predictionsForMultiStops/sf-muni/N|6997&N|3909&useShortTitles=True`		
6. `api/v1/schedule/sf-muni/E`
7. `api/v1/vehicleLocations/sf-muni/E/0`
8. `api/v1/stats`
   

## References 
- [Next Bus XML Feed Documentation](http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf)
- [DMBI Reverse Proxy](https://github.com/dmbi/NextBus-Reverse-Proxy) 
