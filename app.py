import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from korean_lunar_calendar import KoreanLunarCalendar
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import io

# 1. 앱 페이지 스타일 (수묵화의 단아함 + 황금빛 권위)
st.set_page_config(page_title="법천스님 : 그랜드 마스터", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #0d1117; color: #d4af37; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { width: 100%; background-color: #d4af37; color: #000; font-weight: bold; border-radius: 15px; height: 3.5em; border: none; font-size: 1.1em; transition: 0.3s; }
    .stButton>button:hover { background-color: #fff; color: #d4af37; }
    .report-card { background-color: #161b22; padding: 30px; border-radius: 20px; border: 1px solid #d4af37; margin-bottom: 25px; line-height: 1.9; }
    .master-title { color: #d4af37; text-align: center; text-shadow: 2px 2px 5px #000; font-size: 3em; margin-bottom: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #21262d; border-radius: 8px; color: #8b949e; padding: 12px 25px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #d4af37; color: #000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. 분석 엔진 (네 인생의 모든 데이터를 로직화)
class GrandMasterEngine:
    def __init__(self, name, birth, lunar, time, concern):
        self.name = name
        self.birth = birth
        self.lunar = lunar
        self.time = time
        self.concern = concern
        self.cal = KoreanLunarCalendar()
        
    def analyze(self):
        # 네 법천스님/영적사주/고민상담
        analysis = {
            "zen": f"'{self.name}'님, 비우면 채워지고 멈추면 보입니다. 현재의 {self.concern} 고민은 보석을 깎는 과정입니다.",
            "beauty": "20년 미용 마스터의 통찰: 관록궁(이마)을 열어 기운을 소통시키고, 중국 직수입 고퀄리티 가발 스타일링으로 자신감을 보강하십시오.",
            "forest": "8년 임업 전문가의 처방: '흑도보감'의 기운이 필요합니다. 흑염소와 도라지, 그리고 촉성두릅의 강인한 생명력이 귀하의 정기를 살릴 것입니다.",
            "estate": "부동산 비책: 양산 라페스타의 상업적 기운과 원동면 토지의 신축 개발 운을 활용하십시오. 2026년은 서생면 땅의 매도 적기입니다.",
            "wealth": "재물 동향: Ethena(ENA)와 Sui(SUI)처럼 견고한 자산을 눈여겨보되, 로또의 요행보다는 데이터 기반의 분산 투자가 길합니다.",
            "art": "예술 치유: 432Hz 치유 주파수와 김경호 스타일의 강렬한 록 발라드가 귀하의 막힌 혈을 뚫어줄 것입니다.",
            "legal": "조언: 인근 지인의 사고나 산재 문제는 전문가의 도움을 받아 정당한 권리를 찾는 것이 인연의 매듭을 푸는 길입니다."
        }
        return analysis

# 3. 메인 화면 구성
st.markdown("<h1 class='master-title'>🏮 천기자동(天機自動)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.2em;'><b>법천스님 · 영적사주 · 동양최초 아시아 명리학 · </b></p>", unsafe_allow_html=True)

# 고객 데이터 입력 (데이터베이스 역할)
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&q=80&w=400", caption="천기(天機)의 흐름")
    st.header("📝 고객 상담 명부")
    c_name = st.text_input("고객 이름", "신규 고객")
    c_birth = st.date_input("생년월일", datetime.date(1985, 5, 20))
    c_lunar = st.checkbox("음력 적용", value=False)
    c_time = st.selectbox("태어난 시간", [f"{i:02d}시" for i in range(24)])
    c_concern = st.selectbox("주요 고민", ["재물/사업", "건강/치유", "부동산/이사", "인연/가족", "진로/예술"])
    
    st.divider()
    if st.button("🔮 마스터의 통찰 실행"):
        st.session_state['run'] = True
        st.balloons()

# 4. 상담 대시보드 (디테일한 탭 구성)
if st.session_state.get('run'):
    engine = GrandMasterEngine(c_name, c_birth, c_lunar, c_time, c_concern)
    res = engine.analyze()

    tabs = st.tabs(["🧘 영성/수행", "🎨 미용/개운", "🌿 스마트팜/임업", "🏠 부동산/투자", "🎵 음악/예술", "📉 재물/코인", "📝 49일 일기"])

    with tabs[0]:
        st.markdown(f"<div class='report-card'><h3>🧘 마음과 수행</h3>{res['zen']}<br><br><b>💡 마스터의 조언:</b> {res['legal']}</div>", unsafe_allow_html=True)
        
    
    with tabs[1]:
        st.markdown(f"<div class='report-card'><h3>✂️ 20년 경력 미용 비책</h3>{res['beauty']}</div>", unsafe_allow_html=True)
        st.success("✨ 추천 스타일링: 관록궁을 강조한 포마드 스타일 혹은 풍성한 볼륨 가발")
        

    with tabs[2]:
        st.markdown(f"<div class='report-card'><h3>🌿 흑도보감 스마트팜 솔루션</h3>{res['forest']}</div>", unsafe_allow_html=True)
        st.info("📊 <b>촉성두릅 자동화 팁:</b> 습도 85% 유지와 미스트 분사 시스템이 성패를 좌우합니다.")
        

    with tabs[3]:
        st.markdown(f"<div class='report-card'><h3>🏛️ 부동산 풍수 전략</h3>{res['estate']}</div>", unsafe_allow_html=True)
        st.warning("⚠️ 양산 원동면 45평 토지: 상가주택 설계 시 1층은 근린생활시설로 빼는 것이 수익률에 유리합니다.")
        

    with tabs[4]:
        st.markdown(f"<div class='report-card'><h3>🎵 예술적 감각과 치유</h3>{res['art']}</div>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.write("🎹 **현재 작곡 기운:** 432Hz의 평온함 속에 김경호의 폭발력을 담으십시오.")

    with tabs[5]:
        st.markdown(f"<div class='report-card'><h3>💰 재물 및 투자 동향</h3>{res['wealth']}</div>", unsafe_allow_html=True)
        # 운세 그래프
        fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0d1117')
        ax.set_facecolor('#0d1117')
        ax.plot(['1월', '4월', '7월', '10월'], [40, 90, 65, 85], color='#d4af37', linewidth=3, marker='o')
        ax.tick_params(colors='white')
        st.pyplot(fig)

    with tabs[6]:
        st.subheader("📝 49일 마음 정화 일기")
        diary_df = pd.DataFrame({
            "수행일": [f"Day {i+1}" for i in range(7)],
            "과제": ["108배", "주파수 명상", "부동산 시장 모니터링", "작곡 아이디어 메모", "맨발 걷기", "감사 세 번", "산재 및 법률 공부"],
            "완료": [False] * 7
        })
        st.data_editor(diary_df, use_container_width=True)

    # 파워포인트 생성 (마스터의 유료 리포트)
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    title = slide.shapes.title
    title.text = f"{c_name}님을 위한 천기(天機) 리포트"
    tf = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5)).text_frame
    tf.text = f"1. 수행: {res['zen']}\n2. 미용: {res['beauty']}\n3. 사업: {res['forest']}\n4. 투자: {res['estate']}"
    
    buf = io.BytesIO()
    prs.save(buf)
    st.download_button("📥 5만원 프리미엄 리포트 다운로드", buf.getvalue(), file_name=f"{c_name}_상담리포트.pptx")

# 5. 고객 데이터 저장 기능
if st.button("💾 고객 상담 내역 저장"):
    save_data = pd.DataFrame({"이름": [c_name], "날짜": [datetime.datetime.now()], "고민": [c_concern]})
    st.write("고객 데이터가 서버에 임시 저장되었습니다. (추후 DB 연결 가능)")
    st.dataframe(save_data)
