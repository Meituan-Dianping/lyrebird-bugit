import lyrebird
from . import template_loader
from uuid import uuid4
from collections import OrderedDict
from lyrebird import get_logger
from lyrebird import application


logger = get_logger()


android_devices = []
ios_devices = []
attachments = OrderedDict()


def on_android_device(msg):
    logger.debug(f'PluginHandler: [Android.device] {msg}')
    global android_devices
    android_devices = msg
    lyrebird.emit('devices')


def on_ios_device(msg):
    logger.debug(f'PluginHandler: [iOS.device] {msg}')
    global ios_devices
    ios_devices = msg
    lyrebird.emit('devices')


def on_android_screenshot(msg):
    if len(msg) == 0:
        return
    for item in msg:
        attachment_id = str(uuid4())
        attachments[attachment_id] = {'id': attachment_id,
                                      'name': item['screenshot']['name'],
                                      'path': item['screenshot']['path']}
    lyrebird.emit('attachments')


def on_ios_screenshot(msg):
    if len(msg) == 0:
        return
    for item in msg:
        attachment_id = str(uuid4())
        attachments[attachment_id] = {'id': attachment_id,
                                      'name': item['screenshot']['name'],
                                      'path': item['screenshot']['path']}
    lyrebird.emit('attachments')


def on_upload_files(msg):
    if len(msg) == 0:
        return
    for item in msg:
        attachment_id = str(uuid4())
        attachments[attachment_id] = {'id': attachment_id,
                                      'name': item['upload_file']['name'],
                                      'path': item['upload_file']['path']}
    lyrebird.emit('attachments')


def on_notice(msg):
    sender_file = msg.get('sender', {}).get('file', '')
    autoissue_checker = application.config.get('event.notice.autoissue.checker', [])
    if sender_file in autoissue_checker:
        template_loader.notice_handler(msg)
