"""
Code to access Bing Search API
"""
import urllib
import urllib2
import json

class BingAPI:
    #The base URL for all endpoints
    BASE_URL = 'https://api.datamarket.azure.com/Bing/Search/v1'

    def __init__(self):
        """
        Initializes API wrapper
        """

        import os
        try:
            key = os.environ.get('BING_API')
            if not key:
                print('API key not found in environment variable BING_API.')
                sys.exit(0)
            if key == '':
                #The key file should't be blank
                print('API key appears to be blank, please run: export BING_API=YOUR_KEY_HERE')
                sys.exit(0)
            else:
                #setup the key
                self.apikey = key
        except Exception as e:
            print(e)

    def search(self, source, query, market):
        """
        Generic wrapper for the Bing Search API.

        source: API Source, e.g. "News" or "Image"
        query: The search term
        market: Geographic market to search, e.g. "en-US"

        Returns a dict containing the API response.
        """

        query = urllib.quote(query)

        # create credential for authentication
        credentials = (':%s' % self.apikey).encode('base64')[:-1]
        auth = 'Basic %s' % credentials

        url = BingAPI.BASE_URL + '/{0}?Query=%27{1}%27&Market=%27{2}%27&$format=json'.format(source, query, market)

        request = urllib2.Request(url)
        request.add_header('Authorization', auth)
        request_opener = urllib2.build_opener()
        response = request_opener.open(request)
        response_data = response.read()

        raw_result = json.loads(response_data)

        # Process weird API format to get an array of result objects
        result = raw_result['d']['results']

        return result

    def news(self, query):
        """
        Convenience method to search Bing News API.
        Hardcoded to search en-US market for now.

        query: The search term.
        """
        return self.search("News", query, "en-US")

    def image(self, query):
        """
        Convenience method to search Bing Image API.
        Hardcoded to search en-US market for now.

        query: The search term.
        """
        return self.search("Image", query, "en-US")


