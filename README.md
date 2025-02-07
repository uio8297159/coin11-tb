# coin11-tb
使用uiautomator2自动化完成2024年淘宝双11的金币任务，淘金币任务，芭芭农场任务，闲鱼任务。

需要安装adb，自行百度教程。

* 使用uiauto.dev查看ui组件
```
pip3 install uiautodev
# 启动
uiauto.dev
```

adb命令，获取当前打开的app包名和类名
```shell
adb shell dumpsys window | grep mCurrentFocus
```

目前淘宝芭芭农场和淘金币任务相对完善，其他的还有问题。
$\color{red}{目前的问题是，uiautomator2将列表上滑一页后，获取的数据还是上一页的，这个问题已反馈作者但未解决。}$

```shell
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .
adb shell rm /sdcard/screenshot.png
```