from machine import Pin, I2C
import dht

import pcf8574

from const import IO_SCL, IO_SDA

# IO扩展模块初始化
i2c = I2C(0, scl=Pin(IO_SCL), sda=Pin(IO_SDA))
pcf = pcf8574.PCF8574(i2c)
for i in range(8):
    pcf.pin(i, 0)
    
class TemperatureHumidity():
    """温湿度传感器"""
    def __init__(self, tah):
        try:
            self.th = dht.DHT11(Pin(tah))
            self.th.measure() # 第一次执行异常，第二次正常
        except OSError as e:
            print('温湿度工作异常')
    
    def get_tem_hum(self):
        try:
            self.th.measure()
            return {'temperature':self.th.temperature(), 'humidity':self.th.humidity()}
        except OSError as e:
            print('温湿度工作异常')

class Light():
    """开关类设备"""
    def __init__(self, power):
        self.power = power
    
    def on(self):
        pcf.pin(self.power, 1)
        
    def off(self):
        pcf.pin(self.power, 0)
        
    def state(self):
        return pcf.pin(self.power)
    