import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
from src.utils.utils import get_fruit_nutrition, get_fruit_varieties, search_fruits

def show_nutrition_analysis():
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
    
    st.markdown('<div class="title">영양 성분 분석</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">다양한 과일의 영양 성분을 확인하고 비교해보세요</div>', unsafe_allow_html=True)
    
    # 영양 성분 데이터 가져오기
    fruits = get_fruit_nutrition()
    fruits_df = pd.DataFrame([dict(fruit) for fruit in fruits])
    
    # 세션 상태 초기화
    if 'selected_fruit' not in st.session_state:
        st.session_state.selected_fruit = None
    
    # 검색어 변수 초기화 (기본값으로 빈 문자열 설정)
    search_term = ""
    
    # 선택된 과일 상세 정보 표시
    if st.session_state.selected_fruit:
        # 해당 과일의 모든 품종 가져오기
        fruit_varieties_data = get_fruit_varieties(st.session_state.selected_fruit)
        fruit_varieties_df = pd.DataFrame([dict(fruit) for fruit in fruit_varieties_data])
        
        if not fruit_varieties_df.empty:
            # 과일 이름과 대표 이미지 (첫 번째 품종의 이미지 사용)
            first_variety = fruit_varieties_df.iloc[0]
            
            # 나무위키 스타일 상세 페이지
            st.markdown(f"""
            <div class="wiki-card">
                <div class="wiki-title">{first_variety['Name']}</div>
                <div class="wiki-content">
                    {first_variety['Name']}은(는) 다양한 영양소를 함유하고 있는 과일로, 여러 품종이 있습니다.
                    100g당 평균 가격은 약 {fruit_varieties_df['coupang_price'].mean():.0f}원입니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 기본 정보 섹션 시작
            st.markdown('<div class="wiki-section">', unsafe_allow_html=True)
            st.markdown('<div class="wiki-section-title">기본 정보</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # 이미지 표시 로직 (기존과 동일하게 유지하되 fruit_name 대신 Name 사용)
                fruit_name = first_variety['Name'].lower()
                
                # 과일 이름을 이미지 파일명으로 매핑하는 딕셔너리
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
                    '적포도': 'redgrape', '매실': 'plum'
                }
                
                image_filename = fruit_image_mapping.get(first_variety['Name'], fruit_name)
                image_path = os.path.join('assets/images', f"{image_filename}.png")
                
                if os.path.exists(image_path):
                    st.image(image_path, caption=f"{first_variety['Name']}")
                else:
                    st.info("이미지를 찾을 수 없습니다.")
            
            with col2:
                st.markdown("""
                <div class="wiki-table" style="width: 100%;">
                    <table style="width: 100%;">
                        <tr>
                            <th>분류</th>
                            <td>과일</td>
                        </tr>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                        <tr>
                            <th>평균 가격</th>
                            <td>{fruit_varieties_df['coupang_price'].mean():.0f}원/100g</td>
                        </tr>
                        <tr>
                            <th>최저 가격</th>
                            <td>{fruit_varieties_df['coupang_price'].min():.0f}원/100g</td>
                        </tr>
                        <tr>
                            <th>품종 수</th>
                            <td>{len(fruit_varieties_df)}</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            # 기본 정보 섹션 종료
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 품종별 비교 그래프 섹션
            st.markdown('<div class="wiki-section">', unsafe_allow_html=True)
            st.markdown('<div class="wiki-section-title">품종별 가격 비교</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 가격 비교 그래프
            fig_price = px.bar(
                fruit_varieties_df, 
                x='Kind', 
                y='coupang_price',
                title=f"{first_variety['Name']} 품종별 가격 (원/100g)",
                labels={'Kind': '품종', 'coupang_price': '가격 (원/100g)'},
                color='coupang_price',
                color_continuous_scale='Blues'
            )
            fig_price.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)')
            )
            st.plotly_chart(fig_price, use_container_width=True)
            
            # 품종별 상세 정보 섹션
            st.markdown('<div class="wiki-section">', unsafe_allow_html=True)
            st.markdown('<div class="wiki-section-title">품종별 상세 정보</div>', unsafe_allow_html=True)
            st.markdown('<div class="wiki-quote">다양한 품종별 특성을 확인하고 자신에게 맞는 과일을 선택하세요.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 품종별 데이터 테이블로 표시
            st.dataframe(
                fruit_varieties_df[['Kind', 'coupang_price']],
                use_container_width=True,
                column_config={
                    "Kind": "품종",
                    "coupang_price": "가격 (원/100g)"
                }
            )
            
            # 품종별 카드 섹션
            st.markdown('<div class="wiki-section">', unsafe_allow_html=True)
            st.markdown('<div class="wiki-section-title">품종 카드</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 품종별 카드 표시
            cards_per_row = 4
            rows = [fruit_varieties_df.iloc[i:i+cards_per_row] for i in range(0, len(fruit_varieties_df), cards_per_row)]
            
            for row in rows:
                cols = st.columns(cards_per_row)
                for i, (_, variety) in enumerate(row.iterrows()):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="wiki-card" style="height: 100%;">
                            <div class="wiki-title" style="font-size: 1.2rem; text-align: center;">{variety['Kind']}</div>
                            <table class="wiki-table">
                                <tr>
                                    <th>가격</th>
                                    <td>{variety['coupang_price']} 원/100g</td>
                                </tr>
                                <tr>
                                    <th>쇼핑몰</th>
                                    <td>쿠팡</td>
                                </tr>
                            </table>
                        </div>
                        """, unsafe_allow_html=True)
            
            # 위키 참고 자료 섹션
            st.markdown('<div class="wiki-section">', unsafe_allow_html=True)
            st.markdown('<div class="wiki-section-title">참고 자료</div>', unsafe_allow_html=True)
            st.markdown('<div class="wiki-reference">[1] 쿠팡</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # wiki-card 닫기
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 돌아가기 버튼
            if st.button("과일 목록으로 돌아가기"):
                st.session_state.selected_fruit = None
                st.experimental_rerun()
    else:
        # 검색 기능 (선택된 과일이 없을 때만 표시)
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_term = st.text_input("과일 이름 검색", "")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 과일 종류별로 중복 제거하여 대표 과일만 표시
        unique_fruits = fruits_df.drop_duplicates(subset=['Name'])
        
        # 검색 결과 필터링
        if search_term:
            filtered_fruits = unique_fruits[unique_fruits['Name'].str.contains(search_term)]
        else:
            filtered_fruits = unique_fruits
        
        # 과일 그리드 표시
        st.markdown("### 과일 목록")
        
        # 과일이 없는 경우 처리
        if filtered_fruits.empty:
            st.warning("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")
        else:
            # 한 행에 4개씩 표시
            cols_per_row = 4
            
            # 과일 데이터가 있을 경우
            for i in range(0, len(filtered_fruits), cols_per_row):
                # 현재 행의 과일들
                row_fruits = filtered_fruits.iloc[i:min(i+cols_per_row, len(filtered_fruits))]
                
                # 컬럼 생성
                cols = st.columns(cols_per_row)
                
                 
                 
                # 각 컬럼에 과일 카드 배치
                for j, (_, fruit) in enumerate(row_fruits.iterrows()):
                    with cols[j]:
                        fruit_id = fruit['id']
                        
                        # 과일 이름을 이미지 파일명으로 매핑
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
                            '적포도': 'redgrape', '매실': 'plum'
                        }
                        
                        # 카드 스타일의 expander 사용
                        with st.expander(f"**{fruit['Name']}**", expanded=True):
                            # 이미지 표시
                            image_filename = fruit_image_mapping.get(fruit['Name'], fruit['Name'].lower())
                            image_path = os.path.join('assets/images', f"{image_filename}.png")
                            
                            if os.path.exists(image_path):
                                st.image(image_path, width=200, use_column_width=True)
                            else:
                                st.info("이미지 없음")
                            
                            # 과일 정보 표시 (새로운 스키마에 맞게)
                            if fruit['coupang_price'] and fruit['coupang_price'] > 0:
                                st.write(f"💰 **가격:** {fruit['coupang_price']}원/100g")
                            else:
                                st.write(f"💰 **가격:** 정보 없음")
                            
                            st.write(f"🏷️ **품종:** {fruit['Kind']}")
                            st.write(f"🛒 **판매처:** 쿠팡")
                            
                            # 기본 영양 정보 (하드코딩)
                            basic_info = {
                                '사과': {'calories': '52', 'benefits': '비타민C, 식이섬유 풍부'},
                                '배': {'calories': '44', 'benefits': '수분 많음, 소화 도움'},
                                '복숭아': {'calories': '51', 'benefits': '비타민A, 항산화 성분'},
                                '포도': {'calories': '69', 'benefits': '항산화 성분, 혈관 건강'},
                                '망고': {'calories': '60', 'benefits': '비타민A, 베타카로틴'},
                                '키위': {'calories': '61', 'benefits': '비타민C 매우 풍부'},
                                '바나나': {'calories': '89', 'benefits': '칼륨, 에너지 공급'},
                                '딸기': {'calories': '32', 'benefits': '비타민C, 엽산'}
                            }
                            
                            if fruit['Name'] in basic_info:
                                info = basic_info[fruit['Name']]
                                st.write(f"🔥 **칼로리:** {info['calories']} kcal/100g")
                                st.write(f"✨ **주요 효능:** {info['benefits']}")
                            
                            # 버튼
                            if st.button(f"{fruit['Name']} 상세 정보", key=f"fruit_{fruit_id}"):
                                st.session_state.selected_fruit = fruit['Name']
                                st.experimental_rerun()
                        
                        # 구분선
                        st.markdown("<hr style='border: 1px solid #f0f0f0; margin-top: 10px;'>", unsafe_allow_html=True) 