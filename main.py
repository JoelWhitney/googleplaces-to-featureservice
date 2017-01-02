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
import time

__author__='joelwhitney'
"""
  Requires Python 3+

  This script...

"""
from libraries.GooglePlaces.GooglePlacesAPI import GooglePlaces
from libraries.GooglePlaces import types, lang
from libraries.ArcRESTAPI.ArcRESTAPI import AGOLHandler
import argparse
from pyicloud import PyiCloudService

def agolHelper_playground():
    """practice area to test wrapper functions"""
    while True:
        parser = argparse.ArgumentParser()
        parser.add_argument('-portal', dest='sourcePortal', help="url of the source Portal", default="https://www.arcgis.com")
        parser.add_argument('-user', dest='username', help='Portal username', default="joel_Nitro")
        parser.add_argument('-password', dest='password', help='Portal password', default="joel.nitro")
        args = parser.parse_args()

        """get last iPhone location for Google Places search"""
        api = PyiCloudService('whitney.joel.b@gmail.com', 'Whitneyjb5')
        iphone6S = api.devices['SOgZzA09evu1n78fvaGBelmik77fmEl2vFGf+aUHaNmvP0GNtbAPT+HYVNSUzmWV']
        iphone6S_location = '{}, {}'.format(iphone6S.location()['latitude'], iphone6S.location()['longitude'])
        print(iphone6S_location)

        """search Google Places API and add to feature service"""
        api_key = 'AIzaSyDtbpYc0KAQ4-ZMLd6AnTcGfPo2xht8ilQ'
        google_places_handler = GooglePlaces(api_key)
        google_places = google_places_handler.nearby_search(location=iphone6S_location, rankby='distance', types=[types.TYPE_BAR])
        print(google_places.raw_response)

        """delete all features before adding new features to feature service"""
        # Get handler for source Portal for ArcGIS.
        agol_handler = AGOLHandler(args)
        feature_services = agol_handler.search(query='title:json_file type:Feature Service', token=agol_handler.token)
        feature_service = feature_services.results[0]
        print("AGOL: {}".format(google_places.agol_json.raw_agol_json))
        print("ArcREST: {}".format(google_places.agol_json.raw_arcrest_json))
        google_places.agol_json.write_jsonfile(google_places.agol_json.raw_agol_json)
        # delete features
        delete_features_response = agol_handler.delete_features(service_url=feature_service.url, where='ObjectId>0')
        print(delete_features_response)
        # add features
        add_features_response = agol_handler.add_features(service_url=feature_service.url, agol_json=google_places.agol_json.raw_arcrest_json)
        print(add_features_response)
        time.sleep(1800)

agolHelper_playground()







def nearbySearchExample_forAGOL():
    """uses the nearbysearch example to create an AGOL compatible json for a feature collection"""
    YOUR_API_KEY = 'AIzaSyDGFXgvnUHjX3wJkm4mFbwFM_XLj7ENKR8'
    google_places = GooglePlaces(YOUR_API_KEY)

    # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
            location='43.633354,-70.259941', rankby='distance', types=[types.TYPE_BAR])
    if query_result.has_attributions:
        print(query_result.html_attributions)
    agol_json = query_result.agol_json()
    print(agol_json.raw_json())
    agol_json.write_jsonfile()


def nearbySearchExample():
    """generic nearbysearch example"""
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
    """generic radarsearch example"""
    api_key = 'AIzaSyAkL_-vfoqk5tSXdzZMgLjGekpsPtPma58'
    nearbysearch_params = {
        'location': '43.633354,-70.259941',
        'type': 'bar',
        'rankby': 'distance'
    }
    GoogleAPIInterface = Google_Places_API(api_key)
    jsonResults = GoogleAPIInterface.search_places(nearbysearch_params, searchtype='nearbysearch')
    GoogleAPIInterface.write_json(jsonResults, filename='../nearbysearch_results')

