import lyrebird
from uuid import uuid4
from collections import OrderedDict
from lyrebird import get_logger


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
