import time

import uiautomator2 as u2
from uiautomator2 import Direction
from utils import check_chars_exist, other_app, get_current_app

unclick_btn = []
have_clicked = dict()
is_end = False
error_count = 0
in_other_app = False

d = u2.connect()
d.shell("adb kill-server && adb start-server")
time.sleep(5)
# d.app_stop("com.taobao.taobao")
# d.app_clear('com.taobao.taobao')
# time.sleep(2)
d.app_start("com.taobao.taobao", stop=True, use_monkey=True)
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
        if d(text="肥料明细").exists:
            print("当前是任务列表画面，不能继续返回")
            break
        else:
            package_name, activity_name = get_current_app(d)
            # if package_name == "com.miui.home":
            #     d.app_start("com.taobao.taobao")
            #     break
            if package_name == "com.taobao.taobao":
                if activity_name == "com.taobao.tao.welcome.Welcome":
                    find_farm_btn()
                    find_fertilizer_btn()
                    break
            d.press("back")
            time.sleep(0.2)


def find_farm_btn():
    while True:
        farm_btn = d(className="android.widget.FrameLayout", description="芭芭农场")
        if farm_btn.exists(timeout=5):
            farm_btn.click()
            time.sleep(3)
            temp_btn = d(className="android.widget.Button", textContains="每次施肥5次")
            if temp_btn.exists:
                break


def find_fertilizer_btn():
    while True:
        fertilize_btn = d(className="android.widget.Button", textContains="集肥料")
        if fertilize_btn.click_exists(timeout=2):
            print("点击集肥料按钮")
            time.sleep(5)
            if d(text="肥料明细").exists:
                print("进入任务页面")
                break


d.watcher.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[contains(text(), '-tps-')]").click()
d.watcher.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
# d.watcher.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
d.watcher.when("O1CN01sORayC1hBVsDQRZoO_!!6000000004239-2-tps-426-128.png_").click()
d.watcher.when("点击刷新").click()
d.watcher.start()
print("开始查找芭芭农场按钮")
find_farm_btn()
find_fertilizer_btn()
finish_count = 0
while True:
    try:
        print("开始查找按钮")
        time.sleep(4)
        in_other_app = False
        sign_btn = d(className="android.widget.Button", text="去签到")
        if sign_btn.exists:
            sign_btn.click()
            time.sleep(2)
        to_btn = d(className="android.widget.Button", textMatches="去完成|去浏览|去领取")
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
                        if have_clicked[task_name] > 2:
                            continue
                    need_click_index = index
                    need_click_view = view
                    break
            if need_click_view:
                print("点击按钮", task_name)
                if have_clicked.get(task_name) is None:
                    have_clicked[task_name] = 1
                else:
                    have_clicked[task_name] += 1
                if check_chars_exist(task_name, other_app):
                    in_other_app = True
                need_click_view.click()
                time.sleep(2)
                search_view = d(className="android.view.View", text="搜索有福利")
                if search_view.exists:
                    d(className="android.widget.EditText", instance=0).send_keys("笔记本电脑")
                    d(className="android.widget.Button", text="搜索").click()
                    time.sleep(2)
                operate_task()
                finish_count = finish_count + 1
                if finish_count % 3 == 0:
                    d.swipe_ext("up", scale=0.2)
                    time.sleep(4)
            else:
                error_count += 1
                print("未找到可点击按钮", error_count)
                if error_count > 4:
                    break
    except Exception as e:
        print(e)
        continue
d.watcher.remove()
print(f"共自动化完成{finish_count}个任务")
d.shell("settings put system accelerometer_rotation 0")
print("关闭手机自动旋转")
