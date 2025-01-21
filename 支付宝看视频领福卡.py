import time
import uiautomator2 as u2

d = u2.connect()
d.app_start("com.eg.android.AlipayGphone", stop=True, use_monkey=True)
time.sleep(5)
