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

  This sc...
"""
import urllib
import urllib.parse
import urllib.request
import json

class AGOLHandler(object):
    """
    ArcGIS Online handler class.
      -Generates and keeps tokens
    """

    def __init__(self, args):
        self.username = args.username
        self.password = args.password
        self.sourcePortal = args.sourcePortal
        self.token, self.http, self.expires = self.get_token()

    def get_token(self, exp=60):  # expires in 60minutes
        """Generates a token."""
        parameters = urllib.parse.urlencode({'username': self.username,
                                             'password': self.password,
                                             'client': 'requestip',
                                             'referer': self.sourcePortal,
                                             'expiration': exp,
                                             'f': 'json'}).encode("utf-8")
        request = self.sourcePortal + '/sharing/rest/generateToken?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        try:
            if 'token' in json_response:
                return json_response['token'], request, json_response['expires']
            elif 'error' in json_response:
                print(json_response['error']['message'])
                for detail in json_response['error']['details']:
                    print(detail)
        except ValueError as e:
            print('An unspecified error occurred.')
            print(e)

    def search(self, query=None, numResults=100, sortField='numviews',
               sortOrder='desc', start=0, token=None):
        '''Retrieve a single page of search results.'''
        parameters = urllib.parse.urlencode({'q': query,
                                             'num': numResults,
                                             'sortField': sortField,
                                             'sortOrder': sortOrder,
                                             'f': 'json',
                                             'start': start}).encode("utf-8")
        if token:
            # Adding a token provides an authenticated search.
            parameters['token'] = token
        request = self.sourcePortal + '/sharing/rest/search?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        return json_response

    def get_usercontent(self):
        ''''''
        parameters = urllib.parse.urlencode({'token': self.token, 'f': 'json'}).encode("utf-8")
        request = self.sourcePortal + '/sharing/rest/content/users/' + self.username + '?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        return json_response

    def get_itemdescription(self, item_id):
        '''Returns the description for a Portal for ArcGIS item.'''
        parameters = urllib.parse.urlencode({'token': self.token, 'f': 'json'}).encode("utf-8")
        request = self.sourcePortal + '/sharing/rest/content/items/' + item_id + '?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        return json_response

    def get_itemdata(self, item_id):
        '''Returns the description for a Portal for ArcGIS item.'''
        parameters = urllib.parse.urlencode({'token': self.token, 'f': 'json'}).encode("utf-8")
        request = self.sourcePortal + '/sharing/rest/content/items/' + item_id + '/data?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        return json_response

    def delete_features(itemId, portalUrl, token):
        '''Returns the description for a Portal for ArcGIS item.
        http://resources.arcgis.com/en/help/arcgis-rest-api/#/Delete_Features/02r3000000w4000000/'''
        # DELETE http://services.myserver.com/ERmEceOGq5cHrItq/ArcGIS/rest/services/SanFrancisco/311Incidents/FeatureServer/0/deleteFeatures

        parameters = urllib.parse.urlencode({'token': token,
                                             'f': 'json'})
        response = urllib.request.urlopen(portalUrl + "/sharing/rest/content/items/" +
                                          itemId + "/data?" + parameters).read()
        return response

    def add_features(itemId, portalUrl, token):
        '''Returns the description for a Portal for ArcGIS item.
        http://resources.arcgis.com/en/help/arcgis-rest-api/#/Add_Features/02r30000010m000000/'''
        # DELETE http://services.myserver.com/ERmEceOGq5cHrItq/ArcGIS/rest/services/SanFrancisco/311Incidents/FeatureServer/0/addFeatures

        parameters = urllib.parse.urlencode({'token': token,
                                             'f': 'json'})
        response = urllib.request.urlopen(portalUrl + "/sharing/rest/content/items/" +
                                          itemId + "/data?" + parameters).read()
        return response