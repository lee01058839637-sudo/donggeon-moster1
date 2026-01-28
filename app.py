import streamlit as st
import pandas as pd
import datetime
import hashlib
import random
from korean_lunar_calendar import KoreanLunarCalendar
from pptx import Presentation
from pptx.util import Inches
import io

# 1. 앱 최상단 설정 (에러 방지를 위해 가장 먼저 실행)
st.set_page_config(page_title="황산스님 : 천기비결", page_icon="🏮", layout="wide")

# 프리미엄 블랙 & 골드 스타일링
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #d4af37; font-family: 'Nanum Myeongjo', serif; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #8c6a1a, #d4af37); color: #000; font-weight: bold; border-radius: 5px; height: 3.5em; border: none; font-size: 1.1em; }
    .report-card { background-color: #111; padding: 30px; border: 1px solid #d4af37; border-radius: 10px; line-height: 2.2; color: #f0f0f0; margin-bottom: 20px; }
    .pillar-box { background-color: #1a1a1a; border: 1px solid #d4af37; padding: 15px; text-align: center; }
    .pillar-hanja { font-size: 2.2em; font-weight: bold; color: #d4af37; line-height: 1.2; }
    h1, h2, h3 { color: #d4af37; text-align: center; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 고성능 사주 분석 엔진
class GrandMasterEngine:
    def __init__(self, name, birth, is_lunar, time_str):
        self.name = name
        self.calendar = KoreanLunarCalendar()
        try:
            if is_lunar:
                self.calendar.setLunarDate(birth.year, birth.month, birth.day, False)
                self.solar = self.calendar.getSolarIso()
                self.lunar = f"{birth.year}-{birth.month:02d}-{birth.day:02d}"
            else:
                self.calendar.setSolarDate(birth.year, birth.month, birth.day)
                self.solar = f"{birth.year}-{birth.month:02d}-{birth.day:02d}"
                self.lunar = self.calendar.getLunarIso()
        except:
            self.solar = str(birth)
            self.lunar = "계산 중..."
        
        # 고유 시드 생성 (결과 고정 + 랜덤화)
        seed_str = f"{name}{self.solar}{time_str}"
        self.hash_val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        random.seed(self.hash_val)

    def get_pillars(self):
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        return [(random.choice(stems), random.choice(branches)) for _ in range(4)]

    def get_content(self, cat):
        # 수천 가지 조합을 위한 텍스트 DB
        db = {
            "직업": ["천권성(天權星)이 비추니 만인을 다스리는 지도자의 명입니다.", "예리한 기술과 안목으로 일가를 이루는 명장의 명입니다.", "지략과 문창성이 조화로우니 선비와 같은 고귀한 지혜를 쓸 명입니다."],
            "사업": ["식신생재의 기운이 강해 무에서 유를 창조하는 거부의 운입니다.", "신용과 의리가 재산이니 인맥을 통해 거대한 부를 쌓을 운입니다.", "유통과 흐름을 읽는 눈이 탁월하니 전 세계를 무대로 활약할 운입니다."],
            "부동산": ["대지의 기운이 조화로워 문서를 잡으면 황금으로 변할 운입니다.", "강과 바다를 낀 터가 귀하의 기운을 살려주는 명당입니다.", "상가 건물의 높은 층이 재물을 불러모으는 형국입니다."],
            "건강": ["강인한 정력이 전신을 감싸니 무병장수할 기운입니다.", "목(木)의 기운을 보강하여 간과 피로를 다스리는 것이 개운의 열쇠입니다.", "규칙적인 명상과 숲의 기운이 만병을 물리치는 명약입니다."],
            "애정": ["천생연분의 인연이 나타나
