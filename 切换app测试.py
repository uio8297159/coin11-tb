import uiautomator2 as u2

d = u2.connect()
info = d.shell("dumpsys window | grep mCurrentFocus").output
print(info)
