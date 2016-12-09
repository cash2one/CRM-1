# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from igetui.igt_push import IGeTui
from igetui.igt_target import Target
from igetui.igt_message import IGtAppMessage, IGtSingleMessage, IGtListMessage
from igetui.template.igt_link_template import LinkTemplate
from igetui.template.igt_notification_template import NotificationTemplate
from igetui.template.igt_transmission_template import TransmissionTemplate
from igetui.RequestException import RequestException


APPID = 'TCWyAtl8Ep7ScHAh0eLJ8'
APPKEY = 'iZhaS0hq997FQsA73WZSv'
MASTERSECRET = '5vBNsd33HY64dDknYyJUI3'
CID = '101e1aa3044d72b1bd57e87310557d67'
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'


def notificationTemplateDemo():
    """
    点击通知打开App
    """
    template = NotificationTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1
    template.transmissionContent = '透传消息!!!!!'
    template.title = '欢迎使用个推'
    template.text = '这是一条推送消息'
    template.logo = ''
    template.logoURL = ''
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    # begin = "2015-03-04 17:40:22";
    # end = "2015-03-04 17:47:24";
    # template.setDuration(begin, end)
    return template


def linkTemplateDemo():
    """
    点击通知打开url
    """
    template = LinkTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1
    template.transmissionContent = ''
    template.title = '欢迎使用个推'
    template.text = '这是一条推送消息'
    template.logo = ''
    template.url = "http://www.baidu.com"
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    # begin = "2015-03-04 17:40:22";
    # end = "2015-03-04 17:47:24";
    # template.setDuration(begin, end)
    return template


def transmissionTemplateDemo():
    """
    透传, 直接将消息发送到App内部
    """
    template = TransmissionTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1
    template.transmissionContent = '这是一条透传消息'
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
    template = notificationTemplateDemo()
    # template = linkTemplateDemo()
    # template = transmissionTemplateDemo()
    # template = NotyPopLoadTemplateDemo()

    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    message.pushNetWorkType = 0  # 设置是否根据WIFI推送消息(2为4G/3G/2G; 1为wifi推送; 0为不限制推送)

    target = Target()
    target.appId = APPID
    target.clientId = CID

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
    target1.clientId = '101e1aa3044d72b1bd57e87310557d67'  # cid
    # target1.alias = Alias1
    target2 = Target()
    target2.appId = APPID
    target2.clientId = '101e1aa3044d72b1bd57e87310557d60'
    # target2.alias = Alias2

    receivers = [target1, target2]

    contentId = push.getContentId(message, 'ToList_任务别名_可为空')

    ret = push.pushMessageToList(contentId, receivers)
    print ret


if __name__ == '__main__':
    # pushMessageToApp()
    # pushMessageToSingle()
    pushMessageToList()
