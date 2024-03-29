import time
import lvgl as lv

from wifi_item import WifiItem

class ConnectWIFI():
    def __init__(self, scr, wlan):
        self.scr = scr
        # 获取wifi信息
        self.wlan = wlan      
        self.wlan_list = self.wlan.scan()

        # 创建wifi列表
        self.wifi_list = lv.list(self.scr)
        self.wifi_list.set_size(240, 320)
        self.wifi_list.center()
        if self.wlan.isconnected():
            for wlan_item in self.wlan_list:
                if wlan_item[0]:
                    if wlan_item[0].decode('utf-8') == self.wlan.config('essid'):
                        item_btn = self.wifi_list.add_btn(lv.SYMBOL.OK, wlan_item[0])
                    else:
                        item_btn = self.wifi_list.add_btn(lv.SYMBOL.WIFI, wlan_item[0])
                    item_btn.add_event_cb(self.wifi_info,lv.EVENT.ALL, None)
        else:
            for wlan_item in self.wlan_list:
                if wlan_item[0]:
                    item_btn = self.wifi_list.add_btn(lv.SYMBOL.WIFI, wlan_item[0])
                    item_btn.add_event_cb(self.wifi_info,lv.EVENT.ALL, None)

        # 一键配网按钮
        scan_btn = lv.btn(self.scr)
        scan_btn.set_size(50, 50)
        scan_btn.add_flag(lv.obj.FLAG.FLOATING)
        scan_btn.align(lv.ALIGN.BOTTOM_RIGHT, -10, -130)
        scan_btn.set_style_bg_img_src(lv.SYMBOL.IMAGE, 0)
        scan_btn.set_style_text_font(lv.theme_get_font_large(scan_btn), 0)
        scan_btn.add_event_cb(self.sm_config,lv.EVENT.ALL, None)

        # 悬浮刷新按钮
        refresh_btn = lv.btn(self.scr)
        refresh_btn.set_size(50, 50)
        refresh_btn.add_flag(lv.obj.FLAG.FLOATING)
        refresh_btn.align(lv.ALIGN.BOTTOM_RIGHT, -10, -70)
        refresh_btn.set_style_bg_img_src(lv.SYMBOL.REFRESH, 0)
        refresh_btn.set_style_text_font(lv.theme_get_font_large(refresh_btn), 0)
        refresh_btn.add_event_cb(self.refresh_list,lv.EVENT.ALL, None)

        # 悬浮返回按钮
        self.back_btn = lv.btn(self.scr)
        self.back_btn.set_size(50, 50)
        self.back_btn.add_flag(lv.obj.FLAG.FLOATING)
        self.back_btn.align(lv.ALIGN.BOTTOM_RIGHT, -10, -10)
        self.back_btn.set_style_bg_img_src(lv.SYMBOL.NEW_LINE, 0)
        self.back_btn.set_style_text_font(lv.theme_get_font_large(self.back_btn), 0)

    def sm_config(self, e):
        "一键配网"
        code = e.get_code()
        obj = e.get_target()
        if code == lv.EVENT.CLICKED:
            # TODO: 一键配网实现
            self.sc_scr = lv.obj()
            with open('imgs/smcon.png','rb') as f:
                png_data = f.read()

            img_cogwheel_argb = lv.img_dsc_t({
            'data_size': len(png_data),
            'data': png_data
            })

            img1 = lv.img(self.sc_scr)
            img1.set_src(img_cogwheel_argb)
            #img1.align(lv.ALIGN.CENTER, 0, -20)
            img1.set_zoom(120)
            img1.set_size(240, 240)
            label1 = lv.label(self.sc_scr)
            label1.set_text("weixinsaoma")
            label1.set_pos(70, 50)
            
            lv.scr_load(self.sc_scr)

    
    def refresh_list(self, e):
        """刷新wifi列表"""
        code = e.get_code()
        obj = e.get_target()
        if code == lv.EVENT.CLICKED:
            # TODO: 刷新过度动画
            self.wlan_list = self.wlan.scan()
            self.wifi_list.clean()  
            if self.wlan.isconnected():
                for wlan_item in self.wlan_list:
                    if wlan_item[0]:
                        if wlan_item[0].decode('utf-8') == self.wlan.config('essid'):
                            item_btn = self.wifi_list.add_btn(lv.SYMBOL.OK, wlan_item[0])
                        else:
                            item_btn = self.wifi_list.add_btn(lv.SYMBOL.WIFI, wlan_item[0])
                        item_btn.add_event_cb(self.wifi_info,lv.EVENT.ALL, None)
            else:
                for wlan_item in self.wlan_list:
                    if wlan_item[0]:
                        item_btn = self.wifi_list.add_btn(lv.SYMBOL.WIFI, wlan_item[0])
                        item_btn.add_event_cb(self.wifi_info,lv.EVENT.ALL, None)

    
    def wifi_info(self, e):
        """wifi详情"""
        code = e.get_code()
        obj = e.get_target()
        if code == lv.EVENT.CLICKED:
                self.item_scr = lv.obj()
                lv.scr_load(self.item_scr)
                wifi_item = WifiItem(self.item_scr, self.wlan, self.wifi_list.get_btn_text(obj))
                wifi_item.back_btn.add_event_cb(self.item_back,lv.EVENT.CLICKED, None)
                          
    def item_back(self, e):
        """返回wifi列表页"""
        lv.scr_load(self.scr)
        del self.item_scr
        

if __name__ == '__main__':
    
    from espidf import VSPI_HOST, HSPI_HOST
    from ili9XXX import ili9341
    from xpt2046 import xpt2046
    from const import *

    
    disp = ili9341(miso=MISO, mosi=MOSI, clk=CLK, cs=CS, dc=DC, rst=RST,power=POWER,backlight=LED,#rot=0x80,
                    power_on=1,backlight_on=1, spihost=VSPI_HOST, width=WIDTH, height=HEIGHT, factor=16,half_duplex=False)
    touch = xpt2046(cs=T_CS, spihost=VSPI_HOST, mhz=5, max_cmds=16,half_duplex=False,
                    cal_x0 = 3948, cal_y0 = 242, cal_x1 = 423, cal_y1 = 3783)

    scr = lv.obj()
    lv.scr_load(scr)
    ConnectWIFI(scr)
 
