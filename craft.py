'''
 Copyright 2018 Logitech Inc.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files(the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions :

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
'''

import wx
import websocket
import threading

import os
import platform
import json
import uuid
import sys

import time
from googletrans import Translator
try:
    import thread
except ImportError:
    import _thread as thread
from copy import deepcopy
from time import sleep
from json import JSONEncoder
from uuid import UUID
#import pyttsx3
import win32com.client
import time

glist=[]
crownObjectList = []
toolObject = []
sessionId=""
uia = wx.UIActionSimulator()

JSONEncoder_olddefault = JSONEncoder.default

# special encoding for supporting UUID in json payload
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault


def report(event, value):
    toolId = event.get('task_options').get('current_tool')
    na = event.get('task_options').get('current_tool_option')

    response = {
        "message_type" : "tool_update",
        "session_id"   :  sessionId,
        "show_overlay" :  True,
        "tool_id"      :  toolId,
        "tool_options" :  [{
            "name"  : na,
            "value" : value
        }]
    };
    regMsg =  json.dumps(response)
    ws.send(regMsg.encode('utf8'))

def showText(tlist):
    translator = Translator()
    
    for i in tlist:
        str1 = ''.join(i)
        if str1 is not None:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            
            #engine = pyttsx3.init(sapi5)
            #engine.say(str1)
            #engine.runAndWait()
            #print("==========================\n")
            #print("\ntranslated\n")
            #print(str1)
            #print("==========================\n")
            translated = translator.translate(str1, src='la',dest='zh-tw')
            #print("===========================\n")
            #print(" Pronunciation:", translated.pronunciation)
            #print("===========================\n")

            dic_text = translated.text
            txt_left = wx.TextCtrl(panel, -1, dic_text, pos=(10,20), size=(380,180), style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)
            speaker.Speak(translated.text)
        else:
            #print("==========================\n")
            #print("\nNoneType\n")
            print(i)
            #print("==========================\n")
            

def wrapperUpdateUI(msg):
    global glist,sessionId
    totalDeltaValue=0
    totalRatchetDeltaValue=0
    count=0
    listCount=0
    global firstObject

    if(msg['message_type'] == "crown_turn_event"):
        glist.append(msg)
        listCount = len(glist)
        if listCount==0:
            return
        currentToolOption = glist[0]['task_options']['current_tool_option']
        print("+++currentToolOption = ",currentToolOption)
        print("listCount = ",listCount)
        firstObject = glist[0]
        for i in range(listCount):
            if currentToolOption == glist[i]['task_options']['current_tool_option']:
                totalDeltaValue = totalDeltaValue = glist[i]['delta']
                totalRatchetDeltaValue = totalRatchetDeltaValue + glist[i]['ratchet_delta']
            else:
                break
            count += 1

        if listCount >= 0:
            glist.clear()
        print("totalDeltaValue = ",totalDeltaValue)
        print("firstObject = ",firstObject['message_type'])
        if firstObject['message_type'] == "deactivate_plugin":
            return

        try:
            if firstObject['message_type'] == "crown_turn_event":
                print("turn event =====")
                if firstObject['task_options']['current_tool'] == 'Slider':
                    print("\n","selected slider")
                    v = slider.GetValue()
                    tvalue = v + totalDeltaValue
                    if tvalue <= 0:
                        tvalue = 0
                    if tvalue >1000:
                        tvalue = 1000
                    slider.SetValue(tvalue)
                    print("report called....",tvalue,msg)
                    report(msg,tvalue)
                elif firstObject['task_options']['current_tool'] == 'SpinCtrl':
                    print("\n","selected SpinCtrl")
                    v = spin.GetValue()
                    tvalue = v + totalDeltaValue
                    if tvalue <= 0:
                        tvalue = 0
                    if tvalue >1000:
                        tvalue = 1000
                    spin.SetValue(tvalue)
                    report(msg,tvalue)
                elif firstObject['task_options']['current_tool'] == 'Gauge':
                    if firstObject['task_options']['current_tool_option'] == 'gauge':
                        print("\n","selected Gauge")
                        v = gauge.GetValue()
                        tvalue = v + totalDeltaValue
                        if tvalue <= 0:
                            tvalue = 0
                        if tvalue >500:
                            tvalue = 500
                        gauge.SetValue(tvalue)
                        report(msg,tvalue)
                    if firstObject['task_options']['current_tool_option'] == 'gaugeRatchet':
                        print("\n","selected gaugeRatchet")
                        v = gauge.GetValue()
                        tvalue = v + (totalRatchetDeltaValue * 10)
                        if tvalue <= 0:
                            tvalue = 0
                        if tvalue >500:
                            tvalue = 500
                        gauge.SetValue(tvalue)
                        report(msg,tvalue)

                elif firstObject['task_options']['current_tool'] == 'ComboBox':
                    print("\n","selected ComboBox")
                    v = combo.GetSelection()
                    tvalue = v + totalRatchetDeltaValue
                    if tvalue <= 0:
                        tvalue = 0
                    if tvalue >999:
                        tvalue = 999
                    combo.SetSelection(tvalue)
                    report(msg,tvalue)
                elif firstObject['task_options']['current_tool'] == 'TextCtrl':
                    print("\n","selected TextCtrl")
                    global txtNowIndex, txtOriIndex
                    '''
                    v = txt.GetSize()
                    h = v.height + totalDeltaValue
                    w = v.width + totalDeltaValue
                    txt.SetSize(w,h)
                    '''
                    txtNowIndex = txtNowIndex+totalDeltaValue
                    keyLR = wx.WXK_RIGHT
                    change = False

                    if totalDeltaValue < 0:
                        totalDeltaValue = -totalDeltaValue
                        keyLR = wx.WXK_LEFT
                    
                    if txtNowIndex<txtOriIndex:
                        change = True
                        
                    uia.KeyDown(wx.WXK_SHIFT)
                    for i in range(totalDeltaValue):
                        uia.KeyDown(keyLR)
                        uia.KeyUp(keyLR)
                    uia.KeyUp(wx.WXK_RIGHT)
                    
                    text = txt.GetValue()
                    if not change:
                        text = text[txtOriIndex:txtNowIndex]
                    else:
                        text = text[txtNowIndex:txtOriIndex]

                    stext = text.split(' ')
                    if len(stext) > 1:
                        if change:  #go back
                            showText(stext[1:])
                            txtOriIndex = txtNowIndex+len(stext[0])
                        else:
                            showText(stext[0:-1])
                            txtOriIndex = txtNowIndex-len(stext[-1])
                    else:
                        print('not long enough\n')
                        print('ori:'+str(txtOriIndex)+',txt'+str(txtNowIndex)+'\n')
                    report(msg,totalDeltaValue)
                    ## Comment
                elif firstObject['task_options']['current_tool'] == 'ListBox':
                    print("\n","selected ListBox")
                    v = lb.GetSelection()
                    v = v + totalRatchetDeltaValue
                    if v <= 0:
                        v = 0
                    if v > 999:
                        v = 999
                    lb.SetSelection(v)
                    lb.EnsureVisible(v)
                    report(msg,v)

        except ValueError:
            print("Error: update UI")



    elif (msg['message_type'] == "register_ack"):
        print("register_ack = ",msg['message_type'])
        sessionId = msg['session_id']
        print("Session Id = ",sessionId)

        if platform.system() == 'Windows':
            defaultTool = "Slider"
        else:
            defaultTool = "SpinCtrl"

        connectMessage = {
            "message_type": "tool_change",
            "session_id": sessionId,
            "tool_id": defaultTool
        }
        regMsg =  json.dumps(connectMessage)
        ws.send(regMsg.encode('utf8'))

def on_message(ws, message):
    print("on_message called...")
    print(message)
    print('\n')
    # craft events come in as json objects
    craftEventObj = json.loads(message)
    wx.CallAfter(wrapperUpdateUI, craftEventObj)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("on_open called...")
    uid = "6202f2fb-834c-4393-a95f-f5051171e3ec"
    pid = os.getpid()

    connectMessage = {
        "message_type": "register",
        "plugin_guid": uid,
        "PID": pid,
        "execName": 'craft.exe',
        "manifestPath": 'C:\\ProgramData\\Logishrd\\LogiOptionsPlugins\\6202f2fb-834c-4393-a95f-f5051171e3ec\\Manifest',
        "application_version": "0.0.0"
    }

    regMsg =  json.dumps(connectMessage)
    ws.send(regMsg.encode('utf8'))

class CraftClient(object):

    def __init__(self):
        self.executableName=""
        self.manifestPath=""
        self.callback=""
        print("init\n")
    def connect(self, execName,manifestFilePath):
        print("connect callde...")
        global ws
        self.executableName = execName
        self.manifestPath = manifestFilePath

        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://127.0.0.1:10134",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
        #ws.on_open = self.on_open(self)
        ws.on_open = on_open
        #ws.run_forever()
        print("Build WS...")
        print(ws)
        
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
    def registerEventHandler(self, cb):
        self.callback = cb
    '''
    def report(self, event, value):
        toolId = event.get('task_options').get('current_tool')
        na = event.get('task_options').get('current_tool_option')

        response = {
            "message_type" : "tool_update",
            "session_id"   :  sessionId,
            "show_overlay" :  True,
            "tool_id"      :  toolId,
            "tool_options" :  [{
                "name"  : na,
                "value" : value
            }]
        };
        regMsg =  json.dumps(response)
        ws.send(regMsg.encode('utf8'))
    '''
    '''
    def wrapperUpdateUI(self,msg):
        global glist,sessionId
        totalDeltaValue=0
        totalRatchetDeltaValue=0
        count=0
        listCount=0
        global firstObject

        if(msg['message_type'] == "crown_turn_event"):
            glist.append(msg)
            listCount = len(glist)
            if listCount==0:
                return
            currentToolOption = glist[0]['task_options']['current_tool_option']
            print("+++currentToolOption = ",currentToolOption)
            print("listCount = ",listCount)
            firstObject = glist[0]
            for i in range(listCount):
                if currentToolOption == glist[i]['task_options']['current_tool_option']:
                    totalDeltaValue = totalDeltaValue = glist[i]['delta']
                    totalRatchetDeltaValue = totalRatchetDeltaValue + glist[i]['ratchet_delta']
                else:
                    break
                count += 1

            if listCount >= 0:
                glist.clear()
            print("totalDeltaValue = ",totalDeltaValue)
            print("firstObject = ",firstObject['message_type'])
            if firstObject['message_type'] == "deactivate_plugin":
                return

            try:
                if firstObject['message_type'] == "crown_turn_event":
                    print("turn event =====")
                    if firstObject['task_options']['current_tool'] == 'Slider':
                        print("\n","selected slider")
                        v = slider.GetValue()
                        tvalue = v + totalDeltaValue
                        if tvalue <= 0:
                            tvalue = 0
                        if tvalue >1000:
                            tvalue = 1000
                        slider.SetValue(tvalue)
                        print("report called....",tvalue,msg)
                        self.report(msg,tvalue)
                    elif firstObject['task_options']['current_tool'] == 'SpinCtrl':
                        print("\n","selected SpinCtrl")
                        v = spin.GetValue()
                        tvalue = v + totalDeltaValue
                        if tvalue <= 0:
                            tvalue = 0
                        if tvalue >1000:
                            tvalue = 1000
                        spin.SetValue(tvalue)
                        self.report(msg,tvalue)
                    elif firstObject['task_options']['current_tool'] == 'Gauge':
                        if firstObject['task_options']['current_tool_option'] == 'gauge':
                           print("\n","selected Gauge")
                           v = gauge.GetValue()
                           tvalue = v + totalDeltaValue
                           if tvalue <= 0:
                              tvalue = 0
                           if tvalue >500:
                              tvalue = 500
                           gauge.SetValue(tvalue)
                           self.report(msg,tvalue)
                        if firstObject['task_options']['current_tool_option'] == 'gaugeRatchet':
                           print("\n","selected gaugeRatchet")
                           v = gauge.GetValue()
                           tvalue = v + (totalRatchetDeltaValue * 10)
                           if tvalue <= 0:
                              tvalue = 0
                           if tvalue >500:
                              tvalue = 500
                           gauge.SetValue(tvalue)
                           self.report(msg,tvalue)

                    elif firstObject['task_options']['current_tool'] == 'ComboBox':
                        print("\n","selected ComboBox")
                        v = combo.GetSelection()
                        tvalue = v + totalRatchetDeltaValue
                        if tvalue <= 0:
                            tvalue = 0
                        if tvalue >999:
                            tvalue = 999
                        combo.SetSelection(tvalue)
                        self.report(msg,tvalue)
                    elif firstObject['task_options']['current_tool'] == 'TextCtrl':
                        print("\n","selected TextCtrl")
                        v = txt.GetSize()
                        h = v.height + totalDeltaValue
                        w = v.width + totalDeltaValue
                        txt.SetSize(w,h)
                        self.report(msg,w)
                    ## Comment
                    elif firstObject['task_options']['current_tool'] == 'ListBox':
                        print("\n","selected ListBox")
                        v = lb.GetSelection()
                        v = v + totalRatchetDeltaValue
                        if v <= 0:
                            v = 0
                        if v > 999:
                            v = 999
                        lb.SetSelection(v)
                        lb.EnsureVisible(v)
                        self.report(msg,v)

            except ValueError:
                print("Error: update UI")



        elif (msg['message_type'] == "register_ack"):
            print("register_ack = ",msg['message_type'])
            sessionId = msg['session_id']
            print("Session Id = ",sessionId)

            if platform.system() == 'Windows':
                defaultTool = "Slider"
            else:
                defaultTool = "SpinCtrl"

            connectMessage = {
                "message_type": "tool_change",
                "session_id": sessionId,
                "tool_id": defaultTool
            }
            regMsg =  json.dumps(connectMessage)
            ws.send(regMsg.encode('utf8'))
    '''
class TestFrame(wx.Frame):

    def __init__(self, parent, id):
        global craft,slider,spin,gauge,combo,txt,lb
        global txtNowIndex, txtOriIndex
        global panel

        wx.Frame.__init__(self, parent, id, "Craft Python SDK Sample", size=(800,400))

        panel = wx.Panel(self)
        '''
        lbl = wx.StaticText(panel,-1, label="text", pos=(10,20), size=(50,-1))
        lbl.SetLabel("Slider")

        slider=wx.Slider(panel, -1, 0, 1, 1000, (100,20), (200,-1))
        slider.Bind(wx.EVT_SET_FOCUS, self.sliderFocus)
        slider.Bind(wx.EVT_LEFT_UP, self.sliderFocus)

        lbl = wx.StaticText(panel, -1, label="text", pos=(10,100), size=(50,-1))
        lbl.SetLabel("SpinCtrl")

        spin = wx.SpinCtrl(panel, -1, "", pos=(100,100), size=(200,-1), min=0, max=1000)
        spin.Bind(wx.EVT_CHILD_FOCUS, self.spinCtrlFocus)
        spin.Bind(wx.EVT_LEFT_UP, self.spinCtrlFocus)

        lbl = wx.StaticText(panel, -1, label="text", pos=(10,180), size=(50,-1))
        lbl.SetLabel("Gauge")

        gauge = wx.Gauge(panel, -1, range=500, pos=(100,180), size=(200,25))
        gauge.Bind(wx.EVT_LEFT_UP, self.gaugeClick)

        lbl = wx.StaticText(panel, -1, label="text", pos=(10,260), size=(50,-1))
        lbl.SetLabel("ComboBox")

        l=[]
        for i in range(0, 1000):
          l.append(str(i))
        combo = wx.ComboBox(panel, -1, "", pos=(100,260), size=(200,25), choices=l)
        combo.Bind(wx.EVT_SET_FOCUS, self.comboBoxFocus)
        combo.Bind(wx.EVT_LEFT_UP, self.comboBoxFocus)
        

        lbl = wx.StaticText(panel, -1, label="text", pos=(400,20), size=(50,-1))
        lbl.SetLabel("TextCtrl")
        '''
        vtxt = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque semper ut felis non bibendum. " \
        "Suspendisse potenti. Mauris rhoncus auctor quam, non ullamcorper elit interdum a. Aliquam erat volutpat. " \
        "Ut facilisis odio a enim facilisis, at porta lectus hendrerit. Curabitur et vulputate lectus, nec sollicitudin odio. " \
        "Morbi tincidunt iaculis erat, eu bibendum sapien vehicula vel. Etiam sodales malesuada mauris, " \
        "quis viverra eros imperdiet at. Vestibulum maximus dui dolor, sed laoreet arcu laoreet in. "
        
        dic_text = "potential\n"\
        "adjective\n [ before noun ] UK"\
        "/pəˈten.ʃəl/ US ​\n /poʊˈten.ʃəl/B2\n"\
        "possible when the necessary conditions exist潛在的，可能的\n"\
        "A number of potential buyers have expressed interest in the company.\n"\
        "一些潛在的買主表達了對該公司的興趣。\n"\
        "Many potential customers are waiting for a fall in prices before buying.\n"
        
        txt = wx.TextCtrl(panel, -1, vtxt, pos=(400,20), size=(380,360), style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)
        #txt_left = wx.TextCtrl(panel, -1, dic_text, pos=(10,20), size=(380,180), style=wx.TE_MULTILINE|wx.TE_NOHIDESEL)
        txt.Bind(wx.EVT_SET_FOCUS, self.textCtrlFocus)
        txt.Bind(wx.EVT_LEFT_UP, self.textCtrlFocus)

        '''
        lbl = wx.StaticText(panel, -1, label="text", pos=(400,180), size=(50,-1))
        lbl.SetLabel("ListBox")

        li =[]
        for i in range(0, 1000):
            li.append(str(i))

        lb = wx.ListBox(panel, -1, pos=(480,180), size=(100,-1), choices=li)
        lb.Bind(wx.EVT_SET_FOCUS, self.listBoxFocus)
        lb.Bind(wx.EVT_LEFT_UP, self.listBoxFocus)
        '''
    def listBoxFocus(self, event):
        print("ListBox receives focus")
        self.changeTool("ListBox")
        event.Skip()

    def textCtrlFocus(self, event):
        print("TextCtrl receives focus")
        self.changeTool("TextCtrl")
        txt.ShowNativeCaret(True)
        event.Skip()

    def comboBoxFocus(self, event):
        print("ComboBox receives focus")
        self.changeTool("ComboBox")
        event.Skip()

    def gaugeClick(self, event):
        print("Gauge clicked...")
        self.changeTool("Gauge")
        event.Skip()

    def sliderFocus(self, event):
        print("Slider receives focus")
        self.changeTool("Slider")
        event.Skip()

    def spinCtrlFocus(self, event):
        print("SpinCtrl receives focus")
        self.changeTool("SpinCtrl")
        event.Skip()

    def changeTool(self, name):
        connectMessage = {
            "message_type": "tool_change",
            "session_id": sessionId,
            "tool_id": name
        }
        regMsg =  json.dumps(connectMessage)
        ws.send(regMsg.encode('utf8'))


if __name__ == '__main__':
    global ws
    global craft

    app = wx.App()

    craft = CraftClient()
    if platform.system() == 'Windows':
        craft.connect("craft.exe", "")
    else:
        craft.connect("craft.app", "")

    frame = TestFrame(parent=None, id=-1)
    txtNowIndex = 0
    txtOriIndex = 0
    frame.Show()

app.MainLoop()