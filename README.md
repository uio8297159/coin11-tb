# coin11-tb
使用uiautomator2自动化完成2024年淘宝双11的金币任务，淘金币任务，芭芭农场任务。

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

$\color{red}{目前需要完成跳转其他app再返回的操作。}$