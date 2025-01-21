import time
import uiautomator2 as u2

d = u2.connect()
d.app_start("com.eg.android.AlipayGphone", stop=True, use_monkey=True)
ctx = d.watch_context()
ctx.when(xpath="//*[@content-desc='关闭']").click()
ctx.start()
time.sleep(5)
video_btn = d(className="android.widget.TextView", resourceId="com.alipay.android.tablauncher:id/tab_description", text="视频")
if video_btn.exists:
    video_btn.click()
    time.sleep(3)
while True:
    time.sleep(15)
    d.swipe_ext("up")
ctx.stop()
