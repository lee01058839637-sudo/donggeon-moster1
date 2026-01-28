import streamlit as st
import pandas as pd
import datetime
import hashlib
from pptx import Presentation
from pptx.util import Inches
import io

# 1. 앱 페이지 설정 (최고급 수묵화 테마)
st.set_page_config(page_title="황산스님 AI 명리정종", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #0d1117; color: #d4af37; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { width: 100%; background-color: #d4af37; color: #000; font-weight: bold; border-radius: 10px; height: 3.5em; border: 1px solid #fff; }
    .report-card { background-color: #161b22; padding: 30px; border-radius: 20px; border-left: 5px solid #d4af37; margin-bottom: 25px; line-height: 2; color: #e0e0e0; }
    .master-title { text-align: center; color: #d4af37; font-size: 3em; text-shadow: 2px 2px 4px #000; }
    .life-stage-title { color: #d4af37; font-weight: bold; border-bottom: 1px solid #d4af37; padding-bottom: 5px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='master-title'>🏮 황산스님 명리정종(命理正宗)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'><b>우주의 기운과 사주팔자의 이치로 당신의 천명을 읽습니다.</b></p>", unsafe_allow_html=True)

# 2. 사주 입력 정보
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        c_name = st.text_input("👤 고객 성함", "방문객")
    with col2:
        c_birth = st.date_input("📅 생년월일", datetime.date(1985, 5, 20))
    with col3:
        c_time = st.selectbox("⏰ 태어난 시간", [f"{i:02d}시 (자~해시)" for i in range(24)])

    c_lunar = st.radio("🌗 기운의 기준", ["음력(Lunar)", "양력(Solar)"], horizontal=True)

# 3. 고도화된 사주 분석 엔진 (정교한 난수 생성)
def get_detailed_analysis(name, birth, time_str):
    # 이름, 날짜, 시간을 모두 섞어 고유한 해시값 생성 (수만 가지 조합 가능)
    combined_key = f"{name}{birth.strftime('%Y%m%d')}{time_str}"
    hash_val = int(hashlib.md5(combined_key.encode()).hexdigest(), 16)
    
    # 만세력 기운 추출 (가상 로직이지만 결과가 매번 다르게 나옴)
    element_idx = hash_val % 5
    elements = ["목(木) - 청룡의 기운", "화(火) - 주작의 기운", "토(土) - 황룡의 기운", "금(金) - 백호의 기운", "수(水) - 현무의 기운"]
    
    # 초년, 중년, 말년 대운 데이터베이스 (조합형)
    early_fortunes = [
        "이른 시기에 문창성(文昌星)이 비추니 학문과 예술에 두각을 나타낼 상입니다. 부모의 덕이 두터워 평탄한 성장을 보입니다.",
        "청년기에는 역마살이 있어 주거의 변동이 잦으나, 이는 훗날 큰 그릇이 되기 위한 담금질입니다. 스스로 길을 개척해야 합니다.",
        "기운이 맑고 고우니 주변의 도움으로 일찍이 이름을 알립니다. 다만 욕심을 부리면 공든 탑이 무너질 수 있으니 자중함이 길합니다."
    ]
    mid_fortunes = [
        "장년기에 접어들어 천권성(天權星)이 임하니 만인을 다스리는 권세를 얻거나, 큰 재물을 만지는 운세입니다. 사업의 기운이 왕성합니다.",
        "중년에는 다소 풍파가 예상되나 인내하면 반드시 결실을 봅니다. 기술과 장인 정신이 당신을 지탱하는 힘이 될 것입니다.",
        "비로소 만사가 형통하고 가정이 화목해지는 시기입니다. 동쪽에서 귀인이 나타나 큰 기회를 가져다줍니다."
    ]
    late_fortunes = [
        "말년에는 천수성(天壽星)이 비추니 건강하고 안락한 삶이 보장됩니다. 자손들이 번창하여 가문의 영광을 높입니다.",
        "산속의 정취를 즐기며 명예를 얻는 노후가 보입니다. 사회적 존경을 받으며 지혜를 나누는 스승의 삶을 살게 됩니다.",
        "창고에 곡식이 가득 차고 인덕이 끊이지 않으니, 베푸는 삶을 통해 큰 덕을 쌓는 아름다운 황혼입니다."
    ]

    return {
        "element": elements[element_idx],
        "early": early_fortunes[hash_val % 3],
        "mid": mid_fortunes[(hash_val // 3) % 3],
        "late": late_fortunes[(hash_val // 9) % 3],
        "advice": "황산스님의 한마디: '운명은 정해진 것이 아니라 흐르는 강물과 같으니, 삿대를 젓는 것은 당신의 몫입니다.'"
    }

# 4. 분석 실행
if st.button("🔮 황산스님께 천명(天命) 여쭙기"):
    st.balloons()
    res = get_detailed_analysis(c_name, c_birth, c_time)
    
    st.markdown(f"### ✨ {c_name}님의 사주 원국 분석: **{res['element']}**")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown(f"<div class='report-card'><div class='life-stage-title'>🌱 초년운 (靑年運)</div>{res['early']}</div>", unsafe_allow_html=True)
        
        
    with col_b:
        st.markdown(f"<div class='report-card'><div class='life-stage-title'>☀️ 중년운 (壯年運)</div>{res['mid']}</div>", unsafe_allow_html=True)
        
        
    with col_c:
        st.markdown(f"<div class='report-card'><div class='life-stage-title'>🌕 말년운 (晩年運)</div>{res['late']}</div>", unsafe_allow_html=True)
        

    st.markdown(f"<div class='report-card' style='text-align:center; border-left:none; border-top:5px solid #d4af37;'><b>🙏 황산스님의 지혜:</b><br>{res['advice']}</div>", unsafe_allow_html=True)

    # 파워포인트 생성 (내용 보강)
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = f"{c_name}님의 평생 사주 리포트"
    tf = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5)).text_frame
    tf.text = f"[사주기운] {res['element']}\n\n[초년] {res['early']}\n\n[중년] {res['mid']}\n\n[말년] {res['late']}"
    
    buf = io.BytesIO()
    prs.save(buf)
    st.download_button("📥 5만원 상당 프리미엄 평생 운세장 다운로드", buf.getvalue(), file_name=f"{c_name}_인생리포트.pptx")
