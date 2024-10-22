import time

import uiautomator2 as u2
from uiautomator2 import Direction

d = u2.connect()
d.app_start("com.taobao.taobao", stop=True)


def check_close():
    d(className="android.widget.Button", text="关闭")


def operate_task():
    start_time = time.time()
    while True:
        if time.time() - start_time > 20:
            break
        d.swipe_ext(Direction.FORWARD)
        time.sleep(3)
        d.swipe_ext(Direction.BACKWARD)
        time.sleep(3)
    d.press("back")


d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
close_btn = d(className="android.widget.ImageView", description="关闭按钮")
if close_btn.exists:
    close_btn.click()
coin_btn = d(className="android.widget.FrameLayout", description="金币双11", instance=0)
if coin_btn.exists(timeout=3):
    print("存在coin_btn")
    coin_btn.click()
    time.sleep(2)
task_btn = d(text="做任务攒钱")
if task_btn.exists:
    task_btn.click()
    time.sleep(2)
sign_btn = d(text="签到")
if sign_btn.exists:
    sign_btn.click()
    time.sleep(2)
while True:
    to_btn = d(text="去完成")
    if to_btn.exists:
        to_btn.click()
        web_view = d(className="android.webkit.WebView")
        if web_view.exists(timeout=5):
            operate_task()
    else:
        break
    time.sleep(2)
d.watcher.remove()
