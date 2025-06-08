# 🍎 과일 건강 정보 시스템

> 과일의 영양 정보, 가격 비교, 개인 맞춤 건강 추천을 제공하는 통합 플랫폼

## ✨ 주요 기능

### 🔍 과일 검색 및 정보 조회

- **43종 과일, 98개 품종** 상세 정보 제공
- 실시간 검색 기능으로 빠른 과일 찾기
- 과일별 품종 비교 및 가격 정보

### 📊 영양 성분 분석

- 나무위키 스타일의 상세 정보 페이지
- 품종별 가격 비교 차트 (Plotly 인터랙티브 그래프)
- 시각적 카드 레이아웃으로 직관적인 정보 제공

### 💰 실시간 가격 정보

- **식물학적 분류 기반** 체계적 가격 분석
- 이과, 핵과, 장과류, 감과체 등 9개 분류별 비교
- 계절별 가격 트렌드 시뮬레이션
- 최저가 TOP 추천 및 구매 가이드

### 🎯 개인 맞춤 건강 추천

- **5가지 건강 목표**: 다이어트, 면역력 증진, 피부 건강, 소화 개선, 빈혈 예방
- **4가지 연령대**: 어린이, 청소년, 성인, 노인별 맞춤 추천
- **성별/특수상황**: 남성, 여성, 임산부, 갱년기 여성별 개별 추천
- 폼 기반 맞춤 추천 시스템

## 🗄️ 데이터베이스 구조

### fruit 테이블 (SQLite)

실제 쿠팡에서 크롤링한 데이터를 기반으로 구성된 테이블입니다.

| 컬럼명        | 타입    | 설명                         |
| ------------- | ------- | ---------------------------- |
| id            | INTEGER | 기본키 (자동 증가)           |
| Name          | TEXT    | 과일 이름 (한글, 43종)       |
| Kind          | TEXT    | 품종/상품명 (98개 고유 품종) |
| coupang_price | REAL    | 쿠팡 가격 (원/100g)          |

**데이터 특징:**

- 총 **43종 과일, 98개 품종** 데이터
- 영어 코드 기반 품종 구분 (예: `apple_fuji`, `tangerines_sky`)
- 실제 온라인 쇼핑몰 가격 데이터 (중복 처리 완료)

## 📁 프로젝트 구조

```
proejct_test/
├── app.py                          # 🚀 메인 애플리케이션 (네비게이션 및 라우팅)
├── requirements.txt                # 📦 Python 패키지 의존성
├── README.md                       # 📄 프로젝트 문서
├── src/                           # 💻 소스 코드 디렉토리
│   ├── pages/                     # 📑 Streamlit 페이지 모듈
│   │   ├── home.py               # 🏠 홈페이지 (제철 과일, 기능 소개)
│   │   ├── nutrition_analysis.py # 📊 영양 성분 분석 (상세 페이지, 품종 비교)
│   │   ├── price_info.py         # 💰 가격 정보 (식물학적 분류 분석)
│   │   ├── health_recommendations.py # ❤️ 건강 추천 (맞춤형 추천 시스템)
│   │   └── settings.py           # ⚙️ 설정 (미구현)
│   └── utils/                     # 🛠️ 유틸리티 함수
│       └── utils.py              # 데이터베이스 연결, CSS 로드 등
├── database/                      # 🗃️ 데이터베이스 파일
│   └── a.sqlite3                 # SQLite 데이터베이스 (과일 정보)
├── assets/                        # 🖼️ 정적 자원
│   └── images/                   # 과일 이미지 (40+ 종류)
│       ├── apple.png
│       ├── banana.png
│       └── ... (총 40여 개)
└── static/                        # 📁 정적 데이터 파일
```

## 🛠️ 핵심 기능 구현 방법

### 1. 📊 영양 성분 분석 페이지 (nutrition_analysis.py)

**주요 구현 기법:**

- **세션 상태 관리**: `st.session_state`로 선택된 과일 정보 유지
- **동적 라우팅**: 과일 목록 ↔ 상세 페이지 간 전환

```python
# 핵심 함수들
def show_nutrition_analysis():
    # 세션 상태로 페이지 상태 관리
    if st.session_state.selected_fruit:
        # 상세 페이지 표시
        show_fruit_detail_page()
    else:
        # 과일 목록 그리드 표시
        show_fruit_grid()

def get_fruit_varieties(fruit_name):
    # 특정 과일의 모든 품종 데이터 조회
    # 품종별 가격 비교 차트 생성
```

**특징:**

- Plotly를 활용한 인터랙티브 가격 비교 차트
- 이미지 매핑 딕셔너리로 40+ 과일 이미지 자동 매칭

### 2. 💰 가격 정보 페이지 (price_info.py)

**고급 기능 구현:**

- **식물학적 분류 시스템**: 과학적 기준으로 과일 분류
- **계절별 트렌드 시뮬레이션**: NumPy 기반 가격 변동 모델링
- **4단계 탭 구조**: 개요 → 트렌드 → 검색 → 추천

```python
def get_fruit_category(fruit_name):
    """과실의 식물학적 분류 함수"""
    categories = {
        '이과': ['사과', '배'],
        '핵과': ['복숭아', '자두', '살구', '체리', '매실', '망고'],
        '장과류': ['포도', '블루베리', '감', '바나나', '아보카도'],
        '감과체': ['감귤', '레몬', '오렌지', '자몽', '유자'],
        # ... 총 9개 분류
    }

def create_category_overview_chart(df):
    """식물학적 분류별 개요 차트 생성"""
    # 분류별 통계 계산 및 시각화
    # Plotly를 활용한 프리미엄 테마 적용
```

**구현된 분석 기능:**

- 분류별 평균 가격 비교 (막대 차트)
- 가격 분포 버블 차트 (크기: 품종 수, 색상: 분류)
- 계절별 트렌드 라인 차트 (스플라인 곡선)
- 실시간 필터링 및 정렬 시스템

### 3. ❤️ 건강 추천 페이지 (health_recommendations.py)

**맞춤형 추천 알고리즘:**

- **3차원 추천 시스템**: 건강 목표 × 연령대 × 성별/특수상황
- **교집합 기반 추천**: 세 조건의 공통 과일 도출
- **이유 기반 설명**: 각 추천의 과학적 근거 제시

```python
def get_health_recommendations(health_goal, age_group, gender_special):
    """3차원 맞춤 추천 알고리즘"""
    # 딕셔너리 기반 추천 데이터
    health_goal_fruits = {
        "다이어트": {
            "fruits": ["사과", "자두", "딸기", "블루베리"],
            "reason": "저칼로리, 높은 식이섬유로 포만감 제공",
            "nutrients": ["식이섬유", "비타민C", "칼륨"]
        }
        # ... 5가지 건강 목표
    }

    # 교집합 계산으로 최적 과일 도출
    all_recommended_fruits = set(
        recommendations["health_goal"]["fruits"] +
        recommendations["age_group"]["fruits"] +
        recommendations["gender_special"]["fruits"]
    )
```

**UI/UX 특징:**

- Streamlit Form 기반 사용자 입력
- 3단계 결과 표시: 선택 조건 → 추천 과일 → 섭취 가이드
- 카드 기반 시각적 레이아웃

### 4. 🏠 홈페이지 (home.py)

**동적 콘텐츠 생성:**

- **제철 과일 추천**: 현재 월 기준 계절 과일 자동 표시
- **모던 카드 디자인**: CSS Grid 기반 반응형 레이아웃
- **이미지 자동 매칭**: 40+ 과일 이미지 지능형 연결

```python
def show_home():
    # 현재 월 기준 제철 과일 자동 추천
    current_month = datetime.now().month
    seasonal_fruits = get_seasonal_fruits(current_month)

    # 이미지 매핑 딕셔너리 활용
    fruit_image_mapping = {
        '사과': 'apple', '배': 'pear', '복숭아': 'peach'
        # ... 40+ 과일 매핑
    }
```

### 5. 🛠️ 유틸리티 함수 (utils.py)

**데이터베이스 연결 및 조회:**

```python
def get_db_connection():
    """SQLite 연결 (Row Factory 설정)"""
    db_path = os.path.join('database', 'a.sqlite3')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태 반환
    return conn

def get_fruit_nutrition():
    """전체 과일 데이터 조회"""

def get_fruit_varieties(fruit_name):
    """특정 과일의 모든 품종 조회"""

def get_price_comparison_data():
    """가격 비교용 데이터 조회"""
```

## 🚀 설치 및 실행

### 1. 환경 설정

```bash
# 레포지토리 클론
git clone [repository-url]
cd proejct_test

# 의존성 설치
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
streamlit run app.py
```

### 3. 브라우저 접속

```
http://localhost:8501
```

## 📦 기술 스택

- **Python 3.8+**: 메인 언어
- **SQLite3**: 경량 데이터베이스
- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산 (가격 트렌드 시뮬레이션)

- **Streamlit**: 웹 애플리케이션 프레임워크
- **Plotly**: 인터랙티브 차트 생성
- **CSS3**: 커스텀 스타일링 (그라디언트, 애니메이션)
- **HTML5**: 구조화된 마크업

### Data

- **웹 크롤링**: 쿠팡 실시간 가격 데이터
- **이미지 리소스**: 40+ 과일 고품질 이미지
- **식물학적 분류**: 과학적 기준 기반 카테고리화

## 📈 데이터 현황

### 과일 데이터베이스

- **총 43종 과일**: 사과부터 두리안까지 다양한 과일
- **98개 품종**: 상세한 품종별 구분
- **실시간 가격**: 쿠팡 기준 100g당 가격 정보

### 식물학적 분류 체계

1. **이과**: 사과, 배 (2종)
2. **핵과**: 복숭아, 자두, 살구, 체리, 망고 등 (11종)
3. **장과류**: 포도, 블루베리, 바나나, 아보카도 등 (12종)
4. **감과체**: 감귤, 레몬, 오렌지, 자몽, 유자 (5종)
5. **박과열매**: 수박, 멜론, 참외 (3종)
6. **취합과**: 딸기, 체리모야 (2종)
7. **다화과**: 파인애플, 무화과 (2종)
8. **석류과**: 석류 (1종)
9. **삭과**: 두리안 (1종)

## 🔧 주요 구현 기술

### 1. 상태 관리

- **Streamlit Session State**: 페이지 간 데이터 유지
- **동적 라우팅**: 버튼 클릭으로 페이지 전환

### 2. 데이터 시각화

- **Plotly Express**: 빠른 차트 생성
- **Plotly Graph Objects**: 고급 커스터마이징

### 3. 성능 최적화

- **이미지 매핑**: 딕셔너리 기반 빠른 이미지 로드
- **데이터 캐싱**: SQLite Row Factory 활용
