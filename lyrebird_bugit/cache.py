import json
import codecs
import lyrebird
from hashlib import md5
from pathlib import Path
from packaging import version


logger = lyrebird.log.get_logger()

BUGIT_STORAGE = lyrebird.get_plugin_storage()
CACHE_ROOT = Path(BUGIT_STORAGE)/'cache'
LAST_SELECT_TEMPLATE_FILENAME = 'selected_template'
BUGIT_SYSTEM_FILENAME = [LAST_SELECT_TEMPLATE_FILENAME]
DRAFT_INFO_FILE_SUFFIX = '.info'
DEFAULT_DRAFT_NAME = 'Default'
DRAFT_VERSION_V_1_7_0 = version.parse('1.7.0')
DRAFT_VERSION_V_1_8_0 = version.parse('1.8.0')


def get(template_key):
    return _read_cache_from_file(template_key)


def put(template_key, data):
    _save_cache_to_file(template_key, data)


def delete(template_key):
    _delete_cache_from_file(template_key)


def get_filename(template_path, draft_name=''):
    template_key = md5(template_path.encode()).hexdigest()
    if not draft_name:
        return f'{template_key}'

    draft_key = md5(draft_name.encode()).hexdigest()
    return f'{template_key}_{draft_key}'


def selected_template(template_path, cache_name):
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, {'path': template_path, 'cache_name': cache_name})


def get_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if not _cache:
        return None
    return _cache.get('path')


def get_selected_cache():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if not _cache:
        return None
    return _cache.get('cache_name')


def get_draft_list(template_key):
    draft_list = []
    for draft_file in CACHE_ROOT.iterdir():
        if draft_file.suffix != DRAFT_INFO_FILE_SUFFIX:
            continue
        if template_key not in str(draft_file):
            continue

        try:
            with codecs.open(draft_file, 'r') as f:
                cache_name = json.load(f).get('cache_name')
                draft_list.append({'cacheName': cache_name})
        except Exception:
            logger.error(f'Load BugIt cache fail! {str(draft_file)}')

    draft_list.sort(key=lambda x: x['cacheName'])
    return draft_list


def check_draft_version():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if not _cache:
        return DRAFT_VERSION_V_1_8_0
    if 'cache_name' in _cache:
        return DRAFT_VERSION_V_1_8_0
    return DRAFT_VERSION_V_1_7_0


def update_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    _cache['cache_name'] = DEFAULT_DRAFT_NAME
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, _cache)


def update_all_draft_file():
    cache_key = str(md5(DEFAULT_DRAFT_NAME.encode()).hexdigest())

    for cache_file in CACHE_ROOT.iterdir():
        if cache_file.name.startswith('.'):
            continue
        if cache_file.name in BUGIT_SYSTEM_FILENAME:
            continue

        file_name = f'{cache_file.name}_{cache_key}'
        detail_path = CACHE_ROOT / file_name
        info_path = CACHE_ROOT / f'{file_name}.info'
        cache_file.rename(detail_path)
        try:
            with open(info_path, 'w') as f:
                f.write(json.dumps({'cache_name': DEFAULT_DRAFT_NAME}, ensure_ascii=False))
        except Exception:
            logger.error(f'Update cache error! {str(cache_file)}')


def _check_dir():
    if not CACHE_ROOT.exists():
        CACHE_ROOT.mkdir(parents=True, exist_ok=True)


def _save_cache_to_file(name, data):
    _check_dir()
    with codecs.open(str(CACHE_ROOT / name), 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))


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

def _delete_cache_from_file(name):
    target_file = CACHE_ROOT / name
    if target_file.exists() and target_file.is_file():
        target_file.unlink()
