import lvgl as lv

class LightPage():
    def __init__(self, scr, light, png, name=""):
        self.scr = scr
        self.light = light
        self.light_png = png
        
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
        head_label.set_text(name)
        
        # 悬浮返回按钮
        self.back_btn = lv.btn(self.scr)
        self.back_btn.set_size(40, 40)
        self.back_btn.add_flag(lv.obj.FLAG.FLOATING)
        self.back_btn.align(lv.ALIGN.BOTTOM_RIGHT, -10, -270)
        self.back_btn.set_style_bg_img_src(lv.SYMBOL.NEW_LINE, 0)
        self.back_btn.set_style_text_font(lv.theme_get_font_large(self.back_btn), 0)
        
        # 灯光按钮
        self.style_light = lv.style_t()
        self.style_light.init()
        self.style_light.set_radius(10)
        self.style_light.set_size(100, 100)
        self.style_light.set_pad_ver(15)
        self.style_light.set_pad_hor(-5)
        self.style_light.set_x(70)
        self.style_light.set_y(100)
        self.style_light.set_border_width(3)
        self.style_light.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        if self.light.state():
            self.style_light.set_bg_color(lv.color_hex(0xFFDD00))
        else :
            self.style_light.set_bg_color(lv.color_hex(0xDCDCDC))
        
        self.light_btn = lv.btn(self.scr)
        self.light_btn.add_style(self.style_light, 0)
        # 按钮点击事件
        self.light_btn.add_event_cb(self.light_click,lv.EVENT.CLICKED, None)
        
        light_img = lv.img(self.light_btn)
        light_img.set_src(self.light_png)
        light_img.set_zoom(96)
        light_img.set_size(80, 80)
        light_img.set_pos(10, -10)
        light_img.set_size_mode(lv.img.SIZE_MODE.REAL)
        
        self.style_time_btn = lv.style_t()
        self.style_time_btn.init()
        self.style_time_btn.set_radius(10)
        self.style_time_btn.set_size(200, 50)
        self.style_time_btn.set_pad_ver(10)
        self.style_time_btn.set_pad_hor(15)
        self.style_time_btn.set_x(20)
        self.style_time_btn.set_y(250)
        self.style_time_btn.set_border_width(3)
        self.style_time_btn.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.time_btn = lv.btn(self.scr)
        self.time_btn.add_style(self.style_time_btn, 0)
        self.time_label=lv.label(self.time_btn)
        self.time_label.set_text("Timer")
        self.time_label.center()
        # TODO: 按钮点击事件
        #self.bedroom_light_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
    def light_click(self, e):
        """开启关闭灯光"""
        print(self.light.state())
        if self.light.state():
            self.light.off()
            self.style_light.set_bg_color(lv.color_hex(0xDCDCDC))
        else:
            self.light.on()
            self.style_light.set_bg_color(lv.color_hex(0xFFDD00))
        
        