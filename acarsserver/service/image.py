import json
import magic
import os
from PIL import Image
from urllib import request

from acarsserver.mapper.db.aircraft import AircraftDbMapper


class ImageService:

    MEDIAWIKI_URL = 'https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&' + \
        'gcmtitle=Category:{}_(aircraft)&gcmtype=file&redirects=1&prop=imageinfo&iiprop=url&format=json'
    adapter = None
    logger = None

    def __init__(self, adapter, logger):
        self.adapter = adapter
        self.logger = logger

    def handle(self, aircraft):
        # fetch the aircraft image if missing
        if not self.exists(aircraft):
            self.logger.info('Downloading "{}" aircraft image.'.format(aircraft.registration))
            url = ImageService.get_url(aircraft)
            if url:
                filename = self.download_image(url, aircraft)
                AircraftDbMapper(self.adapter).update(aircraft, filename)
                self.logger.info('Aircraft image downloaded.')

                self.logger.info('Optimizing image.')
                self.optimize(filename)

                self.logger.info('Creating thumbnail.')
                self.create_thumbnail(filename)
                return

            self.logger.warning('Aircraft "{}" image URL could not be fetched.'.format(aircraft.registration))
            return

        self.logger.info('Aircraft "{}" image already exists.'.format(aircraft.registration))
        return

    def exists(self, aircraft):
        if not aircraft.image:
            return False

        path = os.path.dirname(os.path.realpath(__file__))
        return os.path.isfile('{}/../app/assets/img/aircrafts/large/{}'.format(path, aircraft.image))

    @staticmethod
    def get_url(aircraft):
        response = request.urlopen(ImageService.MEDIAWIKI_URL.format(aircraft.registration))

        data = json.loads(response.read().decode('utf-8'))
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']

            return [elem for elem in pages.values()][0]['imageinfo'][0]['url']

        return None

    @staticmethod
    def download_image(url, aircraft):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = '{}.{}'.format(aircraft.registration.lower(), url.split('.')[-1:][0].lower())
        filepath = '{}/../app/assets/img/aircrafts/large/{}'.format(path, filename)

        request.urlretrieve(url, filepath)

        return filename

    def create_thumbnail(self, filename):
        base_path = os.path.dirname(os.path.realpath(__file__))
        aircrafts_path = '{}/../app/assets/img/aircrafts/'.format(base_path)

        format = self.get_image_format(filename)
        if not format:
            return False

        try:
            image = Image.open(aircrafts_path + 'large/' + filename)
            image.thumbnail((180, 120))
            image.save(aircrafts_path + 'thumb/' + filename, format)
            self.logger.info('Thumbnail creation successful for "{}".'.format(filename))
            return True
        except (KeyError, IOError) as ex_save:
            self.logger.error('Thumbnail creation failed for "{}": {}'.format(filename, str(ex_save)))

        return False

    def optimize(self, filename):
        base_path = os.path.dirname(os.path.realpath(__file__))
        aircrafts_path = '{}/../app/assets/img/aircrafts/'.format(base_path)

        format = self.get_image_format(filename)
        if not format:
            return False

        try:
            image = Image.open(aircrafts_path + 'large/' + filename)
            image.save(
                aircrafts_path + 'large/' + filename,
                format=format,
                progressive=True,
                quality=95,
                optimize=True
            )
            self.logger.info('Image optimization successful for "{}".'.format(filename))
            return True
        except (KeyError, IOError) as ex_save:
            self.logger.error('Image optimization failed for "{}": {}'.format(filename, str(ex_save)))

        return False

    def get_image_format(self, filepath):
        base_path = os.path.dirname(os.path.realpath(__file__))
        aircrafts_path = '{}/../app/assets/img/aircrafts/large/{}'.format(base_path, filepath)

        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(aircrafts_path)
        except (FileNotFoundError) as ex_mime:
            self.logger.error('Could not get mime type for "{}": {}'.format(filename, str(ex_mime)))
            return None

        return mime_type.split('/')[1].upper()
