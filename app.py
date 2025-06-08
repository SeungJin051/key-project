import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
import plotly.express as px
from src.utils.utils import load_css
from src.pages.home import show_home
from src.pages.nutrition_analysis import show_nutrition_analysis
from src.pages.price_info import show_price_info
from src.pages.health_recommendations import show_health_recommendations

# 페이지 설정
st.set_page_config(
    page_title="과일 건강 정보 시스템",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 로드
load_css()

# 전역 스타일 - 사이드바 숨기기 및 메인 콘텐츠 최적화
st.markdown("""
<style>
/* 사이드바 완전히 숨기기 */
.css-1d391kg, .css-1lcbmhc, .css-18e3th9, .css-hxt7ib, .css-17eq0hr, section[data-testid="stSidebar"] {
    display: none !important;
}

/* 메인 콘텐츠 영역 전체 사용 */
.main .block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

/* 버튼 스타일 통일 */
.stButton button {
    background: linear-gradient(to right, #0064FF, #0096FF);
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
}

.stButton button:hover {
    background: linear-gradient(to right, #0052CC, #0084FF);
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "menu" not in st.session_state:
    st.session_state.menu = "홈"

# 메뉴 버튼들
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 홈", use_container_width=True, type="primary" if st.session_state.menu == "홈" else "secondary"):
        st.session_state.menu = "홈"

with col2:
    if st.button("🧬 영양 성분 분석", use_container_width=True, type="primary" if st.session_state.menu == "영양 성분 분석" else "secondary"):
        st.session_state.menu = "영양 성분 분석"

with col3:
    if st.button("💰 가격 정보", use_container_width=True, type="primary" if st.session_state.menu == "가격 정보" else "secondary"):
        st.session_state.menu = "가격 정보"

with col4:
    if st.button("💡 건강 추천", use_container_width=True, type="primary" if st.session_state.menu == "건강 추천" else "secondary"):
        st.session_state.menu = "건강 추천"

st.markdown("---")

# 메인 컨텐츠 표시
if st.session_state.menu == "홈":
    show_home()
elif st.session_state.menu == "영양 성분 분석":
    show_nutrition_analysis()
elif st.session_state.menu == "가격 정보":
    show_price_info()
elif st.session_state.menu == "건강 추천":
    show_health_recommendations()
