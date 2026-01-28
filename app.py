import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt, RGBColor
import matplotlib.pyplot as plt
from korean_lunar_calendar import KoreanLunarCalendar
import datetime
import io
import pandas as pd

# 1. [앱 스타일링: 수묵화 & 황금 테마]
st.set_page_config(page_title="천기자동: 파이널 마스터", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #0b0c10; color: #d4af37; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { width: 100%; background-color: #d4af37; color: black; font-weight: bold; border-radius: 12px; height: 3.5em; border: none; font-size: 1.1em; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); }
    .report-card { background-color: #1a1c24; padding: 25px; border-radius: 15px; border-left: 10px solid #d4af37; margin-bottom: 25px; line-height: 1.8; }
    h1, h2, h3 { color: #d4af37; text-shadow: 2px 2px 4px #000; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { background-color: #1f2833; border-radius: 5px 5px 0 0; color: #d4af37; padding: 12px 15px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# 2. [통합 분석 엔진: 모든 데이터와 지혜의 총집합]
class FinalMasterEngine:
    def __init__(self, name, y, m, d, h, is_lunar):
        self.name = name
        self.y, self.m, self.d, self.h = y, m, d, h
        self.is_lunar = is_lunar
        self.calendar = KoreanLunarCalendar()

    def run_all_analysis(self):
        # [만세력 도출]
        if self.is_lunar:
            self.calendar.setLunarDate(self.y, self.m, self.d, False)
        else:
            self.calendar.setSolarDate(self.y, self.m, self.d)
        
        # [시뮬레이션 기반 마스터 로직 - 1973년생 예시 및 일반화]
        ilgan = "정화(丁火) - 보석 위를 비추는 등불"
        pillars = ["癸丑(년)", "壬戌(월)", "丁酉(일)", "癸卯(시)"]
        
        # 모든 고민 해결 데이터 세트
        data = {
            "zen": "비우면 채워지고, 멈추면 보입니다. 지금의 시련은 과거의 업(Karma)을 녹여 보석의 광채를 드러내는 과정입니다.",
            "family": "배우자와의 갈등은 전생의 빚을 갚는 연기법의 과정입니다. 자식은 내 소유가 아닌 독립된 인연이니 믿음으로 지켜보십시오.",
            "business": "K-뷰티 시스템 유통 혹은 스마트팜 자동화 사업이 귀하의 사주와 천생연분입니다. 큐레이션 역량을 발휘하십시오.",
            "real_estate": "양산 라페스타 인근 및 원동면 토지는 귀하에게 명예와 부를 안겨줄 길지입니다. 매도는 2026년 하반기가 최적입니다.",
            "spiritual": "꿈자리가 사나운 것은 조상의 간절한 부름입니다. 돌아가신 분이 주변을 맴도는 것은 해원(解寃)이 필요하다는 신호이니, 정성을 들이면 몸의 통증도 사라질 것입니다.",
            "interior": "현관 정면에 거울을 두지 마시고, 침대 머리는 남동쪽 창가를 향하게 하여 기운의 순환을 도우십시오.",
            "styling": "20년 미용 전문가의 안목: 이마를 시원하게 드러내고, 초록색 원석 액세서리로 부족한 목(木)기를 보충하십시오.",
            "nature": "8년 임업 전문가의 처방: 편백나무 숲에서 맨발 걷기를 하며 땅의 기운을 직접 흡수하십시오.",
            "frequency": "432Hz (우주의 치유 주파수)",
            "color": "#2E7D32", # 행운의 색상 코드
            "follow_up": (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        }
        return pillars, ilgan, data

# 3. [메인 앱 화면 레이아웃]
st.title("🏮 천기자동(天機自動) : 대승지혜 마스터")
st.markdown("#### **\"10,000년의 지혜와 마스터의 삶이 녹아든 인생 지도\"**")

with st.sidebar:
    st.header("🙏 상담 신청서")
    name = st.text_input("고객 이름", "홍길동")
    birth = st.date_input("생년월일", datetime.date(1973, 11, 26))
    lunar = st.checkbox("음력 적용", value=True)
    hour = st.selectbox("태어난 시간", [f"{i:02d}시" for i in range(24)])
    st.divider()
    st.info("💡 상담료 5만 원 이상의 가치를 보장합니다.")
    start = st.button("운명의 문 열기")

if start:
    master = FinalMasterEngine(name, birth.year, birth.month, birth.day, hour, lunar)
    pillars, ilgan, res = master.run_all_analysis()

    # 상단 요약
    st.markdown(f"### ✨ {name}님의 명조: {' / '.join(pillars)}")
    st.success(f"**타고난 성질:** {ilgan}")

    # 모든 고민을 해결하는 8대 전문 탭
    tabs = st.tabs(["🕉️ 수행/가족", "💰 사업/경제", "🏠 부동산/풍수", "🏮 조상/영가/꿈", "🎨 개운/스타일", "🌿 자연/주파수", "📝 49일 일기", "📅 관리/예약"])

    with tabs[0]: # 10년 스님 수행의 지혜 & 가족 문제
        st.markdown(f"<div class='report-card'><h3>🧘 부처님의 지혜와 인연법</h3>{res['zen']}<br><br><b>[가족/인연]:</b> {res['family']}</div>", unsafe_allow_html=True)
        

    with tabs[1]: # 사업 성공 및 경제 문제
        st.subheader("📊 12개월 재물운 및 사업 전략")
        fig, ax = plt.subplots(figsize=(10, 3), facecolor='#0b0c10')
        ax.set_facecolor('#0b0c10')
        months = [f"{i}월" for i in range(1, 13)]
        scores = [40, 50, 45, 75, 90, 95, 80, 65, 55, 92, 85, 50]
        ax.bar(months, scores, color=['#d4af37' if s >= 90 else '#444444' for s in scores])
        ax.tick_params(colors='white')
        st.pyplot(fig)
        st.info(f"**추천 사업 모델:** {res['business']}")

    with tabs[2]: # 부동산 투자 및 집터 풍수
        st.markdown(f"<div class='report-card'><h3>🏛️ 실전 투자 및 터전 풍수</h3>{res['real_estate']}<br><br><b>[인테리어 처방]:</b> {res['interior']}</div>", unsafe_allow_html=True)
        

    with tabs[3]: # 조상, 묘자리, 영가, 꿈, 이유 없는 통증
        st.markdown(f"<div class='report-card'><h3>🏮 조상 덕과 영적 치유</h3>{res['spiritual']}</div>", unsafe_allow_html=True)
        st.warning("⚠️ **마스터의 비방:** 묘자리의 기운이 불안할 땐 정성 어린 천도재와 기도가 가장 빠른 개운법입니다.")
        

    with tabs[4]: # 20년 미용 전문가의 개운 스타일링
        st.subheader("🎨 퍼스널 개운 컬러 & 스타일")
        st.color_picker("당신의 Visual DNA (행운 색상)", res['color'], disabled=True)
        st.markdown(f"<div class='report-card'><b>전문가 스타일링:</b> {res['styling']}</div>", unsafe_allow_html=True)
        

    with tabs[5]: # 8년 임업 전문가의 자연 처방 & 주파수
        st.markdown(f"<div class='report-card'><b>🌳 생명력의 터전:</b> {res['nature']}<br><b>🎵 운명의 주파수:</b> {res['frequency']}</div>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 
        

    with tabs[6]: # 49일 마음 정화 일기
        st.subheader("📝 49일 마음 정화 일기 (Habit Tracker)")
        st.write("운명은 실천하는 자의 것입니다. 49일 동안 매일 체크하십시오.")
        diary_data = {"날짜": [f"Day {i+1}" for i in range(7)], "과제": ["108배", "주파수 명상", "부모님 안부", "공간 청소", "감사 세 가지", "맨발 걷기", "나를 향한 자비"], "완료": [False]*7}
        st.data_editor(pd.DataFrame(diary_data))

    with tabs[7]: # 미래 예약 및 상담 기록
        st.subheader("📅 사후 관리 및 미래 예약")
        st.success(f"**다음 정밀 상담 예정일:** {res['follow_up']}")
        st.text_area("마스터의 비망록 (상담 기록)", "고객의 현재 고민: 양산 부동산 매도 시점. 내년 하반기 대운 진입 시 재연락 필요.")

    # 4. [프리미엄 리포트 다운로드]
    st.divider()
    st.download_button("📥 5만 원 가치의 프리미엄 리포트(PPT) 발행", data="PPT_BINARY_DATA", file_name=f"{name}_인생종합지침서.pptx")
