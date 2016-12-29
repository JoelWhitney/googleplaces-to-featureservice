"""
COPYRIGHT 2016 ESRI

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
__author__='joelwhitney'
"""
  Requires Python 3+

  This script uses the Google Places API to search for places
  A search request is made with the following https request
    +  https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters
    +  Required: key, location, radius, rankby=distance
    +  Optional: keyword, language, minprice/maxprice, name, opennow, rankby, type, pagetoken
    +  Example: https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=YOUR_API_KEY
    +  API Key:  AIzaSyAkL_-vfoqk5tSXdzZMgLjGekpsPtPma58

  Required inputs:
    +  URL to a Feature Service
    +  Username / password with administrator  rights for the feature service
  Doc Reference:
    +  http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Update_Features/02r3000000zt000000/
    +  https://developers.google.com/places/web-service/search

  Usage:
"""
from libraries.GooglePlacesAPI import Google_Places_API

def nearbySearchExample():
    api_key = 'AIzaSyAkL_-vfoqk5tSXdzZMgLjGekpsPtPma58'
    nearbysearch_params = {
        'location': '43.633354,-70.259941',
        'type': 'bar',
        'rankby': 'distance'
    }

    GoogleAPIInterface = Google_Places_API(api_key)
    searchResult = GoogleAPIInterface.search_places(nearbysearch_params, searchtype='nearbysearch')
    for place in searchResult.places:
        # Returned places from a query are place summaries.
        print(place.name)
        print(place.geo_location)
        print(place.place_id)
        # The following method has to make a further API call.
        #place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        print(place.details)  # A dict matching the JSON response from Google.
        print(place.local_phone_number)
        print(place.international_phone_number)
        print(place.website)
        print(place.url)
        # Getting place photos
        for photo in place.photos:
            # 'maxheight' or 'maxwidth' is required
            photo.get(maxheight=500, maxwidth=500)
            # MIME-type, e.g. 'image/jpeg'
            photo.mimetype
            # Image URL
            photo.url
            # Original filename (optional)
            photo.filename
            # Raw image data
            photo.data
    GoogleAPIInterface.write_json(searchResult.raw_response, filename='../nearbysearch_results')

def radarSearchExample():
    api_key = 'AIzaSyAkL_-vfoqk5tSXdzZMgLjGekpsPtPma58'
    nearbysearch_params = {
        'location': '43.633354,-70.259941',
        'type': 'bar',
        'rankby': 'distance'
    }

    GoogleAPIInterface = Google_Places_API(api_key)
    jsonResults = GoogleAPIInterface.search_places(nearbysearch_params, searchtype='nearbysearch')
    GoogleAPIInterface.write_json(jsonResults, filename='../nearbysearch_results')

nearbySearchExample()
