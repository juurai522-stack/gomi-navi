import csv, json, re
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
ENA_PDF = Path('/mnt/data/gomihyakka2025.pdf')
NAKA_PDF = Path('/mnt/data/nakatsugawa_guidebook.pdf')

ENA_SOURCE_URL = 'https://www.city.ena.lg.jp/material/files/group/25/gomihyakka2025.pdf'
ENA_PAGE_URL = 'https://www.city.ena.lg.jp/soshikiichiran/suidokankyobu/kankyoka/1/3/2/1741.html'
NAKA_SOURCE_URL = 'https://www.city.nakatsugawa.lg.jp/material/files/group/56/guidebook1.pdf'
NAKA_PAGE_URL = 'https://www.city.nakatsugawa.lg.jp/soshikikarasagasu/kankyocenter/1/1/gomi/7762.html'


def clean(s):
    if s is None:
        return ''
    s = str(s).replace('\u3000',' ').replace('\n',' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def extract_ena():
    allowed = {'可燃ごみ','不燃ごみ','粗大ごみ','回収不可','資源ごみ','処理困難ごみ','家電リサイクル','PCリサイクル'}
    out=[]
    with pdfplumber.open(ENA_PDF) as pdf:
        # 品目50音順: PDF index 25-40 (printed pages 25-40)
        for pno in range(25, 41):
            page = pdf.pages[pno]
            for table in page.extract_tables() or []:
                for row in table:
                    if not row or len(row) < 4:
                        continue
                    name = clean(row[1]); cat = clean(row[2]); notes = clean(row[3])
                    if not name or cat not in allowed or name in {'品 目','品目'}:
                        continue
                    out.append({
                        'id': f'ena-{len(out)+1}',
                        'city': 'ena', 'city_name': '恵那市',
                        'name': name, 'category': cat, 'instructions': notes,
                        'large_sticker': '',
                        'source_title': '恵那市ごみ百科事典（令和7年4月1日現在）',
                        'source_url': ENA_SOURCE_URL,
                        'source_page': pno + 1,
                        'official_page_url': ENA_PAGE_URL,
                        'official_page_updated': '2026-08-07',
                        'manual_date': '2025-04-01',
                        'verified_at': '2026-08-13',
                        'eco_plaza_hint': 'エコプラザ' in notes,
                    })
    return out


def extract_naka():
    allowed = {'燃えるごみ','燃えないごみ','大型ごみ','引取りできないごみ','硬質ごみ','資源となるごみ','有害ごみ','リサイクル対象品','資源ごみ','リサイクル法対象品','火葬'}
    out=[]
    with pdfplumber.open(NAKA_PDF) as pdf:
        # 品目一覧はPDF index 12-25に掲載
        for pno in range(12, 26):
            page = pdf.pages[pno]
            for table in page.extract_tables() or []:
                for row in table:
                    if not row or len(row) < 5:
                        continue
                    name = clean(row[1]); cat = clean(row[2]); notes = clean(row[3]); sticker = clean(row[4])
                    if not name or cat not in allowed or name in {'品 名','品名'}:
                        continue
                    out.append({
                        'id': f'naka-{len(out)+1}',
                        'city': 'nakatsugawa', 'city_name': '中津川市',
                        'name': name, 'category': cat, 'instructions': notes,
                        'large_sticker': sticker,
                        'source_title': '中津川市 ごみの出し方ガイドブック',
                        'source_url': NAKA_SOURCE_URL,
                        'source_page': pno + 1,
                        'official_page_url': NAKA_PAGE_URL,
                        'official_page_updated': '2026-04-17',
                        'manual_date': '',
                        'verified_at': '2026-08-13',
                        'eco_plaza_hint': False,
                    })
    # de-duplicate identical (name,category,instructions)
    seen=set(); ded=[]
    for r in out:
        k=(r['name'],r['category'],r['instructions'])
        if k in seen: continue
        seen.add(k); ded.append(r)
    for i,r in enumerate(ded,1): r['id']=f'naka-{i}'
    return ded

facilities = [
  {
    'id':'ena-eco-plaza','city':'ena','city_name':'恵那市','name':'ふれあいエコプラザ',
    'address':'岐阜県恵那市長島町正家1015-3','phone':'0573-25-1515','type':'資源回収・リユース',
    'hours':'9:00〜16:00（日・月・年末年始休館）※屋外回収場は対象品目のみ24時間・年中無休',
    'accepted':['新聞','チラシ','雑誌','雑がみ','段ボール','米袋','飲料紙パック','古着','羽毛製品','アルミ缶','スチール缶','金属類','情報家電','電線類','CD付オーディオ','白びん','茶びん','その他びん','ペットボトル','ペットボトルキャップ','発泡トレー','発泡スチロール','CD','DVD','コンタクトレンズケース','歯ブラシ','キッチンスポンジ','自動車用バッテリー','インクカートリッジ','廃食用油','乾電池','リチウムイオン電池','蛍光管'],
    'source_url':'https://www.city.ena.lg.jp/soshikiichiran/suidokankyobu/kankyoka/1/3/5/1761.html','source_updated':'2026-05-01','verified_at':'2026-08-13'
  },
  {
    'id':'ena-eco-center','city':'ena','city_name':'恵那市','name':'エコセンター恵那',
    'address':'岐阜県恵那市長島町久須見1013-1','phone':'0573-26-2163','type':'ごみ処理施設',
    'hours':'最新の受付時間は公式ページで確認してください。','accepted':['家庭ごみ直接搬入','粗大ごみ','家電4品目（所定手続き後）'],
    'source_url':'https://www.city.ena.lg.jp/soshikiichiran/suidokankyobu/kankyoka/1/3/2/1741.html','source_updated':'2026-08-07','verified_at':'2026-08-13'
  },
  {
    'id':'ena-aozora','city':'ena','city_name':'恵那市','name':'恵南クリーンセンターあおぞら',
    'address':'岐阜県恵那市明智町吉良見245-1','phone':'0573-26-6866','type':'ごみ処理施設',
    'hours':'最新の受付時間は公式ページで確認してください。','accepted':['家庭ごみ直接搬入','粗大ごみ','家電4品目（所定手続き後）'],
    'source_url':'https://www.city.ena.lg.jp/soshikiichiran/suidokankyobu/kankyoka/1/3/2/1746.html','source_updated':'2025-05-08','verified_at':'2026-08-13'
  },
  {
    'id':'naka-env','city':'nakatsugawa','city_name':'中津川市','name':'中津川市環境センター',
    'address':'岐阜県中津川市駒場2261-6','phone':'0573-62-0085','type':'ごみ処理施設',
    'hours':'燃える・燃えない・大型：平日8:45〜16:30、第2・第4日曜8:45〜12:00 / 13:00〜16:30。資源・有害・硬質は場内リサイクルセンターへ。',
    'accepted':['燃えるごみ','燃えないごみ','大型ごみ','資源ごみ','有害ごみ','硬質ごみ'],
    'source_url':'https://www.city.nakatsugawa.lg.jp/soshikikarasagasu/kankyocenter/1/1/667.html','source_updated':'2026-06-10','verified_at':'2026-08-13'
  },
  {
    'id':'naka-recycle','city':'nakatsugawa','city_name':'中津川市','name':'中津川市リサイクルセンター',
    'address':'岐阜県中津川市駒場2261-6（環境センター場内）','phone':'0573-62-0085','type':'資源回収',
    'hours':'月〜金8:30〜17:15（祝日等除く）、土日祝9:00〜17:00（年末年始除く）',
    'accepted':['資源ごみ','有害ごみ','硬質ごみ','びん','缶','ペットボトル','新聞','雑誌','段ボール','雑がみ','廃食用油','衣類・布類','牛乳パック','食品トレー','発泡スチロール'],
    'source_url':'https://www.city.nakatsugawa.lg.jp/soshikikarasagasu/kankyocenter/1/1/667.html','source_updated':'2026-06-10','verified_at':'2026-08-13'
  },
]

# 中津川市公式リサイクルボックス（住所は利用者が地図リンクで検索できるよう施設名を保持）
for i,name in enumerate(['中津川市役所','坂本事務所','阿木事務所','神坂事務所','中央公民館','サンライフ中津川','桃山公園駐車場','付知総合事務所','蛭川総合事務所','加子母総合事務所','馬籠消防器具庫横'],1):
    facilities.append({
      'id':f'naka-box-{i}','city':'nakatsugawa','city_name':'中津川市','name':name+' リサイクルボックス',
      'address':name+'（中津川市）','phone':'','type':'リサイクルボックス',
      'hours':'施設・地区により異なります。','accepted':['新聞','雑誌','段ボール','雑がみ','スチロールトレイ','牛乳パック'],
      'source_url':'https://www.city.nakatsugawa.lg.jp/soshikikarasagasu/kankyocenter/1/1/667.html','source_updated':'2026-06-10','verified_at':'2026-08-13'
    })

metadata = {
  'generated_at':'2026-08-13',
  'ena': {
    'official_page_updated':'2026-08-07',
    'manual_as_of':'2025-04-01',
    'manual_title':'恵那市ごみ百科事典',
    'official_page_url':ENA_PAGE_URL,
    'manual_url':ENA_SOURCE_URL,
  },
  'nakatsugawa': {
    'official_page_updated':'2026-04-17',
    'guide_title':'中津川市 ごみの出し方ガイドブック',
    'official_page_url':NAKA_PAGE_URL,
    'guide_url':NAKA_SOURCE_URL,
    'leaflet':'令和8年度ごみの出し方リーフレット',
  }
}

ena = extract_ena(); naka = extract_naka(); all_items=ena+naka
DATA.mkdir(exist_ok=True)
with open(DATA/'items.json','w',encoding='utf-8') as f: json.dump(all_items,f,ensure_ascii=False,indent=2)
with open(DATA/'facilities.json','w',encoding='utf-8') as f: json.dump(facilities,f,ensure_ascii=False,indent=2)
with open(DATA/'metadata.json','w',encoding='utf-8') as f: json.dump(metadata,f,ensure_ascii=False,indent=2)
for fn, rows in [('ena_items.csv',ena),('nakatsugawa_items.csv',naka),('all_items.csv',all_items)]:
    with open(DATA/fn,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
print(f'Ena items: {len(ena)}')
print(f'Nakatsugawa items: {len(naka)}')
print(f'Total: {len(all_items)}')
print(f'Facilities: {len(facilities)}')
