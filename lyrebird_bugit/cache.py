from pathlib import Path
import codecs
import json
import lyrebird


BUGIT_STORAGE = lyrebird.get_plugin_storage()
CACHE_ROOT = Path(BUGIT_STORAGE)/'cache'
LAST_SELECT_TEMPLATE_FILENAME = 'selected_template'


def get(template_key):
    return _read_cache_from_file(template_key)


def put(template_key, data):
    _save_cache_to_file(template_key, data)


def selected_template(template_path):
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, {'path': template_path})


def get_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if _cache:
        return _cache.get('path')
    else:
        return None


def _check_dir():
    if not CACHE_ROOT.exists():
        CACHE_ROOT.mkdir(parents=True, exist_ok=True)


def _save_cache_to_file(name, data):
    _check_dir()
    with codecs.open(str(CACHE_ROOT / name), 'w') as f:
        f.write(json.dumps(data))


def _read_cache_from_file(name):
    _check_dir()
    target_file = CACHE_ROOT / name
    if not target_file.exists():
        return None
    try:
        with codecs.open(str(target_file), 'r') as f:
            return json.load(f)
    except Exception:
        return None
