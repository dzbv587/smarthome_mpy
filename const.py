# 巴法云
CLIENT_ID = 'c6bf4f9e4bae40c598815ef1e543d616'
SERVER_IP = 'bemfa.com'
PORT = 9501
BEDROOM_LIGHT_TOPIC = 'light002'

# 屏幕定义
WIDTH = 240
HEIGHT = 320
CS = 18
RST = -1
DC = 17
MOSI = 16
CLK = 15
LED = -1
MISO = 14
T_CS = 13
POWER = -1

WEEK_MAP = {'0':'Mon',
            '1':'Tue',
            '2':'Wed',
            '3':'Thu',
            '4':'Fri',
            '5':'Sat',
            '6':'Sun'
    }

# weather
CITY = '230103'
KEY = '7cd068dc45ffcc5b72e374d98c3e77f4'
WEATHER_API = 'https://restapi.amap.com/v3/weather/weatherInfo?key={0}&city={1}'.format(KEY, CITY)
CLOUDY = {'少云', '晴间多云', '多云'}
WINDY = {'有风', '平静', '微风', '和风', '清风', '强风', '劲风', '疾风', '大风'}
TORNADO = {'烈风', '风暴', '狂爆风', '飓风', '热带风暴'}
UNKNOWN = {'未知', '冷', '热'}
WEATHER_MAP = { '晴': 'imgs/weather_1晴.png',
                '阴': 'imgs/weather_3阴.png'
    }
WEATHER_MAP.update(dict.fromkeys(CLOUDY, 'imgs/weather_2多云.png' ))
WEATHER_MAP.update(dict.fromkeys(WINDY, 'imgs/weather_23风.png'))
WEATHER_MAP.update(dict.fromkeys(TORNADO, 'imgs/weather_24龙卷风.png'))
WEATHER_MAP.update(dict.fromkeys(UNKNOWN, 'imgs/weather_26未知.png'))

# IO扩展引脚
IO_SCL = 3
IO_SDA = 2

# 卧室
# 灯引脚
BEDROOM_LIGHT = 0
# 插座引脚
BEDROOM_SWITCH = 1

# 客厅
# 光敏传感器
LIVING_LIGHT_SEN = 2
# 灯引脚
LIVING_LIGHT = 1
# 风扇引脚
FAN = 2
# 温湿度传感器引脚
TAH = 1

# 窗帘电机引脚
CURTAIN = 3 
# 窗户舵机引脚
WINDOW = 4
# 雨水传感器引脚
RAIN_SEN = 5
# 厨房
# 灯引脚
KITCHEN_LIGHT = 2