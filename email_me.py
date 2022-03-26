# 이메일 발송 클래스

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from json_parser import JsonParser

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SendMail(metaclass=MetaSingleton):

    def __init__(self) -> None:

        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.starttls()

        self.gmail_id = JsonParser("gmail_id")
        gmail_pw = JsonParser("gmail_app_pw")

        self.mail_content: MIMEMultipart = MIMEMultipart('alternative')

        try:
            self.session.login(self.gmail_id.value, gmail_pw.value)
        except smtplib.SMTPAuthenticationError as se:
            print(se, "/ login failure, init fail")

    def __del__(self) -> None:
        try:
            if self.session:
                self.session.close()
        except AttributeError as e:
            print(f'{e} while deleting NewMailService Object')

    def create_mail(self, *, title: str = None, plain_text: str = None, html_contents: str = None) -> MIMEMultipart:
        if not title:
            title = "제목 없는 메일"
        if not plain_text:
            plain_text = "이 메일은 본문이 없습니다."
        if not html_contents:
            html_contents = plain_text

        html_contents = f"""
        <!DOCTYPE html>
        <html lang="kor">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            </head>
            <body>
                {html_contents}
            </body>
        </html>"""

        mail_content: MIMEMultipart = MIMEMultipart('alternative')
        mail_content["Subject"] = f'[RpiTemp] {title}'
        mail_content.attach(MIMEText(html_contents, "html"))

        return mail_content

    def send_mail(self, content: MIMEMultipart, receivers: str, bcc: list=None) -> bool:
        if not self.session:
            print("cannot send email - session lost")
            self.__init__()
        if not bcc:
            bcc = []

        content["To"] = receivers
        allocatee = [receivers] + bcc if receivers else bcc

        try:
            self.session.sendmail(self.gmail_id.value, allocatee, content.as_string())
            print(f"email sent to {allocatee}, title: {content.get('Subject', 'Error-title not found')}")
            return True
        except Exception as e:
            print(f"Cannot Send Email / {e}")
            return False

if __name__ == '__main__':

    a= SendMail()
    b= SendMail()
    c= SendMail()
    d= SendMail()

    content = a.create_mail(
        title='알림',
        plain_text='테스트용 메일입니다'
    )
    b.send_mail(content, '', [JsonParser('mail_to').value])
    c.send_mail(c.create_mail(
        title='일반',
        plain_text='테스트입니다'
    ))