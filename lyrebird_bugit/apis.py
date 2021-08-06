import imp
import json
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
from . import attachment
import traceback
from hashlib import md5


logger = log.get_logger()

def template():
    if request.method == 'GET':
        templates = template_loader.template_list()
        selected_index = None
        last_selected_template = cache.get_selected_template()
        for index, template in enumerate(templates):
            if template['path'] == last_selected_template:
                selected_index = index
        return application.make_ok_response(selected_index=selected_index, templates=templates)
    elif request.method == 'POST':
        '''
        Get template detail by path
        And save lastest_selected_template
        '''
        if request.json and 'path' in request.json:
            template_path = request.json['path']
            template = template_loader.get_template(template_path)
            # load from cache
            template_key = md5(template_path.encode()).hexdigest()
            template_detail = cache.get(template_key)
            # load from template
            if inspect.getargspec(template.form).args:
                template_detail = template.form({'cache': template_detail})
            else:
                template_detail = template.form()
            cache.selected_template(template_path)
            return jsonify(template_detail)
        else:
            return application.make_fail_response('Need path argument for getting template detail')


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

#get available device from iOS&Android plugin
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
            return jsonify(list(event_handler.attachments.values()))
        else:
            attachment = event_handler.attachments.get(attachment_id)
            if attachment:
                return send_file(attachment['path'])
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
        event_handler.attachments.pop(attachment_id)
        return make_ok_response()


def ui_cache(key):
    if request.method == 'GET':
        data = cache.get(key)
        if data:
            return application.make_ok_response(data=data)
        else:
            return application.make_fail_response(f'Not found cache by key {key}')
    elif request.method == 'POST':
        data = request.json
        for field in data:
            if 'extraMsg' in field:
                del field['extraMsg']
        cache.put(key, data)
        return application.make_ok_response()
