import time

import uiautomator2 as u2
from uiautomator2 import Direction

d = u2.connect()
d.app_start("com.taobao.taobao", stop=True)
screen_width = d.info['displayWidth']
screen_height = d.info['displayHeight']
time.sleep(2)
in_search = False


def check_close():
    d(className="android.widget.Button", text="关闭")


def check_chars_exist(arr, text):
    for char in arr:
        if char in text:
            return True
    return False


def operate_task():
    global in_search
    start_time = time.time()
    taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
    if taolive_btn.exists:
        time.sleep(20)
        while True:
            taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
            if not taolive_btn.exists:
                break
            d.press("back")
            time.sleep(5)
    else:
        while True:
            if time.time() - start_time > 20:
                break
            d.swipe_ext(Direction.FORWARD)
            time.sleep(3)
            d.swipe_ext(Direction.BACKWARD)
            time.sleep(3)
        d.press("back")
        if in_search:
            time.sleep(2)
            in_search = False
            d.press("back")


d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
# d.watcher.when(xpath="//android.widget.Button[@text='关闭']").click()
# d.watcher.when("关闭").click()
d.watcher.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
d.watcher.start()
close_btn = d(className="android.widget.ImageView", description="关闭按钮")
if close_btn.exists:
    close_btn.click()
coin_btn = d(className="android.widget.FrameLayout", description="金币双11", instance=0)
if coin_btn.exists(timeout=3):
    coin_btn.click()
    time.sleep(2)
d.watch_context().wait_stable()
# task_btn = d.xpath('//android.widget.TextView[@text="做任务攒钱"]')
while True:
    time.sleep(2)
    underway_btn = d(text="进行中")
    if underway_btn.exists:
        continue
    task_btn = d(text="做任务攒钱")
    if task_btn.exists:
        break
# task_btn = d(resourceId="eva-canvas")
error_count = 0
if task_btn.click_exists(timeout=10):
    # left, bottom, right = task_btn.info['bounds']['left'], task_btn.info['bounds']['bottom'], task_btn.info['bounds']['right']
    # d.click((right - left) // 2, bottom - 10)
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
                need_click_view = None
                need_click_index = 0
                task_name = None
                for index, view in enumerate(to_btn):
                    text_div = view.sibling(className="android.view.View", instance=0).child(className="android.widget.TextView", instance=0)
                    if text_div.exists:
                        if check_chars_exist(["拉好友", "农场", "快手", "点淘", "支付宝", "抢红包", "闲鱼", "蚂蚁"], text_div.get_text()):
                            if view not in unclick_btn:
                                unclick_btn.append(view)
                            continue
                        task_name = text_div.get_text()
                        need_click_index = index
                        need_click_view = view
                        break
                if need_click_view:
                    print("点击按钮", task_name)
                    need_click_view.click()
                    time.sleep(2)
                    search_view = d(className="android.view.View", text="搜索有福利")
                    if search_view.exists:
                        d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
                        d(className="android.widget.Button", text="搜索").click()
                        in_search = True
                        time.sleep(2)
                    web_view = d(className="android.webkit.WebView")
                    if web_view.exists(timeout=5):
                        operate_task()
                else:
                    if not is_end:
                        d.swipe_ext(Direction.FORWARD)
                        d(scrollable=True).scroll.toEnd()
                        is_end = True
                    else:
                        error_count += 1
                        print("未找到可点击按钮", error_count)
                        if error_count > 6:
                            break
            else:
                break
            time.sleep(6)
else:
    print("未找到做任务按钮")
d.watcher.stop()
d.watcher.remove()
