from pathlib import Path
import codecs
import json
import lyrebird
import requests
from lyrebird.application import config

BUGIT_STORAGE = lyrebird.get_plugin_storage()
ATTACHMENT_ROOT = Path(BUGIT_STORAGE)/'attachments'

EXPORT_URL = 'http://%s:%s/api/snapshot/export/event' %(config.get('ip'), config.get('mock.port'))

def _check_dir():
    if not ATTACHMENT_ROOT.exists():
       CACHE_ROOT.mkdir(parents=True, exist_ok=True)

def export_snapshot(snapshot):
    _check_dir()
    file_content = requests.post(EXPORT_URL,json=snapshot['eventObj'],stream=True).content
    with codecs.open(str(ATTACHMENT_ROOT / snapshot['name'])+'.lb', 'wb') as f:
        f.write(file_content)
    return {'id':snapshot['eventObj']['id'],'name':snapshot['name']+'.lb',
    'path':str(ATTACHMENT_ROOT / snapshot['name'])+'.lb'}
