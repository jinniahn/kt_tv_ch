'''\
getting TV Channel information for KT IPV.

USES:

from kt_tv_cahnnel import *

channels = get_all_channels()
for ch in channels:
    get_schedule(ch)
'''
import requests
from pyquery import PyQuery as pq
from pprint import pprint
import datetime

__all__ = ['get_all_channels', 'get_schedule']

def get_all_channels():
    '''get all tv channel from kt olleh

    return tuple('ch num', 'ch name')
    '''
    
    req = {'compressed': True,
           'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		       'Accept-Encoding': 'gzip, deflate',
		       'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
		       'Cache-Control': 'no-cache',
		       'Connection': 'keep-alive',
		       'Cookie': None,
		       'Pragma': 'no-cache',
		       'Upgrade-Insecure-Requests': '1',
		       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) '
		       'AppleWebKit/537.36 (KHTML, like Gecko) '
		       'Chrome/62.0.3202.94 Safari/537.36'},
           'url': 'http://tv.kt.com/tv/channel/pChInfo.asp'}

    resp = requests.get(req['url'], headers=req['headers'])
    content = resp.content.decode('euc-kr')

    h = pq(content)
    ret = []
    for t in h("a[name='linkChannel']"):
        x = t.attrib['href'].strip()
        if 'fnSelSchedule' not in x: continue
        x = x.split("'")[1]
        ret.append((int(x), pq(t).text().strip()))

    return ret


def get_schedule(ch, date=None):
    'schedules of channel today'
    # options:
    #   - seldate:20171122
    #   - available date : +7days
    req = {'compressed': True,
           'data': [('ch_type', '1'), ('service_ch_no', ch), ('view_type', '1')],
           'headers': {'Accept': 'text/html, */*; q=0.01',
		       'Accept-Encoding': 'gzip, deflate',
		       'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
		       'Cache-Control': 'no-cache',
		       'Connection': 'keep-alive',
		       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		       'Cookie': None,
		       'Origin': 'http://tv.kt.com',
		       'Pragma': 'no-cache',
		       'Referer': 'http://tv.kt.com/tv/channel/pChInfo.asp',
		       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) '
		       'AppleWebKit/537.36 (KHTML, like Gecko) '
		       'Chrome/62.0.3202.94 Safari/537.36',
		       'X-Requested-With': 'XMLHttpRequest'},
           'url': 'http://tv.kt.com/tv/channel/pSchedule.asp'}

    # add specific date if |date| is existed
    if date:
        if isinstance(date, datetime.date):
            req['data'].append(('seldate', '{:%Y%m%d}'.format(date)))
        else:
            req['data'].append(('seldate', data))
            

    # get web page
    resp = requests.post(req['url'], req['data'], headers=req['headers'])
    content = resp.content.decode('euc-kr')

    # parsing pages
    h = pq(content)
    
    ret = []
    for t in h(".tbl_area > table.tb_schedule > tbody > tr"):
        item = pq(t)
        h, m = tuple(item('td.time'))

        hour = int(pq(h).text())
        mins  = [int(x) for x in pq(m).text().split()]
        programs = [pq(x).text() for x in item('td.program > p')]

        for x in zip(mins, programs):
            min = x[0]
            prog = x[1]
            if prog.startswith('방송중'): 
                prog = prog.split(maxsplit=1)[1]
            ret.append((hour, min, prog))
    return ret


