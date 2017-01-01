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

"""
from libraries.GooglePlaces.GooglePlacesAPI import GooglePlaces
from libraries.GooglePlaces import types, lang
from libraries.ArcRESTAPI.ArcRESTAPI import AGOLHandler
import argparse

def agolHelper_playground():
    parser = argparse.ArgumentParser()
    parser.add_argument('-portal', dest='sourcePortal', help="url of the source Portal", default="https://www.arcgis.com")
    parser.add_argument('-user', dest='username', help='Portal username', default="joel_Nitro")
    parser.add_argument('-password', dest='password', help='Portal password', default="joel.nitro")
    args = parser.parse_args()
    # Get handler for source Portal for ArcGIS.
    agol_handler = AGOLHandler(args)
    search_results = agol_handler.search(query='title:json_file type:Feature Service', token=agol_handler.token)

    result = search_results.results[0]
    delete_features_response = agol_handler.delete_features(service_url=result.url)
    print(delete_features_response)

    # for item in services['results']:
    #     print(item)
    # delete_features = agol_handler.delete_features()

    # token = agol_handler.token
    # print(agol_handler.token)
    #
    # # Get a list of the content matching the query.
    # content = getUserContent(portalUrl=sourcePortal, username=user, token=token)
    #
    # resultsCount = len(content)
    # if resultsCount != 0:
    #     count = 1
    #     # Copy the content into the destination user's account.
    #     for item in content:
    #         print(item)
    #         # description = getItemDescription(item['id'], sourcePortal, token)
    #         # data = getItemData(item['id'], sourcePortal, sourceToken)
    #         # print(('*' * 30) + ' ITEM {} '.format(count) + ('*' * 30))
    #         # print(description)
    #         count += 1
    #     print(("*" * 90) + "\nFinished showing {} results..\nQUERY: {}\nPORTAL: {}".format(resultsCount, query,
    #                                                                                        sourcePortal))
    # else:
    #     print(("*" * 90) + "\nQuery returned no results..\nQUERY: {}\nPORTAL: {}".format(query, sourcePortal))

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

