import time

import uiautomator2 as u2
from uiautomator2 import Direction
from utils import check_chars_exist

unclick_btn = []
have_clicked = []
is_end = False
error_count = 0
in_other_app = False


def operate_task():
    start_time = time.time()
    while True:
        if time.time() - start_time > 16:
            break
        d.swipe_ext(Direction.FORWARD)
        time.sleep(3)
        d.swipe_ext(Direction.BACKWARD)
        time.sleep(3)
    while True:
        if d(text="肥料明细").exists:
            print("当前是任务列表画面，不能继续返回")
            # d.swipe_ext(Direction.FORWARD)
            break
        else:
            d.press("back")
            time.sleep(0.5)


d = u2.connect()
d.shell("adb kill-server && adb start-server")
time.sleep(5)
d.app_stop("com.taobao.taobao")
# d.app_clear('com.taobao.taobao')
time.sleep(2)
d.app_start("com.taobao.taobao", stop=True)
time.sleep(5)

d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[contains(text(), '-tps-')]").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
d.watcher.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
d.watcher.when("O1CN01sORayC1hBVsDQRZoO_!!6000000004239-2-tps-426-128.png_").click()
d.watcher.start()
farm_btn = d(className="android.widget.FrameLayout", description="芭芭农场", instance=0)
if not farm_btn.click_exists(timeout=10):
    raise Exception("没有找到芭芭农场按钮")
time.sleep(3)
while True:
    fertilize_btn = d(className="android.widget.Button", textContains="集肥料")
    if fertilize_btn.click_exists(timeout=2):
        break
time.sleep(5)
sign_btn = d(className="android.widget.Button", text="去签到")
if sign_btn.exists:
    sign_btn.click()
    time.sleep(2)
while True:
    to_btn = d(className="android.widget.Button", textMatches="去完成|去浏览")
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
                if task_name in have_clicked:
                    continue
                need_click_index = index
                need_click_view = view
                break
        if need_click_view:
            print("点击按钮", task_name)
            if task_name not in have_clicked:
                have_clicked.append(task_name)
            need_click_view.click()
            time.sleep(2)
            search_view = d(className="android.view.View", text="搜索有福利")
            if search_view.exists:
                d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
                d(className="android.widget.Button", text="搜索").click()
                time.sleep(2)
            web_view = d(className="android.webkit.WebView")
            if web_view.exists(timeout=5):
                operate_task()
        else:
            if not is_end:
                d.swipe_ext(Direction.FORWARD)
                d(scrollable=True).scroll.toEnd()
                fertilizer_detail = d(resourceId="fissionOverlayPortal", className="android.view.View")
                if fertilizer_detail.exists:
                    fertilizer_detail.click()
                    time.sleep(2)
                    d.press("back")
                is_end = True
            else:
                error_count += 1
                print("未找到可点击按钮", error_count)
                if error_count > 6:
                    break
d.watcher.remove()


