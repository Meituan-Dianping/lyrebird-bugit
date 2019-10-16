import imp
import traceback
from pathlib import Path
from lyrebird import application
from lyrebird import get_logger


logger = get_logger()


def get_workspace():
    bugit_workspace = application.config.get('bugit.workspace')

    if bugit_workspace and Path(bugit_workspace).exists():
        return Path(bugit_workspace)

    ROOT = application._cm.root
    metadata_dir = ROOT/'downloads'/'lyrebird_bugit'
    metadata_dir.mkdir(parents=True, exist_ok=True)
    logger.warning(
        f'Bugit workspace not exists! Create on {metadata_dir._str}')

    return metadata_dir


def template_list():
    template_list = []
    for template_file in get_workspace().iterdir():
        if not template_file.name.endswith('.py'):
            continue
        try:
            logger.debug(f'Load template {template_file}')
            template = imp.load_source(template_file.stem, str(template_file))
            template_check(template)
            template_list.append(
                {'name': template.name, 'path': str(template_file)})
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
