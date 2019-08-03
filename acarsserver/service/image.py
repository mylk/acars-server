import json
import os
from urllib import request


class ImageService:

    MEDIAWIKI_URL = 'https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&' + \
        'gcmtitle=Category:{}_(aircraft)&gcmtype=file&redirects=1&prop=imageinfo&iiprop=url&format=json'

    @staticmethod
    def handle(msg):
        # fetch the aircraft image if missing
        if not ImageService.exists(msg.aircraft):
            print('Downloading {} aircraft image.'.format(msg.aircraft))
            url = ImageService.get_url(msg.aircraft)
            if url:
                ImageService.download_image(url, msg.aircraft)
                print('Aircraft image downloaded.')
            else:
                print('Aircraft image URL could not be fetched.')

    @staticmethod
    def exists(aircraft):
        path = os.path.dirname(os.path.realpath(__file__))
        return os.path.isfile('{}/../app/assets/img/aircrafts/{}.jpg'.format(path, aircraft.lower()))

    @staticmethod
    def get_url(aircraft):
        response = request.urlopen(ImageService.MEDIAWIKI_URL.format(aircraft))

        data = json.loads(response.read().decode('utf-8'))
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']

            return [elem for elem in pages.values()][0]['imageinfo'][0]['url']

        return None

    @staticmethod
    def download_image(url, aircraft):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = '{}/../app/assets/img/aircrafts/{}.{}'.format(path, aircraft.lower(), url.split('.')[-1:][0])

        request.urlretrieve(url, filename)
