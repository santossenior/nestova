# listings/utils/indexnow.py

import requests
import logging

logger = logging.getLogger(__name__)

INDEXNOW_KEY = '8ba8973ffc2f4f8f81e991d958529808'
INDEXNOW_HOST = 'nestovaproperty.com'
INDEXNOW_KEY_LOCATION = f'https://{INDEXNOW_HOST}/{INDEXNOW_KEY}.txt'


def notify_indexnow(urls):
    if isinstance(urls, str):
        urls = [urls]

    payload = {
        "host": INDEXNOW_HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": INDEXNOW_KEY_LOCATION,
        "urlList": urls
    }

    try:
        response = requests.post(
            'https://api.indexnow.org/indexnow',
            json=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=10
        )
        logger.info(f"IndexNow submitted {len(urls)} URLs — status: {response.status_code}")
        return response.status_code

    except requests.RequestException as e:
        logger.error(f"IndexNow failed: {e}")
        return None