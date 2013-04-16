#-*-coding:utf-8-*-
#!/usr/bin/env python
#
# 文 件 名：setup.py
# 功能描述：cx_freeze封装Python脚本的配置文件
#
# 作者：Xiongyan    日期：2013/04/15
# 版权：可以使用、传播，但请保留出处；如需修改，请告知作者。
#
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "sms_tx",
        version = "1.0",
        description = u"天波短信实时监控发声提醒程序v1.0",
        author = "XiongYan",
        author_email = "xiongyan@goopins.com",
        executables = [Executable("main.py",base = base,icon = "simple.ico")]
    )

# 这里可以编写客户化的封装后处理代码。例如：临时数据的清除，数据包的发布等
# 到此，整个setup脚本已经完成。
