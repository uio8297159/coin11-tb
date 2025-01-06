import time

import uiautomator2 as u2

d = u2.connect()
d.app_stop("com.taobao.idlefish")
time.sleep(3)
d.app_start("com.taobao.idlefish", stop=True)
ctx = d.watch_context()
ctx.start()
in_browse = False


def operate_task():
    global in_browse
    start_time = time.time()
    while True:
        if time.time() - start_time > 16:
            break
        d.swipe_ext("up")
        time.sleep(1)
        d.swipe_ext("down")
        time.sleep(1)
    while True:
        if in_browse:
            d(scrollable=True).scroll.toBeginning()
            in_browse = False
            break
        if d(className="android.webkit.WebView", text="闲鱼币首页").exists:
            print("当前是闲鱼币首页，不能继续返回")
            break
        else:
            d.press("back")
            time.sleep(0.5)


time.sleep(5)
ctx.wait_stable()
sign_btn = d(resourceId="com.taobao.idlefish:id/icon_entry_lottie", className="android.widget.ImageView", clickable=True)
if not sign_btn.exists(timeout=5):
    raise Exception("找不到签到按钮")
sign_btn.click()
time.sleep(5)
sign_btn = d(className="android.widget.TextView", text="签到", clickable=True)
if sign_btn.exists:
    sign_btn.click()
    time.sleep(2)
while True:
    try:
        time.sleep(4)
        to_btn = d(className="android.widget.TextView", text="去完成", clickable=True)
        if to_btn.exists:
            to_btn.click()
            time.sleep(2)
            operate_task()
    except Exception as e:
        print(e)
        continue

ctx.stop()
