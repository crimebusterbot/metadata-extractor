#!/usr/local/env python3

import exifread
import io
import magic
import pprint
import urllib
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup as bs


class MetadataExtractor:

    def __init__(self, url):
        self.url = url

    def get_file_mime(self):
        request = urllib.request.Request(self.url)
        response = urlopen(request)
        mime_type = magic.from_buffer(response.readline())
#        mime_type = magic.from_buffer(response.read(128))
        return mime_type

    def get_file_exif(self, f):
        resp = requests.get(self.url, stream=True)
        return self._get_image_exif(f)


    @staticmethod
    def _get_file_exif(filepath):
        # EXIF official docs: https://www.exif.org/Exif2-2.PDF
        # Open image file for reading (binary mode)
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, strict=True)
            tags_dict = {k: v.values for k, v in tags.items()
                if k not in (
                    'JPEGThumbnail',
                    'EXIF UserComment',
                    'EXIF MakerNote',
                    'MakerNote Tag 0x0022',
                    'MakerNote Tag 0x001F',
                    'MakerNote Tag 0x0018',
                    'MakerNote Tag 0x0000',
                )
            }
            #import pdb; pdb.set_trace()

        return tags_dict


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    # test any file mime type
    url = ('https://mosaic03.ztat.net/vgs/media/spp-media/w320'
           '/e678931a754049c7b72d61d702d582f0'
           '/20f9980b73af40509e4c6e5abf992bc2.jpeg')
    extractor = MetadataExtractor(url)
    print(extractor.get_file_mime())

    # test exif of image
    f = '/home/alexandr/Pictures/toyota-prius-2010-13.jpg'
    exif_dict = extractor.get_file_exif(f)
    pp.pprint(exif_dict)
    #print(exif_dict['MakerNote Macromode'].values)
