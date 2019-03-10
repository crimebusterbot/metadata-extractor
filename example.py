import pprint

from metadata_extractor import MetadataExtractor


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    # test any file mime type
    url = ('https://mosaic03.ztat.net/vgs/media/spp-media/w320'
           '/e678931a754049c7b72d61d702d582f0'
           '/20f9980b73af40509e4c6e5abf992bc2.jpeg')
    extractor = MetadataExtractor(url)
    print(extractor.get_file_mime())

    # test exif of image
    f = '20f9980b73af40509e4c6e5abf992bc2.jpeg'
    exif_dict = extractor.get_file_exif(f)
    pp.pprint(exif_dict)
