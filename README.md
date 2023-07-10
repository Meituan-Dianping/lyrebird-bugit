<h1 align="center">Lyrebird - BugIt plugin</h1>

[![Unit Test](https://github.com/Meituan-Dianping/lyrebird-bugit/actions/workflows/unittest.yml/badge.svg)](https://github.com/Meituan-Dianping/lyrebird-bugit/actions/workflows/unittest.yml)
[![Publish to pypi](https://github.com/Meituan-Dianping/lyrebird-bugit/actions/workflows/publish.yml/badge.svg)](https://github.com/Meituan-Dianping/lyrebird-bugit/actions/workflows/publish.yml)
[![CodeQL](https://github.com/Meituan-Dianping/lyrebird-bugit/actions/workflows/codeql.yml/badge.svg)](https://github.com/Meituan-Dianping/lyrebird-bugit/actions/workflows/codeql.yml)

[![PyPI](https://img.shields.io/pypi/v/lyrebird-bugit.svg)](https://pypi.python.org/pypi/lyrebird-bugit)
![PyPI](https://img.shields.io/pypi/pyversions/lyrebird-bugit.svg)
![GitHub](https://img.shields.io/github/license/meituan-dianping/lyrebird-bugit.svg)

**[Lyrebird](https://github.com/Meituan-Dianping/lyrebird)**
是一个基于拦截以及模拟HTTP/HTTPS网络请求的面向移动应用的插件化测试平台。

**BugIt plugin是一个Lyrebird的插件，用于汇总Lyrebird各插件信息，提交Bug。**

----

# 简介
BugIt是一个[Lyrebird](https://github.com/Meituan-Dianping/lyrebird)插件。

通过BugIt可以轻松的将Lyrebird中收集的人机交互数据作为描述或者附件提交到Bug管理系统中(如JIRA)。

与[检查器](https://meituan-dianping.github.io/lyrebird/guide/checker.html#%E8%BD%BD%E5%85%A5%E6%A3%80%E6%9F%A5%E5%99%A8)(Checker)结合，即可实现一键提交bug的功能。

# 快速开始
## 环境要求

- macOS OR Linux

- Python3.7及以上

- Lyrebird 1.6及以上
## 安装

```bash
pip3 install lyrebird-bugit
```

## 启动

```bash
lyrebird
```

# 功能介绍

## Bug提交
读取脚本文件后，BugIt会得到一个Bug信息填充的界面，称之为Bug表单。

用户可以自定义Bug字段的 名称、先后顺序、填写样式、默认值。

![Bug表单](./image/bugit_bug.png)

BugIt可以通过配置服务向任意Bug管理系统提交Issue

## API数据获取
BugIt支持自动填充Lyrebird运行过程中抓取到的数据信息。

![BugIt 获取API信息](./image/bugit_api.gif)

## 报警获取

在[检查器](https://meituan-dianping.github.io/lyrebird/guide/checker.html#载入检查器)([Checker](https://meituan-dianping.github.io/lyrebird/guide/checker.html#载入检查器))捕获报警后，可以通过通知中心随时跳转至BugIt。

在右侧数据面板中，可以对历史[消息总线](/advance/eventbus.md)中的信息进行回溯，补充至Bug中。

![BugIt获取报警信息](./image/bugit_alert.gif)

## 缓存功能

按下[Commond]+[s]键，会将Bug相关字段信息进行存储。

缓存信息不受Lyrebird服务开关、浏览器缓存、脚本/界面切换的影响。

![BugIt缓存功能](./image/bugit_cache.gif)

有效的利用缓存功能，是提高Bug上报效率的关键。

## 插件在Bugit中的应用


### Android iOS插件

安装[Android插件](https://meituan-dianping.github.io/lyrebird/guide/plugin.html#android插件)、[iOS插件](https://meituan-dianping.github.io/lyrebird/guide/plugin.html#ios插件)后，BugIt支持设备信息扩展服务。

- 设备信息获取
   - BugIt 支持将设备名称、设备系统版本、被测 App 信息（Bundle ID(iOS)/PackageName(Android)）填充到Issue内容中。
- 实时设备截图
   - BugIt 可以实时获取设备截图，并支持在截图上进行涂鸦、文本标记。
   - 提交 Bug 时，截图将作为附件一并提交给脚本配置服务。
- Crash Log 获取
   - 在Lyrebird运行过程中，如发生 被测 App 发生 Crash，BugIt 会捕获到 Crash Log。
   - 提交 Bug 时，Crash Log 将作为附件一并提交给脚本配置服务。
   - Crash 获取 暂不支持 iOS 设备

![其他插件在BugIt中的应用](./image/bugit_devices.gif)

## BugIt脚本

在 ~/.lyrebird/conf.json 中，BugIt会读取 “bugit.workspace”字段。并将此字段值作为读取模板的根目录。

该目录下所有模板都会加载到BugIt中，并在UI中可选。

刷新BugIt界面即可重新加载所有模板。

### 模板使用说明

BugIt通过模板定义UI以及提交的行为。通过不同的模板支持JIRA以及其他的Bug管理系统。

BugIt模板是一个Python文件，要求使用Python3.7及以上的版本编写。
![BugIt 脚本工作原理示意图](./image/bugit_callback.png)
配置脚本需包含以下三部分
- init配置文件
- form()
- submit()

### init配置文件

BugIt 通过 name 来标识配置文件。

>注意：BugIt 脚本必须含有 'name' 属性


```python
"""
Template name
"""        
name = 'TEST-JIRA'
```
name 用于在 BugIt 前端页面上展示脚本名称。

![name](./image/bugit_name.png)

选中配置文件后，BugIt init 脚本文件，获取脚本文件中回调方法form()、submit()。

### form()

form() 方法用于自定义Bug表单的字段与填写样式。

Bug 中的每一字段由一dict定义（通常称之为FormItem），表单配置时，通过dict的以下关键字去控制字段的名称、默认值、样式等内容。

>form()方法应返回一由FormItem组成的list。

#### FormItem dict说明
key|说明|枚举值|是否必填
:--:|:--|:--:|:--:
name|展示在页面上的字段名称|--|Y
value|对应字段填充的值|--|N
component|字段展示的组件形式|'input'、'select'、'compoundTextarea'|Y
options|配合 select component使用，用于存放select component的选项内容|--|N
custom keys|自定义属性，不影响UI组件展示，可以帮住更好地处理数据，详细用法请参考[脚本高级](https://meituan-dianping.github.io/lyrebird/plugins/bugit.html)|--|N

#### BugIt 支持的 component
- input

```python
form_item_input = {
    'name': '主题',
    'component': 'input',
    'value': 'defalut value'
}
```

![input组件](./image/bugit_input.png)

input 组件会生成一个文本输入框，在声明时如果 value 不为空，则会作为默认值填充在输入框中

- select

```python
form_item_select = {
    'name': '版本',
    'component': 'select',
    'options':[
        {'id':'001','name':'option_1'},
        {'id':'002','name':'option_2'}
    ],
    'value': '001'
}
```

![select组件](./image/bugit_select.png)

select组件会生成一个筛选框，筛选项由 options 定义，options 为一个 list，其中每一元素为 dict 类型。

option dict说明
key|说明|是否必填
:--:|:--|:--:
id|筛选项唯一标识|Y
name|筛选项在前端展示文本内容|Y

select 组件中，value应为option dict中对应 id 的值

- compoundTextarea

compoundTextarea组件会生成一个文本框，在声明时如果 value 不为空，则会作为默认值填充在文本框中

```python
form_item_text = {
    'name': '描述',
    'component': 'compoundTextarea',
    'value': 'defalut value'
}
```
![compoundTextarea组件](./image/bugit_text.png)

compoundTextarea组件在 BugIt 中还用于支持 Lyrebird 其他信息的扩展。

选择[消息总线](https://meituan-dianping.github.io/lyrebird/advance/eventbus.html)或其他[插件](https://meituan-dianping.github.io/lyrebird/plugins/)的数据时，该数据将作为附加信息展示在 compoundTextarea 中。

![附加信息](./image/bugit_text_extra.gif)

对应的数据信息将作为 'extraMsg' 存放在 FormItem中。
此时From Item变成

```python
form_item_text = {
    'name': '描述',
    'component': 'compoundTextarea',
    'value': 'defalut value',
    'extraMsg':[
        {'message':'Flow Info'},
        {'message':'Notice Info'},
        {'message':'Devices Info'}
    ]
}
```

#### form()方法示例代码

```python
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
    return form
```
示例代码生成的 Bug 表单如下图所示
![测试脚本表单生成](./image/bugit_form.png)

>form()方法入参 context ，可用于传递缓存数据，相关用法详见[脚本高级](https://meituan-dianping.github.io/lyrebird/plugins/bugit.html)


### submit()

提交函数返回一个数组，数组中包含若干提交步骤需要回调的函数。

>submit()方法返回一组用于处理 submit 行为的方法。

方法说明
方法名|入参|说明
:--:|:--:|:--
issue|context|处理 Bug表单中的信息，通过 API 向 Bug 管理系统提交 Issue
attachments|context|处理附件信息（如 [Android插件](https://meituan-dianping.github.io/lyrebird/guide/plugin.html#android插件)、[iOS插件](https://meituan-dianping.github.io/lyrebird/guide/plugin.html#ios插件)提供的截图或 Log），通过 API 向 创建的 Issue 中添加附件

#### submit()方法示例代码（以JIRA服务为例）
```python
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
            # add extraMsg to description 
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
```

完整脚本请参考: [示例脚本](example/TEST.py)

脚本高级功能请参考:[脚本高级](https://meituan-dianping.github.io/lyrebird/plugins/bugit.html)

----
# 开发者指南

## 开发环境
- macOS OR Linux
- Python3
- NodeJS
- vscode(推荐)
- Chrome(推荐)

## 调试代码

### Vscode debug配置
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Terminal (integrated)",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Server",
            "type": "python",
            "request": "launch",
            "module": "lyrebird",
            "args": [
                "-b",
                "-vvv",
                "--plugin",
                "${workspaceFolder}"
            ],
            "console": "integratedTerminal"
        },
        {
            "name": "Client",
            "type": "chrome",
            "request": "launch",
            "url": "http://localhost:8080/",
            "webRoot": "${workspaceFolder}/frontend/src/",
            "sourceMapPathOverrides": {
                "webpack:///src/*": "${webRoot}/*"
            },
            "timeout": 30000
        }
    ]
}
```
### 后端代码
1. 激活python虚拟环境

    通过 source venv/bin/activate 来激活该环境
2.  通过Debug功能启动
    
    按照上面 debug配置中 python:Lyrebrid配置启动即可
### 前端代码
1. 启动node server

```
# 进入前端目录
cd frontend

# 启动前端node serve
npm run serve
```

2. 通过Debug功能启动浏览器

    按照上面 debug配置中 vuejs: chrome 配置启动即可
    >注意: vscode 需要安装chrome debug插件
