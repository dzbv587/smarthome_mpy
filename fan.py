import lvgl as lv

class FanPage():
    def __init__(self, scr, fan, png, name=""):
        self.scr = scr
        self.fan = fan
        self.fan_png = png
        
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
        self.style_fan = lv.style_t()
        self.style_fan.init()
        self.style_fan.set_radius(10)
        self.style_fan.set_size(100, 40)
        self.style_fan.set_pad_ver(15)
        self.style_fan.set_pad_hor(-5)
        self.style_fan.set_x(70)
        self.style_fan.set_y(70)
        self.style_fan.set_border_width(3)
        self.style_fan.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.fan_btn = lv.btn(self.scr)
        self.fan_btn.add_style(self.style_fan, 0)
        # 按钮点击事件
        self.fan_btn.add_event_cb(self.on_click,lv.EVENT.CLICKED, None)
        
        self.on_label = lv.label(self.fan_btn)
        self.on_label.set_text('   one')
        
        self.style_fan2 = lv.style_t()
        self.style_fan2.init()
        self.style_fan2.set_radius(10)
        self.style_fan2.set_size(100, 40)
        self.style_fan2.set_pad_ver(15)
        self.style_fan2.set_pad_hor(-5)
        self.style_fan2.set_x(70)
        self.style_fan2.set_y(120)
        self.style_fan2.set_border_width(3)
        self.style_fan2.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.fan2_btn = lv.btn(self.scr)
        self.fan2_btn.add_style(self.style_fan2, 0)
        # 按钮点击事件
        self.fan2_btn.add_event_cb(self.two_click,lv.EVENT.CLICKED, None)
        
        self.two_label = lv.label(self.fan2_btn)
        self.two_label.set_text('   two')
        
        self.style_fan3 = lv.style_t()
        self.style_fan3.init()
        self.style_fan3.set_radius(10)
        self.style_fan3.set_size(100, 40)
        self.style_fan3.set_pad_ver(15)
        self.style_fan3.set_pad_hor(-5)
        self.style_fan3.set_x(70)
        self.style_fan3.set_y(170)
        self.style_fan3.set_border_width(3)
        self.style_fan3.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.fan3_btn = lv.btn(self.scr)
        self.fan3_btn.add_style(self.style_fan3, 0)
        # 按钮点击事件
        self.fan3_btn.add_event_cb(self.three_click,lv.EVENT.CLICKED, None)
        
        self.three_label = lv.label(self.fan3_btn)
        self.three_label.set_text('   three')
        
        self.style_fan5 = lv.style_t()
        self.style_fan5.init()
        self.style_fan5.set_radius(10)
        self.style_fan5.set_size(100, 40)
        self.style_fan5.set_pad_ver(15)
        self.style_fan5.set_pad_hor(-5)
        self.style_fan5.set_x(70)
        self.style_fan5.set_y(220)
        self.style_fan5.set_border_width(3)
        self.style_fan5.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.fan5_btn = lv.btn(self.scr)
        self.fan5_btn.add_style(self.style_fan5, 0)
        # 按钮点击事件
        self.fan5_btn.add_event_cb(self.off_click,lv.EVENT.CLICKED, None)
        
        self.off_label = lv.label(self.fan5_btn)
        self.off_label.set_text('   off')
        
        self.style_time_btn = lv.style_t()
        self.style_time_btn.init()
        self.style_time_btn.set_radius(10)
        self.style_time_btn.set_size(200, 50)
        self.style_time_btn.set_pad_ver(10)
        self.style_time_btn.set_pad_hor(15)
        self.style_time_btn.set_x(20)
        self.style_time_btn.set_y(280)
        self.style_time_btn.set_border_width(3)
        self.style_time_btn.set_border_color(lv.palette_main(lv.PALETTE.GREY))
        
        self.time_btn = lv.btn(self.scr)
        self.time_btn.add_style(self.style_time_btn, 0)
        self.time_label=lv.label(self.time_btn)
        self.time_label.set_text("Timer")
        self.time_label.center()
        # TODO: 按钮点击事件
        #self.bedroom_fan_btn.add_event_cb(self.conn_wifi,lv.EVENT.CLICKED, None)
        
    def on_click(self, e):
        """开启关闭灯光"""
        self.fan.on(1)
        
    def two_click(self, e):
        """开启关闭灯光"""
        self.fan.on(2)
        
    def three_click(self, e):
        """开启关闭灯光"""
        self.fan.on(3)
        
    def four_click(self, e):
        """开启关闭灯光"""
        self.fan.on(4)
            
    def off_click(self, e):
        """开启关闭灯光"""
        self.fan.off()