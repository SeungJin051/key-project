import streamlit as st
import pandas as pd
from datetime import datetime
import os
from src.utils.utils import get_seasonal_fruits

def show_home():
    # 메인 타이틀
    st.markdown('<div class="title">과일로 시작하는 건강한 하루</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">당신의 건강 목표에 맞는 최적의 과일을 찾아보세요. 계절별 신선한 과일과 함께 건강한 라이프스타일을 시작하세요.</div>', unsafe_allow_html=True)
    
    # 현재 월의 계절 과일 추천
    current_month = datetime.now().month
    seasonal_fruits = get_seasonal_fruits(current_month)
    
    if seasonal_fruits:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight-title">{current_month}월 제철 과일 추천</div>', unsafe_allow_html=True)
        st.markdown('<div class="highlight-desc">지금이 가장 맛있고 영양가 높은 제철 과일입니다. 신선함과 영양을 모두 만족시키는 과일로 건강한 하루를 시작하세요.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # CSS 스타일 추가
    st.markdown("""
    <style>
    /* 메인 콘텐츠 영역 max-width 설정 */
    .main .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    .modern-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: none;
        overflow: hidden;
        position: relative;
        height: 350px; /* 높이 조정 */
        display: flex;
        flex-direction: column;
    }
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    .modern-card-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        display: inline-block;
        /* 그라디언트 색상 제거 */
    }
    .modern-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
        color: #222;
    }
    .modern-card-desc {
        color: #666;
        margin-bottom: 20px;
        line-height: 1.6;
        flex-grow: 1; /* 내용이 늘어나도록 설정 */
        min-height: 80px; /* 최소 높이 설정 */
    }
    .card-footer {
        margin-top: auto; /* 하단에 고정 */
    }
    .modern-btn {
        background: linear-gradient(135deg, #0064FF, #00B8D4);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-align: center;
    }
    .modern-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 100, 255, 0.3);
    }
    .modern-tips-card {
        border-radius: 20px;
        padding: 25px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        height: 280px; /* 고정 높이 설정 */
        display: flex;
        flex-direction: column;
    }
    .modern-tips-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(to bottom, #0064FF, #00B8D4);
    }
    .modern-tips-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 15px;
        color: #222;
        padding-left: 10px;
    }
    .modern-tips-desc {
        color: #444;
        line-height: 1.7;
        padding-left: 10px;
        flex-grow: 1; /* 내용이 늘어나도록 설정 */
    }
    .modern-tips-icon {
        font-size: 2rem;
        margin-bottom: 15px;
        display: inline-block;
        /* 색상 제거 - 이모지 원래 색상 유지 */
    }
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 3개의 주요 기능 섹션 - 모던 카드 디자인 적용
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 첫 번째 기능 카드 - 영양 성분 분석 (모던 디자인)
        st.markdown("""
        <div class="modern-card">
            <div class="modern-card-icon">📊</div>
            <div class="modern-card-title">영양 성분 분석</div>
            <div class="modern-card-desc">과일별 상세 영양 성분을 확인하고 비교해보세요. 비타민, 미네랄, 항산화 물질 등 건강에 도움이 되는 영양소를 한눈에 확인할 수 있습니다.</div>
            <div class="card-footer">
                <div class="tag-container">
                    <span class="tag">비타민</span>
                    <span class="tag">미네랄</span>
                    <span class="tag">항산화</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("영양 성분 분석 보기", key="nutrition"):
            st.session_state.menu = "영양 성분 분석"
            st.experimental_rerun()
    
    with col2:
        # 두 번째 기능 카드 - 시즌별 가격 정보 (모던 디자인)
        st.markdown("""
        <div class="modern-card">
            <div class="modern-card-icon">💰</div>
            <div class="modern-card-title">시즌별 가격 정보</div>
            <div class="modern-card-desc">계절별 과일 가격 변동을 확인하고 합리적인 소비를 계획하세요. 최적의 구매 시기를 찾아 경제적인 소비를 도와드립니다.</div>
            <div class="card-footer">
                <div class="tag-container">
                    <span class="tag">가격 트렌드</span>
                    <span class="tag">시즌</span>
                    <span class="tag">구매 가이드</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("가격 정보 보기", key="price"):
            st.session_state.menu = "가격 정보"
            st.experimental_rerun()
    
    with col3:
        # 세 번째 기능 카드 - 건강 맞춤 추천 (모던 디자인)
        st.markdown("""
        <div class="modern-card">
            <div class="modern-card-icon">❤️</div>
            <div class="modern-card-title">건강 맞춤 추천</div>
            <div class="modern-card-desc">당신의 건강 목표에 맞는 최적의 과일을 추천받으세요. 다이어트, 면역력 강화, 피부 건강 등 목적별 맞춤 추천을 제공합니다.</div>
            <div class="card-footer">
                <div class="tag-container">
                    <span class="tag">맞춤 추천</span>
                    <span class="tag">건강 목표</span>
                    <span class="tag">영양 가이드</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("건강 추천 보기", key="recommend"):
            st.session_state.menu = "건강 추천"
            st.experimental_rerun()
    
    # 이달의 인기 과일 섹션
    st.markdown('<div class="seasonal-title">이달의 제철 과일</div>', unsafe_allow_html=True)
    
    # 과일 이름을 이미지 파일명으로 매핑하는 딕셔너리
    fruit_image_mapping = {
        '사과': 'apple',
        '살구': 'apricot',
        '아보카도': 'avocado',
        '바나나': 'banana',
        '블루베리': 'blueberry',
        '체리모야': 'cherimoya',
        '체리': 'cherry',
        '용과': 'dragonfruit',
        '두리안': 'durian',
        '무화과': 'fig',
        '포도': 'grape',
        '자몽': 'grapefruit',
        '청포도': 'greengrape',
        '구아바': 'guava',
        '키위': 'kiwi',
        '참외': 'koreamelon',
        '자두': 'plum',
        '한국 자두': 'koreanplum',
        '레몬': 'lemon',
        '리치': 'lychee',
        '망고': 'mango',
        '망고스틴': 'mangosteen',
        '멜론': 'melon',
        '오렌지': 'orange',
        '파파야': 'papaya',
        '복숭아': 'peach',
        '배': 'pear',
        '감': 'persimmon',
        '파인애플': 'pineapple',
        '석류': 'pomegranate',
        '람부탄': 'rambutan',
        '적포도': 'redgrape',
        '스타프루트': 'starfruit',
        '딸기': 'strawberry',
        '귤': 'tangerine',
        '감귤': 'tangerine',
        '수박': 'watermelon',
        '백포도': 'white',
        '황금키위': 'yellow',
        '유자': 'yuzu',
        '매실': 'plum'
    }

    # 영어 과일 이름을 이미지 파일명에 직접 사용할 수 있는 매핑
    english_fruit_mapping = {
        'apple': 'apple',
        'apricot': 'apricot',
        'avocado': 'avocado',
        'banana': 'banana',
        'blueberry': 'blueberry',
        'cherimoya': 'cherimoya',
        'cherry': 'cherry',
        'dragonfruit': 'dragonfruit',
        'dragon fruit': 'dragonfruit',
        'durian': 'durian',
        'fig': 'fig',
        'grape': 'grape',
        'grapefruit': 'grapefruit',
        'green grape': 'greengrape',
        'guava': 'guava',
        'kiwi': 'kiwi',
        'korean melon': 'koreamelon',
        'plum': 'plum',
        'korean plum': 'koreanplum',
        'lemon': 'lemon',
        'lychee': 'lychee',
        'mango': 'mango',
        'mangosteen': 'mangosteen',
        'melon': 'melon',
        'orange': 'orange',
        'papaya': 'papaya',
        'peach': 'peach',
        'pear': 'pear',
        'persimmon': 'persimmon',
        'pineapple': 'pineapple',
        'pomegranate': 'pomegranate',
        'rambutan': 'rambutan',
        'red grape': 'redgrape',
        'star fruit': 'starfruit',
        'starfruit': 'starfruit',
        'strawberry': 'strawberry',
        'tangerine': 'tangerine',
        'watermelon': 'watermelon',
        'yuzu': 'yuzu'
    }
    
    # 계절 과일 표시
    if seasonal_fruits:
        cols = st.columns(4)
        for idx, fruit in enumerate(seasonal_fruits[:4]):
            with cols[idx % 4]:
                # Streamlit expander를 사용하여 카드 형태 구현
                fruit_name = fruit['Name']
                fruit_kind = fruit['Kind']
                with st.expander(f"**{fruit['Name']} ({fruit_kind})**", expanded=True):
                    # 과일 이미지 표시 (로컬 이미지 폴더에서 가져오기)
                    image_folder = 'assets/images'
                    image_found = False
                    
                    # 매핑 딕셔너리를 사용하여 올바른 이미지 파일명 찾기
                    image_filename = None
                    
                    # 한글 이름으로 매핑 시도
                    if fruit['Name'] in fruit_image_mapping:
                        image_filename = fruit_image_mapping[fruit['Name']]
                    # 영어 이름으로 매핑 시도
                    elif fruit_name.lower() in english_fruit_mapping:
                        image_filename = english_fruit_mapping[fruit_name.lower()]
                    # Kind 필드를 기반으로 이미지 매핑 시도
                    elif fruit_kind:
                        # Kind에서 언더스코어를 제거하고 첫 번째 단어만 사용
                        kind_base = fruit_kind.split('_')[0]
                        if kind_base in english_fruit_mapping:
                            image_filename = english_fruit_mapping[kind_base]
                        else:
                            image_filename = kind_base
                    # 그 외에는 원래 이름을 소문자로 변환하여 사용
                    else:
                        image_filename = fruit_name.lower()
                    
                    # 가능한 확장자 시도
                    if image_filename:
                        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
                        for ext in possible_extensions:
                            image_path = os.path.join(image_folder, f"{image_filename}{ext}")
                            if os.path.exists(image_path):
                                st.image(image_path, width=180)
                                image_found = True
                                break
                    
                    # 이미지를 찾지 못한 경우, 각 단어 별로 매핑 시도
                    if not image_found and ' ' in fruit_name:
                        fruit_parts = fruit_name.lower().split()
                        for part in fruit_parts:
                            if part in english_fruit_mapping:
                                image_filename = english_fruit_mapping[part]
                                for ext in possible_extensions:
                                    image_path = os.path.join(image_folder, f"{image_filename}{ext}")
                                    if os.path.exists(image_path):
                                        st.image(image_path, width=180)
                                        image_found = True
                                        break
                            if image_found:
                                break
                    
                    # 그래도 이미지를 찾지 못한 경우 기본 이미지나 메시지 표시
                    if not image_found:
                        # 대부분의 과일 이미지를 찾기 위한 마지막 시도
                        fallback_image = None
                        for img_file in os.listdir(image_folder):
                            if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                base_name = os.path.splitext(img_file)[0].lower()
                                if fruit_name.lower() in base_name or base_name in fruit_name.lower():
                                    fallback_image = os.path.join(image_folder, img_file)
                                    break
                        
                        if fallback_image and os.path.exists(fallback_image):
                            st.image(fallback_image, width=180)
                        else:
                            # 아예 이미지를 찾지 못하면 기본 아이콘 표시
                            st.markdown("## 🍎", unsafe_allow_html=True)
                    
                    # 과일 정보 (새로운 스키마에 맞게 수정)
                    if fruit['coupang_price'] and fruit['coupang_price'] > 0:
                        st.write(f"💰 **가격:** {fruit['coupang_price']}원/100g")
                    else:
                        st.write(f"💰 **가격:** 정보 없음")
                    
                    st.write(f"🏷️ **품종:** {fruit_kind}")
                    st.write(f"🛒 **판매처:** 쿠팡")
                    
                    # 과일별 간단한 정보 추가 (하드코딩된 기본 정보)
                    basic_info = {
                        '사과': {'calories': '52', 'benefits': '비타민C, 식이섬유 풍부'},
                        '배': {'calories': '44', 'benefits': '수분 많음, 소화 도움'},
                        '복숭아': {'calories': '51', 'benefits': '비타민A, 항산화 성분'},
                        '포도': {'calories': '69', 'benefits': '항산화 성분, 혈관 건강'},
                        '망고': {'calories': '60', 'benefits': '비타민A, 베타카로틴'},
                        '키위': {'calories': '61', 'benefits': '비타민C 매우 풍부'},
                        '바나나': {'calories': '89', 'benefits': '칼륨, 에너지 공급'},
                        '딸기': {'calories': '32', 'benefits': '비타민C, 엽산'},
                        '오렌지': {'calories': '47', 'benefits': '비타민C, 구연산'},
                        '레몬': {'calories': '17', 'benefits': '비타민C, 해독 작용'}
                    }
                    
                    if fruit['Name'] in basic_info:
                        info = basic_info[fruit['Name']]
                        st.write(f"🔥 **칼로리:** {info['calories']} kcal/100g")
                        st.write(f"✨ **주요 효능:** {info['benefits']}")
                    else:
                        st.write(f"📝 **특징:** 신선하고 영양가 풍부한 과일")
    
    # 건강 팁 섹션 - 모던 디자인 적용
    st.markdown('<div class="seasonal-title">건강한 과일 섭취 팁</div>', unsafe_allow_html=True)
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        # 첫 번째 팁 카드 (모던 디자인)
        st.markdown("""
        <div class="modern-tips-card">
            <div class="modern-tips-icon">⏰</div>
            <div class="modern-tips-title">과일 섭취의 최적 시간</div>
            <div class="modern-tips-desc">아침 식사와 함께 과일을 섭취하면 하루 에너지를 충전할 수 있습니다. 비타민 C가 풍부한 과일은 아침에, 소화를 돕는 과일은 식후에, 그리고 수면에 도움이 되는 과일은 취침 전에 섭취하는 것이 좋습니다.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col2:
        # 두 번째 팁 카드 (모던 디자인)
        st.markdown("""
        <div class="modern-tips-card">
            <div class="modern-tips-icon">❄️</div>
            <div class="modern-tips-title">과일 보관 방법</div>
            <div class="modern-tips-desc">사과, 배는 냉장 보관이 좋으며, 바나나, 파인애플은 실온 보관이 적합합니다. 딸기, 블루베리는 씻지 않은 상태로 냉장 보관하고, 수박, 참외는 먹기 전에 냉장고에 1~2시간 정도 두었다가 먹으면 더 시원하고 맛있게 즐길 수 있습니다.</div>
        </div>
        """, unsafe_allow_html=True) 
        