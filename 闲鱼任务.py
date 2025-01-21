import time

import uiautomator2 as u2
from utils import get_current_app, fish_not_click
import ddddocr

d = u2.connect()
d.app_start("com.taobao.idlefish", stop=True)
screen_width, screen_height = d.window_size()
ctx = d.watch_context()
ctx.when("暂不升级").click()
ctx.start()
have_clicked = dict()
error_count = 0
ocr = ddddocr.DdddOcr(show_ad=False)


def click_earn():
    while True:
        throw_btn = d(className="android.view.View", resourceId="mapDiceBtn")
        if throw_btn.exists:
            d.click(throw_btn[0].bounds()[2] + 50, throw_btn[0].center()[1] + 30)
            time.sleep(5)
            if d(className="android.view.View", resourceId="taskWrap").exists:
                break


def operate_task():
    if d(className="android.view.View", resourceId="mapDiceBtn").exists and not d(className="android.view.View", resourceId="taskWrap").exists:
        print("首页滑动，开始模拟滑动")
        d.touch.down(screen_width * 0.5, screen_height * 0.8)
        time.sleep(0.5)
        d.touch.move(screen_width * 0.5, screen_height * 0.2)
        d.touch.up(screen_width * 0.5, screen_height * 0.1)
        start_time = time.time()
        while True:
            if time.time() - start_time > 20:
                break
            d.swipe_ext("up", scale=0.5)
            time.sleep(1)
        d(scrollable=True).fling.vert.toBeginning(max_swipes=1000)
        time.sleep(2)
        click_earn()
    else:
        search_view = d(className="android.view.View", text="搜索有福利")
        search_edit = d(resourceId="com.taobao.taobao:id/searchEdit")
        search_btn = d(resourceId="com.taobao.taobao:id/searchbtn")
        if search_view.exists:
            d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
            d(className="android.widget.Button", text="搜索").click()
            time.sleep(2)
        elif search_edit.exists and search_btn.exists:
            search_edit.send_keys("笔记本电脑")
            search_btn.click()
            time.sleep(2)
        start_time = time.time()
        while True:
            if time.time() - start_time > 16:
                break
            d.swipe_ext("up")
            time.sleep(1)
            d.swipe_ext("down")
            time.sleep(1)
        while True:
            if d(className="android.webkit.WebView", text="闲鱼币首页").exists:
                print("当前是闲鱼币首页，不能继续返回")
                break
            else:
                d.press("back")
                time.sleep(0.5)


time.sleep(5)
ctx.wait_stable()
while True:
    _, activity_name = get_current_app(d)
    if activity_name == "com.taobao.idlefish.maincontainer.activity.MainActivity":
        sign_btn = d(resourceId="com.taobao.idlefish:id/icon_entry_lottie", className="android.widget.ImageView", clickable=True)
        if sign_btn.exists:
            sign_btn.click()
            time.sleep(4)
    elif activity_name == "com.taobao.idlefish.webview.WebHybridActivity":
        if d(className="android.view.View", resourceId="mapDiceBtn").exists:
            break
    else:
        d.app_start("com.taobao.idlefish", stop=True)
    time.sleep(4)
time.sleep(3)
receive_btn = d(className="android.widget.TextView", textContains="领取酬金", clickable=True)
if receive_btn.exists:
    receive_btn.click()
    time.sleep(5)
click_earn()
while True:
    try:
        print("正在查找按钮...")
        time.sleep(4)
        sign_btn = d(className="android.widget.TextView", text="签到", clickable=True)
        if sign_btn.exists:
            sign_btn.click()
            time.sleep(4)
        receive_btn = d(className="android.widget.TextView", text="领取奖励", clickable=True)
        if receive_btn.exists:
            receive_btn.click()
            print("点击领取奖励")
            time.sleep(3)
            continue
        to_btn = d(className="android.widget.TextView", text="去完成", clickable=True)
        if to_btn.exists:
            need_click_view = None
            task_name = None
            for btn in to_btn:
                screen_shot = d.screenshot()
                cropped_rect = (200, btn.bounds()[1] - 50, btn.bounds()[0] - 50, btn.bounds()[1] + 30)
                cropped_image = screen_shot.crop(cropped_rect)
                task_name = ocr.classification(cropped_image)
                if fish_not_click(task_name):
                    continue
                if task_name in have_clicked:
                    if have_clicked[task_name] > 2:
                        continue
                need_click_view = btn
                break
            if need_click_view and task_name:
                need_click_view.click()
                print("点击按钮", task_name)
                if have_clicked.get(task_name) is None:
                    have_clicked[task_name] = 1
                else:
                    have_clicked[task_name] += 1
                time.sleep(3)
                operate_task()
            else:
                error_count += 1
                print("未找到可点击按钮", error_count)
                if error_count > 3:
                    break
    except Exception as e:
        print(e)
        continue

ctx.stop()
