import imp
import traceback
from hashlib import md5
from pathlib import Path
from lyrebird import application
from lyrebird import get_logger


logger = get_logger()

default_template_ready = None

def get_workspace():
    bugit_workspace = application.config.get('bugit.workspace')

    if bugit_workspace and Path(bugit_workspace).exists():
        return Path(bugit_workspace)

    ROOT = application._cm.ROOT
    metadata_dir = ROOT/'downloads'/'lyrebird_bugit'
    metadata_dir.mkdir(parents=True, exist_ok=True)
    logger.warning(
        f'Bugit workspace not exists! Create on {metadata_dir._str}')

    return metadata_dir


def get_default_template_path():
    bugit_workspace = application.config.get('bugit.workspace', '')
    bugit_default_template = application.config.get('bugit.default_template', '')
    if default_template_ready is None:
        default_template_check(bugit_workspace, bugit_default_template)
    template_path = Path(bugit_workspace + bugit_default_template)
    if bugit_default_template:
        return template_path


def template_list():
    template_list = []
    default_template_path = get_default_template_path()
    if not default_template_ready:
        return template_list

    for template_file in get_workspace().iterdir():
        if not template_file.name.endswith('.py'):
            continue
        if default_template_path and template_file != default_template_path:
            continue
        try:
            logger.debug(f'Load template {template_file}')
            template = imp.load_source(template_file.stem, str(template_file))
            template_check(template)
            relative_template_file_path = str(template_file).replace(str(Path.home()), '~')
            template_key = md5(relative_template_file_path.encode()).hexdigest()
            template_list.append({
                'name': template.name,
                'path': str(template_file),
                'id': template_key
            })
            del template
        except Exception:
            logger.error(
                f'Load bug template failed:\nBad template: {template_file}\n{traceback.format_exc()}')
    return template_list


def template_check(template):
    assert hasattr(template, 'name'), "BugIt template should have name attr"
    assert hasattr(template, 'form'), "BugIt template should have form attr"
    assert callable(template.form), "BugIt template should have form function"
    assert hasattr(
        template, 'submit'), "BugIt template should have submit attr"
    assert callable(
        template.submit), "BugIt template should have submit function"


def default_template_check(workspace, default_template):
    global default_template_ready

    template_path = Path(workspace + default_template)
    if not template_path.exists():
        logger.error('Default template path is not existed.')
        default_template_ready = False
        return
    
    if application.config.get('event.notice.autoissue.checker'):
        if not default_template:
            logger.error('Default template is not configured.')
            default_template_ready = False
            return
        template = get_template(template_path)
        if not (hasattr(template, 'auto_issue_handler') and callable(template.auto_issue_handler)):
            logger.error('BugIt template should have auto_issue_handler function.')
            default_template_ready = False
            return
    
    default_template_ready = True


def get_template(file_path):
    template = imp.load_source(Path(file_path).stem, str(file_path))
    return template


def notice_handler(msg):
    default_template_path = get_default_template_path()

    if not default_template_ready:
        return
    
    # Filter out messages with invalid types
    if not isinstance(msg, dict):
        return
    
    template = get_template(default_template_path)
    template.auto_issue_handler(msg)
