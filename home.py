import lvgl as lv

class HomePage():
    def __init__(self, scr):
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
    HomePage(scr)