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
# WEATHER_MAP = { '晴': 'lib/weather_1晴.png',
#                 cloudy: 'lib/weather_2多云.png' for cloudy in CLOUDY,
#                 '阴': 'lib/weather_3阴.png',
#                 windy: 'lib/weather_23风.png' for windy in WINDY,
#                 tornado: 'lib/weather_24.png' for tornado in TORNADO,
#                 unknown: 'lib/weather_26.png' for unknown in UNKNOWN
#     }
WEATHER_MAP = { '晴': 'imgs/weather_1晴.png',
                '阴': 'imgs/weather_3阴.png'
    }
WEATHER_MAP.update(dict.fromkeys(CLOUDY, 'imgs/weather_2多云.png' ))
WEATHER_MAP.update(dict.fromkeys(WINDY, 'imgs/weather_23风.png'))
WEATHER_MAP.update(dict.fromkeys(TORNADO, 'imgs/weather_24龙卷风.png'))
WEATHER_MAP.update(dict.fromkeys(UNKNOWN, 'imgs/weather_26未知.png'))