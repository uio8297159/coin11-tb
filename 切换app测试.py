import uiautomator2 as u2
import re

d = u2.connect()
info = d.shell("dumpsys window | grep mCurrentFocus").output
match = re.search(r'mCurrentFocus=Window\{.*? u0 (.*?)/(.*?)\}', info)
if match:
    package_name = match.group(1)
    activity_name = match.group(2)
    print(package_name, activity_name)
d.shell("am start -n com.taobao.taobao/com.taobao.themis.container.app.TMSActivity")
