from lyrebird.plugins import manifest
from . import apis
from . import event_handler


manifest(
    id='bugit',
    name='BugIt',
    icon='mdi-bug-outline',
    api=[
        ('/api/template', apis.template, ['GET', 'POST']),
        ('/api/device', apis.device, ['GET']),
        ('/api/issue', apis.issue, ['GET', 'POST']),
        ('/api/take_screenshot/<string:platform>/<string:device_id>', apis.take_screenshot, ['GET']),
        ('/api/attachments', apis.attachments, ['GET', 'POST']),
        ('/api/attachments/<string:attachment_id>', apis.attachments, ['GET', 'PUT', 'DELETE']),
        ('/api/cache/<string:template_key>', apis.ui_cache, ['GET', 'POST', 'DELETE'])
    ],
    event=[
        ('android.device', event_handler.on_android_device),
        ('ios.device', event_handler.on_ios_device),
        ('android.screenshot', event_handler.on_android_screenshot),
        ('ios.screenshot', event_handler.on_ios_screenshot),
        ('upload_files', event_handler.on_upload_files)
    ]
)
