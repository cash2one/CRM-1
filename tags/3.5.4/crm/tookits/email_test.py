# -*- coding: utf-8 -*-

'''发送邮件测试'''

import smtplib
from email.mime.text import MIMEText


mailto_list = ["xue.bai@100credit.com"]
mail_host = "smtp.100credit.com"
mail_user = "crmtest@100credit.com"
mail_pass = "OGUlHhKjMW"
mail_postfix = "credit.com"

content = "python email test!"
msg = MIMEText(content, _charset='gbk')
msg['Subject'] = "python email test!"
msg['From'] = "crmtest@100credit.com"
msg['To'] = ";".join(mailto_list)

server = smtplib.SMTP()
server.connect(mail_host)
server.login(mail_user, mail_pass)
server.sendmail(mail_user, mailto_list, msg.as_string())
server.close()

