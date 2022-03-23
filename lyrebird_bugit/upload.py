import os
import time
import codecs
import shutil
import uuid
import lyrebird
from pathlib import Path
from lyrebird import publish


logger = lyrebird.log.get_logger()

BUGIT_STORAGE = lyrebird.get_plugin_storage()
UPLOAD_ROOT = Path(BUGIT_STORAGE)/'upload'


def get(file_name):
    _check_dir()
    file_path = Path(UPLOAD_ROOT).joinpath(file_name)
    if not file_path.exists():
        return None
    try:
        with codecs.open(str(file_path), 'rb') as f:
            return f.read()
    except Exception:
        return None


def _build_file_name(stream):
    if not stream.filename:
        return str(uuid.uuid4())
    file_name_base, file_name_ext = os.path.splitext(stream.filename)
    file_name = f'{file_name_base}_{int(time.time())}{file_name_ext}'
    return file_name


def add(stream):
    _check_dir()
    file_name = _build_file_name(stream)
    file_path = Path(UPLOAD_ROOT).joinpath(file_name)
    stream.save(str(file_path))
    upload_files = []
    upload_files.append(
        {
            'id': file_name,
            'upload_file': {
                'name': file_name,
                'path': str(file_path)
            }
        }
    )
    publish('upload_files', upload_files)


def delete(file_path):
    file_path = Path(file_path)
    if file_path.parent != UPLOAD_ROOT:
        return
    if file_path.exists() and file_path.is_file():
        file_path.unlink()


def _check_dir():
    if not UPLOAD_ROOT.exists():
        UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


def reset_dir():
    logger.debug('Upload files reset')
    if UPLOAD_ROOT.exists():
        shutil.rmtree(UPLOAD_ROOT)
