
import pandas as pd
import re
from fuzzywuzzy import process

# 데이터 로드
df_price = pd.read_csv("서울_아파트_시세.csv")
df_info = pd.read_csv("서울_단지목록.csv")

# 병합: 단지명 기준으로 주소, 세대수, 면적 등 추가
df = pd.merge(df_price, df_info, on="단지명", how="left")

def get_apartment_info(user_input):
    if df.empty:
        return "❗ 아파트 데이터가 로드되지 않았습니다."

    # 아파트 이름 유사 매칭
    apt_name_match = process.extractOne(user_input, df['단지명'].dropna().unique())
    if not apt_name_match or apt_name_match[1] < 40:
        return "❗ 아파트 이름을 인식하지 못했습니다."

    apt_name = apt_name_match[0]
    sub_df = df[df['단지명'] == apt_name]

    # 평형 필터링
    pyeong_match = re.search(r'(\d+)\s*평', user_input)
    if pyeong_match:
        pyeong = int(pyeong_match.group(1))
        sub_df = sub_df[sub_df['평형'].astype(str).str.contains(str(pyeong))]

    if sub_df.empty:
        return f"❗ {apt_name} 아파트에 해당하는 평형 정보를 찾을 수 없습니다."

    row = sub_df.iloc[0]
    response = f"🏢 **{row['단지명']}**\n📍 주소: {row['주소_x']}\n👥 세대수: {row.get('세대수', '정보 없음')}세대\n📐 평형: {row['평형']}\n"

    if '전세' in user_input:
        response += f"🔹 전세가: {row['시세']}"
    elif '매매' in user_input:
        response += f"🔸 매매가: {row['시세']}"
    else:
        response += f"🔸 매매가/전세가: {row['시세']}"

    return response
