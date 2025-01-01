import time

import uiautomator2 as u2
from uiautomator2 import Direction
from utils import check_chars_exist, other_app

unclick_btn = []
have_clicked = []
is_end = False
error_count = 0
in_other_app = False
d = u2.connect()
d.shell("adb kill-server && adb start-server")
time.sleep(5)
d.app_stop("com.taobao.taobao")
# d.app_clear('com.taobao.taobao')
time.sleep(2)
d.app_start("com.taobao.taobao", stop=True)
ctx = d.watch_context()
ctx.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
ctx.when("O1CN01sORayC1hBVsDQRZoO_!!6000000004239-2-tps-426-128.png_").click()
ctx.when(xpath="//android.app.Dialog//android.widget.Button[contains(text(), '-tps-')]").click()
ctx.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
# ctx.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
ctx.start()
time.sleep(5)


def operate_task():
    start_time = time.time()
    while True:
        if time.time() - start_time > 16:
            break
        if not in_other_app:
            d.swipe_ext(Direction.FORWARD)
            time.sleep(3)
            d.swipe_ext(Direction.BACKWARD)
            time.sleep(3)
    while True:
        if d(className="android.widget.TextView", text="赚金币抵钱").exists or d(className="android.widget.TextView", text="今日累计奖励").exists:
            print("当前是任务列表画面，不能继续返回")
            # d.swipe_ext(Direction.FORWARD)
            break
        else:
            d.press("back")
            time.sleep(0.5)


ctx.wait_stable()
coin_btn = d(className="android.widget.FrameLayout", description="领淘金币", clickable=True)
if coin_btn.exists(timeout=10):
    coin_btn.click()
    time.sleep(5)
    # home_btn = d(className="android.widget.Button", textContains="首页来访")
    # if home_btn.exists(timeout=4):
    #     home_btn.click()
    #     print("点击首页来访")
    #     time.sleep(3)
else:
    d(className="android.view.View", description="搜索栏").click()
    d(resourceId="com.taobao.taobao:id/searchEdit").send_keys("淘金币")
    time.sleep(3)
    d(className="android.view.View", descriptionContains="淘金币").click()
    time.sleep(5)
earn_btn = d(className="android.widget.TextView", textContains="签到领金币")
if earn_btn.exists(timeout=4):
    earn_btn.click()
    time.sleep(5)
earn_btn = d(className="android.widget.TextView", textContains="赚更多金币")
if earn_btn.exists(timeout=4):
    earn_btn.click()
    time.sleep(3)
else:
    raise Exception("没有找到金币任务按钮")
print("点击开始做任务")
while True:
    in_other_app = False
    time.sleep(4)
    earn_btn = d(className="android.widget.TextView", text="赚更多金币")
    if earn_btn.exists and not d(className="android.widget.TextView", text="赚金币抵钱").exists:
        earn_btn.click()
        time.sleep(2)
        continue
    print("开始查找按钮。。。")
    get_btn = d(className="android.widget.Button", text="领取奖励")
    if get_btn.exists:
        get_btn.click()
        print("点击领取奖励")
        time.sleep(4)
        continue
    de_btn = d(className="android.widget.Button", text="点击得")
    if de_btn.exists:
        de_btn.click()
        print("点击点击得")
        time.sleep(4)
        continue
    to_btn = d(className="android.widget.Button", textMatches="去完成|去逛逛|去浏览|逛一逛")
    if to_btn.exists:
        need_click_view = None
        need_click_index = 0
        task_name = None
        for index, view in enumerate(to_btn):
            text_div = view.sibling(className="android.view.View", instance=0).child(className="android.widget.TextView", instance=0)
            if text_div.exists:
                task_name = text_div.get_text()
                if check_chars_exist(task_name):
                    if view not in unclick_btn:
                        unclick_btn.append(view)
                    continue
                # if task_name in have_clicked:
                #     print("已经点击过了。", task_name)
                #     continue
                need_click_index = index
                need_click_view = view
                break
        if need_click_view:
            print("点击按钮", task_name)
            if task_name not in have_clicked:
                have_clicked.append(task_name)
            if check_chars_exist(task_name, other_app):
                in_other_app = True
            need_click_view.click()
            time.sleep(2)
            search_view = d(className="android.view.View", text="搜索有福利")
            if search_view.exists:
                d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
                d(className="android.widget.Button", text="搜索").click()
                time.sleep(2)
            # web_view = d(className="android.webkit.WebView")
            # live_view = d(resourceId="com.taobao.taobao:id/layermanager_penetrate_webview_container_id")
            # if web_view.exists(timeout=5) or live_view.exists(timeout=5):
            operate_task()
        else:
            error_count += 1
            print("未找到可点击按钮", error_count)
            if error_count > 3:
                break
while True:
    draw_down_btn = d(className="android.widget.Button", text="立即领取")
    if draw_down_btn.exists:
        draw_down_btn.click()
        time.sleep(2)
    else:
        break
ctx.close()
