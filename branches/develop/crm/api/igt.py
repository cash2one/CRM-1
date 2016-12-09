# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from igetui.igt_push import IGeTui
from igetui.template.igt_transmission_template import TransmissionTemplate
from igetui.template.igt_link_template import LinkTemplate
from igetui.template.igt_notification_template import NotificationTemplate
from igetui.template.igt_apn_template import APNTemplate
from igetui.RequestException import RequestException
from igetui.igt_target import Target
from igetui.igt_message import IGtAppMessage, IGtListMessage, IGtSingleMessage
from igetui.payload.APNPayload import APNPayload, SimpleAlertMsg, DictionaryAlertMsg


APPID = 'TCWyAtl8Ep7ScHAh0eLJ8'
APPKEY = 'iZhaS0hq997FQsA73WZSv'
MASTERSECRET = '5vBNsd33HY64dDknYyJUI3'
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

APPID = "7Puws0MSBf6LAJRmV3vnJ"
APPKEY = "7CdwSrUQVP87sEvVQIAvS1"
MASTERSECRET = "Pzf9OE8fva6Hz3bETREgv7"
DeviceToken = "1faebd51773972945564b92e3a62564d440877586b6a4fba899ac742f66eac91"
CID = "6a16bde046ad620096f5c986b44e0b82"

#define kGtAppId        @"i2eZJaPg4H85chDFI28Hv3"
#define kGtAppKey       @"urswM0mugA7Rnf7fCKxlP"
#define kGtAppSecret    @"uVwH0ky9No6OopgT1A78T1"
APPID = "i2eZJaPg4H85chDFI28Hv3"
APPKEY = "urswM0mugA7Rnf7fCKxlP"
MASTERSECRET = "PwOzuBgN6Y7jJKuLeTeDv5"
#DeviceToken = "1faebd51773972945564b92e3a62564d440877586b6a4fba899ac742f66eac91"
#测试的demo cid
#CID = "6a16bde046ad620096f5c986b44e0b82"
#正式的guoyucid
CID = "a8155e99d96bcb788efca37a3b5a6af5"
#正式的刘迎新cid
CID = 'f7849e7947206e4898f121c5b6772376'
class IGT(object):

    def __init__(self):
        self.push = IGeTui(HOST, APPKEY, MASTERSECRET)
    @staticmethod
    def make_transmission_template(content):
        """
        透传 -- 直接将消息发送到App内部
        """
        template = TransmissionTemplate()
        template.appId = APPID
        template.appKey = APPKEY
        template.transmissionType = 1
        template.transmissionContent = content  # 透传消息
        return template

    @staticmethod
    def make_notification_template(title='', text='', content=''):
        """
        点击通知打开App
        """
        template = NotificationTemplate()
        template.appId = APPID
        template.appKey = APPKEY
        template.transmissionType = 1
        template.transmissionContent = content
        template.title = title
        template.text = text
        template.isRing = True
        template.isVibrate = True
        template.isClearable = True
        # begin = "2015-03-04 17:40:22"
        # end = "2015-03-04 17:47:24"
        # template.setDuration(begin, end)
        return template

    @staticmethod
    def make_link_template(title='', text='', url=''):
        """
        点击通知打开url
        """
        template = LinkTemplate()
        template.appId = APPID
        template.appKey = APPKEY
        template.transmissionType = 1
        template.transmissionContent = ''
        template.title = title
        template.text = text
        template.url = url
        template.isRing = True
        template.isVibrate = True
        template.isClearable = True
        return template

    @staticmethod
    def make_target(cid, alias=''):
        target = Target()
        target.appId = APPID
        target.clientId = cid
        target.alias = alias
        return target

    def push_message_to_app(self, template):
        message = IGtAppMessage()
        message.isOffline = True  # 是否支持离线发送
        message.offlineExpireTime = 1000 * 3600 * 12  # 12小时 - 离线消息有效期(单位毫秒)
        message.appIdList.extend([APPID])  # 目标App列表
        message.data = template  # 设置消息内容模板
        return self.push.pushMessageToApp(message)

    def push_message_to_single(self, template, cid):
        message = IGtSingleMessage()
        message.isOffline = True
        message.offlineExpireTime = 1000 * 3600 * 12
        message.pushNetWorkType = 0  # 2: 4G/3G/2G; 1: wifi推送; 0: 不限制推送
        message.data = template

        target = self.make_target(cid)

        try:
            return self.push.pushMessageToSingle(message, target)
        except RequestException as e:
            request_id = e.getRequestId()
            return self.push.pushMessageToSingle(message, target, request_id)

    def push_message_to_list(self, template, targets):
        message = IGtListMessage()
        message.isOffline = True
        message.offlineExpireTime = 1000 * 3600 * 12
        message.pushNetWorkType = 0
        message.data = template
        targets = map(self.make_target, targets)
        content_id = self.push.getContentId(message, 'ToList_任务别名_可为空')
        return self.push.pushMessageToList(content_id, targets)

    def get_cid_status(self, cid):
        return self.push.getClientIdStatus(APPID, cid)

    def close(self):
        return self.push.close()


class IGTApn(IGT):

    def __init__(self):
        super(IGTApn, self).__init__()

    @staticmethod
    def make_apn_template_simple(msg, content='', **custom_msg):
        template = IGT.make_transmission_template(content)
        alert_msg = SimpleAlertMsg()
        alert_msg.alertMsg = msg
        apn_payload = APNPayload()
        apn_payload.alertMsg = alert_msg
        apn_payload.contentAvailable = 1
        apn_payload.category = "ACTIONABLE"
        for k, v in custom_msg.items():
            apn_payload.addCustomMsg(k, v)
        template.setApnInfo(apn_payload)
        return template

    @staticmethod
    def make_apn_template(title, body='', content='', **custom_msg):
        template = IGT.make_transmission_template(content)
        alert_msg = DictionaryAlertMsg()
        alert_msg.title = title
        alert_msg.body = body
        alert_msg.actionLocKey = 'actionLockey'
        alert_msg.locKey = ''
        alert_msg.locArgs = ['locArgs']
        alert_msg.launchImage = 'launchImage'
        # IOS8.2以上版本支持
        # alertMsg.titleLocArgs = ['TitleLocArg']
        # alertMsg.titleLocKey = 'TitleLocKey'

        apn_payload = APNPayload()
        apn_payload.alertMsg = alert_msg
        apn_payload.contentAvailable = 1
        apn_payload.category = "ACTIONABLE"
        for k, v in custom_msg.items():
            apn_payload.addCustomMsg(k, v)
        template.setApnInfo(apn_payload)
        return template

    def push_apn_message_to_single(self, template, device_token):
        message = IGtSingleMessage()
        message.data = template
        return self.push.pushAPNMessageToSingle(APPID, device_token, message)

    def push_apn_message_to_list(self, template, device_token_list):
        message = IGtListMessage()
        message.data = template
        content_id = self.push.getAPNContentId(APPID, message)
        return self.push.pushAPNMessageToList(APPID, content_id, device_token_list)


class BaseMessage(object):
    def __init__(self):
        self.igt = IGT()
        self.template = None

    def push_to_app(self):
        return self.igt.push_message_to_app(self.template)

    def push_to_single(self, cid):
        return self.igt.push_message_to_single(self.template, cid)

    def push_to_list(self, cid_list):
        return self.igt.push_message_to_list(self.template, cid_list)


class TransmissionMessage(BaseMessage):

    def __init__(self, content):
        super(TransmissionMessage, self).__init__()
        self.template = self.igt.make_transmission_template(content)


class NotificationMessage(BaseMessage):

    def __init__(self, title='', body='', content=''):
        super(NotificationMessage, self).__init__()
        self.template = self.igt.make_notification_template(title, body, content=content)


class LinkMessage(BaseMessage):

    def __init__(self, title='', body='', url=''):
        super(LinkMessage, self).__init__()
        self.template = self.igt.make_link_template(title, body, url=url)


class BaseApnMessage(BaseMessage):

    def __init__(self):
        self.igt = IGTApn()
        self.template = None

    def push_to_single_apn(self, device_token):
        return self.igt.push_apn_message_to_single(self.template, device_token)

    def push_to_list_apn(self, device_token_list):
        return self.igt.push_apn_message_to_list(self.template, device_token_list)


class SimpleApnMessage(BaseApnMessage):

    def __init__(self, msg, content='', **custom_msg):
        super(SimpleApnMessage, self).__init__()
        self.template = self.igt.make_apn_template_simple(msg, content, **custom_msg)


class ApnMessage(BaseApnMessage):

    def __init__(self, title, body='', content='', **custom_msg):
        super(ApnMessage, self).__init__()
        self.template = self.igt.make_apn_template(title, body, content, **custom_msg)


if __name__ == '__main__':
    # 常规测试
    CID = '101e1aa3044d72b1bd57e87310557d67'
    # msg = LinkMessage(
    #         title='这是推送title',
    #         body='这是推送body',
    #         url='http://www.baidu.com'
    #     )
    # msg = NotificationMessage(
    #         title='这是推送title',
    #         body='这是推送body',
    #         content='这是透传消息'
    #     )
    # msg = TransmissionMessage('这是透传消息嘿嘿嘿')
    # print msg.push_to_single(CID)
    # print msg.push_to_app()
    # print msg.push_to_list([CID])

    # Apn推送测试
    APPID = '7Puws0MSBf6LAJRmV3vnJ'
    APPKEY = '7CdwSrUQVP87sEvVQIAvS1'
    APPSECRET = 'IS9N7SLY0Y8pFTWYeQDJu9'
    MASTERSECRET = 'Pzf9OE8fva6Hz3bETREgv7'
    HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

    CID1 = '5e8efe8b2622c6d5ef46d9239d72e895'
    DEVICETOKEN1 = 'b0f9100dea96078f1d9a3c96d65d37ae4018a820fc4cd6bca1d73df0c9b7c405'

    CID2 = '8720104ba98536dd1f56ecbc5951afbf'
    DEVICETOKEN2 = '9f8ef9a7dda661a80cc6f61287542a3447b72236f992bb2beb2b88a00a726a71'
    CID = "6a16bde046ad620096f5c986b44e0b82"
    # apn_msg = SimpleApnMessage('这是推送title', '这是推送body')
    apn_msg = ApnMessage(
            title='这是推送title',
            body='这是推送body',
            content='这是推送content'
        )

    # print apn_msg.push_to_single_apn(DEVICETOKEN1)
    # print apn_msg.push_to_list_apn([DEVICETOKEN1, DEVICETOKEN2])

    # print apn_msg.push_to_app()
    print apn_msg.push_to_single(CID)
    #print apn_msg.push_to_list([CID1, CID2])
