import pandas as pd
import os

# ── 路径设置 ──────────────────────────────────────────────────────────────
BASE    = os.path.dirname(__file__)
COJADS  = os.path.join(BASE, 'cojads-2026', 'cojads_2026_merged.csv')
GSRJD   = os.path.join(BASE, 'GSR-JD', 'gsr-jd.csv')
OUTPUT  = os.path.join(BASE, 'japanese_dialect_merged.csv')

# ── 映射字典 ──────────────────────────────────────────────────────────────
# GSR-JD dialect (prefecture name) → prefecture_en
pref_name_to_en = {
    'Hokkaido':  '01_Hokkaido', 'Aomori':    '02_Aomori',
    'Iwate':     '03_Iwate',    'Miyagi':     '04_Miyagi',
    'Akita':     '05_Akita',    'Yamagata':   '06_Yamagata',
    'Fukushima': '07_Fukushima','Ibaraki':    '08_Ibaraki',
    'Tochigi':   '09_Tochigi',  'Gunma':      '10_Gunma',
    'Saitama':   '11_Saitama',  'Chiba':      '12_Chiba',
    'Tokyo':     '13_Tokyo',    'Kanagawa':   '14_Kanagawa',
    'Niigata':   '15_Niigata',  'Toyama':     '16_Toyama',
    'Ishikawa':  '17_Ishikawa', 'Fukui':      '18_Fukui',
    'Yamanashi': '19_Yamanashi','Nagano':     '20_Nagano',
    'Gifu':      '21_Gifu',     'Shizuoka':   '22_Shizuoka',
    'Aichi':     '23_Aichi',    'Mie':        '24_Mie',
    'Shiga':     '25_Shiga',    'Kyoto':      '26_Kyoto',
    'Osaka':     '27_Osaka',    'Hyogo':      '28_Hyogo',
    'Nara':      '29_Nara',     'Wakayama':   '30_Wakayama',
    'Tottori':   '31_Tottori',  'Shimane':    '32_Shimane',
    'Okayama':   '33_Okayama',  'Hiroshima':  '34_Hiroshima',
    'Yamaguchi': '35_Yamaguchi','Tokushima':  '36_Tokushima',
    'Kagawa':    '37_Kagawa',   'Ehime':      '38_Ehime',
    'Kochi':     '39_Kochi',    'Fukuoka':    '40_Fukuoka',
    'Saga':      '41_Saga',     'Nagasaki':   '42_Nagasaki',
    'Kumamoto':  '43_Kumamoto', 'Oita':       '44_Oita',
    'Miyazaki':  '45_Miyazaki', 'Kagoshima':  '46_Kagoshima',
    'Okinawa':   '47_Okinawa',
}

dialect_category_dict = {
    '01_Hokkaido':  'Hokkaido dialect',
    '02_Aomori':    'Tohoku dialect',    '03_Iwate':     'Tohoku dialect',
    '04_Miyagi':    'Tohoku dialect',    '05_Akita':     'Tohoku dialect',
    '06_Yamagata':  'Tohoku dialect',    '07_Fukushima': 'Tohoku dialect',
    '08_Ibaraki':   'Kanto dialect',     '09_Tochigi':   'Kanto dialect',
    '10_Gunma':     'Kanto dialect',     '11_Saitama':   'Kanto dialect',
    '12_Chiba':     'Kanto dialect',     '13_Tokyo':     'Kanto dialect',
    '14_Kanagawa':  'Kanto dialect',
    '15_Niigata':   'Hokuriku dialect',  '16_Toyama':    'Hokuriku dialect',
    '17_Ishikawa':  'Hokuriku dialect',  '18_Fukui':     'Hokuriku dialect',
    '19_Yamanashi': 'Tokai-Tosan dialect','20_Nagano':   'Tokai-Tosan dialect',
    '21_Gifu':      'Tokai-Tosan dialect','22_Shizuoka': 'Tokai-Tosan dialect',
    '23_Aichi':     'Tokai-Tosan dialect',
    '24_Mie':       'Kinki dialect',     '25_Shiga':     'Kinki dialect',
    '26_Kyoto':     'Kinki dialect',     '27_Osaka':     'Kinki dialect',
    '28_Hyogo':     'Kinki dialect',     '29_Nara':      'Kinki dialect',
    '30_Wakayama':  'Kinki dialect',
    '31_Tottori':   'Chugoku dialect',   '32_Shimane':   'Chugoku dialect',
    '33_Okayama':   'Chugoku dialect',   '34_Hiroshima': 'Chugoku dialect',
    '35_Yamaguchi': 'Chugoku dialect',
    '36_Tokushima': 'Shikoku dialect',   '37_Kagawa':    'Shikoku dialect',
    '38_Ehime':     'Shikoku dialect',   '39_Kochi':     'Shikoku dialect',
    '40_Fukuoka':   'Hichiku dialect',   '41_Saga':      'Hichiku dialect',
    '42_Nagasaki':  'Hichiku dialect',   '43_Kumamoto':  'Hichiku dialect',
    '44_Oita':      'Toyonichi dialect',
    '45_Miyazaki':  'Satsugu dialect',   '46_Kagoshima': 'Satsugu dialect',
    '47_Okinawa':   'Ryukyuan dialect',
}

# ── 处理 COJADS ───────────────────────────────────────────────────────────
print('读取 COJADS...')
cojads = pd.read_csv(COJADS, low_memory=False, encoding='utf-8', encoding_errors='replace')

# 统一性别为 male/female
cojads['speaker_gender'] = cojads['speaker_gender'].map({'男': 'male', '女': 'female'})

cojads_out = pd.DataFrame({
    'dataset':          'COJADS',
    'source_file':      cojads['source_file'],
    'prefecture_en':    cojads['prefecture_en'],
    'dialect_category': cojads['dialect_category'],
    'dialect_text':     cojads['dialect_text'],
    'standard_text':    cojads['standard_text'],
    'speaker':          cojads['speaker'],
    'gender':           cojads['speaker_gender'],
    'age_group':        None,
    'speaker_age':      cojads['speaker_age'],
    'speaker_birth_year': cojads['speaker_birth_year'],
    'speech_type':      'spontaneous',
    'topic':            cojads['topic'],
    'recording_date':   cojads['recording_date'],
    'xmin':             cojads['xmin'],
    'xmax':             cojads['xmax'],
    'duration':         None,
    'location':         cojads['location'],
})
print(f'  COJADS: {len(cojads_out)} 行')

# ── 处理 GSR-JD ───────────────────────────────────────────────────────────
print('读取 GSR-JD...')
gsrjd = pd.read_csv(GSRJD, encoding='utf-8', encoding_errors='replace')

gsrjd['prefecture_en']    = gsrjd['dialect'].map(pref_name_to_en)
gsrjd['dialect_category'] = gsrjd['prefecture_en'].map(dialect_category_dict)

gsrjd_out = pd.DataFrame({
    'dataset':          'GSR-JD',
    'source_file':      gsrjd['file'],
    'prefecture_en':    gsrjd['prefecture_en'],
    'dialect_category': gsrjd['dialect_category'],
    'dialect_text':     gsrjd['text'],
    'standard_text':    None,
    'speaker':          gsrjd['speaker'],
    'gender':           gsrjd['gender'],
    'age_group':        gsrjd['age_group'],
    'speaker_age':      None,
    'speaker_birth_year': None,
    'speech_type':      gsrjd['speech_type'],
    'topic':            None,
    'recording_date':   None,
    'xmin':             None,
    'xmax':             None,
    'duration':         gsrjd['duration'],
    'location':         None,
})
print(f'  GSR-JD: {len(gsrjd_out)} 行')

# ── 垂直合并 ──────────────────────────────────────────────────────────────
merged = pd.concat([cojads_out, gsrjd_out], ignore_index=True)
merged.to_csv(OUTPUT, index=False, encoding='utf-8')

print(f'\n合并完成：{len(merged)} 行，已保存至 {OUTPUT}')
print('\ndataset 分布:')
print(merged['dataset'].value_counts().to_string())
print('\nprefecture_en 覆盖（GSR-JD）:')
print(gsrjd_out['prefecture_en'].value_counts().to_string())
print('\ndialect_category 分布:')
print(merged['dialect_category'].value_counts().to_string())
