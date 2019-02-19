#!/usr/local/env python3

import exifread
import magic
import urllib
from urllib.request import urlopen


class MetadataExtractor:
    '''This class extracts data from files. Requires file url.'''

    def __init__(self, url):
        self.url = url

    def get_file_mime(self):
        '''Extracts the MIME type of the file.'''
        request = urllib.request.Request(self.url)
        response = urlopen(request)
        mime_type = magic.from_buffer(response.readline())
#        mime_type = magic.from_buffer(response.read(128))
        return mime_type

    def get_file_exif(self, f):
        '''Extracts the file metadata.
        Currently only supports local files.
        '''
        return self._get_file_exif(f)


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

        return tags_dict
