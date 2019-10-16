import json

"""
Template name
"""
name = 'TEST-JIRA'

def form(context):
    """
    BugIt callback function

    BugIt will call this function when user select this template from UI.
    This function should return a array, list all FormItem dict.

    """
    form_item_input = {
        'name': '主题',
        'component': 'input',
        'value': 'defalut value'
    }
    form_item_select = {
        'name': '版本',
        'component': 'select',
        'options':[
            {'id':'001','name':'option_1'},
            {'id':'002','name':'option_2'}
        ],
        'value': '001'
    }
    form_item_text = {
        'name': '描述',
        'component': 'compoundTextarea',
        'value': 'defalut value'
    }
    form = [form_item_input,form_item_select,form_item_text]

    """
    get cache if it exsit
    field value will be filled with cache value
    """
    if context.get('cache'):
        for field in form:
            for cache_field in context.get('cache'):
                if cache_field['key'] == field['key']:
                    field['value'] = cache_field.get('value','')

    return form


def submit():
    """
    BugIt callback function

    BugIt will call this function when user tap submit button.
    This function should return a array, contains all submit actions.

    Each submit-action function have a argument. It contains form data and attachments info.
    """
    return [issue, attachments]


def issue(context):
    """
    This function is used to submit Issue 
    """
    form_data = context['issue']
    jira_fields = {}

    # transform from_data to payload submited to API of JIRA
    for form_item in form_data:
        if form_item['name'] == '主题' :
            jira_fields['summary'] = form_item['value']
        elif form_item['name'] == '版本':
            jira_fields['version'] = {
                id:form_item['value']
                }
        elif form_item['name'] == '描述':
            jira_fields['description'] = form_item['value']
            if form_item['extraMsg']:
                for add_des in form_item['extraMsg']:
                    jira_fields['description'] +='\n'
                    jira_fields['description'] +='------------------------------\n'
                    jira_fields['description'] +=add_des['message']

    url = 'http://www.example.com/jira/rest/api/2/issue'
    header = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    resp = requests.post(url, auth=('YOUR JIRA_USER_NAME', 'YOUR_JIRA_PASSWD'),json={"fields": jira_fields},headers=header)
    
    if resp.status_code >= 200 and resp.status_code < 300:
        body = json.loads(response.text)
        if body.get('key') :
            context['key'] = body['key']
        else:
            raise Exception(f'Submit failed {response.text}')
    else:
        raise Exception(f'Create issue failed with code {response.status_code}\n{response.text}')


def attachments(context):
    """
    This function is used to upload attachments to the Issue which has been created
    """
    key = context['key']
    attachments = context['attachments']

    if len(attachments) == 0:
        # No attachments
        return

    url = f'http://www.example.com/jira/rest/api/2/issue/{key}/attachments'
    headers = {
        'X-Atlassian-Token': 'nocheck'
    }
    multiple_files = []

    # transform attachment data to payload submited to API of JIRA
    for attachment in attachments:
        attachment_path = Path(attachment['path'])
        multiple_files.append(
            ('file', (attachment_path.name, open(str(attachment_path), 'rb')))
        )
    response = requests.post(url, files=multiple_files, headers=headers)

    if response.status_code == 200 and response.json()['code'] == 0:
        print('Submit attachments success')
    else:
        raise Exception(f'Submit failed {response.text}')