import lvgl as lv
import time
import ntptime
import network
import urequests
from machine import Timer, Pin, reset
from umqtt.simple import MQTTClient

from const import *
from connect_wifi import ConnectWIFI
from home import HomePage
from cam import CameraPage
from sensor import TemperatureHumidity, Light, Fan, Curtain, Sound, Touch, LightSensitive, RainSensitive

class IndexPage():
    def __init__(self, scr):
        self.scr = scr
        self.time_now = time.localtime()
        self.wlan = network.WLAN(network.STA_IF) # 激活wifi
        #self.wlan.active(False)
        self.wlan.active(True)
        print(self.wlan.scan())
        
        with open('wifi_info.txt', 'r') as f:
            ssid = f.readline().rstrip("\n")
            password = f.readline().rstrip("\n")
        print(ssid)
        print(password)
        self.wlan.config(reconnects=5)
        self.wlan.connect(ssid, password)
        
        self.bedroom_light = Light(BEDROOM_LIGHT)
        self.bedroom_switch = Light(BEDROOM_SWITCH)
        self.living_light = Light(LIVING_LIGHT)
        self.living_fan = Fan(LIVING_FAN)
        self.kitchen_light = Light(KITCHEN_LIGHT)
        self.dht11 = TemperatureHumidity(TAH)
        self.curtain = Curtain(CURTAIN_A, CURTAIN_B, CURTAIN_C, CURTAIN_D)
        self.sound = Sound(SOUND)
        self.touch = Touch(TOUCH)
        self.lightness = LightSensitive(LIVING_LIGHT_SEN)
        self.rain = RainSensitive(RAIN_SEN)
        self.air = LightSensitive(AIR)
        
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
        self.weather_img.cache_set_size(8)
        
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
        self.tt = lv.timer_create(self.wait_wifi,1000, None )
        self.tt.set_repeat_count(10)
        self.touch_t = lv.timer_create(self.touchif,1000, None )
        
        
    def wait_wifi(self, timer):
        if self.wlan.isconnected():
            self.tt.pause()
            ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
            #ntptime.host = 'ntp1.aliyun.com'  # 可选，ntp服务器，默认是"pool.ntp.org"
            self.time_now = time.localtime()
            self.wifi_path = 'imgs/wifi_on.png'
            with open(self.wifi_path, 'rb') as f:
                wifi_data = f.read()

            self.wifi_png = lv.img_dsc_t({
            'data_size': len(wifi_data),
            'data': wifi_data
            })
            self.wifi_img.clean()
            self.wifi_img.set_src(self.wifi_png)
            self.flush_weather()
            ntptime.settime()   # 修改设备时间,到这就已经设置好
            self.connect_mqtt()
            lv.timer_create(self.check_msg, 1000, None)
            lv.timer_create(self.keep_client, 10000, None)
            self.date_label.set_text('{0:0>4d}-{1:0>2d}-{2:0>2d} {3}'.format(self.time_now[0], self.time_now[1], self.time_now[2], WEEK_MAP[str(self.time_now[6])]))
            del self.tt
        
    def MsgOK(self, topic, msg):          # 回调函数，用于收到消息
        print((topic, msg))             # 打印主题值和消息值
        if topic == BEDROOM_LIGHT_TOPIC.encode():     # 判断是不是发给myTopic的消息
            if b'on' in msg:                # 当收到on
                self.bedroom_light.on()
            elif b"off" in msg:             #  当收到off
                self.bedroom_light.off()
        elif topic == BEDROOM_SWITCH_TOPIC.encode():
            if b'on' in msg:                # 当收到on
                self.bedroom_switch.on()
            elif b"off" in msg:             #  当收到off
                self.bedroom_switch.off()
        elif topic == SOUND_TOPIC.encode():
            if b'on' in msg:                # 当收到on
                self.sound.run(5)
            elif b"off" in msg:             #  当收到off
                self.sound.run(5)
        elif topic == LIVINGROOM_FAN_TOPIC.encode():
            if b'on' in msg:                # 当收到on
                level = msg[3:].decode()
                if level:
                    self.living_fan.on(int(level))
                else:
                    self.living_fan.on()
            elif b"off" in msg:             #  当收到off
                self.living_fan.off()
        elif topic == CURTAIN_TOPIC.encode():
            if b'on' in msg:                # 当收到on
                level = msg[3:].decode()
                if level:
                    self.curtain.num(int(level))
                else:
                    self.curtain.num(100)
            elif b"off" in msg:             #  当收到off
                self.curtain.num(0)
        elif topic == WINDOW_TOPIC.encode():
            if b'on' in msg:                # 当收到on
                self.bedroom_switch.on()
            elif b"off" in msg:             #  当收到off
                self.bedroom_switch.off()
                
    def connect_mqtt(self):
        self.client = MQTTClient(CLIENT_ID, SERVER_IP,PORT)
        self.client.set_callback(self.MsgOK)
        print('setback')
        self.client.connect()
        print('connect')
        self.client.subscribe(BEDROOM_LIGHT_TOPIC)
        self.client.subscribe(BEDROOM_SWITCH_TOPIC)
        self.client.subscribe(LIVINGROOM_LIGHT_TOPIC)
        self.client.subscribe(LIVINGROOM_FAN_TOPIC)
        self.client.subscribe(KITCHEN_LIGHT_TOPIC)
        self.client.subscribe(CURTAIN_TOPIC)
        self.client.subscribe(WINDOW_TOPIC)
        self.client.subscribe(SOUND_TOPIC)
        #self.client.subscribe(TEM_HUM_YOPIC)
        
        
    def check_msg(self, timer):
        self.client.check_msg()
    
    def keep_client(self, timer):
        self.client.ping()
        
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
        
        self.date_label.set_text('{0:0>4d}-{1:0>2d}-{2:0>2d} {3}'.format(self.time_now[0], self.time_now[1], self.time_now[2], WEEK_MAP[str(self.time_now[6])]))
        if self.wlan.isconnected():
            msg = '#{0}#{1}'.format(self.tem_hum['temperature'], self.tem_hum['humidity'])
            try:
                self.client.publish(TEM_HUM_YOPIC, msg)         
                self.client.publish(LIGHTNESS_TOPIC, '#{}'.format(self.lightness.read()))
                self.client.publish(RAIN_TOPIC, '#{}'.format(self.rain.read()))
                self.client.publish(AIR_TOPIC, '#{}'.format(self.air.read_mq()))
            except :
                pass
    
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
        self.wifi_page = ConnectWIFI(self.wifi_scr, self.wlan)
        self.wifi_page.back_btn.add_event_cb(self.back_index,lv.EVENT.CLICKED, None)
    
    
    def back_index(self, e):
        """回到首页"""
        code = e.get_code()
        obj = e.get_target() 
        lv.scr_load(self.scr)
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
        try:
            if self.wifi_page.flag:
                self.tt = lv.timer_create(self.wait_wifi,1000, None )
                self.tt.set_repeat_count(10)
        except:
            pass
            

        
    def go_home(self, e):
        kwargs = {
            'bedroom_light': self.bedroom_light,
            'bedroom_switch': self.bedroom_switch,
            'living_light': self.living_light,
            'living_fan': self.living_fan,
            'kitchen_light': self.kitchen_light,
            'curtain': self.curtain,
            }
        self.home_scr = lv.obj()
        lv.scr_load(self.home_scr)
        home_page = HomePage(self.home_scr, **kwargs)
        home_page.back_btn.add_event_cb(self.back_index,lv.EVENT.CLICKED, None)
        
    def touchif(self, e):
        if self.touch.read():
            print(1)
            self.touch_t.pause()
            self.go_camera()
        
    def go_camera(self):
        self.camera_scr = lv.obj()
        lv.scr_load(self.camera_scr)
        self.camera_page = CameraPage(self.camera_scr)
        self.camera_page.back_btn.add_event_cb(self.back_index_camera,lv.EVENT.CLICKED, None)
        
    def back_index_camera(self, e):
        """回到首页"""
        self.camera_page.t.pause()
        self.camera_page.destory()
        lv.scr_load(self.scr)
        del self.camera_page.t
        del self.camera_page
        self.touch_t.ready()
        


if __name__ == '__main__':
    from umqtt.simple import MQTTClient
    from espidf import VSPI_HOST, HSPI_HOST
    from ili9XXX import ili9341
    from xpt2046 import xpt2046
    import fs_driver
    import _thread

    
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
    


   
