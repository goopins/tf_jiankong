#!/usr/bin/env python
#coding=utf-8
#@author: xiongyan

import wx
from wx import xrc
import sys, os, time
import threading
#import timeit #计时
import urllib
import codecs  #解决读取中文配置的问题
import ConfigParser  #分析配置文件模块

#全局配置-----start
config_file="config.ini"
config = ConfigParser.ConfigParser()
config.readfp(codecs.open(config_file, "r", "utf-8-sig"))
#config.readfp(open(config_file,'r','utf-8'))
#--公共配置
CHECK_URL = config.get("public", "check_url")
SLEEP_TIM = config.get("public", "sleep_time")
CHECK_URL = CHECK_URL or "http://sms.yebanwan.com/index.php/Public/checkMsgAdd"
SLEEP_TIM = int(SLEEP_TIM) or 60
#全局配置-----end

soundFile = 'Sound/msg.wav'
#发声方法
def soundStart():
    if sys.platform[:5] == 'linux':
        import os
        os.popen2('aplay -q' + soundFile)
    else:
        import winsound
        winsound.PlaySound(soundFile, winsound.SND_FILENAME)

class MyApp(wx.App):
    
    def OnInit(self):
        self.res = xrc.XmlResource('main.xrc')
        self.init_frame()
        return True

    #自定义初始界面 
    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'MainFrame')
        self.send_num = xrc.XRCCTRL(self.frame, 'm_staticText_num')
        self.log_text = xrc.XRCCTRL(self.frame, 'log_text') #日志
        self.log_text.SetValue(u"系统正常，每%s秒自动刷新1次" %SLEEP_TIM)

        threading.Thread(target=self.OnCheckAdd, args=()).start() #多线程调用
        #事件绑定
        #self.frame.Bind(wx.EVT_CLOSE, self.OnCloseWin, id=xrc.XRCID('m_button1'))
        self.SetTopWindow(self.frame) #总是靠前
        self.frame.Show()

    #是否有更新
    def OnCheckAdd(self):
        not_executed = 1
        while(not_executed):
        #10s后响
            A = urllib.urlopen(CHECK_URL)#"http://sms.yebanwan.com/index.php/Public/checkMsgAdd"
            curr_num_str = A.read()
            A.close()
            if len(curr_num_str) >= 100:
                self.log_text.SetValue("%s" %curr_num_str)
                curr_num_str = '0'
            else:
                curr_num_str = curr_num_str or '0'
            curr_num = int(curr_num_str)
            self.send_num.SetLabel("%s" %curr_num)
            if curr_num > 0:
                soundStart() #发声
            time.sleep(SLEEP_TIM) #配置sleep时间
        
    
    def OnCloseWin(self, event):
        self.Destroy()

        #析构方法
    def __del__( self ):
        self.Destroy()


if __name__ == '__main__':
    app = MyApp(False)
    #soundStart()
    app.MainLoop()

