# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json

from igetui.igt_push import IGeTui
from igetui.template.igt_transmission_template import TransmissionTemplate
from igetui.template.igt_link_template import LinkTemplate
from igetui.template.igt_notification_template import NotificationTemplate
from igetui.template.igt_notypopload_template import NotyPopLoadTemplate
from igetui.template.igt_apn_template import APNTemplate
from igetui.RequestException import RequestException
from igetui.igt_message import IGtAppMessage, IGtListMessage, IGtSingleMessage
from igetui.igt_target import Target
from igetui.BatchImpl import BatchImpl
from igetui.payload.APNPayload import APNPayload, SimpleAlertMsg, DictionaryAlertMsg


# IOS
APPID = '7Puws0MSBf6LAJRmV3vnJ'
APPKEY = '7CdwSrUQVP87sEvVQIAvS1'
APPSECRET = 'IS9N7SLY0Y8pFTWYeQDJu9'
MASTERSECRET = 'Pzf9OE8fva6Hz3bETREgv7'
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

CID1 = '5e8efe8b2622c6d5ef46d9239d72e895'
DEVICETOKEN1 = 'b0f9100dea96078f1d9a3c96d65d37ae4018a820fc4cd6bca1d73df0c9b7c405'

CID2 = '8720104ba98536dd1f56ecbc5951afbf'
DEVICETOKEN2 = '9f8ef9a7dda661a80cc6f61287542a3447b72236f992bb2beb2b88a00a726a71'


def notificationTemplateDemo():
    """
    通知透传模板动作内容
    """
    template = NotificationTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1
    template.transmissionContent = "白雪推送"
    template.title = "白雪推送通知标题"
    template.text = "白雪推送通知内容"
    template.logo = "icon.png"
    template.logoURL = ""
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    # begin = "2015-03-04 17:40:22"
    # end = "2015-03-04 17:47:24"
    # template.setDuration(begin, end)
    return template


def linkTemplateDemo():
    """
    通知链接模板动作内容
    """
    template = LinkTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.title = "白雪推送通知标题"
    template.text = "白雪推送通知内容"
    template.logo = ""
    template.url = "http://www.baidu.com"
    template.transmissionType = 1
    template.transmissionContent = ''
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    return template


def transmissionTemplateDemo():
    """
    透传模板动作内容
    """
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '这是Content'

    # APN简单推送
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = "嘿嘿嘿"
    # apn = APNPayload()
    # apn.alertMsg = alertMsg
    # apn.badge = 2
    # apn.sound = "default"
    # apn.addCustomMsg("payload", "payload")
    # # apn.contentAvailable = 1
    # # apn.category = "ACTIONABLE"
    # template.setApnInfo(apn)

    # APN高级推送
    apnpayload = APNPayload()
    apnpayload.badge = 0
    apnpayload.sound = "com.gexin.ios.silence"
    # apnpayload.addCustomMsg("payload", "payload")
    # apnpayload.addCustomMsg("payloadData", "呵呵呵")
    apnpayload.contentAvailable = 1
    apnpayload.category = "ACTIONABLE"

    alertMsg = DictionaryAlertMsg()
    alertMsg.body = '这是body'
    alertMsg.actionLocKey = 'actionLockey'
    alertMsg.locKey = 'lockey'
    alertMsg.locArgs = ['locArgs']
    alertMsg.launchImage = 'launchImage'
    # IOS8.2以上版本支持
    alertMsg.title = '这是Title'
    # alertMsg.titleLocArgs = ['TitleLocArg']
    # alertMsg.titleLocKey = 'TitleLocKey'
    apnpayload.alertMsg = alertMsg
    template.setApnInfo(apnpayload)

    return template


def pushMessageToApp():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # 定义"AppMessage"类型消息对象, 设置消息内容模板, 发送的目标App列表,
    # 是否支持离线发送, 以及离线消息有效期(单位毫秒)
    message = IGtAppMessage()
    message.data = linkTemplateDemo()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 600
    message.appIdList.extend([APPID])

    ret = push.pushMessageToApp(message)
    print ret


def pushMessageToSingle():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    # template = notificationTemplateDemo()
    # template = linkTemplateDemo()
    template = transmissionTemplateDemo()
    # template = NotyPopLoadTemplateDemo()

    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    message.pushNetWorkType = 0  # 设置是否根据WIFI推送消息(2为4G/3G/2G; 1为wifi推送; 0为不限制推送)

    target = Target()
    target.appId = APPID
    target.clientId = CID1

    try:
        ret = push.pushMessageToSingle(message, target)
        print ret
    except RequestException as e:
        requstId = e.getRequestId()
        ret = push.pushMessageToSingle(message, target, requstId)
        print ret


def pushMessageToList():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    template = notificationTemplateDemo()
    # template = linkTemplateDemo()
    # template = transmissionTemplateDemo()
    # template = NotyPopLoadTemplateDemo()

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.pushNetWorkType = 0

    target1 = Target()
    target1.appId = APPID
    target1.clientId = CID1
    # target1.alias = Alias1

    target2 = Target()
    target2.appId = APPID
    target2.clientId = CID2
    # target2.alias = Alias2

    receivers = [target1, target2]

    contentId = push.getContentId(message, 'ToList_任务别名_可为空')

    ret = push.pushMessageToList(contentId, receivers)
    print ret


def pushAPN():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # message = IGtSingleMessage()

    # APN旧版推送Demo
    # template = APNTemplate()
    # template.setPushInfo("", -1, "", "", "", "", "", "")

    # APN简单推送
    # template = APNTemplate()
    # apn = APNPayload()
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = "嘿嘿嘿"
    # apn.alertMsg = alertMsg
    # apn.badge = 10
    # apn.sound = "default"
    # # apn.addCustomMsg("payload", "哈哈哈")
    # # apn.contentAvailable = 1
    # # apn.category = "ACTIONABLE"
    # template.setApnInfo(apn)

    # APN高级推送
    # template = APNTemplate()
    # apnpayload = APNPayload()
    # apnpayload.badge = 0
    # apnpayload.sound = "default"
    # # apnpayload.addCustomMsg("payload", "哈哈哈")
    # # apnpayload.contentAvailable = 1
    # # apnpayload.category = "ACTIONABLE"
    #
    # alertMsg = DictionaryAlertMsg()
    # alertMsg.body = '这是body'
    # alertMsg.actionLocKey = 'actionLockey'
    # alertMsg.locKey = ''
    # alertMsg.locArgs = ['locArgs']
    # alertMsg.launchImage = 'launchImage'
    # # IOS8.2以上版本支持
    # alertMsg.title = '这是title'
    # # alertMsg.titleLocArgs = ['TitleLocArg']
    # # alertMsg.titleLocKey = 'TitleLocKey'
    # apnpayload.alertMsg = alertMsg
    # template.setApnInfo(apnpayload)

    template = transmissionTemplateDemo()

    # 单个用户推送接口
    # message.data = template
    # ret = push.pushAPNMessageToSingle(APPID, DEVICETOKEN1, message)
    # print message
    # print ret

    # 多个用户推送接口
    message = IGtListMessage()
    message.data = template
    contentId = push.getAPNContentId(APPID, message)
    deviceTokenList = [DEVICETOKEN1, DEVICETOKEN2]
    ret = push.pushAPNMessageToList(APPID, contentId, deviceTokenList)
    print ret


if __name__ == '__main__':
    # pushAPN()
    # pushMessageToApp()
    pushMessageToSingle()
    # pushMessageToList()
