import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fac=json.load(open(ROOT/'data/facilities.json',encoding='utf-8'))
# upgrade existing records
for f in fac:
    f.setdefault('operator','自治体')
    f.setdefault('source_kind','自治体公式')
    f.setdefault('confidence','official')
    f.setdefault('fee','品目・持込方法により異なります。公式情報をご確認ください。')
    f.setdefault('notes','')
    f.setdefault('hours_mode','text')

baro_items=['ダンボール','段ボール','牛乳パック','食品トレー（白トレーのみ）','ペットボトル','アルミ缶','スチール缶','アルミつき紙パック','新聞','チラシ','雑誌','古紙']
baro=[
('ena','baro-ena','スーパーマーケットバロー恵那店','岐阜県恵那市大井町180-1','0573-25-5001','月〜金 10:00〜20:00／土日 9:30〜20:00','https://stores.valor.jp/detail/1/'),
('ena','baro-shoge','スーパーマーケットバロー正家店','岐阜県恵那市長島町正家3丁目8-64-3','0573-20-3455','月〜金 10:00〜20:00／土日 9:30〜20:00','https://stores.valor.jp/detail/285/'),
('ena','baro-iwamura','スーパーマーケットバロー岩村店','岐阜県恵那市岩村町飯羽間字松割2294-1','0573-43-0300','月〜土 10:00〜20:00／日 9:30〜20:00','https://stores.valor.jp/detail/68/'),
('ena','baro-akechi','スーパーマーケットバロー明智店','岐阜県恵那市明智町石坪469-2','0573-54-3111','月・水〜土 10:00〜19:00／日 9:30〜19:00／火曜定休（祝日は営業の場合あり）','https://stores.valor.jp/detail/2/'),
('nakatsugawa','baro-naka-east','スーパーマーケットバロー中津川東店','岐阜県中津川市中津川字上金1155','0573-62-2511','月〜金 10:00〜20:00／土日 9:30〜20:00','https://stores.valor.jp/detail/98/'),
('nakatsugawa','baro-naegi','スーパーマーケットバロー苗木店','岐阜県中津川市苗木字柳ノ木4892番地','0573-62-0633','月〜金 10:00〜20:00／土日 9:30〜20:00','https://stores.valor.jp/detail/55/'),
('nakatsugawa','baro-lubit','スーパーマーケットバロールビットタウン店','岐阜県中津川市淀川町3-8','0573-62-7011','月〜日 10:00〜20:00（臨時変更あり）','https://stores.valor.jp/detail/277/'),
('nakatsugawa','baro-sakamoto','スーパーマーケットバロー坂本店','岐阜県中津川市茄子川2223-1','0573-78-0030','月〜金 10:00〜20:00／土日 9:30〜20:00','https://stores.valor.jp/detail/186/'),
('nakatsugawa','baro-komaba','スーパーマーケットバロー中津川駒場店','岐阜県中津川市手賀野132-5','0573-64-8639','月〜金 10:00〜20:00／土日 9:30〜20:00','https://stores.valor.jp/detail/310/'),
]
for c,id_,name,address,phone,hours,url in baro:
    fac.append(dict(id=id_,city=c,city_name='恵那市' if c=='ena' else '中津川市',name=name,address=address,phone=phone,type='民間店頭回収',operator='バロー',hours=hours,hours_mode='store',accepted=baro_items,fee='無料（店頭回収。回収条件は店舗表示に従ってください）',notes='洗浄・分別など回収条件があります。店舗の回収ボックス表示を優先してください。',source_url=url,source_updated='2026-08-13',verified_at='2026-08-13',source_kind='企業公式店舗ページ',confidence='official'))

# DCM / Eco Family
fac.append(dict(id='dcm-ena-ink',city='ena',city_name='恵那市',name='DCM21恵那店',address='岐阜県恵那市長島町正家3丁目8-119',phone='',type='民間店頭回収',operator='DCM',hours='店舗営業時間内（最新は公式店舗ページで確認）',hours_mode='store',accepted=['インクカートリッジ'],fee='無料',notes='公式店舗ページでインクカートリッジ回収（無料）を確認。',source_url='https://www.dcm-hc.co.jp/shop/detail/01_0324.html',source_updated='2026-08-13',verified_at='2026-08-13',source_kind='企業公式店舗ページ',confidence='official'))
fac.append(dict(id='ecofamily-dcm-naka',city='nakatsugawa',city_name='中津川市',name='エコファミリー DCM中津川店',address='岐阜県中津川市手賀野354-1',phone='0800-200-1063',type='民間資源回収',operator='エコファミリー',hours='9:30〜19:00',hours_mode='daily',accepted=['新聞','チラシ','雑誌','雑がみ','段ボール','牛乳パック','古着','フライパン','アルミ缶'],fee='無料',notes='DCM中津川店駐車場内。公式サイトの現行BOX一覧を優先。',source_url='https://ecofamily.jp/1224/',source_updated='2026-08-13',verified_at='2026-08-13',source_kind='事業者公式',confidence='official'))

# Tokai Shigen stations
TS_URL_ENA='https://www.tokaishigen.com/recycling-station/location/ena/'
TS_URL_NAKA='https://www.tokaishigen.com/recycling-station/location/nakatsugawa/'
ts_items=['新聞','チラシ','雑誌','雑がみ','段ボール','古着','アルミ缶']
ena_ts=[
('tokai-ena-nakano','東海資源 長島中野店','岐阜県恵那市長島町中野大隅屋敷205-4',True),
('tokai-ena-takenami','東海資源 大井町武並神社前店','岐阜県恵那市長島町正家1057-1',True),
('tokai-ena-kusumi','東海資源 恵那久須見店','岐阜県恵那市長島町久須見1083-21',True),
('tokai-ena-iwamura','東海資源 岩村店','岐阜県恵那市岩村町飯羽間2345-4（ファミリーマート恵那岩村店駐車場）',False),
]
for id_,name,address,al in ena_ts:
    accepted=ts_items if al else [x for x in ts_items if x!='アルミ缶']
    fac.append(dict(id=id_,city='ena',city_name='恵那市',name=name,address=address,phone='0573-68-5733',type='民間24時間回収',operator='東海資源',hours='24時間',hours_mode='24h',accepted=accepted,fee='無料。対象資源はポイント還元制度あり（条件は公式サイト確認）',notes='無人回収ステーション。',source_url=TS_URL_ENA,source_updated='2026-08-13',verified_at='2026-08-13',source_kind='事業者公式',confidence='official'))

naka_ts=[
('tokai-naka-inter','東海資源 中津川インター店','岐阜県中津川市千旦林222-1',True),
('tokai-naka-tegano','東海資源 中津川手賀野店','岐阜県中津川市手賀野西沼182-6',True),
('tokai-naka-center','東海資源 東海リサイクルセンター店','岐阜県中津川市千旦林2644-1',True),
('tokai-naka-hinode','東海資源 日の出町店','岐阜県中津川市日の出町1470-1',True),
('tokai-naka-nasukawa','東海資源 坂本茄子川店','岐阜県中津川市茄子川1389-5',True),
('tokai-naka-sakamoto','東海資源 中津川坂本店','岐阜県中津川市茄子川筑田2135',True),
('tokai-naka-enakyo','東海資源 坂本恵那峡店','岐阜県中津川市茄子川151-40',True),
('tokai-naka-naegi-motoki','東海資源 苗木元起店','岐阜県中津川市苗木1826-1（ひだ路元起駐車場内）',True),
('tokai-naka-naegi257','東海資源 257号苗木店','岐阜県中津川市苗木並松4827-906',True),
('tokai-naka-shimono','東海資源 福岡下野店','岐阜県中津川市下野大湫438-69',False),
('tokai-naka-tase','東海資源 福岡田瀬店','岐阜県中津川市田瀬995-1',False),
('tokai-naka-tsukechi','東海資源 中津川付知店','岐阜県中津川市付知町6847-13',True),
('tokai-naka-kashimo','東海資源 中津川加子母店','岐阜県中津川市加子母3366-1',True),
('tokai-naka-ochiai','東海資源 落合店','岐阜県中津川市落合字屋下735-3',True),
('tokai-naka-sakashita','東海資源 中津川坂下店','岐阜県中津川市坂下435-28（ショッピングセンターサラ駐車場内）',False),
]
for id_,name,address,al in naka_ts:
    accepted=ts_items if al else [x for x in ts_items if x!='アルミ缶']
    fac.append(dict(id=id_,city='nakatsugawa',city_name='中津川市',name=name,address=address,phone='0573-68-5733',type='民間24時間回収',operator='東海資源',hours='24時間',hours_mode='24h',accepted=accepted,fee='無料。対象資源はポイント還元制度あり（条件は公式サイト確認）',notes='無人回収ステーション。',source_url=TS_URL_NAKA,source_updated='2026-08-13',verified_at='2026-08-13',source_kind='事業者公式',confidence='official'))

# de-dupe by id
out=[]; seen=set()
for f in fac:
    if f['id'] in seen: continue
    seen.add(f['id']); out.append(f)
json.dump(out,open(ROOT/'data/facilities.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('facilities',len(out),'ena',sum(x['city']=='ena' for x in out),'naka',sum(x['city']=='nakatsugawa' for x in out))
