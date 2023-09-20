import imp
import traceback
from hashlib import md5
from pathlib import Path
from lyrebird import application
from lyrebird import get_logger


logger = get_logger()


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
    template_path = Path(bugit_workspace + bugit_default_template)
    if bugit_workspace and bugit_default_template and template_path.exists():
        return template_path


def template_list():
    template_list = []
    default_template_path = get_default_template_path()
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


def get_template(file_path):
    template = imp.load_source(Path(file_path).stem, str(file_path))
    return template


def notice_handler(msg):
    # Filter out messages with invalid types
    if not isinstance(msg, dict):
        return
    
    # Filter out messages from unconfigured extensions
    checker_switch = application.config.get('autoissue.checker.switch', {})
    sender_file = msg.get('sender', {}).get('file', '')
    if sender_file not in checker_switch:
        return
    
    default_template_path = get_default_template_path()
    if default_template_path is None:
        logger.error(f'Init Auto Issue Server Failed. Template path is configured incorrectly: {default_template_path}')
        return
    
    template = get_template(default_template_path)
    template.AutoIssue().auto_issue_handler(msg)
