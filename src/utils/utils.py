import sqlite3
import os
import streamlit as st

# 데이터베이스 연결 함수
def get_db_connection():
    db_path = os.path.join('database', 'a.sqlite3')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# 과일 정보 가져오기 (기존 과일 영양 정보 + 가격 정보 통합)
def get_fruit_nutrition():
    conn = get_db_connection()
    fruits = conn.execute("SELECT * FROM fruit").fetchall()
    conn.close()
    return fruits

# 과일 가격 정보 가져오기 (새로운 스키마에 맞게 수정)
def get_fruit_prices(fruit_name=None, variety=None):
    conn = get_db_connection()
    query = "SELECT * FROM fruit"
    params = []
    
    if fruit_name:
        query += " WHERE Name = ?"
        params.append(fruit_name)
        
        if variety:
            query += " AND Kind LIKE ?"
            params.append(f"%{variety}%")
    
    prices = conn.execute(query, params).fetchall()
    conn.close()
    return prices

# 계절 과일 가져오기 (임시로 모든 과일 반환 - 계절 정보가 없으므로)
def get_seasonal_fruits(month):
    conn = get_db_connection()
    # 새로운 스키마에는 계절 정보가 없으므로 모든 과일을 반환
    fruits = conn.execute("SELECT * FROM fruit").fetchall()
    conn.close()
    return fruits

# 과일 이름으로 검색하기
def search_fruits(search_term):
    conn = get_db_connection()
    fruits = conn.execute('''
        SELECT * FROM fruit 
        WHERE Name LIKE ?
    ''', (f'%{search_term}%',)).fetchall()
    conn.close()
    return fruits

# 특정 과일의 모든 품종 가져오기
def get_fruit_varieties(fruit_name):
    conn = get_db_connection()
    varieties = conn.execute('''
        SELECT * FROM fruit 
        WHERE Name = ?
    ''', (fruit_name,)).fetchall()
    conn.close()
    return varieties

# 과일 이름 목록 가져오기 (중복 제거)
def get_unique_fruit_names():
    conn = get_db_connection()
    fruits = conn.execute("SELECT DISTINCT Name FROM fruit").fetchall()
    conn.close()
    return [fruit['Name'] for fruit in fruits]

# 과일 가격 비교 데이터 가져오기
def get_price_comparison_data():
    conn = get_db_connection()
    fruits = conn.execute('''
        SELECT Name, Kind, coupang_price 
        FROM fruit 
        WHERE coupang_price > 0
        ORDER BY Name, coupang_price
    ''').fetchall()
    conn.close()
    return fruits

# CSS 스타일 로드
def load_css():
    st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background-color: #0064FF;
            color: white;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #0052CC;
        }
        .card {
            background-color: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            cursor: pointer;
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
        .feature-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #191F28;
            margin-bottom: 1rem;
        }
        .feature-desc {
            color: #4E5968;
            font-size: 1rem;
            line-height: 1.6;
        }
        .seasonal-title {
            font-size: 2rem;
            font-weight: 700;
            color: #191F28;
            margin: 2rem 0 1rem 0;
            text-align: center;
        }
        .fruit-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.2s;
        }
        .fruit-card:hover {
            transform: translateY(-5px);
        }
        .fruit-name {
            font-size: 1.5rem;
            font-weight: 600;
            color: #191F28;
            margin: 1rem 0;
        }
        .fruit-info {
            color: #4E5968;
            font-size: 0.9rem;
            margin: 0.5rem 0;
        }
        .highlight-box {
            background: linear-gradient(45deg, #0064FF, #00B8D4);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
        }
        .highlight-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .highlight-desc {
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .tag {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            background-color: #E8F0FE;
            color: #0064FF;
            border-radius: 20px;
            font-size: 0.9rem;
            margin: 0.2rem;
        }
        .fruit-list-card {
            background: white;
            border-radius: 15px;
            padding: 1.2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            transition: transform 0.2s;
            cursor: pointer;
        }
        .fruit-list-card:hover {
            transform: translateY(-5px);
            background-color: #f0f9ff;
        }
        .search-container {
            margin-bottom: 2rem;
        }
        .coming-soon {
            text-align: center;
            padding: 5rem 0;
            color: #4E5968;
            font-size: 1.5rem;
        }
        .nutrition-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            transition: transform 0.2s;
            height: 100%;
            cursor: pointer;
            position: relative;
        }
        .nutrition-card:hover {
            transform: translateY(-5px);
            background-color: #f0f9ff;
        }
        .nutrition-card-header {
            font-size: 1.3rem;
            font-weight: 600;
            color: #191F28;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .nutrition-card-content {
            color: #4E5968;
            font-size: 0.9rem;
            margin: 0.5rem 0;
            text-align: center;
        }
        .nutrition-image {
            display: block;
            margin: 0 auto 1rem auto;
            height: 100px;
            object-fit: contain;
        }
        .nutrition-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #0064FF;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        .variety-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        .variety-card:hover {
            transform: translateY(-3px);
            background-color: #f0f9ff;
        }
        .variety-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #191F28;
            margin-bottom: 0.5rem;
        }
        .variety-info {
            color: #4E5968;
            font-size: 0.85rem;
            margin: 0.3rem 0;
        }
        .table-header {
            background-color: #f0f9ff;
            font-weight: 600;
        }
        
        /* 나무위키 스타일 */
        .wiki-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            border: 1px solid #e0e0e0;
            transition: all 0.2s ease;
        }
        .wiki-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        .wiki-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 0.7rem;
            padding-bottom: 0.7rem;
            border-bottom: 1px solid #eaeaea;
        }
        .wiki-section {
            margin: 1.5rem 0;
        }
        .wiki-section-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 0.8rem;
            padding-left: 0.5rem;
            border-left: 4px solid #0064FF;
        }
        .wiki-content {
            line-height: 1.6;
            color: #333;
            font-size: 1rem;
        }
        .wiki-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.95rem;
        }
        .wiki-table th {
            background-color: #f4f4f4;
            padding: 0.7rem;
            border: 1px solid #ddd;
            text-align: left;
            font-weight: 600;
        }
        .wiki-table td {
            padding: 0.7rem;
            border: 1px solid #ddd;
        }
        .wiki-quote {
            background-color: #f5f5f5;
            border-left: 4px solid #0064FF;
            padding: 1rem;
            margin: 1rem 0;
            font-style: italic;
            color: #555;
        }
        .wiki-reference {
            font-size: 0.9rem;
            color: #666;
            margin: 0.5rem 0;
        }
        .fruit-grid-card {
            background: white;
            border-radius: 8px;
            padding: 1.2rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.2rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            transition: all 0.2s ease;
            border: 1px solid #e0e0e0;
        }
        .fruit-grid-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .fruit-grid-img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 6px;
            margin-bottom: 1rem;
        }
        .fruit-grid-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
        }
        .fruit-grid-info {
            margin-bottom: 0.4rem;
            color: #555;
            display: flex;
            justify-content: space-between;
        }
        .fruit-grid-label {
            font-weight: 500;
            color: #777;
        }
        .fruit-grid-value {
            font-weight: 600;
            color: #333;
        }
        .fruit-tag {
            background-color: #e8f0fe;
            color: #0064FF;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-right: 0.4rem;
            display: inline-block;
            margin-bottom: 0.4rem;
        }
        
        /* 고정된 카드 컨테이너 스타일 */
        .fruit-card-container {
            background: white;
            border-radius: 8px;
            padding: 1.2rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.2rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            border: 1px solid #e0e0e0;
            transition: transform 0.2s;
        }
        .fruit-card-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .fruit-image-placeholder {
            width: 100%;
            height: 150px;
            background-color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .fruit-card-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1a1a1a;
            margin: 0.5rem 0;
            text-align: center;
        }
        .fruit-card-info {
            display: flex;
            justify-content: space-between;
            margin: 0.4rem 0;
            font-size: 0.9rem;
        }
        .fruit-card-label {
            color: #777;
            font-weight: 500;
        }
        .fruit-card-value {
            color: #333;
            font-weight: 600;
        }
        .fruit-card-season {
            background-color: #e8f0fe;
            color: #0064FF;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-top: 0.6rem;
            display: inline-block;
        }
        
        /* 모던 카드 스타일 추가 */
        .modern-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            height: 100%;
            border: none;
            transition: all 0.3s ease;
            position: relative;
        }
        .modern-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        }
        
        /* 추가 모던 스타일 */
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
        
        /* 과일 카드 컨테이너 스타일 */
        .fruit-card {
            border: 1px solid rgba(0, 100, 255, 0.1);
            border-radius: 16px;
            padding: 15px;
            background-color: white;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        .fruit-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            border-color: rgba(0, 100, 255, 0.3);
        }
        .custom-heading {
            font-size: 1.5rem;
            font-weight: 700;
            color: #333;
            margin: 10px 0;
            position: relative;
            padding-bottom: 5px;
        }
        .custom-heading:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 40px;
            height: 3px;
            background: linear-gradient(to right, #0064FF, #00B8D4);
            transition: width 0.3s ease;
        }
        .fruit-card:hover .custom-heading:after {
            width: 100%;
        }
        .info-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
        }
        .info-icon {
            color: #0064FF;
            margin-right: 10px;
            font-size: 1.1rem;
        }
        .info-label {
            color: #666;
            font-size: 0.95rem;
            flex: 1;
        }
        .info-value {
            font-weight: 600;
            color: #333;
            font-size: 0.95rem;
        }
        .season-badge {
            background-color: #e8f0fe;
            color: #0064FF;
            padding: 6px 12px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin-top: 10px;
        }
        .no-image-placeholder {
            display: flex;
            height: 100%;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            color: #777;
            background-color: #f5f5f5;
        }
    </style>
    """, unsafe_allow_html=True) 