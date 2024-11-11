import time
from pydoc import classname

import uiautomator2 as u2
from dulwich.porcelain import describe
from uiautomator2 import Direction
from utils import check_chars_exist

in_search = False
unclick_btn = []
is_end = False
error_count = 0
in_other_app = False
d = u2.connect()
d.app_start("com.taobao.taobao", stop=True)
time.sleep(5)


def operate_task():
    global in_search
    start_time = time.time()
    taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
    close_btn = d(resourceId="com.taobao.taobao.liveroom_android_plugin_AType:id/taolive_room_top_close_btn")
    if taolive_btn.exists:
        time.sleep(20)
        while True:
            taolive_btn = d(resourceId="com.taobao.taobao:id/taolive_close_btn")
            if not taolive_btn.exists:
                break
            d.press("back")
            time.sleep(5)
    elif close_btn.exists:
        time.sleep(20)
        while True:
            close_btn = d(resourceId="com.taobao.taobao.liveroom_android_plugin_AType:id/taolive_room_top_close_btn")
            if not close_btn.exists:
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
        if in_other_app:
            # while True:
            time.sleep(0.5)
            d.press("back")


d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
d.watcher.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
d.watcher.start()
d(className="android.view.View", description="搜索栏").click()
d(resourceId="com.taobao.taobao:id/searchEdit").send_keys("淘金币")
time.sleep(3)
d(className="android.view.View", descriptionContains="淘金币").click()
time.sleep(5)
# home_btn = d(className="android.widget.Button", textContains="首页来访")
# if home_btn.exists(timeout=4):
#     home_btn.click()
#     print("点击首页来访")
#     time.sleep(3)
receive_btn = d(className="android.widget.Button", textContains="收货奖励")
if receive_btn.exists(timeout=4):
    receive_btn.click()
    print("点击收货奖励")
    time.sleep(3)
earn_btn = d(className="android.widget.TextView", textContains="赚更多金币")
if earn_btn.exists(timeout=4):
    earn_btn.click()
    time.sleep(3)
else:
    earn_btn = d(className="android.widget.TextView", textContains="签到领金币")
    if earn_btn.exists(timeout=4):
        earn_btn.click()
        time.sleep(3)
    else:
        raise Exception("没有找到金币任务按钮")
print("点击开始做任务")
while True:
    time.sleep(4)
    get_btn = d(className="android.widget.Button", text="领取奖励")
    if get_btn.exists:
        get_btn.click()
        print("点击领取奖励")
        time.sleep(4)
    to_btn = d(className="android.widget.Button", text="去完成")
    print("查找去完成按钮")
    if not to_btn.exists(timeout=5):
        to_btn = d(className="android.widget.Button", text="去逛逛")
    if to_btn.exists:
        need_click_view = None
        need_click_index = 0
        task_name = None
        for index, view in enumerate(to_btn):
            text_div = view.sibling(className="android.view.View", instance=0).child(className="android.widget.TextView", instance=0)
            if text_div.exists:
                if check_chars_exist(text_div.get_text()):
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
d.watcher.remove()

