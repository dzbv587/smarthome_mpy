import lvgl as lv
import time

class WifiItem():
    def __init__(self, scr, wlan, ssid):
        self.scr = scr
        self.wlan = wlan
        self.ssid = ssid
        ssid_label = lv.label(self.scr)
        ssid_label.set_text(self.ssid)
        ssid_label.set_pos(20, 20)
        pwd_label = lv.label(self.scr)
        pwd_label.set_text("Password:")
        pwd_label.set_pos(20, 50)
        pwd_ta = lv.textarea(self.scr)
        pwd_ta.set_text("")
        pwd_ta.set_password_mode(True)
        pwd_ta.set_one_line(True)
        pwd_ta.set_width(180)
        pwd_ta.set_pos(20, 70)
        pwd_ta.add_event_cb(self.ta_event_cb, lv.EVENT.ALL, None)
        self.kb = lv.keyboard(self.scr)
        self.kb.set_size(240, 120)
        self.kb.set_textarea(pwd_ta)  


        # 悬浮返回按钮
        self.back_btn = lv.btn(self.scr)
        self.back_btn.set_size(50, 50)
        self.back_btn.add_flag(lv.obj.FLAG.FLOATING)
        self.back_btn.align(lv.ALIGN.BOTTOM_RIGHT, -95, -140)
        self.back_btn.set_style_bg_img_src(lv.SYMBOL.NEW_LINE, 0)
        self.back_btn.set_style_text_font(lv.theme_get_font_large(self.back_btn), 0)

    def ta_event_cb(self, e):
        """连接wifi"""
        code = e.get_code()
        ta = e.get_target()
        if code == lv.EVENT.CLICKED or code == lv.EVENT.FOCUSED:
            # Focus on the clicked text area
            if self.kb != None:
                self.kb.set_textarea(ta)

        elif code == lv.EVENT.READY:
            # TODO: 等待连接动画          
            self.wlan.active(False)
            self.wlan.active(True)
            self.wlan.connect(self.ssid, ta.get_text())           
            
            # TODO: 连接信息优化 help(network) http://micropython.circuitpython.com.cn/en/latet/library/network.WLAN.html#network.WLAN.status
            for _ in range(10):
                time.sleep_ms(500)
                if self.wlan.isconnected():
                    mbox = lv.msgbox(self.scr, "Warning", "Connected to {} successfully!".format(self.ssid), None, True)
                    mbox.center()
                    self.back_btn.set_style_bg_img_src(lv.SYMBOL.OK, 0)
                    break
            else:
                mbox = lv.msgbox(self.scr, "Warning", "The connection timed out, please check if the password is correct.", None, True)
                mbox.center()

