import time
from asyncio import timeout

import uiautomator2 as u2
from uiautomator2 import Direction

d = u2.connect()
d.app_start("com.taobao.taobao", stop=True)
screen_width = d.info['displayWidth']
screen_height = d.info['displayHeight']
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
    taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
    if taolive_btn.exists:
        time.sleep(20)
        taolive_btn.click()
    else:
        while True:
            if time.time() - start_time > 20:
                break
            time.sleep(1)
            d.swipe_ext(Direction.FORWARD)
            time.sleep(3)
            d.swipe_ext(Direction.BACKWARD)
            time.sleep(3)
        while True:
            d.press("back")
            time.sleep(5)
            find_text = d(text="做任务向前冲")
            print(find_text.info)
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
# task_btn = d.xpath('//android.widget.TextView[@text="做任务攒钱"]')
task_btn = d(resourceId="eva-canvas")
if task_btn.exists(timeout=10):
    left, bottom, right = task_btn.info['bounds']['left'], task_btn.info['bounds']['bottom'], task_btn.info['bounds']['right']
    d.click((right - left) // 2, bottom - 10)
    time.sleep(2)

    sign_btn = d(text="签到")
    if sign_btn.exists:
        sign_btn.click()
        time.sleep(2)
    list_view = d(className="android.widget.ListView", instance=0)
    if list_view.exists:
        unclick_btn = []
        is_end = False
        while True:
            to_btn = d(className="android.widget.Button", text="去完成")
            if to_btn.exists:
                if is_end:
                    if len(unclick_btn) > 0 and to_btn.count <= len(unclick_btn):
                        break
                else:
                    if len(unclick_btn) > 0 and to_btn.count <= len(unclick_btn):
                        d.long_click(200, screen_height-30)
                        time.sleep(2)
                        d(scrollable=True).fling.toEnd()
                        is_end = True
                        continue
                for view in to_btn:
                    text_div = view.sibling(className="android.view.View", instance=0).child(className="android.widget.TextView", instance=0)
                    if text_div.exists:
                        if check_chars_exist(["拉好友", "点淘", "支付宝", "抢红包"], text_div.get_text()):
                            if view not in unclick_btn:
                                unclick_btn.append(view)
                            continue
                    view.click()
                    search_view = d(className="android.view.View", text="搜索有福利")
                    if search_view.exists:
                        d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
                        d(className="android.widget.Button", text="搜索").click()
                        time.sleep(2)
                    web_view = d(className="android.webkit.WebView")
                    if web_view.exists(timeout=5):
                        operate_task()
            else:
                break
            time.sleep(2)
d.watcher.remove()
