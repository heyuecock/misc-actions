import sys
import os
import queue
import logging
import threading
from imap_tools import MailBox, A
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright, expect

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    GLADOS_EMAIL = os.getenv('GLADOS_EMAIL')
    GLADOS_PASSWORD = os.getenv('GLADOS_PASSWORD')
except KeyError:
    logging.error("请设置环境变量 GLADOS_EMAIL 和 GLADOS_PASSWORD")
    sys.exit(1)


q = queue.Queue()
playwright = sync_playwright().start()

def get_code(msg):
    html_content = msg.html
    soup = bs(html_content, "lxml")
    code = soup.find_all("b")[-1].get_text()
    q.put(code)

def on_new_mail():
    with MailBox('imap.gmail.com').login(GLADOS_EMAIL, GLADOS_PASSWORD, 'INBOX') as mailbox:
        logging.info('等待邮件到来')
        responses = mailbox.idle.wait(timeout=120)
        if responses:
            last_msg = None
            for msg in mailbox.fetch(A(seen=False, subject='GLaDOS Authentication')):
                logging.info(f'收到邮件: {msg.date_str}')
                last_msg = msg
            get_code(last_msg)
        else:
            logging.error('2分钟内没有收到邮件 退出')
            sys.exit(1)

def request_send_mail():
    browser = playwright.firefox.launch()
    page = browser.new_page()
    page.set_default_timeout(60*1000)
    page.goto("https://glados.network/login")
    page.locator("#email").fill(GLADOS_EMAIL)
    page.get_by_text("send access code to email",exact=True).click()
    try:
        expect(page.get_by_text("access code sent. please check mailbox",exact=True)).to_be_visible()
        logging.info("发送验证码成功")
    except Exception:
        logging.warning("发送验证码可能失败")
    browser.close()

def login(code):
    browser = playwright.firefox.launch()
    page = browser.new_page()
    page.set_default_timeout(60*1000)
    logging.info('正在尝试登录页面')
    page.goto("https://glados.network/login")
    page.locator("#email").fill(GLADOS_EMAIL)
    page.locator("#mailcode").fill(code)
    page.get_by_text("Login", exact=True).click()
    logging.info('登录成功')
    return browser, page

def checkin(page):
    logging.info('正在尝试切换英文页面')
    page.get_by_text('Switch language', exact=True).click()
    page.get_by_text('English', exact=True).click()
    logging.info('正在尝试签到')
    page.get_by_text("Checkin", exact=True).click()
    page.get_by_role("button", name="Checkin").click()

    try:
        expect(page.get_by_text(
            "Check in success Checkin Repeats! Please Try Tomorrow",
            exact=True)).to_be_visible()
        logging.warning("签到重复")
    except Exception:
        try:
            expect(page.get_by_text("Check in success Checkin! Got")).to_be_visible()
            logging.info("签到成功")
        except Exception:
            logging.error("签到失败")
    finally:
        page.screenshot(path="glados/checkin.png", full_page=True)

def main():
    mail_thread = threading.Thread(target=on_new_mail, daemon=True)
    mail_thread.start()

    request_send_mail()
    request_send_mail()
    try:
        code = q.get(timeout=120)
        logging.info(f'获取到验证码: {code}')
    except queue.Empty:
        logging.error('2分钟内没有收到验证码 退出')
        sys.exit(1)

    browser, page = login(code)
    checkin(page)

    browser.close()
    playwright.stop()

if __name__ == '__main__':
    main()
