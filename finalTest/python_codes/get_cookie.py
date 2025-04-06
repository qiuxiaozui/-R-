import random
import time
from urllib.parse import quote

def gen_timestamp(offset=0, millisecond=False):
    #Unix时间戳
    ts = time.time() + offset
    if millisecond:
        return f"{int(ts * 1000)}"
    return f"{int(ts)}.{str(ts).split('.')[1][:6]}"

# #生成未来1小时的时间戳（测试）
# future_ts = gen_timestamp(offset=3600, millisecond=False)
def build_sinaglobal(ip=None):
    if not ip:
    # 模拟IP随机生成
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
    return f"{ip}_{gen_timestamp(millisecond=True)}"

def build_ulv(ip, initial_ts):
    #维护用户会话状态
    last_activity = gen_timestamp(millisecond=True)
    return f"{last_activity}:6:6:6:{ip}_{initial_ts}:{initial_ts}"

def build_sfa_version(version="8.10.0", days=365):
    #生成版本过期时间（UTC时间+URL编码）
    expire_time = time.time() + days*86400
    utc_str = time.strftime("%Y-%m-%d %H:%M", time.gmtime(expire_time))
    return quote(utc_str.replace(" ", "%20")).replace(":", "%3A")
class CookieGenerator:
    def __init__(self, stock_code, stock_name):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.client_ip = self._gen_ip()
        self.initial_ts = gen_timestamp(millisecond=True)

    def _gen_ip(self):
        return ".".join(str(random.randint(100, 200)) for _ in range(4))

    def generate(self):
        return {
            'UOR': 'cn.bing.com,finance.sina.com.cn,',
            'SFA_version8.10.0': build_sfa_version(),
            'SINAGLOBAL': build_sinaglobal(self.client_ip),
            'SFA_version8.10.0_click': '1',
            'U_TRS1': f'00000090.e3ef176b8.{random.randint(1000000, 9999999)}.b395c16a',# 防固定值检测,好像没用
            'FIN_ALL_VISITED': self.stock_code,
            'FINA_V_S_2': self.stock_code,
            'SR_SEL': '1_511',
            'Apache': f"{self.client_ip}_{gen_timestamp(millisecond=True)}",
            'close_rightAppMsg': '1',
            'rotatecount': str(random.randint(1, 5)),  # 防固定值检测,好像没用
            'ULV': build_ulv(self.client_ip, self.initial_ts),
        }

    def generate_cookie(self):
        return {
            'UOR': 'cn.bing.com,finance.sina.com.cn,',
            'SINAGLOBAL': build_sinaglobal(self.client_ip),
            'U_TRS1': f'00000090.e3ef176b8.{random.randint(1000000, 9999999)}.b395c16a',
            'Apache': f"{self.client_ip}_{gen_timestamp(millisecond=True)}",
            'U_TRS2': '00000090.fbaf1d843.67f0cfc2.6c99dce1',
            'rotatecount': str(random.randint(1, 5)),
            'ULV': build_ulv(self.client_ip, self.initial_ts),
            'INGRESSCOOKIE': build_sinaglobal(self.client_ip),
            'gubaBarVisits': 'a%3A1%3A%7Bi%3A0%3Bs%3A5%3A%2210199%22%3B%7D',
            'hqEtagMode': '1',
            'brvt': f'{self.stock_code}_{quote(self.stock_name)}',  # 修复编码问题
        }