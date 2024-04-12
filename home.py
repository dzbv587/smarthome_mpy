import lvgl as lv

from light import LightPage


class HomePage():
    def __init__(self, scr, **kwargs):
        print(kwargs)
        self.scr = scr
        style_head_label = lv.style_t()
        style_head_label.init()
        style_head_label.set_radius(10)
        style_head_label.set_size(240, 60)
        style_head_label.set_pad_ver(10)
        style_head_label.set_pad_hor(35)
        style_head_label.set_x(0)
        style_head_label.set_y(0)
        style_head_label.set_border_width(3)
        style_head_label.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        # TODO: 设置北京颜色
        style_head_label.set_bg_color(lv.color_hex(0xFF0000))
        head_label = lv.label(self.scr)
        head_label.add_style(style_head_label, 0)
        head_label.set_style_text_font(lv.font_montserrat_20, 0) # 字体像素大小
        head_label.set_text("My Home")
        
        # 悬浮返回按钮
        self.back_btn = lv.btn(self.scr)
        self.back_btn.set_size(40, 40)
        self.back_btn.add_flag(lv.obj.FLAG.FLOATING)
        self.back_btn.align(lv.ALIGN.BOTTOM_RIGHT, -10, -270)
        self.back_btn.set_style_bg_img_src(lv.SYMBOL.NEW_LINE, 0)
        self.back_btn.set_style_text_font(lv.theme_get_font_large(self.back_btn), 0)
        
        style_tab = lv.style_t()
        style_tab.init()
        style_tab.set_radius(10)
        style_tab.set_x(0)
        style_tab.set_y(60)
        style_tab.set_border_width(3)
        style_tab.set_border_color(lv.color_hex(0x11ACCF))
        
        tabview = lv.tabview(self.scr, lv.DIR.TOP, 50)
        tabview.add_style(style_tab, 0)
        tab_bedroom = tabview.add_tab('Bedroom')
        tab_livingroom = tabview.add_tab('Livingroom')
        tab_kitchen = tabview.add_tab('Kitchen')
        
        # tab1页面
        # 灯按钮
        self.bedroom_light = kwargs['bedroom_light']
        self.style_bedroom_light = lv.style_t()
        self.style_bedroom_light.init()
        self.style_bedroom_light.set_radius(10)
        self.style_bedroom_light.set_size(100, 50)
        self.style_bedroom_light.set_pad_ver(10)
        self.style_bedroom_light.set_pad_hor(15)
        self.style_bedroom_light.set_x(0)
        self.style_bedroom_light.set_y(0)
        self.style_bedroom_light.set_border_width(3)
        self.style_bedroom_light.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        if self.bedroom_light.state():
            self.style_bedroom_light.set_bg_color(lv.color_hex(0xFFDD00))
        else :
            self.style_bedroom_light.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.bedroom_light_btn = lv.btn(tab_bedroom)
        self.bedroom_light_btn.add_style(self.style_bedroom_light, 0)
        self.bedroom_light_btn.add_event_cb(lambda e: self.light_click(e,
            {"light":self.bedroom_light, "name":"BedroomLight", "style":self.style_bedroom_light}), lv.EVENT.CLICKED, None)
        
        with open('imgs/灯光.png', 'rb') as f:
            light_data = f.read()

        self.light_png = lv.img_dsc_t({
        'data_size': len(light_data),
        'data': light_data
        })
        bedroom_light_img = lv.img(self.bedroom_light_btn)
        bedroom_light_img.set_src(self.light_png)
        bedroom_light_img.set_zoom(48)
        bedroom_light_img.set_size(45, 45)
        bedroom_light_img.set_pos(10, -10)
        bedroom_light_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 开关按钮
        self.bedroom_switch = kwargs['bedroom_switch']
        self.style_bedroom_switch = lv.style_t()
        self.style_bedroom_switch.init()
        self.style_bedroom_switch.set_radius(10)
        self.style_bedroom_switch.set_size(100, 50)
        self.style_bedroom_switch.set_pad_ver(10)
        self.style_bedroom_switch.set_pad_hor(15)
        self.style_bedroom_switch.set_x(110)
        self.style_bedroom_switch.set_y(0)
        self.style_bedroom_switch.set_border_width(3)
        self.style_bedroom_switch.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        if self.bedroom_switch.state():
            self.style_bedroom_switch.set_bg_color(lv.color_hex(0x11ACCF))
        else :
            self.style_bedroom_switch.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.bedroom_switch_btn = lv.btn(tab_bedroom)
        self.bedroom_switch_btn.add_style(self.style_bedroom_switch, 0)
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        with open('imgs/智能插座.png', 'rb') as f:
            switch_data = f.read()

        self.switch_png = lv.img_dsc_t({
        'data_size': len(switch_data),
        'data': switch_data
        })
        bedroom_switch_img = lv.img(self.bedroom_switch_btn)
        bedroom_switch_img.set_src(self.switch_png)
        bedroom_switch_img.set_zoom(48)
        bedroom_switch_img.set_size(45, 45)
        bedroom_switch_img.set_pos(10, -10)
        bedroom_switch_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # tab2页面
        # 灯按钮
        self.living_light = kwargs['living_light']
        self.style_living_light = lv.style_t()
        self.style_living_light.init()
        self.style_living_light.set_radius(10)
        self.style_living_light.set_size(100, 50)
        self.style_living_light.set_pad_ver(10)
        self.style_living_light.set_pad_hor(15)
        self.style_living_light.set_x(0)
        self.style_living_light.set_y(0)
        self.style_living_light.set_border_width(3)
        self.style_living_light.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        if self.living_light.state():
            self.style_living_light.set_bg_color(lv.color_hex(0xFFDD00))
        else :
            self.style_living_light.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.living_light_btn = lv.btn(tab_livingroom)
        self.living_light_btn.add_style(self.style_living_light, 0)
        # TODO: 按钮点击事件
        self.living_light_btn.add_event_cb(lambda e: self.light_click(e,
            {"light":self.living_light, "name":"LivingLight", "style":self.style_living_light}), lv.EVENT.CLICKED, None)
        
        living_light_img = lv.img(self.living_light_btn)
        living_light_img.set_src(self.light_png)
        living_light_img.set_zoom(48)
        living_light_img.set_size(45, 45)
        living_light_img.set_pos(10, -10)
        living_light_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 风扇按钮
        self.style_fan = lv.style_t()
        self.style_fan.init()
        self.style_fan.set_radius(10)
        self.style_fan.set_size(100, 50)
        self.style_fan.set_pad_ver(10)
        self.style_fan.set_pad_hor(15)
        self.style_fan.set_x(110)
        self.style_fan.set_y(0)
        self.style_fan.set_border_width(3)
        self.style_fan.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        # TODO:背景颜色
        
        self.fan_btn = lv.btn(tab_livingroom)
        self.fan_btn.add_style(self.style_fan, 0)
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        with open('imgs/风扇.png', 'rb') as f:
            fan_data = f.read()

        self.fan_png = lv.img_dsc_t({
        'data_size': len(fan_data),
        'data': fan_data
        })
        
        fan_img = lv.img(self.fan_btn)
        fan_img.set_src(self.fan_png)
        fan_img.set_zoom(48)
        fan_img.set_size(45, 45)
        fan_img.set_pos(10, -10)
        fan_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 温度按钮
        self.style_temperature = lv.style_t()
        self.style_temperature.init()
        self.style_temperature.set_radius(10)
        self.style_temperature.set_size(100, 50)
        self.style_temperature.set_pad_ver(10)
        self.style_temperature.set_pad_hor(15)
        self.style_temperature.set_x(0)
        self.style_temperature.set_y(70)
        self.style_temperature.set_border_width(3)
        self.style_temperature.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        self.style_temperature.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.temperature_btn = lv.btn(tab_livingroom)
        self.temperature_btn.add_style(self.style_temperature, 0)
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        with open('imgs/温度.png', 'rb') as f:
            temperature_data = f.read()

        self.temperature_png = lv.img_dsc_t({
        'data_size': len(temperature_data),
        'data': temperature_data
        })
        
        temperature_img = lv.img(self.temperature_btn)
        temperature_img.set_src(self.temperature_png)
        temperature_img.set_zoom(48)
        temperature_img.set_size(45, 45)
        temperature_img.set_pos(10, -10)
        temperature_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 湿度按钮
        self.style_humidity = lv.style_t()
        self.style_humidity.init()
        self.style_humidity.set_radius(10)
        self.style_humidity.set_size(100, 50)
        self.style_humidity.set_pad_ver(10)
        self.style_humidity.set_pad_hor(15)
        self.style_humidity.set_x(110)
        self.style_humidity.set_y(70)
        self.style_humidity.set_border_width(3)
        self.style_humidity.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        self.style_humidity.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.humidity_btn = lv.btn(tab_livingroom)
        self.humidity_btn.add_style(self.style_humidity, 0)
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        with open('imgs/湿度.png', 'rb') as f:
            humidity_data = f.read()

        self.humidity_png = lv.img_dsc_t({
        'data_size': len(humidity_data),
        'data': humidity_data
        })
        
        humidity_img = lv.img(self.humidity_btn)
        humidity_img.set_src(self.humidity_png)
        humidity_img.set_zoom(48)
        humidity_img.set_size(45, 45)
        humidity_img.set_pos(10, -10)
        humidity_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 窗户按钮
        self.style_window = lv.style_t()
        self.style_window.init()
        self.style_window.set_radius(10)
        self.style_window.set_size(100, 50)
        self.style_window.set_pad_ver(10)
        self.style_window.set_pad_hor(15)
        self.style_window.set_x(0)
        self.style_window.set_y(140)
        self.style_window.set_border_width(3)
        self.style_window.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        self.style_window.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.window_btn = lv.btn(tab_livingroom)
        self.window_btn.add_style(self.style_window, 0)
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        with open('imgs/窗户.png', 'rb') as f:
            window_data = f.read()

        self.window_png = lv.img_dsc_t({
        'data_size': len(window_data),
        'data': window_data
        })
        
        window_img = lv.img(self.window_btn)
        window_img.set_src(self.window_png)
        window_img.set_zoom(48)
        window_img.set_size(45, 45)
        window_img.set_pos(10, -10)
        window_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # 窗帘按钮
        self.style_curtain = lv.style_t()
        self.style_curtain.init()
        self.style_curtain.set_radius(10)
        self.style_curtain.set_size(100, 50)
        self.style_curtain.set_pad_ver(10)
        self.style_curtain.set_pad_hor(15)
        self.style_curtain.set_x(110)
        self.style_curtain.set_y(140)
        self.style_curtain.set_border_width(3)
        self.style_curtain.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        self.style_curtain.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.curtain_btn = lv.btn(tab_livingroom)
        self.curtain_btn.add_style(self.style_curtain, 0)
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
        with open('imgs/窗帘.png', 'rb') as f:
            curtain_data = f.read()

        self.curtain_png = lv.img_dsc_t({
        'data_size': len(curtain_data),
        'data': curtain_data
        })
        
        curtain_img = lv.img(self.curtain_btn)
        curtain_img.set_src(self.curtain_png)
        curtain_img.set_zoom(48)
        curtain_img.set_size(45, 45)
        curtain_img.set_pos(10, -10)
        curtain_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        # tab3页面
        # 灯按钮
        self.kitchen_light = kwargs['kitchen_light']
        self.style_kitchen_light = lv.style_t()
        self.style_kitchen_light.init()
        self.style_kitchen_light.set_radius(10)
        self.style_kitchen_light.set_size(100, 50)
        self.style_kitchen_light.set_pad_ver(10)
        self.style_kitchen_light.set_pad_hor(15)
        self.style_kitchen_light.set_x(0)
        self.style_kitchen_light.set_y(0)
        self.style_kitchen_light.set_border_width(3)
        self.style_kitchen_light.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        if self.kitchen_light.state():
            self.style_kitchen_light.set_bg_color(lv.color_hex(0xFFDD00))
        else :
            self.style_kitchen_light.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.kitchen_light_btn = lv.btn(tab_kitchen)
        self.kitchen_light_btn.add_style(self.style_kitchen_light, 0)
        # TODO: 按钮点击事件
        self.kitchen_light_btn.add_event_cb(lambda e: self.light_click(e,                                                                       
            {"light":self.kitchen_light, "name":"KitchenLight", "style":self.style_kitchen_light}), lv.EVENT.CLICKED, None)
        
        kitchen_light_img = lv.img(self.kitchen_light_btn)
        kitchen_light_img.set_src(self.light_png)
        kitchen_light_img.set_zoom(48)
        kitchen_light_img.set_size(45, 45)
        kitchen_light_img.set_pos(10, -10)
        kitchen_light_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        
    def light_click(self, event, data=None):
        """灯类点击事件"""
        self.light_scr = lv.obj()
        lv.scr_load(self.light_scr)
        light_page = LightPage(self.light_scr, data['light'], self.light_png, data['name'])
        light_page.back_btn.add_event_cb(lambda e:self.back_home_light(e, data['style'], data['light']),lv.EVENT.CLICKED, None)
        
    def back_home_light(self, e, style, light):
        if light.state():
            style.set_bg_color(lv.color_hex(0xFFDD00))
        else:
            style.set_bg_color(lv.color_hex(0xDCDCDC))
        lv.scr_load(self.scr)
        