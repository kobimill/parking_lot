import os
import json
import requests

API_KEY = 'c489d8fc3e88957'


def ocr_space(filename_or_url, overlay=False, language='eng'):
    """ OCR.space API request with local file/ URL.
    :param filename_or_url: Your file path / Url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    payload = {'isOverlayRequired': overlay,
               'apikey': API_KEY,
               'language': language,
               }

    if os.path.isfile(filename_or_url):  # Image-file
        with open(filename_or_url, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename_or_url: f},
                              data=payload,
                              )

    elif filename_or_url.startswith('http'):  # Url
        payload['url'] = filename_or_url
        r = requests.post('https://api.ocr.space/parse/image',
                          data=payload)

    else:
        return {}

    json_str = r.content.decode()
    json_data = json.loads(json_str)
    return json_data


