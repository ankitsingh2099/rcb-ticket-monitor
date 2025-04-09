from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import smtplib
import time
import os

# Configs
URL = "https://shop.royalchallengers.com/ticket"
TARGET_CLASS = "css-q38j1a"
CHECK_INTERVAL = 300  # 5 minutes
LAST_COUNT = None

# Email config
EMAIL_SENDER = "ankit.singh2099@gmail.com"
EMAIL_RECEIVER = "ankit.singh2099@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def get_class_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find_all(class_=TARGET_CLASS)
    all_classes = set()
    for tag in soup.find_all(True):  # Find all tags
        if tag.has_attr('class'):
            all_classes.update(tag['class'])  # Add all classes from the tag to the set
    
    print("All unique class names found on the page:")
    print(all_classes)
    return len(elements)

def send_email_notification(new_count):
    subject = "RCB Ticket Page Changed!"
    body = f"The number of elements with class '{TARGET_CLASS}' changed. New count: {new_count}"
    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
    server.quit()
    print(f"[INFO] Notification sent for count change to {new_count}")

def monitor():
    global LAST_COUNT
    while True:
        try:
            current_count = get_class_count()
            print(f"[INFO] Checked count: {current_count}")
            if LAST_COUNT is None:
                LAST_COUNT = current_count
                send_email_notification(current_count)
            elif current_count != LAST_COUNT:
                print(f"[CHANGE DETECTED] Old: {LAST_COUNT}, New: {current_count}")
                send_email_notification(current_count)
                LAST_COUNT = current_count
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()

# pip install playwright
# playwright install