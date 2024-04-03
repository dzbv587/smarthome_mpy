import lvgl as lv
import time
import network
import urequests
from machine import Timer, Pin

from const import *
from connect_wifi import ConnectWIFI
from home import HomePage
from sensor import TemperatureHumidity, Light

class IndexPage():
    def __init__(self, scr):
        self.scr = scr
        self.time_now = time.localtime()
        
        self.bedroom_light = Light(BEDROOM_LIGHT)
        self.bedroom_switch = Light(BEDROOM_SWITCH)
        self.living_light = Light(LIVING_LIGHT)
        self.kitchen_light = Light(KITCHEN_LIGHT)
        self.dht11 = TemperatureHumidity(TAH)
        
#         self.dh = dht.DHT11(Pin(5))
#         try:
#             self.dh.measure() # 第一次执行异常，第二次正常
#         except OSError as e:
#             self.dh.measure()
        self.wlan = network.WLAN(network.STA_IF) # 激活wifi
        self.wlan.active(True)
        # TODO: 连接wifi
        
        # 时间标签
        style_time_label = lv.style_t()
        style_time_label.init()
        style_time_label.set_radius(10)
        style_time_label.set_size(220, 100)
        style_time_label.set_pad_ver(20)
        style_time_label.set_pad_hor(10)
        style_time_label.set_x(10)
        style_time_label.set_y(20)
        style_time_label.set_border_width(3)
        style_time_label.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        style_time_label.set_bg_color(lv.color_white())
        
        self.time_label = lv.label(self.scr)
        self.time_label.add_style(style_time_label, 0)
        self.time_label.set_style_text_font(lv.font_montserrat_44, 0) # 字体像素大小
        self.time_label.set_text('{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(self.time_now[3], self.time_now[4], self.time_now[5])) 
        
        # 日期标签
        style_date_label = lv.style_t()
        style_date_label.init()
        style_date_label.set_radius(10)
        style_date_label.set_size(220, 50)
        style_date_label.set_pad_ver(10)
        style_date_label.set_pad_hor(10)
        style_date_label.set_x(10)
        style_date_label.set_y(135)
        style_date_label.set_border_width(3)
        style_date_label.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        style_date_label.set_bg_color(lv.color_white())
        
        self.date_label = lv.label(self.scr)
        self.date_label.add_style(style_date_label, 0)
        self.date_label.set_style_text_font(lv.font_montserrat_24, 0)
        self.date_label.set_text('{0:0>4d}-{1:0>2d}-{2:0>2d} {3}'.format(self.time_now[0], self.time_now[1], self.time_now[2], WEEK_MAP[str(self.time_now[6])]))
        
        # 天气按钮
        style_weather_btn = lv.style_t()
        style_weather_btn.init()
        style_weather_btn.set_radius(10)
        style_weather_btn.set_size(80, 50)
        style_weather_btn.set_pad_ver(10)
        style_weather_btn.set_pad_hor(5)
        style_weather_btn.set_x(10)
        style_weather_btn.set_y(200)
        style_weather_btn.set_border_width(3)
        style_weather_btn.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        style_weather_btn.set_bg_color(lv.color_white())
        
        self.weather_btn = lv.btn(self.scr)
        self.weather_btn.add_style(style_weather_btn, 0)
        self.weather_btn.add_event_cb(self.flush_weather,lv.EVENT.CLICKED, None)
        
        # 获取天气详情
        try:
            response = urequests.get(WEATHER_API)
            weather = response.json()['lives'][0]['weather']
            self.weather_path = WEATHER_MAP[weather]
        except (KeyError, OSError) as e:
            self.weather_path = WEATHER_MAP['未知']
        with open(self.weather_path, 'rb') as f:
            png_data = f.read()

        self.weather_png = lv.img_dsc_t({
        'data_size': len(png_data),
        'data': png_data
        })
        self.weather_img = lv.img(self.weather_btn)
        self.weather_img.set_src(self.weather_png)
        self.weather_img.set_zoom(48)
        self.weather_img.set_size(45, 45)
        self.weather_img.set_pos(10, -10)
        self.weather_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        self.weather_img.cache_set_size(7)
        
        # WIFI按钮
        style_wifi_btn = lv.style_t()
        style_wifi_btn.init()
        style_wifi_btn.set_radius(10)
        style_wifi_btn.set_size(80, 50)
        style_wifi_btn.set_pad_ver(10)
        style_wifi_btn.set_pad_hor(5)
        style_wifi_btn.set_x(10)
        style_wifi_btn.set_y(260)
        style_wifi_btn.set_border_width(3)
        style_wifi_btn.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        style_wifi_btn.set_bg_color(lv.color_white())
        
        self.wifi_btn = lv.btn(self.scr)
        self.wifi_btn.add_style(style_wifi_btn, 0)
        self.wifi_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        # 获取wifi图标
        if self.wlan.isconnected():
            self.wifi_path = 'imgs/wifi_on.png'
        else:
            self.wifi_path = 'imgs/wifi_off.png'
        with open(self.wifi_path, 'rb') as f:
            wifi_data = f.read()

        self.wifi_png = lv.img_dsc_t({
        'data_size': len(wifi_data),
        'data': wifi_data
        })
        self.wifi_img = lv.img(self.wifi_btn)
        self.wifi_img.set_src(self.wifi_png)
        self.wifi_img.set_zoom(48)
        self.wifi_img.set_size(45, 45)
        self.wifi_img.set_pos(10, -10)
        self.wifi_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 温湿度标签
        self.tem_hum = self.dht11.get_tem_hum()
        style_temp_label = lv.style_t()
        style_temp_label.init()
        style_temp_label.set_radius(10)
        style_temp_label.set_size(130, 50)
        style_temp_label.set_pad_ver(10)
        style_temp_label.set_pad_hor(10)
        style_temp_label.set_x(100)
        style_temp_label.set_y(200)
        style_temp_label.set_border_width(3)
        style_temp_label.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.temp_label = lv.label(self.scr)
        self.temp_label.add_style(style_temp_label, 0)
        self.temp_label.set_style_text_font(lv.font_montserrat_20, 0)
        self.temp_label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
        self.temp_label.set_text('Tem:{0:0>2d}  Hum:{1:0>2d}'.format(self.tem_hum['temperature'], self.tem_hum['humidity']))
        
        # home按钮
        style_home_btn = lv.style_t()
        style_home_btn.init()
        style_home_btn.set_radius(10)
        style_home_btn.set_size(130, 50)
        style_home_btn.set_pad_ver(10)
        style_home_btn.set_pad_hor(15)
        style_home_btn.set_x(100)
        style_home_btn.set_y(260)
        style_home_btn.set_border_width(3)
        style_home_btn.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        style_home_btn.set_bg_color(lv.color_white())
        
        self.home_btn = lv.btn(self.scr)
        self.home_btn.add_style(style_home_btn, 0)
        self.home_btn.add_event_cb(self.go_home,lv.EVENT.CLICKED, None)
    
        home_label = lv.label(self.home_btn)
        home_label.set_style_text_font(lv.font_montserrat_20, 0)
        home_label.set_recolor(True) 
        home_label.set_text('#000000 My Home#')
        
        
        lv.timer_create(self.timer_cb, 1000, None) # 每秒刷新时间
        lv.timer_create(self.flush_dht, 5000, None ) # 每5秒刷新温湿度

        
    def timer_cb(self, timer):
        """刷新时间标签"""
        self.time_now = time.localtime()
        self.time_label.set_text('{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(self.time_now[3], self.time_now[4], self.time_now[5]))
        if not self.time_now[0] and not self.time_now[1] and not self.time_now[2]:
            self.date_label.set_text('{0:0>4d}-{1:0>2d}-{2:0>2d} {3}'.format(self.time_now[0], self.time_now[1], self.time_now[2], WEEK_MAP[str(self.time_now[6])]))
    
    def flush_dht(self, timer):
        """刷新温湿度标签"""
        self.tem_hum = self.dht11.get_tem_hum()
        self.temp_label.set_text('Tem:{0:0>2d}  Hum:{1:0>2d}'.format(self.tem_hum['temperature'], self.tem_hum['humidity']))
    
    def flush_weather(self, e=None):
        """更新天气图标"""
        try:
            response = urequests.get(WEATHER_API)
            weather = response.json()['lives'][0]['weather']
            self.weather_path = WEATHER_MAP[weather]
        except (KeyError, OSError) as e:
            self.weather_path = WEATHER_MAP['未知']
        with open(self.weather_path, 'rb') as f:
            png_data = f.read()

        self.weather_png = lv.img_dsc_t({
        'data_size': len(png_data),
        'data': png_data
        })
        self.weather_img.clean()
        self.weather_img.set_src(self.weather_png)
        
    def conn_wifi(self, e):
        """连接wifi界面"""
        self.wifi_scr = lv.obj()
        lv.scr_load(self.wifi_scr)
        wifi_page = ConnectWIFI(self.wifi_scr, self.wlan)
        wifi_page.back_btn.add_event_cb(self.back_index,lv.EVENT.CLICKED, None)
    
    
    def back_index(self, e):
        """回到首页"""
        code = e.get_code()
        obj = e.get_target() 
        lv.scr_load(self.scr)
        self.wifi_scr.delete()
        # 更新wifi图标
        if self.wlan.isconnected():
            self.wifi_path = 'imgs/wifi_on.png'
        else:
            self.wifi_path = 'imgs/wifi_off.png'
        with open(self.wifi_path, 'rb') as f:
            wifi_data = f.read()

        self.wifi_png = lv.img_dsc_t({
        'data_size': len(wifi_data),
        'data': wifi_data
        })
        self.wifi_img.clean()
        self.wifi_img.set_src(self.wifi_png)
        self.flush_weather()

        
    def go_home(self, e):
        kwargs = {
            'bedroom_light': self.bedroom_light,
            'bedroom_switch': self.bedroom_switch,
            'living_light': self.living_light,
            'kitchen_light': self.kitchen_light,
            }
        self.home_scr = lv.obj()
        home_page = HomePage(self.home_scr, **kwargs)
        lv.scr_load(self.home_scr)
#         wifi_page = ConnectWIFI(self.wifi_scr, self.wlan)
#         wifi_page.back_btn.add_event_cb(self.back_index,lv.EVENT.CLICKED, None)
        


if __name__ == '__main__':
    
    from espidf import VSPI_HOST, HSPI_HOST
    from ili9XXX import ili9341
    from xpt2046 import xpt2046
    import fs_driver

    
    disp = ili9341(miso=MISO, mosi=MOSI, clk=CLK, cs=CS, dc=DC, rst=RST,power=POWER,backlight=LED,#rot=0x80,
                    power_on=1,backlight_on=1, spihost=VSPI_HOST, width=WIDTH, height=HEIGHT, factor=16,half_duplex=False)
    touch = xpt2046(cs=T_CS, spihost=VSPI_HOST, mhz=5, max_cmds=16,half_duplex=False,
                    cal_x0 = 3948, cal_y0 = 242, cal_x1 = 423, cal_y1 = 3783)

    scr = lv.obj()  # scr====> screen 屏幕
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    scr = lv.scr_act()
    scr.clean()
    i = IndexPage(scr)
   
