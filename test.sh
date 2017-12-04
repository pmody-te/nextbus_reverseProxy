#! /bin/bash

# Small script for testing endpoints. Every endpoint will return JSON response.

function endpointTesting()
{
    declare -a endpoints=( "agencyList"
        "routeList/sf-muni"
        "routeConfig/sf-muni/E"
        "predictByStopId/sf-muni/15184"
        "predictByStop/sf-muni/E/5184"
        "predictByStop/sf-muni/E/5184&useShortTitles=True"
        "predictionsForMultiStops/sf-muni/N|6997"
        "predictionsForMultiStops/sf-muni/N|6997&N|3909&useShortTitles=True"
        "schedule/agencyList/E"
        "vehicleLocations/sf-muni/E/0"
        "stats" )

    for i in "${endpoints[@]}"
    do
    if curl -s --head  --request GET http://127.0.0.1:8080/api/v1/$i | grep "xml\|json" > /dev/null; then
    sleep 0.1
    echo "Endpoint "$i "is OK"
    else
    echo "Endpoint "$i "is NOT OK"
    fi
    done
}

function gzipTesting()
{
    if curl -s -H "Accept-Encoding: gzip, deflate" --head  --request GET http://127.0.0.1:8080/api/v1/agencyList | grep "gzip" > /dev/null; then
    sleep 0.1
    echo "gzip responses is OK"
    else
    echo "gzip responses is NOT OK"
    fi    
}

echo "Checking Endpoints"
echo "=================="
endpointTesting

echo 
echo "Checking gzip responses"
echo "======================="
gzipTesting

