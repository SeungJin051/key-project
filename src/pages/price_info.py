import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import os
from datetime import datetime, timedelta
import numpy as np

def get_db_connection():
    """데이터베이스 연결"""
    db_path = os.path.join('database', 'a.sqlite3')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_fruits_with_prices():
    """가격 정보가 있는 모든 과일 데이터 가져오기"""
    conn = get_db_connection()
    fruits = conn.execute('''
        SELECT * FROM fruit 
        WHERE coupang_price > 0
        ORDER BY Name, coupang_price
    ''').fetchall()
    conn.close()
    return fruits

def get_price_statistics():
    """가격 통계 정보 가져오기"""
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total_count,
            AVG(coupang_price) as avg_price,
            MIN(coupang_price) as min_price,
            MAX(coupang_price) as max_price,
            Name
        FROM fruit 
        WHERE coupang_price > 0
        GROUP BY Name
        ORDER BY avg_price DESC
    ''').fetchall()
    conn.close()
    return stats

def get_seasonal_price_trends():
    """계절별 가격 트렌드 데이터 생성 (시뮬레이션)"""
    fruits = get_all_fruits_with_prices()
    df = pd.DataFrame([dict(fruit) for fruit in fruits])
    
    # 계절별 가격 변동 시뮬레이션 (실제 데이터가 없으므로)
    seasons = ['봄', '여름', '가을', '겨울']
    seasonal_data = []
    
    for _, fruit in df.iterrows():
        base_price = fruit['coupang_price']
        for i, season in enumerate(seasons):
            # 계절별 가격 변동 (랜덤하게 생성)
            variation = np.random.uniform(0.8, 1.2)
            price = base_price * variation
            seasonal_data.append({
                'Name': fruit['Name'],
                'Kind': fruit['Kind'],
                'Season': season,
                'Price': price,
                'Base_Price': base_price
            })
    
    return pd.DataFrame(seasonal_data)

def create_premium_theme():
    """프리미엄 테마 설정"""
    return {
        'primary_colors': ['#0064FF', '#00B8D4', '#4285F4', '#1976D2', '#2196F3', '#03DAC6'],
        'gradient_colors': ['#0064FF', '#00B8D4', '#4285F4', '#1976D2', '#2196F3', '#03DAC6', '#00BCD4', '#009688'],
        'background_color': 'rgba(255, 255, 255, 0.95)',
        'grid_color': 'rgba(151, 151, 151, 0.1)',
        'text_color': '#2c3e50',
        'font_family': 'Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif'
    }

def get_fruit_category(fruit_name):
    """과실의 식물학적 분류 함수"""
    categories = {
        '이과': ['사과', '배'],
        '핵과': ['복숭아', '자두', '살구', '체리', '매실', '망고', '람부탄', '리치', '백도', '황도', '청도'],
        '장과류': ['포도', '블루베리', '감', '구아바', '망고스틴', '바나나', '스타프루트', '아보카도', '용과', '적포도', '청포도', '파파야'],
        '감과체': ['감귤', '레몬', '오렌지', '자몽', '유자'],
        '박과열매': ['수박', '멜론', '참외'],
        '취합과': ['딸기', '체리모야'],
        '다화과': ['파인애플', '무화과'],
        '석류과': ['석류'],
        '삭과': ['두리안'],
        '기타과실': []
    }
    
    for category, fruits in categories.items():
        if any(fruit in fruit_name for fruit in fruits):
            return category
    return '기타과실'

def create_category_overview_chart(df):
    """식물학적 분류별 개요 차트 생성"""
    # 식물학적 분류별 분류
    df['botanical_type'] = df['Name'].apply(get_fruit_category)
    
    # 식물학적 분류별 통계 계산
    category_stats = df.groupby('botanical_type')['coupang_price'].agg(['mean', 'min', 'max', 'count']).reset_index()
    category_stats.columns = ['botanical_type', 'avg_price', 'min_price', 'max_price', 'count']
    category_stats = category_stats.sort_values('avg_price', ascending=False)
    
    theme = create_premium_theme()
    
    # 식물학적 분류별 평균 가격 차트
    fig1 = go.Figure()
    
    fig1.add_trace(go.Bar(
        x=category_stats['botanical_type'],
        y=category_stats['avg_price'],
        name='평균 가격',
        marker=dict(
            color=category_stats['avg_price'],
            colorscale=[[0, '#0064FF'], [0.5, '#00B8D4'], [1, '#4285F4']],
            line=dict(color='white', width=2)
        ),
        text=[f'{v:.0f}원' for v in category_stats['avg_price']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>평균 가격: %{y:.0f}원<br>품종 수: %{customdata}개<extra></extra>',
        customdata=category_stats['count']
    ))
    
    fig1 = apply_premium_layout(fig1, "🍎 과실 식물학적 분류별 평균 가격", 400)
    fig1.update_xaxes(title_text="식물학적 분류", title_font_size=12)
    fig1.update_yaxes(title_text="평균 가격 (원)", title_font_size=12)
    
    # 식물학적 분류별 가격 범위 차트
    fig2 = go.Figure()
    
    for i, row in category_stats.iterrows():
        fig2.add_trace(go.Scatter(
            x=[row['botanical_type']],
            y=[row['avg_price']],
            mode='markers',
            marker=dict(
                size=20 + row['count'] * 3,
                color=theme['primary_colors'][i % len(theme['primary_colors'])],
                line=dict(color='white', width=2)
            ),
            name=row['botanical_type'],
            hovertemplate=f'<b>{row["botanical_type"]}</b><br>평균: {row["avg_price"]:.0f}원<br>최저: {row["min_price"]:.0f}원<br>최고: {row["max_price"]:.0f}원<br>품종 수: {row["count"]}개<extra></extra>',
            showlegend=False
        ))
        
        # 가격 범위 표시
        fig2.add_trace(go.Scatter(
            x=[row['botanical_type'], row['botanical_type']],
            y=[row['min_price'], row['max_price']],
            mode='lines',
            line=dict(color=theme['primary_colors'][i % len(theme['primary_colors'])], width=3),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig2 = apply_premium_layout(fig2, "📊 과실 식물학적 분류별 가격 분포", 400)
    fig2.update_xaxes(title_text="식물학적 분류", title_font_size=12)
    fig2.update_yaxes(title_text="가격 (원)", title_font_size=12)
    
    return fig1, fig2, category_stats, df

def create_category_detail_chart(df, selected_category):
    """선택된 식물학적 분류의 상세 분석 차트"""
    category_df = df[df['botanical_type'] == selected_category].copy()
    
    if len(category_df) == 0:
        return None, None
    
    theme = create_premium_theme()
    
    # 개별 과일 가격 비교
    fig1 = go.Figure()
    
    category_df_sorted = category_df.sort_values('coupang_price', ascending=True)
    
    fig1.add_trace(go.Bar(
        x=category_df_sorted['Name'] + ' (' + category_df_sorted['Kind'] + ')',
        y=category_df_sorted['coupang_price'],
        name='가격',
        marker=dict(
            color=category_df_sorted['coupang_price'],
            colorscale=[[0, '#E3F2FD'], [0.5, '#2196F3'], [1, '#0064FF']],
            line=dict(color='white', width=1)
        ),
        text=[f'{v:.0f}원' for v in category_df_sorted['coupang_price']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>가격: %{y:.0f}원/100g<extra></extra>'
    ))
    
    fig1 = apply_premium_layout(fig1, f"🔍 {selected_category} 과실별 가격 분석", 500)
    fig1.update_xaxes(title_text="과일 (품종)", title_font_size=12)
    fig1.update_yaxes(title_text="가격 (원/100g)", title_font_size=12)
    fig1.update_layout(xaxis_tickangle=45)
    
    # 통계 정보
    stats = {
        'count': len(category_df),
        'avg_price': category_df['coupang_price'].mean(),
        'min_price': category_df['coupang_price'].min(),
        'max_price': category_df['coupang_price'].max(),
        'std_price': category_df['coupang_price'].std()
    }
    
    # 가격 분포 히스토그램
    fig2 = go.Figure()
    
    fig2.add_trace(go.Histogram(
        x=category_df['coupang_price'],
        nbinsx=min(10, len(category_df)),
        name='가격 분포',
        marker=dict(
            color='rgba(0, 100, 255, 0.7)',
            line=dict(color='#0064FF', width=1)
        ),
        hovertemplate='가격 범위: %{x}<br>개수: %{y}<extra></extra>'
    ))
    
    fig2 = apply_premium_layout(fig2, f"📈 {selected_category} 가격 분포 분석", 400)
    fig2.update_xaxes(title_text="가격 (원)", title_font_size=12)
    fig2.update_yaxes(title_text="개수", title_font_size=12)
    
    return fig1, fig2, stats

def create_category_trend_chart(seasonal_trends):
    """식물학적 분류별 계절 트렌드 차트"""
    # 식물학적 분류별 분류 추가
    seasonal_trends['botanical_type'] = seasonal_trends['Name'].apply(get_fruit_category)
    
    # 식물학적 분류별 계절 평균 계산
    category_seasonal = seasonal_trends.groupby(['botanical_type', 'Season'])['Price'].mean().reset_index()
    
    theme = create_premium_theme()
    fig = go.Figure()
    
    for i, category in enumerate(category_seasonal['botanical_type'].unique()):
        cat_data = category_seasonal[category_seasonal['botanical_type'] == category]
        fig.add_trace(go.Scatter(
            x=cat_data['Season'],
            y=cat_data['Price'],
            mode='lines+markers',
            name=category,
            line=dict(
                color=theme['gradient_colors'][i % len(theme['gradient_colors'])],
                width=4,
                shape='spline'
            ),
            marker=dict(
                size=12,
                color=theme['gradient_colors'][i % len(theme['gradient_colors'])],
                line=dict(color='white', width=2)
            ),
            hovertemplate=f'<b>{category}</b><br>계절: %{{x}}<br>평균 가격: %{{y:.0f}}원<extra></extra>'
        ))
    
    fig = apply_premium_layout(fig, "📈 과실 식물학적 분류별 계절 변화", 500)
    fig.update_xaxes(title_text="계절", title_font_size=12)
    fig.update_yaxes(title_text="평균 가격 (원)", title_font_size=12)
    
    return fig, category_seasonal

def apply_premium_layout(fig, title="", height=500):
    """프리미엄 레이아웃 적용"""
    theme = create_premium_theme()
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'family': theme['font_family'], 'color': theme['text_color']}
        },
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=theme['background_color'],
        font={'family': theme['font_family'], 'color': theme['text_color']},
        margin=dict(l=60, r=60, t=80, b=60),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1
        )
    )
    
    # 그리드 스타일 개선
    fig.update_xaxes(
        gridcolor=theme['grid_color'],
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='rgba(151, 151, 151, 0.3)',
        tickfont={'family': theme['font_family'], 'size': 12}
    )
    
    fig.update_yaxes(
        gridcolor=theme['grid_color'],
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='rgba(151, 151, 151, 0.3)',
        tickfont={'family': theme['font_family'], 'size': 12}
    )
    
    return fig

def show_price_info():
    # 사이드바 숨기기 및 헤더 스타일 CSS
    st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 메인 콘텐츠 영역 전체 사용 */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* 헤더 스타일 */
    .header-container {
        background: linear-gradient(135deg, #0064FF 0%, #00B8D4 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 8px 32px rgba(0, 100, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.08)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
        text-align: center;
        color: white;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .header-title {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .header-subtitle {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.4rem;
        font-weight: 400;
        opacity: 0.95;
        line-height: 1.6;
        margin-bottom: 2rem;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .header-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        flex-wrap: wrap;
        margin-top: 2rem;
    }
    
    .header-stat-item {
        text-align: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .header-stat-item:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .header-stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .header-stat-label {
        font-size: 1rem;
        opacity: 0.9;
        color: white;
        font-weight: 500;
    }
    
    .toss-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 24px;
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08), 0 8px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }
    
    .toss-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.9);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .toss-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0064FF, #00B8D4, #4285F4);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .toss-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12), 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    
    .toss-card:hover::before {
        opacity: 1;
    }
    
    .title {
        font-size: 3rem;
        font-weight: 700;
        color: #191F28;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #0064FF, #00B8D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: #4E5968;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #0064FF 0%, #00B8D4 100%);
        color: white;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        margin: 12px 0;
        box-shadow: 0 10px 30px rgba(0, 100, 255, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    .stat-card:hover::before {
        animation: shine 0.6s ease;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .stat-number {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    
    .stat-label {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.95rem;
        opacity: 0.95;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .fruit-price-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        border-left: 4px solid;
        border-image: linear-gradient(135deg, #0064FF, #00B8D4) 1;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .fruit-price-card:hover {
        transform: translateX(4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    
    .price-badge {
        background: linear-gradient(135deg, #0064FF 0%, #00B8D4 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(0, 100, 255, 0.3);
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .trend-indicator {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 12px;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .trend-up {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
        color: #dc2626;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    .trend-down {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(22, 163, 74, 0.1));
        color: #16a34a;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .section-title {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
        position: relative;
        padding-bottom: 12px;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #0064FF, #00B8D4);
        border-radius: 2px;
    }
    
    .category-button {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #0064FF;
        border-radius: 12px;
        padding: 12px 20px;
        margin: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        color: #0064FF;
    }
    
    .category-button:hover {
        background: linear-gradient(135deg, #0064FF 0%, #00B8D4 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 100, 255, 0.3);
    }
    
    .category-button.selected {
        background: linear-gradient(135deg, #0064FF 0%, #00B8D4 100%);
        color: white;
        box-shadow: 0 4px 16px rgba(0, 100, 255, 0.3);
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }
        
        .header-stats {
            gap: 1.5rem;
        }
        
        .header-stat-item {
            padding: 1rem 1.5rem;
        }
        
        .toss-container, .toss-card {
            margin: 16px 0;
            padding: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # 메인 타이틀
    st.markdown('<div class="title">가격 정보</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">과실을 식물학적 분류로 체계적으로 분석하고, 상세 정보를 확인해보세요.</div>', unsafe_allow_html=True)

    # 데이터 로드
    all_fruits = get_all_fruits_with_prices()
    price_stats = get_price_statistics()
    seasonal_trends = get_seasonal_price_trends()
    
    if not all_fruits:
        st.warning("💡 가격 정보가 있는 과일 데이터가 없습니다.")
        return

    # 데이터프레임 변환
    df = pd.DataFrame([dict(fruit) for fruit in all_fruits])
    
    # 과실별 기본 통계 계산
    df['botanical_type'] = df['Name'].apply(get_fruit_category)
    total_fruits = len(df)
    total_categories = len(df['botanical_type'].unique())
    avg_price = df['coupang_price'].mean()
    price_range = df['coupang_price'].max() - df['coupang_price'].min()

    # 주요 통계 카드들
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_categories}</div>
            <div class="stat-label">식물학적 분류 종류</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_fruits}</div>
            <div class="stat-label">총 과일 수</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg_price:.0f}원</div>
            <div class="stat-label">평균 가격</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{price_range:.0f}원</div>
            <div class="stat-label">가격 편차</div>
        </div>
        """, unsafe_allow_html=True)

    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["🍎 식물학적 분류별 가격분석", "📈 식물학적 분류별 트렌드", "🔍 상세 검색", "💡 추천 정보"])
    
    with tab1:
        st.markdown('<div class="section-title">🍎 식물학적 분류별 가격 개요</div>', unsafe_allow_html=True)
        
        # 식물학적 분류별 개요 차트 생성
        fig1, fig2, category_stats, df_with_category = create_category_overview_chart(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        
        # 식물학적 분류 선택
        st.markdown('<div class="section-title">🔍 식물학적 분류별 상세 분석</div>', unsafe_allow_html=True)
        
        # 세션 상태 초기화
        if 'selected_category' not in st.session_state:
            st.session_state.selected_category = None
        
        # 식물학적 분류 버튼들
        categories = sorted(df_with_category['botanical_type'].unique())
        
        # 버튼 레이아웃
        cols = st.columns(len(categories))
        for i, category in enumerate(categories):
            with cols[i]:
                if st.button(category, key=f"cat_btn_{category}"):
                    st.session_state.selected_category = category
        
        # 선택된 식물학적 분류의 상세 분석
        if st.session_state.selected_category:
            selected_cat = st.session_state.selected_category
            
            st.markdown(f'<div class="section-title">📊 {selected_cat} 상세 분석</div>', unsafe_allow_html=True)
            
            # 상세 차트 생성
            detail_fig1, detail_fig2, stats = create_category_detail_chart(df_with_category, selected_cat)
            
            if detail_fig1 is not None:
                # 통계 요약
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("품종 수", f"{stats['count']}개")
                with col2:
                    st.metric("평균 가격", f"{stats['avg_price']:.0f}원")
                with col3:
                    st.metric("최저가", f"{stats['min_price']:.0f}원")
                with col4:
                    st.metric("최고가", f"{stats['max_price']:.0f}원")
                
                # 상세 차트
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.plotly_chart(detail_fig1, use_container_width=True)
                with col2:
                    st.plotly_chart(detail_fig2, use_container_width=True)
                
                # 개별 과일 정보
                st.markdown(f'<div class="section-title">📋 {selected_cat} 개별 과일 정보</div>', unsafe_allow_html=True)
                category_fruits = df_with_category[df_with_category['botanical_type'] == selected_cat].sort_values('coupang_price')
                
                for idx, (_, fruit) in enumerate(category_fruits.iterrows(), 1):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        rank_in_category = idx
                        total_in_category = len(category_fruits)
                        st.markdown(f"""
                        <div class="fruit-price-card">
                            <h4>#{rank_in_category} {fruit['Name']} - {fruit['Kind']}</h4>
                            <p><strong>가격:</strong> {fruit['coupang_price']}원/100g</p>
                            <p><strong>{selected_cat} 내 순위:</strong> {rank_in_category}/{total_in_category}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        delta_from_cat_avg = fruit['coupang_price'] - stats['avg_price']
                        st.metric("식물학적 분류 평균 대비", f"{delta_from_cat_avg:+.0f}원")
                    
                    with col3:
                        delta_from_total_avg = fruit['coupang_price'] - avg_price
                        st.metric("전체 평균 대비", f"{delta_from_total_avg:+.0f}원")
    
    with tab2:
        st.markdown('<div class="section-title">📈 식물학적 분류별 계절 트렌드</div>', unsafe_allow_html=True)
        
        # 트렌드 차트 생성
        trend_fig, category_seasonal = create_category_trend_chart(seasonal_trends)
        st.plotly_chart(trend_fig, use_container_width=True)
        
        # 계절별 식물학적 분류 순위
        st.markdown('<div class="section-title">🏆 계절별 식물학적 분류 순위</div>', unsafe_allow_html=True)
        
        seasons = ['봄', '여름', '가을', '겨울']
        cols = st.columns(4)
        
        for i, season in enumerate(seasons):
            with cols[i]:
                season_data = category_seasonal[category_seasonal['Season'] == season].sort_values('Price', ascending=False)
                
                st.markdown(f"**{season} 🏆**")
                for idx, (_, row) in enumerate(season_data.head(3).iterrows(), 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"
                    st.markdown(f"{medal} {row['botanical_type']}: {row['Price']:.0f}원")
    
    with tab3:
        st.markdown('<div class="section-title">🎯 상세 검색 및 정렬</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 식물학적 분류 선택
            selected_category_search = st.selectbox(
                "🍎 식물학적 분류 선택",
                options=["전체"] + sorted(df['botanical_type'].unique()),
                index=0
            )
        
        with col2:
            # 과일 선택
            if selected_category_search != "전체":
                available_fruits = df[df['botanical_type'] == selected_category_search]['Name'].unique()
            else:
                available_fruits = df['Name'].unique()
            
            selected_fruit = st.selectbox(
                "🍓 과일 선택",
                options=["전체"] + list(available_fruits),
                index=0
            )
        
        with col3:
            # 정렬 옵션
            sort_option = st.selectbox(
                "📊 정렬 기준",
                options=["최저가순", "최고가순", "이름순"],
                index=0
            )
        
        # 필터링된 데이터
        filtered_df = df.copy()
        if selected_category_search != "전체":
            filtered_df = filtered_df[filtered_df['botanical_type'] == selected_category_search]
        if selected_fruit != "전체":
            filtered_df = filtered_df[filtered_df['Name'] == selected_fruit]
        
        # 정렬 적용
        if sort_option == "최저가순":
            filtered_df = filtered_df.sort_values('coupang_price', ascending=True)
        elif sort_option == "최고가순":
            filtered_df = filtered_df.sort_values('coupang_price', ascending=False)
        elif sort_option == "이름순":
            filtered_df = filtered_df.sort_values(['Name', 'Kind'], ascending=True)
        
        if len(filtered_df) > 0:
            # 검색 결과 요약
            st.markdown(f"""
            <div class="toss-container">
                <h4>📋 검색 결과: {len(filtered_df)}개 상품</h4>
                <p>평균 가격: <strong>{filtered_df['coupang_price'].mean():.0f}원</strong> | 
                   최저가: <strong>{filtered_df['coupang_price'].min():.0f}원</strong> | 
                   최고가: <strong>{filtered_df['coupang_price'].max():.0f}원</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # 검색 결과 표시
            for idx, (_, fruit) in enumerate(filtered_df.iterrows(), 1):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="fruit-price-card">
                        <h4>#{idx} {fruit['Name']} - {fruit['Kind']}</h4>
                        <p><strong>식물학적 분류:</strong> {fruit['botanical_type']}</p>
                        <p><strong>가격:</strong> {fruit['coupang_price']}원/100g</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    delta_value = fruit['coupang_price'] - avg_price
                    st.metric("전체 평균 대비", f"{delta_value:+.0f}원")
                
                with col3:
                    rank = (df['coupang_price'] < fruit['coupang_price']).sum() + 1
                    total = len(df)
                    st.metric("전체 순위", f"{rank}/{total}위")
        else:
            st.info("검색 조건에 맞는 과일이 없습니다.")
    
    with tab4:
        st.markdown('<div class="section-title">💡 스마트 구매 추천</div>', unsafe_allow_html=True)
        
        # 식물학적 분류별 최저가 TOP 3
        st.markdown("### 🏆 식물학적 분류별 최저가 TOP 3")
        
        categories = sorted(df['botanical_type'].unique())
        cols = st.columns(min(3, len(categories)))
        
        for i, category in enumerate(categories):
            with cols[i % 3]:
                category_df = df[df['botanical_type'] == category]
                cheapest = category_df.nsmallest(3, 'coupang_price')
                
                st.markdown(f"**{category}**")
                for idx, (_, fruit) in enumerate(cheapest.iterrows(), 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"
                    st.markdown(f"""
                    <div class="fruit-price-card">
                        {medal} <strong>{fruit['Name']} ({fruit['Kind']})</strong><br>
                        <span class="price-badge">{fruit['coupang_price']:.0f}원/100g</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 전체 최저가 TOP 5
        st.markdown("### 🌟 전체 최저가 TOP 5")
        cheapest_overall = df.nsmallest(5, 'coupang_price')
        
        for idx, (_, fruit) in enumerate(cheapest_overall.iterrows(), 1):
            st.markdown(f"""
            <div class="toss-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>#{idx} {fruit['Name']} ({fruit['Kind']})</h4>
                        <p><strong>식물학적 분류:</strong> {fruit['botanical_type']}</p>
                        <p>가성비 최고의 선택!</p>
                    </div>
                    <div class="price-badge">
                        {fruit['coupang_price']:.0f}원/100g
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 하단 정보
    st.markdown("""
    <div class="toss-container">
        <h3>🔬 식물학적 분류란?</h3>
        <p>과실의 구조와 발달 과정에 따른 과학적 분류 체계입니다.</p>
        <ul>
            <li><strong>이과:</strong> 씨방 바깥 부분이 과육, 씨는 중심부 (사과, 배)</li>
            <li><strong>핵과:</strong> 단단한 씨(핵)를 중심으로 과육 (복숭아, 자두, 체리, 망고)</li>
            <li><strong>장과류:</strong> 전체가 과육이며 씨가 여러 개 (포도, 블루베리, 바나나, 감)</li>
            <li><strong>감과체:</strong> 감귤류 특유의 구조, 두꺼운 껍질과 즙낭 (오렌지, 레몬, 자몽)</li>
            <li><strong>박과열매:</strong> 박과 식물의 열매, 두꺼운 껍질 (수박, 멜론, 참외)</li>
            <li><strong>취합과:</strong> 여러 씨방이 모여 하나의 열매 (딸기, 체리모야)</li>
            <li><strong>다화과:</strong> 여러 꽃에서 생긴 열매가 합쳐짐 (파인애플, 무화과)</li>
            <li><strong>석류과:</strong> 석류 특유의 구조, 여러 방에 씨가 들어있음</li>
            <li><strong>삭과:</strong> 여러 칸으로 나뉜 씨방, 다육질 형태 (두리안)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True) 
    