"""
Code to access Freebase API
"""
from apiclient import discovery
import json

class FreebaseAPI:

    IMAGE_BASE = 'https://www.googleapis.com/freebase/v1/image'

    def __init__(self, mid=None):
        """
        Initializes API wrapper
        """
        import os
        try:
            key = os.environ.get('FREEBASE_API')
            if not key:
                print('API key not found in environment variable FREEBASE_API.')
                sys.exit(0)
            if key == '':
                #The key file should't be blank
                print('API key appears to be blank, please run: export FREEBASE_API=YOUR_KEY_HERE')
                sys.exit(0)
            else:
                #setup the key
                self.apikey = key
        except Exception as e:
            print(e)

        self.mid = mid

        self._service = discovery.build('freebase', 'v1',  developerKey=self.apikey)

        self._cache = {}
        

    def _fetch_all(self, mid=None):
        """
        Internal method to fetch all the Freebase data associated with
        a given MQL ID.
        """
        if not mid:
            mid = self.mid
        request = self._service.search(query=mid, output='(all)')
        response = request.execute(num_retries=5)
        raw_result = json.loads(response)
        self._cache[mid] = raw_result['result'][0]['output']['all']

    def description(self, mid=None):
        """
        Returns the description for the given entity.
        """
        if not mid:
            mid = self.mid
        if mid not in self._cache:
            self._fetch_all(mid)
        all = self._cache[mid]
        return all['description./common/topic/description'][0]

    def image_url(self, mid=None):
        """
        Returns an image URL for the given entity.  Size parameters
        may be added to the URL by the frontend.
        """
        if not mid:
            mid = self.mid
        return self.IMAGE_BASE + mid