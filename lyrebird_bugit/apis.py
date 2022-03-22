import base64
import codecs
import inspect
from pathlib import Path
from flask import request, jsonify, send_file
import lyrebird
from lyrebird import log
from lyrebird import application
from lyrebird.mock.context import make_fail_response, make_ok_response
from . import event_handler
from . import template_loader
from . import cache
from . import upload
from . import attachment
import traceback


logger = log.get_logger()


def template():
    if request.method == 'GET':
        '''
        Get all template list, all draft list, last selected template and last selected draft
        '''
        draft_version = cache.check_draft_version()
        if draft_version < cache.DRAFT_VERSION_V_1_8_0:
            logger.info('Updating draft into v1.8.0 from v1.7.0')
            cache.update_selected_template()
            cache.update_all_draft_file()

        templates = template_loader.template_list()
        last_selected_template = cache.get_selected_template()
        selected_template_index = None
        for index, template in enumerate(templates):
            if template['path'] == last_selected_template:
                selected_template_index = index
                break
        if not selected_template_index:
            return application.make_ok_response(templates=templates)

        template_key = cache.get_filename(last_selected_template)
        drafts = cache.get_draft_list(template_key)
        last_selected_cache = cache.get_selected_cache()

        return application.make_ok_response(
            selected_template_index=selected_template_index,
            templates=templates,
            selected_cache=last_selected_cache,
            drafts=drafts
        )

    elif request.method == 'POST':
        '''
        Get template detail by path
        And save lastest_selected_template
        '''
        if not request.json or not request.json.get('path'):
            return application.make_fail_response('Missing required argument: path')

        template_path = request.json['path']
        draft_name = request.json.get('cache_name', '')
        draft_filename = cache.get_filename(template_path, draft_name)
        template_detail = cache.get(draft_filename)

        template = template_loader.get_template(template_path)
        if inspect.getargspec(template.form).args:
            template_detail = template.form({'cache': template_detail})
        else:
            template_detail = template.form()

        cache.selected_template(template_path, draft_name)
        return jsonify(template_detail)


def issue():
    issue_req = request.json
    template_info = issue_req['template']
    template = template_loader.get_template(template_info['path'])

    issue_data = issue_req['issue']
    attachments = issue_req['attachments']
    snapshots = issue_req['snapshots']

    all_bugit_message = ''

    # Export Snapshot
    for snapshot in snapshots:
        attachments.append(attachment.export_snapshot(snapshot))
    # Set bugit script context
    context = {'issue': issue_data, 'attachments': attachments}
    # Set submit actions
    submit_action_functions = template.submit()
    # Do submit
    for action_function in submit_action_functions:
        try:
            bug_url = action_function(context)
            if bug_url:
                all_bugit_message += bug_url
        except Exception as e:
            if e.__class__.__name__ == 'BugitFormInputError':
                return application.make_fail_response(str(e))
            error_message = traceback.format_exc()
            trace = "<br/>".join(error_message.split("\n"))
            lyrebird.report({
                'action': 'bugit.submit',
                'bugit': {
                    'status': 'failure',
                    'data': issue_data,
                    'error': error_message
                }
            })
            return application.make_fail_response(f'Script function "{action_function.__name__}" crash.<br/>{trace}')
    lyrebird.report({
        'action': 'bugit.submit',
        'bugit': {
            'status': 'success',
            'data': issue_data
        }
    })
    #Delete Snapshot
    attachment.remove_attach()
    return application.make_ok_response(message=f'Create issue success! {all_bugit_message}')


def take_screenshot(platform, device_id):
    """
    channel: {platform}.cmd
    """
    channel = platform+'.cmd'
    cmd = {}
    cmd['cmd'] = 'screenshot'
    cmd['device_id'] = [device_id]
    lyrebird.publish(channel.lower(), cmd)
    return application.make_ok_response(message=f'Take screenshot success!')

# Get available device from iOS&Android plugin
def device():
    if request.method == 'GET':
        all_devices = [
            *[_update_device_info(d, platform='Android')
              for d in event_handler.android_devices],
            *[_update_device_info(d, platform='iOS') for d in event_handler.ios_devices]
        ]
        return jsonify(all_devices)


def _update_device_info(device_info, platform="Android"):
    device_info['platform'] = platform
    return device_info


def attachments(attachment_id=None):
    if request.method == 'GET':
        if not attachment_id:
            attachment_list = list(event_handler.attachments.values())
            if not attachment_list:
                upload.reset_dir()
                attachment.remove_attach()
            return jsonify(attachment_list)
        else:
            attachment_item = event_handler.attachments.get(attachment_id)
            if attachment_item:
                return send_file(attachment_item['path'])
            else:
                return make_fail_response('Not found attachment')

    elif request.method == 'PUT':
        path = Path(event_handler.attachments[attachment_id].get('path'))
        name = event_handler.attachments[attachment_id].get('name')
        image_data = request.json.get('imageData')

        image_data = image_data.replace('data:image/png;base64,', '', 1)

        with codecs.open(str(path), 'wb') as f:
            image_data = base64.decodebytes(image_data.encode())
            f.write(image_data)
        return make_ok_response(message=f'Edited picture {name} has been saved')

    elif request.method == 'DELETE':
        attachment_item = event_handler.attachments.pop(attachment_id)
        upload.delete(attachment_item.get('path'))
        return make_ok_response()

    # Upload attachment files
    elif request.method == 'POST':
        if request.files:
            stream = request.files['file']
            if not stream:
                return application.make_fail_response('Missing file data')

            upload.add(stream)
            return application.make_ok_response()
        return application.make_fail_response('No upload file found')


def ui_cache(template_key):
    if request.method == 'GET':
        data = cache.get_draft_list(template_key)
        return application.make_ok_response(data=data)

    elif request.method == 'POST':
        template_path = request.json.get('template_path')
        if not template_path:
            return application.make_fail_response('Missing required argument: template_path')

        cache_name = request.json.get('cache_name')
        if not cache_name:
            return application.make_fail_response('Missing required argument: cache_name')

        template_detail = request.json.get('data')
        if not template_detail:
            return application.make_fail_response('Missing required argument: data')

        for field in template_detail:
            if 'extraMsg' in field:
                del field['extraMsg']

        draft_name = cache.get_filename(template_path, cache_name)
        cache.put(draft_name, template_detail)
        cache.put(f'{draft_name}{cache.DRAFT_INFO_FILE_SUFFIX}', {'cache_name': cache_name})
        cache.selected_template(template_path, cache_name)
        return application.make_ok_response()

    elif request.method == 'DELETE':
        template_path = request.json.get('template_path')
        if not template_path:
            return application.make_fail_response('Missing required argument: template_path')

        cache_name = request.json.get('cache_name')
        if not cache_name:
            return application.make_fail_response('Missing required argument: cache_name')

        draft_name = cache.get_filename(template_path, cache_name)
        cache.delete(draft_name)
        cache.delete(f'{draft_name}{cache.DRAFT_INFO_FILE_SUFFIX}')
        return application.make_ok_response()
