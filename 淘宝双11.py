import time

import uiautomator2 as u2
from uiautomator2 import Direction
from websockets.asyncio.async_timeout import timeout

d = u2.connect()
d.app_start("com.taobao.taobao", stop=True)
time.sleep(2)


def check_close():
    d(className="android.widget.Button", text="关闭")


def check_chars_exist(arr, text):
    for char in arr:
        if char in text:
            return True
    return False


def operate_task():
    start_time = time.time()
    while True:
        if time.time() - start_time > 20:
            break
        time.sleep(3)
        d.swipe_ext(Direction.FORWARD)
        time.sleep(3)
        d.swipe_ext(Direction.BACKWARD)
        time.sleep(3)
    while True:
        d.press("back")
        time.sleep(5)
        find_text = d(text="做任务向前冲")
        if not find_text.exists(timeout=5):
            d.press("back")
            time.sleep(5)
        else:
            break


d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
d.watcher.when("//android.app.Dialog//android.widget.Button[@text='关闭']").click()
close_btn = d(className="android.widget.ImageView", description="关闭按钮")
if close_btn.exists:
    close_btn.click()
coin_btn = d(className="android.widget.FrameLayout", description="金币双11", instance=0)
if coin_btn.exists(timeout=3):
    coin_btn.click()
    time.sleep(2)
task_btn = d(className="android.widget.TextView", textContains="做任务")
if task_btn.exists:
    x, y = task_btn.info['bounds']['left'], task_btn.info['bounds']['top']
    d.click(x + 10, y + 10)
    time.sleep(2)
else:
    raise Exception("未找到任务按钮")
sign_btn = d(text="签到")
if sign_btn.exists:
    sign_btn.click()
    time.sleep(2)
while True:
    to_btn = d(text="去完成")
    if to_btn.exists:
        for view in to_btn:
            text_div = view.sibling(className="android.view.View", instance=0).child(className="android.widget.TextView", instance=0)
            if text_div.exists:
                if check_chars_exist(["拉好友", "点淘", "支付宝"], text_div.get_text()):
                    continue
            view.click()
            web_view = d(className="android.webkit.WebView")
            if web_view.exists(timeout=5):
                operate_task()
    else:
        break
    time.sleep(2)
d.watcher.remove()
