#!/usr/bin/env python3
import re, urllib.request
SOURCES={
 '恵那市':'https://www.city.ena.lg.jp/soshikiichiran/suidokankyobu/kankyoka/1/3/2/1741.html',
 '中津川市':'https://www.city.nakatsugawa.lg.jp/soshikikarasagasu/kankyocenter/1/1/gomi/7762.html',
 '中津川市・直接搬入':'https://www.city.nakatsugawa.lg.jp/soshikikarasagasu/kankyocenter/1/1/667.html',
 '恵那市・ふれあいエコプラザ':'https://www.city.ena.lg.jp/soshikiichiran/suidokankyobu/kankyoka/1/3/5/1761.html',
}
for name,url in SOURCES.items():
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 GomiNaviLocalChecker/1.0'})
        text=urllib.request.urlopen(req,timeout=15).read().decode('utf-8','ignore')
        text=re.sub(r'<[^>]+>',' ',text)
        m=re.search(r'更新日[：:\s]*([0-9]{4})年\s*([0-9]{1,2})月\s*([0-9]{1,2})日',text)
        date=f'{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}' if m else '更新日を自動取得できませんでした'
        print(f'{name}: {date}\n  {url}')
    except Exception as e:
        print(f'{name}: 確認失敗 ({e})\n  {url}')
