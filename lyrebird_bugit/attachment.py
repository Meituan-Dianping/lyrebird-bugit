from pathlib import Path
import os
import codecs
import json
from uuid import uuid4
import lyrebird
import requests
import shutil
from lyrebird.application import config

BUGIT_STORAGE = lyrebird.get_plugin_storage()
ATTACHMENT_ROOT = Path(BUGIT_STORAGE)/'attachments'

EXPORT_URL = f'http://127.0.0.1:{config.get("mock.port")}/api/snapshot/export/event'


def _check_dir():
    if not ATTACHMENT_ROOT.exists():
        ATTACHMENT_ROOT.mkdir(parents=True, exist_ok=True)


def export_snapshot(snapshot):
    _check_dir()
    res = requests.post(EXPORT_URL, json=snapshot['eventObj'], stream=True)
    # SnapshotId is unique id of snapshot
    id_ = res.headers.get('SnapshotId')
    with codecs.open(str(ATTACHMENT_ROOT / snapshot['name'])+'.lb', 'wb') as f:
        for chunck in res.iter_content():
            f.write(chunck)
    return {
        'id': id_,
        'name': snapshot['name']+'.lb',
        'path': str(ATTACHMENT_ROOT / snapshot['name'])+'.lb',
    }


def export_attachment_file(attachment_obj):
    _check_dir()
    id_ = str(uuid4())
    full_name = f'{attachment_obj.get("name", "")}.{attachment_obj.get("attachmentType", "json")}'
    with codecs.open(str(ATTACHMENT_ROOT / full_name), 'w') as f:
        f.write(json.dumps(attachment_obj.get("eventObj", {}), indent=4, ensure_ascii=False))
    return {
        'id': id_,
        'name': full_name,
        'path': str(ATTACHMENT_ROOT / full_name),
    }


def remove_attach():
    if not ATTACHMENT_ROOT.exists():
        pass
    else:
        shutil.rmtree(ATTACHMENT_ROOT)


def rename(attachment_item, new_file_name):
    raw_file_path = Path(attachment_item.get('path'))
    if not raw_file_path.exists():
        raise FileNotFoundError(f'File [{raw_file_path.name}] not exists.')
    new_file_path = raw_file_path.parent.joinpath(new_file_name)
    os.rename(raw_file_path, new_file_path)
    attachment_item['path'] = str(new_file_path)
    attachment_item['name'] = new_file_path.name
