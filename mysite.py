# encoding=utf8  
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import os
import string
import time
import hashlib
import json
import requests

from tornado.options import define, options
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

define("port", default=8009, help="run on the given port", type=int)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class WroughtHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("wrought.html")

class RoofHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("roof.html")

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("contact.html")

class SendEmailHandler(tornado.web.RequestHandler):
    def send_cust_message(self,email="",name="",html=""):
	resp = requests.post(
		"https://api.mailgun.net/v2/sandboxec8349fac8bf404cb27e4faba876dec5.mailgun.org/messages",
		auth=("api", "key-efbc07e796db14dc6671eda883a36d48"),
		files=[("attachment", open("files/signstep_product.pdf"))],
		data={"from": "signstep.th@gmail.com",
		      "to": [email],
		      "subject": "สวัสดีครับคุณ " + name,
		      "html": html})

    def send_sign_message(self,name="",html=""):
	resp = requests.post(
		"https://api.mailgun.net/v2/sandboxec8349fac8bf404cb27e4faba876dec5.mailgun.org/messages",
		auth=("api", "key-efbc07e796db14dc6671eda883a36d48"),
		data={"from": "signstep.th@gmail.com",
		      "to": "signstep.th@gmail.com",
		      "subject": "คุณ " + name + "ได้ทำการขอข้อมูล",
		      "html": html})

    def post(self):
        email_address = self.get_argument('email')
	name = self.get_argument('name')
	phone = self.get_argument('phone')
	message = self.get_argument('message')
	if name and email_address and phone:
		f = open('email_log.txt','a')
		s = "####################################################\n"
		s+= "Date" + time.strftime("%Y-%m-%d %H:%M:%S")+"\n"
		s+= "Email: " + email_address +"\n"
		s+= "Name: " + name +"\n"
		s+= "Phone: " + phone +"\n"
		s+= "####################################################\n"
		f.write(s)
		f.close()

		html = "<p>สวัสดีครับคุณ  " + name + "</p>"
		html+= "<p>ทาง Signstep ยินดีเป็นอย่างมากที่คุณให้ความสนใจ</p>"
		html+= "<p>เราได้แนบข้อมูลสเปคและราคาสินค้ามาใน email นี้แล้ว (signstep_product.pdf) รวม2หน้า</p>"
		html+= "<p>กรุณาดาวน์โหลดได้ที่ด้านล่างครับ</p>"
		html+= "<p>หากท่านมีข้อสงสัยอื่นๆนอกจากราคาทางเราจะรีบตอบกลับทันทีที่ได้อ่านอีเมล์ของท่านครับ</p>"
		html+= "<p>หรือต้องการติดต่อด่วน กรุณาโทร 081 840 0258 / 083 293 7391</p><br>"
		html+= "<p>ขอแสดงความนับถือ</p>"
		html+= "<p>สุทธิกิตติ์ โกมลวิภาต</p>"
		self.send_cust_message(email_address,name,html)

		html = "<p>คุณ  " + name + "</p>"
		html+= "<p>เบอร์โทร: " + phone + "</p>"
		html+= "<p>Email: " + email_address + "</p>"
		html+= "<p>ข้อความ: "+message+"</p>"
		self.send_sign_message(name,html)
		self.redirect("/")


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/home", HomeHandler),
        (r"/wrought", WroughtHandler),
        (r"/roof", RoofHandler),
        (r"/contact", ContactHandler),
	(r'/(.*)', tornado.web.StaticFileHandler, {'path': "."}),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
