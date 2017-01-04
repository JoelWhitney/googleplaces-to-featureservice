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

  This script...
nohup python bgservice.py &
tail -f nohup.out

"""
from libraries.GooglePlaces.GooglePlacesAPI import GooglePlaces, AGOL_JSON
from libraries.GooglePlaces import types, lang
from libraries.ArcRESTAPI.ArcRESTAPI import AGOLHandler
import argparse
import time
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
        print('***' * 10 + 'GETTING IPHONE LOCATION' + '***' * 10)
        icloud_handler = PyiCloudService('whitney.joel.b@gmail.com', 'Whitneyjb5')
        iphone6S = icloud_handler.devices['SOgZzA09evu1n78fvaGBelmik77fmEl2vFGf+aUHaNmvP0GNtbAPT+HYVNSUzmWV']
        iphone6S_location = '{}, {}'.format(iphone6S.location()['latitude'], iphone6S.location()['longitude'])
        print("Location: {}, {}\nTimestamp: {}".format(iphone6S.location()['latitude'], iphone6S.location()['longitude'], iphone6S.location()['timeStamp']))


        # Get handler for source Portal for ArcGIS.
        agol_handler = AGOLHandler(args)

        # add my location features
        print('***' * 10 + 'ADDING MY LOCATION TO FEATURE SERVICE' + '***' * 10)
        feature_params = [{'geometry': {'latitude': iphone6S.location()['latitude'],
                                        'longitude': iphone6S.location()['longitude']},
                           'properties': {'timeStamp': str(iphone6S.location()['timeStamp']),
                                          'horizontalAccuracy': iphone6S.location()['horizontalAccuracy']}}]
        my_location_handler = AGOL_JSON(features=feature_params)
        feature_service_search2 = agol_handler.search(query='id:12ce9d04418a43a08044d9a6d527a8ff',
                                                      token=agol_handler.token)
        feature_service2 = feature_service_search2.results[0]
        delete_features_response2 = agol_handler.delete_features(service_url=feature_service2.url, where='ObjectId>0')
        print(delete_features_response2)
        add_features_response2 = agol_handler.add_features(service_url=feature_service2.url,
                                                           agol_json=my_location_handler.raw_arcrest_json)
        print(add_features_response2)

        """search Google Places API and add to feature service"""
        print('***' * 10 + 'ADDING GOOGLE PLACES TO FEATURE SERVICE' + '***' * 10)
        api_key = 'AIzaSyDtbpYc0KAQ4-ZMLd6AnTcGfPo2xht8ilQ'
        google_places_handler = GooglePlaces(api_key)
        google_places = google_places_handler.nearby_search(location=iphone6S_location, rankby='distance', types=[types.TYPE_BAR])
        places_agol_json = google_places.agol_json
        #places_agol_json.write_jsonfile(google_places.agol_json.raw_agol_json, filename='Beer_Near_Me')
        print(google_places.raw_response)

        """delete all features before adding new features to feature service"""
        feature_service_search1 = agol_handler.search(query='id:a697917677464992a8be2a93e3014db9', token=agol_handler.token)
        feature_service1 = feature_service_search1.results[0]
        # delete existing features
        delete_features_response = agol_handler.delete_features(service_url=feature_service1.url, where='ObjectId>0')
        print(delete_features_response)
        # add new Google Place features
        add_features_response1 = agol_handler.add_features(service_url=feature_service1.url, agol_json=google_places.agol_json.raw_arcrest_json)
        print(add_features_response1)

        # sleep 20 min before repeating
        time.sleep(1200)

if __name__ == '__main__':
    try:
        agolHelper_playground()
    except Exception as e:
        print("Error: " + str(e))


# def nearbySearchExample_forAGOL():
#     """uses the nearbysearch example to create an AGOL compatible json for a feature collection"""
#     YOUR_API_KEY = 'AIzaSyDGFXgvnUHjX3wJkm4mFbwFM_XLj7ENKR8'
#     google_places = GooglePlaces(YOUR_API_KEY)
#
#     # You may prefer to use the text_search API, instead.
#     query_result = google_places.nearby_search(
#             location='43.633354,-70.259941', rankby='distance', types=[types.TYPE_BAR])
#     if query_result.has_attributions:
#         print(query_result.html_attributions)
#     agol_json = query_result.agol_json()
#     print(agol_json.raw_json())
#     agol_json.write_jsonfile()
#
#
# def nearbySearchExample():
#     """generic nearbysearch example"""
#     api_key = 'AIzaSyAkL_-vfoqk5tSXdzZMgLjGekpsPtPma58'
#     nearbysearch_params = {
#         'location': '43.633354,-70.259941',
#         'type': 'bar',
#         'rankby': 'distance'
#     }
#     GoogleAPIInterface = Google_Places_API(api_key)
#     searchResult = GoogleAPIInterface.search_places(nearbysearch_params, searchtype='nearbysearch')
#     for place in searchResult.places:
#         # Returned places from a query are place summaries.
#         print(place.name)
#         print(place.geo_location)
#         print(place.place_id)
#         # The following method has to make a further API call.
#         #place.get_details()
#         # Referencing any of the attributes below, prior to making a call to
#         # get_details() will raise a googleplaces.GooglePlacesAttributeError.
#         print(place.details)  # A dict matching the JSON response from Google.
#         print(place.local_phone_number)
#         print(place.international_phone_number)
#         print(place.website)
#         print(place.url)
#         # Getting place photos
#         for photo in place.photos:
#             # 'maxheight' or 'maxwidth' is required
#             photo.get(maxheight=500, maxwidth=500)
#             # MIME-type, e.g. 'image/jpeg'
#             photo.mimetype
#             # Image URL
#             photo.url
#             # Original filename (optional)
#             photo.filename
#             # Raw image data
#             photo.data
#     GoogleAPIInterface.write_json(searchResult.raw_response, filename='../nearbysearch_results')
#
# def radarSearchExample():
#     """generic radarsearch example"""
#     api_key = 'AIzaSyAkL_-vfoqk5tSXdzZMgLjGekpsPtPma58'
#     nearbysearch_params = {
#         'location': '43.633354,-70.259941',
#         'type': 'bar',
#         'rankby': 'distance'
#     }
#     GoogleAPIInterface = Google_Places_API(api_key)
#     jsonResults = GoogleAPIInterface.search_places(nearbysearch_params, searchtype='nearbysearch')
#     GoogleAPIInterface.write_json(jsonResults, filename='../nearbysearch_results')
#
