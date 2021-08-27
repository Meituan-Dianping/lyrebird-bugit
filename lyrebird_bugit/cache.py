from pathlib import Path
import codecs
import json
from flask.json import jsonify
import lyrebird

BUGIT_STORAGE = lyrebird.get_plugin_storage()
CACHE_ROOT = Path(BUGIT_STORAGE)/'cache'
LAST_SELECT_TEMPLATE_FILENAME = 'selected_template'


def get(template_key):
    return _read_cache_from_file(template_key)


def put(template_key, data):
    _save_cache_to_file(template_key, data)

    
def getCacheName(template_key):
    p_obj = Path(CACHE_ROOT)
    cache_name_list = []
    for file in p_obj.iterdir():
        if file.suffix == '.info' and template_key in str(file):
            cache_dic = {}
            try:
                with codecs.open(file, 'r') as f:
                    cache_name = json.load(f).get('cache_name')
                    cache_dic['cache_name'] = cache_name
                    cache_name_list.append(cache_dic)
            except Exception:
                continue
    if len(cache_name_list) == 0:
        return None
    return cache_name_list

def isOldFile():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if _cache:
        return 'cache_name' not in _cache
    return None


def delete(filename):
    target_file = CACHE_ROOT / filename
    if not target_file.exists():
        return False
    try:
        target_file.unlink()
        return True
    except Exception:
        return False


def selected_template(template_path, cache_name):
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, {'path': template_path, 'cache_name': cache_name})


def get_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if _cache:
        return _cache.get('path'), _cache.get('cache_name')
    else:
        return None


def add_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    _cache['cache_name'] = '默认草稿'
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, _cache)

def add_info_file_to_cache(cache_key):
    cache_info = {
        'cache_name': '默认草稿'
    }
    try:
        for file in CACHE_ROOT.iterdir():
            if file.name != 'selected_template' and not file.name.startswith('.'):
                file_name = file.name + '_' + str(cache_key)
                file_path = CACHE_ROOT / file_name
                info_path = CACHE_ROOT / (file_name+'.info')
                file.rename(file_path)
                with open(info_path, 'w') as f:
                    f.write(json.dumps(cache_info))
        return True
    except Exception:
        return False

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
