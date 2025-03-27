import pandas as pd
import re
from fuzzywuzzy import process

try:
    df = pd.read_csv('data_store.csv')
except Exception as e:
    df = pd.DataFrame()
    print("❗ CSV 파일을 불러오는 데 실패했습니다:", e)

def get_apartment_info(user_input):
    if df.empty:
        return "❗ 아파트 데이터가 로드되지 않았습니다."

    apt_name_match = process.extractOne(user_input, df['단지명'])
    if not apt_name_match or apt_name_match[1] < 60:
        return "❗ 아파트 이름을 인식하지 못했습니다."

    apt_name = apt_name_match[0]
    sub_df = df[df['단지명'] == apt_name]

    pyeong_match = re.search(r'(\d+)\s*평', user_input)
    if pyeong_match:
        pyeong = int(pyeong_match.group(1))
        sub_df = sub_df[sub_df['평형'].astype(str).str.contains(str(pyeong))]

    if sub_df.empty:
        return f"❗ {apt_name} 아파트에 해당하는 평형 정보를 찾을 수 없습니다."

    row = sub_df.iloc[0]
    response = f"🏢 **{row['단지명']}**\n📍 주소: {row['주소']}\n📐 평형: {row['평형']}\n"

    if '전세' in user_input:
        response += f"🔹 전세가: {row['전세가']}"
    elif '매매' in user_input:
        response += f"🔸 매매가: {row['매매가']}"
    else:
        response += f"🔸 매매가: {row['매매가']}\n🔹 전세가: {row['전세가']}"

    return response
