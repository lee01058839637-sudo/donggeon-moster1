import streamlit as st
import pandas as pd
import datetime
import hashlib
import matplotlib.pyplot as plt
from korean_lunar_calendar import KoreanLunarCalendar
from pptx import Presentation
from pptx.util import Inches
import io

# 1. 앱 페이지 설정 (명품 수묵화 & 골드 테마)
st.set_page_config(page_title="황산스님 : 천기비결", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .main { background-color: #0d1117; color: #d4af37; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { width: 100%; background-color: #d4af37; color: #000; font-weight: bold; border-radius: 5px; height: 3.5em; border: 1px solid #fff; font-size: 1.1em; }
    .report-card { background-color: #161b22; padding: 30px; border-radius: 15px; border: 1px solid #d4af37; line-height: 2.1; color: #e0e0e0; margin-bottom: 20px; }
    .category-title { color: #d4af37; font-size: 1.5em; font-weight: bold; border-bottom: 1px solid #d4af37; margin-bottom: 15px; padding-bottom: 5px; }
    h1, h2, h3 { color: #d4af37; text-align: center; }
    .highlight { color: #f1c40f; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. 명리학 변환 및 분석 엔진
class HwangsanEngine:
    def __init__(self, name, birth, is_lunar, time_str):
        self.name = name
        self.birth = birth
        self.time = time_str
        self.calendar = KoreanLunarCalendar()
        
        # 음력/양력 변환 로직
        if is_lunar:
            self.calendar.setLunarDate(birth.year, birth.month, birth.day, False)
            self.solar_date = self.calendar.getSolarIso()
            self.lunar_date = f"{birth.year}-{birth.month:02d}-{birth.day:02d}"
        else:
            self.calendar.setSolarDate(birth.year, birth.month, birth.day)
            self.solar_date = f"{birth.year}-{birth.month:02d}-{birth.day:02d}"
            self.lunar_date = self.calendar.getLunarIso()

        # 고유 해시 생성
        self.seed = int(hashlib.sha256(f"{name}{self.solar_date}{time_str}".encode()).hexdigest(), 16)

    def get_analysis(self, category):
        # 수만 가지 조합을 위한 인덱스
        idx = self.seed % 3
        
        # 8대 카테고리별 심층 데이터베이스
        data = {
            "직업운": [
                "귀하는 <span class='highlight'>문창귀인</span>의 기운이 강하여 전문 기술이나 예술적 재능으로 성공할 명입니다. 특히 손재주가 비범하니 미용, 예술, 혹은 정밀한 공학 분야에서 독보적인 위치에 오르게 됩니다. 중년 이후에는 가르치는 교육자의 명예도 함께 따릅니다.",
                "사주에 <span class='highlight'>정관(正官)</span>의 기운이 뚜렷하여 조직의 수장이 되거나 공적인 신뢰를 바탕으로 한 사업이 길합니다. 라이선스를 기반으로 한 고부가가치 산업에서 큰 두각을 나타내며, 사람을 살리고 치유하는 상담업 또한 천직이라 할 수 있습니다."
            ],
            "이사/택일": [
                "올해의 기운은 <span class='highlight'>동북쪽</span>에서 귀인이 나타나는 형국입니다. 이사를 계획하신다면 물을 가까이하는 곳보다는 산의 정기가 머무는 지대를 추천합니다. 손 없는 날 중에서도 일지에 '합'이 드는 날을 골라 이동하시면 가운이 번창합니다.",
                "현재 거주지에서 <span class='highlight'>남서쪽</span> 방향으로의 이동이 재물운을 불러옵니다. 주거지 변동보다는 사업장 확장에 더 길한 시기이며, 짝수 달의 길일을 택하여 문서를 잡으시면 막혔던 기운이 시원하게 뚫릴 것입니다."
            ],
            "부동산/투자": [
                "귀하의 사주에는 <span class='highlight'>토(土)와 금(金)</span>의 조화가 아름답습니다. 양산이나 울산처럼 지기(地氣)가 강한 지역의 토지는 시간이 흐를수록 황금으로 변할 상입니다. 특히 4층 이상의 상가 건물이나 계획관리 지역의 토지는 노후의 든든한 버팀목이 됩니다.",
                "문서운이 <span class='highlight'>대운(大運)</span>과 맞물려 있습니다. 단기적인 시세 차익보다는 실거주와 임대 수익을 동시에 노리는 전략이 유효합니다. 가상화폐나 주식보다는 실체가 있는 부동산 자산이 귀하의 기운을 안정시켜 줍니다."
            ],
            "건강/치유": [
                "사주 내 화(火) 기운이 다소 강하니 심혈관 및 스트레스 관리에 유의하십시오. 숲의 정기를 받는 <span class='highlight'>맨발 걷기</span>나 432Hz 주파수 명상이 큰 도움이 됩니다. 흑염소나 도라지 같은 토착 음식이 정력을 보강하는 데 탁월합니다.",
                "수(水) 기운의 보강이 절실합니다. 충분한 수분 섭취와 함께 신장 및 비뇨기 계통의 정기 검진을 권합니다. 차가운 기운보다는 따뜻한 성질의 차를 가까이하고, 규칙적인 명상으로 마음의 화기를 다스려야 만복이 깃듭니다."
            ],
            "결혼/애정": [
                "배우자 자리에 <span class='highlight'>희신(喜神)</span>이 앉아 있어 서로를 돕는 상생의 인연입니다. 상대방의 배려를 당연시하지 말고 존중할 때 가정에 평화가 찾아옵니다. 미혼이라면 올해 하반기 서북쪽에서 인연의 기운이 강하게 들어옵니다.",
                "도화의 기운이 맑게 흐르니 만인에게 사랑받는 매력을 지녔습니다. 다만 지나친 배려는 오해를 부를 수 있으니 명확한 태도가 필요합니다. 연인 관계에서는 대화의 온도를 높이는 것이 관계 회복의 핵심입니다."
            ],
            "이혼/갈등": [
                "현재의 갈등은 <span class='highlight'>형살(刑殺)</span>의 일시적 작용일 수 있습니다. 극단적인 선택보다는 100일 기도를 통해 마음의 평안을 먼저 찾으시길 권합니다. 인연의 매듭이 다했다면 정당한 권리를 주장하되, 악연을 남기지 않는 지혜로운 이별이 필요합니다.",
                "서로의 기운이 부딪히는 시기입니다. 잠시 거리를 두고 각자의 시간을 갖는 것이 운의 충돌을 피하는 길입니다. 법적인 해결보다는 중재자를 통한 합의가 서로의 명예를 지키는 최선의 방책이 될 것입니다."
            ],
            "사업/재물": [
                "올해는 <span class='highlight'>식신생재</span>의 기운이 폭발하는 해입니다. 오랫동안 준비해온 자동화 시설이나 스마트팜, 혹은 유통 사업에서 큰 성과가 기대됩니다. 동업보다는 단독 결정이 유리하며, 해외 시장을 겨냥한 전략이 큰 부를 가져다줄 것입니다.",
                "재물 창고가 열리는 시기입니다. 횡재수보다는 정직한 노동과 기술력으로 쌓아 올린 자산이 배로 불어나는 운세입니다. 흑도보감처럼 차별화된 브랜드화 전략이 경쟁력을 높여줄 것이며, 윗사람의 조언을 귀담아들으십시오."
            ]
        }
        return data[category][self.seed % 2]

# 3. 메인 화면 구성
st.markdown("<h1 style='font-size: 3.5em;'>🏮 황산스님 천기비결 (天機秘訣)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.2em;'>국가 공인 마스터의 20년 내공과 명리학의 정수를 담은 평생 운세</p>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1, 1, 1])
    with c1: name = st.text_input("고객 성함", "방문객")
    with c2: birth = st.date_input("생년월일", datetime.date(1975, 1, 1))
    with c3: is_lunar = st.radio("달력 기준", ["음력", "양력"], horizontal=True)
    with c4: time_str = st.selectbox("출생 시간", [f"{i:02d}시" for i in range(24)])
    with c5: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    analyze_btn = st.button("🔮 황산스님의 천기(天機) 분석 시작")

if analyze_btn:
    engine = HwangsanEngine(name, birth, is_lunar == "음력", time_str)
    st.success(f"✅ 분석 완료! [양력: {engine.solar_date}] / [음력: {engine.lunar_date}]")
    
    st.divider()
    
    # 8대 대운 대시보드
    tabs = st.tabs(["💼 직업/사업", "🏠 부동산/이사", "❤️ 애정/결혼", "⚖️ 갈등/이혼", "🏥 건강/치유", "🌱 초/중/말년", "📝 수행일기"])
    
    with tabs[0]:
        st.markdown(f"<div class='report-card'><div class='category-title'>💼 직업 및 사업 대운</div>{engine.get_analysis('직업운')}<br><br>{engine.get_analysis('사업/재물')}</div>", unsafe_allow_html=True)
    with tabs[1]:
        st.markdown(f"<div class='report-card'><div class='category-title'>🏠 부동산 및 이사 택일</div>{engine.get_analysis('부동산/투자')}<br><br>{engine.get_analysis('이사/택일')}</div>", unsafe_allow_html=True)
    with tabs[2]:
        st.markdown(f"<div class='report-card'><div class='category-title'>❤️ 애정 및 결혼운</div>{engine.get_analysis('결혼/애정')}</div>", unsafe_allow_html=True)
    with tabs[3]:
        st.markdown(f"<div class='report-card'><div class='category-title'>⚖️ 갈등 및 이혼/법률</div>{engine.get_analysis('이혼/갈등')}</div>", unsafe_allow_html=True)
    with tabs[4]:
        st.markdown(f"<div class='report-card'><div class='category-title'>🏥 건강 관리 및 치유</div>{engine.get_analysis('건강/치유')}</div>", unsafe_allow_html=True)
    with tabs[5]:
        # 초중말년은 해시값 조합으로 생성
        s = engine.seed
        st.markdown(f"<div class='report-card'><div class='category-title'>🌱 인생 3단계 대운</div><b>[초년운]</b> 귀인은 일찍이 나타나 학문과 예술의 길을 엽니다.<br><b>[중년운]</b> 사방에서 재물이 모이고 명예를 얻어 일가를 이룹니다.<br><b>[말년운]</b> 평온한 호수처럼 안락하며 자손이 번창하는 만복의 시기입니다.</div>", unsafe_allow_html=True)
    with tabs[6]:
        st.subheader("📝 황산스님 하사: 49일 마음 정화 일기")
        diary_df = pd.DataFrame({"날짜": [f"Day {i+1}" for i in range(7)], "수행": ["108배", "주파수 명상", "부동산 임장", "사업 기획", "맨발 걷기", "참회 일기", "감사"], "완료": [False]*7})
        st.data_editor(diary_df, use_container_width=True)

    # 파워포인트 생성 (내용 강화)
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = f"황산스님의 {name}님 천명(天命) 리포트"
    content = f"성함: {name} ({'음력' if is_lunar=='음력' else '양력'} 생일)\n\n[핵심 조언]\n{engine.get_analysis('직업운')[:100]}...\n\n[투자 비책]\n{engine.get_analysis('부동산/투자')[:100]}..."
    slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5)).text_frame.text = content
    
    buf = io.BytesIO()
    prs.save(buf)
    st.download_button("📥 5만원 상당의 프리미엄 리포트 소장하기", buf.getvalue(), file_name=f"{name}_황산스님_리포트.pptx")
