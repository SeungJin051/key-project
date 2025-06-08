import streamlit as st
import pandas as pd
import os
from src.utils.utils import get_fruit_nutrition

def get_health_recommendations(health_goal, age_group, gender_special):
    """건강 목표, 연령대, 성별에 따른 과일 추천"""
    
    # 건강 목표별 추천 과일
    health_goal_fruits = {
        "다이어트": {
            "fruits": ["사과", "자두", "딸기", "블루베리", "키위", "자몽"],
            "reason": "저칼로리, 높은 식이섬유로 포만감을 주며 신진대사를 촉진합니다.",
            "nutrients": ["식이섬유", "비타민C", "칼륨"]
        },
        "면역력 증진": {
            "fruits": ["오렌지", "키위", "딸기", "블루베리", "망고", "파파야"],
            "reason": "비타민C와 항산화 물질이 풍부하여 면역체계를 강화합니다.",
            "nutrients": ["비타민C", "항산화물질", "비타민A"]
        },
        "피부 건강": {
            "fruits": ["아보카도", "망고", "파파야", "딸기", "석류", "블루베리"],
            "reason": "비타민E, 비타민C, 항산화 물질이 피부 재생과 콜라겐 생성을 돕습니다.",
            "nutrients": ["비타민E", "비타민C", "베타카로틴"]
        },
        "소화 개선": {
            "fruits": ["파인애플", "파파야", "바나나", "키위", "사과", "배"],
            "reason": "소화효소와 식이섬유가 풍부하여 장 건강을 개선합니다.",
            "nutrients": ["식이섬유", "소화효소", "칼륨"]
        },
        "빈혈 예방": {
            "fruits": ["석류", "건포도", "살구", "체리", "딸기", "키위"],
            "reason": "철분과 비타민C가 풍부하여 혈액 생성과 철분 흡수를 돕습니다.",
            "nutrients": ["철분", "비타민C", "엽산"]
        }
    }
    
    # 연령대별 추천 과일
    age_group_fruits = {
        "어린이 (5-12세)": {
            "fruits": ["바나나", "사과", "딸기", "포도", "오렌지", "복숭아"],
            "reason": "성장에 필요한 영양소가 풍부하고 달콤한 맛으로 아이들이 좋아합니다.",
            "nutrients": ["칼슘", "비타민C", "자연당"]
        },
        "청소년 (13-19세)": {
            "fruits": ["바나나", "사과", "키위", "블루베리", "망고", "아보카도"],
            "reason": "두뇌 발달과 에너지 공급에 필요한 영양소를 제공합니다.",
            "nutrients": ["오메가3", "비타민B", "항산화물질"]
        },
        "성인 (20-64세)": {
            "fruits": ["사과", "키위", "아보카도", "블루베리", "자몽", "석류"],
            "reason": "만성질환 예방과 건강 유지에 도움이 되는 항산화 물질이 풍부합니다.",
            "nutrients": ["항산화물질", "식이섬유", "칼륨"]
        },
        "노인 (65세 이상)": {
            "fruits": ["바나나", "사과", "배", "오렌지", "키위", "멜론"],
            "reason": "소화가 쉽고 혈압 조절과 뼈 건강에 도움이 되는 영양소를 함유합니다.",
            "nutrients": ["칼륨", "칼슘", "비타민D"]
        }
    }
    
    # 성별/특수상황별 추천 과일
    gender_special_fruits = {
        "남성": {
            "fruits": ["토마토", "수박", "아보카도", "바나나", "석류", "블루베리"],
            "reason": "남성 건강에 중요한 라이코펜과 아연이 풍부합니다.",
            "nutrients": ["라이코펜", "아연", "마그네슘"]
        },
        "여성": {
            "fruits": ["석류", "딸기", "아보카도", "키위", "체리", "크랜베리"],
            "reason": "여성 호르몬 균형과 철분 보충에 도움이 됩니다.",
            "nutrients": ["철분", "엽산", "안토시아닌"]
        },
        "임산부": {
            "fruits": ["아보카도", "바나나", "오렌지", "망고", "사과", "딸기"],
            "reason": "태아 발달에 필요한 엽산과 비타민이 풍부합니다.",
            "nutrients": ["엽산", "비타민B6", "칼슘"]
        },
        "갱년기 여성": {
            "fruits": ["석류", "체리", "아보카도", "블루베리", "자두", "무화과"],
            "reason": "호르몬 변화에 따른 증상 완화와 뼈 건강에 도움이 됩니다.",
            "nutrients": ["식물성 에스트로겐", "칼슘", "마그네슘"]
        },
        "해당없음": {
            "fruits": ["사과", "바나나", "오렌지", "키위", "딸기", "포도"],
            "reason": "일반적으로 건강에 도움이 되는 기본적인 과일들입니다.",
            "nutrients": ["비타민C", "식이섬유", "칼륨"]
        }
    }
    
    # 추천 결과 조합
    recommendations = {
        "health_goal": health_goal_fruits.get(health_goal, health_goal_fruits["면역력 증진"]),
        "age_group": age_group_fruits.get(age_group, age_group_fruits["성인 (20-64세)"]),
        "gender_special": gender_special_fruits.get(gender_special, gender_special_fruits["해당없음"])
    }
    
    # 공통 과일 찾기
    all_recommended_fruits = set(recommendations["health_goal"]["fruits"] + 
                               recommendations["age_group"]["fruits"] + 
                               recommendations["gender_special"]["fruits"])
    
    return recommendations, list(all_recommended_fruits)

def show_fruit_card(fruit_name, reason, nutrients, category):
    """과일 추천 카드 표시"""
    # 과일 이미지 매핑
    fruit_image_mapping = {
        '사과': 'apple', '배': 'pear', '복숭아': 'peach', '포도': 'grape',
        '망고': 'mango', '키위': 'kiwi', '바나나': 'banana', '딸기': 'strawberry',
        '오렌지': 'orange', '레몬': 'lemon', '자두': 'plum', '체리': 'cherry',
        '블루베리': 'blueberry', '수박': 'watermelon', '멜론': 'melon', '참외': 'koreamelon',
        '파인애플': 'pineapple', '아보카도': 'avocado', '석류': 'pomegranate', '무화과': 'fig',
        '감': 'persimmon', '자몽': 'grapefruit', '용과': 'dragonfruit', '망고스틴': 'mangosteen',
        '두리안': 'durian', '스타프루트': 'starfruit', '구아바': 'guava', '리치': 'lychee',
        '파파야': 'papaya', '체리모야': 'cherimoya', '람부탄': 'rambutan', '살구': 'apricot',
        '유자': 'yuzu', '감귤': 'tangerine', '귤': 'tangerine', '청포도': 'greengrape',
        '적포도': 'redgrape', '매실': 'plum', '크랜베리': 'cranberry', '건포도': 'raisin',
        '토마토': 'tomato'
    }
    
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="card-header {category}-header">
            <h4>{fruit_name}</h4>
        </div>
        <div class="card-content">
            <p class="reason">{reason}</p>
            <div class="nutrients">
                <strong>주요 영양소:</strong>
                <div class="nutrient-tags">
                    {' '.join([f'<span class="nutrient-tag">{nutrient}</span>' for nutrient in nutrients])}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_health_recommendations():
    # CSS 스타일 추가
    st.markdown("""
    <style>
    /* 메인 콘텐츠 영역 max-width 설정 */
    .main .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="title">개인 맞춤 과일 추천</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">당신의 건강 목표와 상황에 맞는 최적의 과일을 찾아보세요</div>', unsafe_allow_html=True)
    
    # CSS 스타일 추가
    st.markdown("""
    <style>
    .recommendation-form {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .form-section {
        margin-bottom: 1.5rem;
    }
    .form-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        display: block;
    }
    .recommendation-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .recommendation-card:hover {
        transform: translateY(-5px);
    }
    .card-header {
        padding: 1rem 1.5rem;
        color: white;
        font-weight: 600;
    }
    .health_goal-header {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
    }
    .age_group-header {
        background: linear-gradient(135deg, #3498db, #2980b9);
    }
    .gender_special-header {
        background: linear-gradient(135deg, #9b59b6, #8e44ad);
    }
    .card-content {
        padding: 1.5rem;
    }
    .reason {
        color: #34495e;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .nutrients {
        margin-top: 1rem;
    }
    .nutrient-tags {
        margin-top: 0.5rem;
    }
    .nutrient-tag {
        display: inline-block;
        background: linear-gradient(135deg, #0064FF, #00B8D4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem 0.3rem 0.2rem 0;
    }
    .final-recommendations {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
    }
    .final-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }
    .fruit-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    .fruit-final-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .fruit-final-card:hover {
        transform: scale(1.05);
    }
    .fruit-final-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .submit-btn {
        background: linear-gradient(135deg, #0064FF, #00B8D4);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    .submit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 100, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 추천 폼
    st.markdown("### 📝 개인 정보 입력")
    
    with st.form("health_recommendation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            health_goal = st.selectbox(
                "🎯 건강 목표",
                ["다이어트", "면역력 증진", "피부 건강", "소화 개선", "빈혈 예방"]
            )
            
            age_group = st.selectbox(
                "👥 연령대",
                ["어린이 (5-12세)", "청소년 (13-19세)", "성인 (20-64세)", "노인 (65세 이상)"]
            )
        
        with col2:
            gender_special = st.selectbox(
                "🚻 성별/특수상황",
                ["남성", "여성", "임산부", "갱년기 여성", "해당없음"]
            )
        
        submitted = st.form_submit_button("🔍 맞춤 과일 추천받기", use_container_width=True)
    
    # 폼 제출 시 추천 결과 표시
    if submitted:
        recommendations, final_fruits = get_health_recommendations(health_goal, age_group, gender_special)
        
        # 최종 추천 과일
        st.markdown("---")
        st.markdown("## 🏆 당신을 위한 맞춤 추천 과일")
        st.markdown(f"**{health_goal}**, **{age_group}**, **{gender_special}** 조건을 종합하여 추천드립니다")
        
        # 추천 과일 그리드로 표시
        cols = st.columns(min(6, len(final_fruits)))
        for i, fruit in enumerate(final_fruits[:6]):  # 최대 6개까지만 표시
            with cols[i % len(cols)]:
                # 과일 이미지 표시
                fruit_image_mapping = {
                    '사과': 'apple', '배': 'pear', '복숭아': 'peach', '포도': 'grape',
                    '망고': 'mango', '키위': 'kiwi', '바나나': 'banana', '딸기': 'strawberry',
                    '오렌지': 'orange', '레몬': 'lemon', '자두': 'plum', '체리': 'cherry',
                    '블루베리': 'blueberry', '수박': 'watermelon', '멜론': 'melon', '참외': 'koreamelon',
                    '파인애플': 'pineapple', '아보카도': 'avocado', '석류': 'pomegranate', '무화과': 'fig',
                    '토마토': 'tomato', '크랜베리': 'cranberry'
                }
                
                image_filename = fruit_image_mapping.get(fruit, 'apple')
                image_path = os.path.join('assets/images', f"{image_filename}.png")
                
                if os.path.exists(image_path):
                    st.image(image_path, use_column_width=True)
                    st.markdown(f"<div style='text-align: center; font-weight: 600; margin-top: 0.5rem;'>{fruit}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background: #f8f9fa; padding: 2rem; border-radius: 10px; text-align: center; font-weight: 600;'>{fruit}</div>", unsafe_allow_html=True)
        
        # 선택한 조건별 간단한 설명
        st.markdown("---")
        st.markdown("## 💡 추천 이유")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**🎯 {health_goal}**")
            st.write(recommendations["health_goal"]["reason"])
            st.markdown(f"**주요 영양소:** {', '.join(recommendations['health_goal']['nutrients'])}")
        
        with col2:
            st.markdown(f"**👥 {age_group}**")
            st.write(recommendations["age_group"]["reason"])
            st.markdown(f"**주요 영양소:** {', '.join(recommendations['age_group']['nutrients'])}")
        
        with col3:
            st.markdown(f"**🚻 {gender_special}**")
            st.write(recommendations["gender_special"]["reason"])
            st.markdown(f"**주요 영양소:** {', '.join(recommendations['gender_special']['nutrients'])}")
        
        # 추가 건강 팁
        st.markdown("---")
        st.markdown("## 🍎 섭취 가이드")
        st.success(f"""
        **{health_goal}**을 위한 과일 섭취 팁:
        - 하루에 2-3가지 다양한 과일을 섭취하세요
        - 가능한 한 신선한 제철 과일을 선택하세요
        - 과일 주스보다는 생과일을 드시는 것이 좋습니다
        - 개인의 알레르기나 질환이 있다면 전문의와 상담 후 섭취하세요
        """) 