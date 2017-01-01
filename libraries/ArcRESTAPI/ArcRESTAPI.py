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

  A simple wrapper around the ArcREST API..
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

    def get_token(self, exp=60):  # expires in 60 minutes
        """Generates a token."""
        parameters = urllib.parse.urlencode({'username': self.username,
                                             'password': self.password,
                                             'client': 'referer',
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

    def search(self, query=None, numResults=100, sortField='numviews', sortOrder='desc', start=0, token=None):
        '''Retrieve a single page of search results.'''
        parameters = {'q': query,
                      'num': numResults,
                      'sortField': sortField,
                      'sortOrder': sortOrder,
                      'f': 'json',
                      'start': start}
        if token:
            parameters['token'] = token
        parameters = urllib.parse.urlencode(parameters).encode("utf-8")
        request = self.sourcePortal + '/sharing/rest/search?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        # try:
        #     if 'token' in json_response:
        #         return AGOLResults(self, json_response)
        #     elif 'error' in json_response:
        #         print(json_response['error']['message'])
        #         for detail in json_response['error']['details']:
        #             print(detail)
        # except ValueError as e:
        #     print('An unspecified error occurred.')
        #     print(e)
        return AGOLResults(self, json_response)

    def get_user_content(self):
        ''''''
        parameters = urllib.parse.urlencode({'token': self.token, 'f': 'json'}).encode("utf-8")
        request = self.sourcePortal + '/sharing/rest/content/users/' + self.username + '?'
        json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
        return json_response

    def get_item_description(self, item_id):
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

    def delete_features(self, service_url, layer_id=0, where='ObjectId>0'):
        '''Returns the description for a Portal for ArcGIS item.
        http://resources.arcgis.com/en/help/arcgis-rest-api/#/Delete_Features/02r3000000w4000000/'''
        parameters = urllib.parse.urlencode({'where': where,
                                             'f': 'json',
                                             'token': self.token}).encode("utf-8")
        request = service_url + '/{}/deleteFeatures?'.format(str(layer_id))
        try:
            json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
            if 'deleteResults' in json_response:
                return json_response
            elif 'error' in json_response:
                print(json_response['error']['code'])
                print(json_response['error']['message'])
                for detail in json_response['error']['details']:
                    print(detail)
        except ValueError as e:
            print('An unspecified error occurred.')
            print(e)

    def add_features(self, service_url, agol_json):
        '''Returns the description for a Portal for ArcGIS item.
        http://resources.arcgis.com/en/help/arcgis-rest-api/#/Add_Features/02r30000010m000000/'''
        parameters = urllib.parse.urlencode({'features': agol_json,
                                             'f': 'json',
                                             'token': self.token}).encode("utf-8")
        request = service_url + '/{}/addFeatures?'.format(str(agol_json))
        try:
            json_response = json.loads(urllib.request.urlopen(request, parameters).read().decode("utf-8"))
            if 'deleteResults' in json_response:
                return json_response
            elif 'error' in json_response:
                print(json_response['error']['code'])
                print(json_response['error']['message'])
                for detail in json_response['error']['details']:
                    print(detail)
        except ValueError as e:
            print('An unspecified error occurred.')
            print(e)


class AGOLResults(object):
    """
    Wrapper around the AGOLHandler search function.
    """

    def __init__(self, search_instance, json_response):
        self._search_instance = search_instance
        self._response = json_response
        self._results = []
        for json_result in json_response['results']:
            self._results.append(Result(search_instance, json_result))

    def some_function(self):
        pass

    @property
    def raw_response(self):
        return self._response

    @property
    def results(self):
        return self._results


class Result(object):
    """
    Wrapper around the AGOLResults.
    """

    def __init__(self, search_instance, json_result):
        self._search_instance = search_instance
        self._result = json_result
        self._id = json_result.get('id', None)
        self._url = json_result.get('url', None)

    @property
    def raw_response(self):
        return self._result

    @property
    def id(self):
        return self._id

    @property
    def url(self):
        return self._url