import json
import codecs
import lyrebird
import os
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
DRAFT_VERSION_V_1_8_0 = version.parse('1.8.0')
DRAFT_VERSION_V_1_12_4 = version.parse('1.12.4')


def get(template_key):
    return _read_cache_from_file(template_key)


def put(template_key, data):
    _save_cache_to_file(template_key, data)


def delete(template_key):
    _delete_cache_from_file(template_key)


def get_filename(abs_template_path, draft_name=''):
    relative_template_path = _change_home(abs_template_path, str(Path.home()), '~')
    template_key = md5(relative_template_path.encode()).hexdigest()
    if not draft_name:
        return f'{template_key}'

    draft_key = md5(draft_name.encode()).hexdigest()
    return f'{template_key}_{draft_key}'


def selected_template(abs_template_path, cache_name):
    relative_template_path = _change_home(abs_template_path, str(Path.home()), '~')
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, 
                        {'path': relative_template_path, 'cache_name': cache_name, 'draft_version': '1.12.4'})


def get_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    if not _cache:
        return None
    selected_template_path = _cache.get('path')
    return str(Path(selected_template_path).expanduser())


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
        return DRAFT_VERSION_V_1_12_4
    if 'draft_version' in _cache:
        return DRAFT_VERSION_V_1_12_4
    return DRAFT_VERSION_V_1_8_0


def update_selected_template():
    _cache = _read_cache_from_file(LAST_SELECT_TEMPLATE_FILENAME)
    template_path = _change_home(_cache['path'], str(Path.home()), '~')  # for macOS and winOS
    template_path = _change_home(_cache['path'], '/root', '~')  # for Linux OS
    _cache['path'] = template_path
    if 'cache_name' not in _cache:
        _cache['cache_name'] = DEFAULT_DRAFT_NAME
    _cache['draft_version'] = '1.12.4'
    _save_cache_to_file(LAST_SELECT_TEMPLATE_FILENAME, _cache)


def generate_template_keys(templates):
    if 'HOST_HOME' in os.environ:
        other_home_path = os.environ['HOST_HOME']
    else:
        other_home_path = '/root'
    
    template_keys_map = {}
    for template in templates:
        new_template_key = template['id']
        template_key = str(md5(template['path'].encode()).hexdigest())
        template_keys_map[template_key] = new_template_key
        other_absolute_path = _change_home(template['path'], str(Path.home()), other_home_path)
        other_template_key = str(md5(other_absolute_path.encode()).hexdigest())
        template_keys_map[other_template_key] = new_template_key
    return template_keys_map


def update_all_draft_file(templates):
    template_keys_map = generate_template_keys(templates)

    for cache_file in CACHE_ROOT.iterdir():
        if cache_file.name.startswith('.'):
            continue
        if cache_file.name in BUGIT_SYSTEM_FILENAME:
            continue
        if cache_file.name.endswith(DRAFT_INFO_FILE_SUFFIX):
            continue

        cache_name_parts = cache_file.name.split('_')
        if len(cache_name_parts) < 2:
            continue
        old_template_key = cache_name_parts[0]
        cache_key = cache_name_parts[1]
        if old_template_key not in template_keys_map:
            continue
        
        new_template_key = template_keys_map[old_template_key]
        file_name = f'{new_template_key}_{cache_key}'
        detail_path = CACHE_ROOT / file_name
        info_path = CACHE_ROOT / f'{cache_file}.info'
        new_info_path = CACHE_ROOT / f'{file_name}.info'
        if detail_path.exists():
            try:
                with codecs.open(str(info_path), 'r') as f:
                    cache_name = json.load(f)['cache_name']
            except Exception:
                logger.error(f'Update cache from v1.8.0 to v1.12.4 error! \
                             Cannot read the info file: {str(cache_file)}')
                continue
            cache_name = f'{cache_name}_copy'
            try:
                with open(info_path, 'w') as f:
                    f.write(json.dumps({'cache_name': cache_name}, ensure_ascii=False))
            except Exception:
                logger.error(f'Update cache from v1.8.0 to v1.12.4 error! \
                             Cannot write the info file: {str(cache_file)}')
                continue
            cache_key = str(md5(cache_name.encode()).hexdigest())
            file_name = f'{new_template_key}_{cache_key}'
            detail_path = CACHE_ROOT / file_name
            new_info_path = CACHE_ROOT / f'{file_name}.info'
        cache_file.rename(detail_path)
        info_path.rename(new_info_path)


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


def _change_home(original_path, old_home, new_home):
    """
    Change the home part of the original path:
    from an old OS to a new OS, or from absolute to relative (when new_home = '~')
    """
    _path = original_path.replace(old_home, new_home)
    return _path
