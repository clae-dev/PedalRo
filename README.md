# 페달로 (PedalRo)

**AI 기반 자전거 관광 코스 큐레이션 서비스**

> 2026년 전국 통합데이터 활용 공모전 출품작

전국 공영자전거 실시간 대여 데이터와 한국관광공사 관광 API를 융합하여, 사용자의 취향에 맞춘 테마별 자전거 관광 코스를 추천하고 그 추천 이유를 **설명 가능한 인공지능(XAI)** 방식으로 제공하는 웹 기반 관광 안내 서비스입니다.

---

## 목차

- [서비스 소개](#서비스-소개)
- [핵심 기능](#핵심-기능)
- [시스템 아키텍처](#시스템-아키텍처)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [환경 설정](#환경-설정)
- [실행 방법](#실행-방법)
- [API 명세](#api-명세)
- [데이터베이스 스키마](#데이터베이스-스키마)
- [활용 공공데이터](#활용-공공데이터)
- [배포](#배포)

---

## 서비스 소개

### 배경

- **관광 패러다임의 변화**: 목적지 중심 '점'의 관광에서 이동 과정을 즐기는 '선'의 관광으로 변화하는 트렌드 반영
- **선택 피로 해소**: 실시간 공공데이터와 AI가 결합된 초개인화 큐레이션으로 관광객의 의사결정 지원
- **친환경 이동성 강화**: 공영자전거 이용률 제고 및 로컬 골목 상권으로의 관광객 유입을 통한 지역 경제 균형 발전

### 차별점

| 구분 | 기존 지도/관광 앱 | 페달로 (PedalRo) |
|------|----------------|-----------------|
| 경로 기준 | 최단거리/최소시간 중심 | 사용자 설정 테마 중심의 경험 큐레이션 |
| 추천 방식 | 단순 거리/평점 정렬 | LangChain 프롬프트 체이닝 + RAG 기반 다단계 AI 추론 |
| 추천 근거 | 결과만 제시 (블랙박스) | XAI 방식으로 "왜 이 코스인지" 자연어 근거 제시 |
| 데이터 활용 | 정적 DB 기반 | 실시간 공공데이터 API + LangChain 컨텍스트 주입 |

---

## 핵심 기능

### 1. 하이브리드 실시간 데이터 파이프라인

- **동적 가용성 필터링**: 공영자전거 실시간 API를 `httpx/asyncio` 비동기 통신으로 호출하여, 잔여 자전거 **2대 이상**인 대여소만 유효 노드로 설정
- **관광 정보 매칭**: 한국관광공사 위치 기반 POI 데이터를 수집하여 경로 주변 유효 관광지 추출

### 2. LangChain 기반 XAI 테마 큐레이션 엔진

LangChain LCEL(LangChain Expression Language)을 활용한 **3단계 프롬프트 체이닝**:

```
[1단계] 테마별 관광지 필터링
    → 수집된 관광지에서 사용자 선택 테마(자연, 역사, 맛집 등)에 부합하는 후보군 선별

[2단계] 자전거 대여소 연계 코스 생성
    → 필터링된 후보와 실시간 자전거 대여소 데이터를 결합하여 최적 코스 조합 생성

[3단계] XAI 추천 사유 생성
    → "경로 반경 500m 이내 '자연/힐링' 관광 데이터가 밀집되어 추천합니다" 등
      데이터 기반 신뢰할 수 있는 근거를 자연어로 생성
```

- **RAG 아키텍처**: LLM이 학습 데이터에 의존하지 않고, 실시간 수집 공공데이터를 `PromptTemplate`에 직접 주입하여 AI 환각(Hallucination) 방지
- **구조화된 출력**: LangChain `JsonOutputParser`를 통해 추천 결과를 정형화된 JSON으로 출력

### 3. 인터랙티브 지도 시각화

- **카카오맵 API 연동**: AI 생성 추천 경로를 `Polyline` + `Marker`로 시각화
- **실시간 잔여 수치 위젯**: 대여소별 실시간 자전거 수 및 빈 거치대 현황 표시

### 4. 데이터베이스 기반 개인화

- **PostGIS 공간 쿼리**: `ST_DWithin`, `ST_Distance` 등 공간 함수로 위치 기반 고속 조회
- **피드백 루프**: 주행 코스 이력 및 만족도 데이터 저장을 통한 추천 품질 지속 개선

---

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│  Client (React / Next.js + 카카오맵 SDK)                             │
│  - 테마 선택 UI, 지도 시각화, 실시간 위젯 렌더링                          │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTP (REST)
┌──────────────────────────▼──────────────────────────────────────────┐
│  API Server (FastAPI)                                               │
│  - 비동기 REST API, 요청 라우팅, Pydantic 데이터 검증                    │
├─────────────────────────────────────────────────────────────────────┤
│  Data Layer (httpx / asyncio)                                       │
│  - 공공데이터 API 병렬 호출, 외부 LLM API 연동                          │
├────────────────────┬────────────────────────────────────────────────┤
│  AI Engine         │  Persistence                                   │
│  LangChain + Claude│  PostgreSQL + PostGIS + SQLAlchemy              │
│  LCEL 3단계 체인    │  사용자 프로필, 코스 이력, 피드백 저장               │
└────────────────────┴────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│  Infra: AWS EC2 + Nginx (리버스 프록시)                               │
└─────────────────────────────────────────────────────────────────────┘
```

**핵심 기술 흐름:**

```
사용자 취향 입력
  → httpx 비동기 API 호출 (자전거 + 관광 데이터)
  → LangChain [1단계] 테마별 관광지 필터링
  → [2단계] 자전거 대여소 연계 코스 생성
  → [3단계] XAI 추천 사유 생성
  → 카카오맵 시각화 출력
```

---

## 기술 스택

| 계층 | 기술 | 선정 사유 |
|------|------|---------|
| **Backend** | FastAPI, httpx/asyncio, Pydantic | Python 네이티브 비동기 처리로 다수 공공데이터 API 병렬 호출. Pydantic으로 응답 데이터 검증 및 타입 안전성 확보 |
| **Frontend** | React / Next.js, TypeScript, Tailwind CSS | 카카오맵 API 연동 시각화, 실시간 데이터 반영 인터랙티브 UI 구현 |
| **Database** | PostgreSQL + PostGIS, SQLAlchemy, Alembic | PostGIS 확장으로 공간 인덱싱 및 위치 기반 고속 조회. SQLAlchemy ORM으로 사용자 이력 관리 |
| **AI / XAI** | LangChain, Claude API, LCEL, PromptTemplate | LCEL 체인으로 필터링 → 코스 생성 → 사유 설명 다단계 추론. PromptTemplate에 실시간 데이터 주입 (RAG) |
| **지도** | 카카오맵 API | Polyline/Marker 기반 경로 시각화, 자전거 도로 우선순위 반영 |
| **배포** | AWS EC2, Nginx, Docker Compose | Nginx 리버스 프록시로 프론트/백엔드 통합 서빙 |

---

## 프로젝트 구조

```
PedalRo/
├── backend/                              # FastAPI 백엔드
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── course.py             # 코스 추천 API 라우터
│   │   │       └── health.py             # 헬스체크 엔드포인트
│   │   ├── core/
│   │   │   ├── config.py                 # 환경 변수 설정 (Pydantic Settings)
│   │   │   └── database.py              # AsyncSession + DB 엔진 설정
│   │   ├── models/
│   │   │   ├── user.py                   # 사용자 모델
│   │   │   └── course.py                # 코스, 경유지, 피드백 모델 (PostGIS)
│   │   ├── schemas/
│   │   │   └── course.py                # Pydantic 요청/응답 스키마
│   │   ├── services/
│   │   │   ├── bike_station.py          # 공영자전거 실시간 API 연동
│   │   │   ├── tourism.py               # 한국관광공사 관광정보 API 연동
│   │   │   └── course_generator.py      # LangChain LCEL 3단계 체인 엔진
│   │   └── main.py                      # FastAPI 앱 엔트리포인트
│   ├── tests/                            # 테스트
│   ├── alembic.ini                       # Alembic 마이그레이션 설정
│   ├── requirements.txt                  # Python 의존성
│   ├── Dockerfile
│   └── .env.example                      # 환경 변수 템플릿
│
├── frontend/                             # Next.js + TypeScript 프론트엔드
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx                # 루트 레이아웃
│   │   │   └── page.tsx                  # 메인 페이지 (테마 선택 → 추천 → 지도)
│   │   ├── components/
│   │   │   ├── KakaoMap.tsx             # 카카오맵 Polyline/Marker 시각화
│   │   │   ├── ThemeSelector.tsx        # 테마 선택 UI (자연, 역사, 맛집, 힐링, 문화)
│   │   │   └── CourseResult.tsx         # XAI 추천 사유 + 경유지 목록 표시
│   │   ├── lib/
│   │   │   └── api.ts                   # 백엔드 API 호출 함수
│   │   └── types/
│   │       └── course.ts                # TypeScript 타입 정의
│   ├── Dockerfile
│   └── .env.example                      # 환경 변수 템플릿
│
├── nginx/
│   └── default.conf                      # Nginx 리버스 프록시 설정
│
├── docker-compose.yml                    # 전체 서비스 오케스트레이션
├── .gitignore
└── README.md
```

---

## 환경 설정

### 사전 요구사항

- **Python** 3.12+
- **Node.js** 20+
- **PostgreSQL** 16+ (PostGIS 확장 포함)
- **Docker** & **Docker Compose** (선택 - 컨테이너 실행 시)

### API 키 발급

본 서비스는 다음 외부 API를 사용합니다. 각 서비스에서 API 키를 발급받아야 합니다.

| API | 발급처 | 용도 |
|-----|-------|------|
| Anthropic API | https://console.anthropic.com | LangChain을 통한 LLM 추론 (Claude) |
| 한국관광공사 국문 관광정보 서비스 | https://www.data.go.kr | 위치 기반 관광지 정보 조회 |
| 카카오맵 JavaScript SDK | https://developers.kakao.com | 지도 시각화 및 경로 표시 |
| 공영자전거 실시간 API | 행정안전부 / 각 지자체 | 실시간 자전거 대여소 정보 |

### 환경 변수 설정

**Backend** (`backend/.env`):

```env
# API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key
KAKAO_REST_API_KEY=your_kakao_rest_api_key
TOUR_API_KEY=your_tour_api_service_key

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/pedalro

# App
APP_ENV=development
DEBUG=true
```

**Frontend** (`frontend/.env.local`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_KAKAO_APP_KEY=your_kakao_javascript_key
```

> `.env.example` 파일을 복사하여 실제 키 값을 입력하세요.

---

## 실행 방법

### 방법 1: Docker Compose (권장)

모든 서비스를 한 번에 실행합니다.

```bash
# 환경 변수 파일 준비
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
# 각 파일에 실제 API 키 입력

# 전체 서비스 실행
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs

### 방법 2: 로컬 개별 실행

#### 1) 데이터베이스

```bash
# Docker로 PostGIS 데이터베이스만 실행
docker compose up db

# 또는 로컬 PostgreSQL에 PostGIS 확장 활성화
# psql -U postgres -c "CREATE DATABASE pedalro;"
# psql -U postgres -d pedalro -c "CREATE EXTENSION postgis;"
```

#### 2) Backend

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# DB 마이그레이션 (초기 1회)
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

#### 3) Frontend

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
# .env.local 파일에 API 키 입력

# 개발 서버 실행
npm run dev
```

---

## API 명세

### 헬스체크

```
GET /health
```

**응답:**

```json
{
  "status": "ok",
  "service": "PedalRo API"
}
```

### 코스 추천

```
POST /api/v1/courses/recommend
```

**요청 Body:**

```json
{
  "latitude": 37.5665,
  "longitude": 126.978,
  "theme": "자연",
  "radius_km": 5.0,
  "max_waypoints": 5
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `latitude` | float | O | 사용자 현재 위도 |
| `longitude` | float | O | 사용자 현재 경도 |
| `theme` | string | O | 테마 (`자연`, `역사`, `맛집`, `힐링`, `문화`) |
| `radius_km` | float | X | 탐색 반경 km (기본값: 5.0) |
| `max_waypoints` | int | X | 최대 경유지 수 2~10 (기본값: 5) |

**응답:**

```json
{
  "title": "한강변 힐링 자전거 코스",
  "theme": "자연",
  "explanation": "사용자님의 '자연' 테마 선호와 현재 위치 반경 5km 내 수변 공원 포함 비율(85%)을 고려하여 이 코스를 추천합니다. 출발 대여소에서 잔여 자전거 12대가 확보되어 있으며, 경로 전체가 자전거 전용 도로로 연결되어 안전한 주행이 가능합니다. 특히 여의도 한강공원 구간은 현재 시즌 벚꽃 명소로 높은 관광 만족도가 기대됩니다.",
  "total_distance_km": 12.3,
  "estimated_minutes": 65,
  "waypoints": [
    {
      "order": 1,
      "name": "여의나루역 대여소",
      "category": "bike_station",
      "latitude": 37.5270,
      "longitude": 126.9328,
      "description": "잔여 자전거 12대"
    },
    {
      "order": 2,
      "name": "여의도 한강공원",
      "category": "tourist_spot",
      "latitude": 37.5284,
      "longitude": 126.9346,
      "description": "한강변 대표 자연 관광지"
    }
  ]
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `title` | string | AI가 생성한 코스 제목 |
| `theme` | string | 선택된 테마 |
| `explanation` | string | XAI 추천 사유 (데이터 기반 근거 포함) |
| `total_distance_km` | float | 총 경로 거리 (km) |
| `estimated_minutes` | int | 예상 소요 시간 (분) |
| `waypoints` | array | 경유지 목록 (순서대로) |
| `waypoints[].category` | string | `bike_station` (자전거 대여소) 또는 `tourist_spot` (관광지) |

> Swagger UI에서 전체 API 문서를 확인할 수 있습니다: http://localhost:8000/docs

---

## 데이터베이스 스키마

PostgreSQL + PostGIS 기반으로 다음 테이블을 사용합니다.

### users

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER (PK) | 사용자 고유 ID |
| nickname | VARCHAR(50) | 닉네임 |
| preferred_themes | VARCHAR(200) | 선호 테마 (콤마 구분) |
| created_at | TIMESTAMPTZ | 가입일시 |

### courses

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER (PK) | 코스 고유 ID |
| user_id | INTEGER (FK → users) | 사용자 ID |
| theme | VARCHAR(50) | 테마 (자연, 역사, 맛집 등) |
| title | VARCHAR(200) | 코스 제목 |
| explanation | TEXT | XAI 추천 사유 |
| total_distance_km | FLOAT | 총 거리 (km) |
| estimated_minutes | INTEGER | 예상 소요 시간 (분) |
| created_at | TIMESTAMPTZ | 생성일시 |

### course_waypoints

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER (PK) | 경유지 고유 ID |
| course_id | INTEGER (FK → courses) | 코스 ID |
| order | INTEGER | 경유 순서 |
| name | VARCHAR(200) | 장소명 |
| category | VARCHAR(50) | `bike_station` 또는 `tourist_spot` |
| location | GEOMETRY(POINT, 4326) | PostGIS 좌표 (WGS84) |
| description | TEXT | 장소 설명 |

### course_feedbacks

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER (PK) | 피드백 고유 ID |
| course_id | INTEGER (FK → courses) | 코스 ID |
| user_id | INTEGER (FK → users) | 사용자 ID |
| rating | INTEGER | 만족도 (1~5) |
| comment | TEXT | 코멘트 |
| created_at | TIMESTAMPTZ | 작성일시 |

---

## 활용 공공데이터

### 필수 공공데이터

| 데이터 | 출처 | 활용 방식 |
|--------|------|----------|
| **국문 관광정보 서비스 API** | 한국관광공사 (공공데이터포털) | 위치 기반 관광지 좌표, 소개, 카테고리 → LangChain RAG 컨텍스트 주입 |
| **전국 공영자전거 실시간 대여소 정보 API** | 행정안전부 / 각 지자체 | 실시간 잔여 자전거, 빈 거치대, 대여소 좌표 → 코스 생성 입력 데이터 |

### 민간 데이터

| 데이터 | 출처 | 활용 방식 |
|--------|------|----------|
| **카카오맵 API** | 카카오 | 지도 시각화, Polyline 경로 표시, 자전거 도로 정보 |
| **Claude API** | Anthropic | LangChain 프롬프트 체이닝 기반 테마 분석 및 추천 사유 생성 |

### 데이터 처리 방식

- 별도 벡터 DB 없이 FastAPI 백엔드에서 API 응답 데이터를 직접 LLM 컨텍스트로 구성하는 **경량 RAG** 방식 채택
- API 실시간 연동으로 최신 데이터를 지속적으로 유지
- 관광 데이터의 텍스트 속성을 LangChain `PromptTemplate`에 구조화된 형태로 전처리하여 주입

---

## 배포

### AWS EC2 + Nginx 구성

```
[클라이언트] → [Nginx :80]
                  ├── /       → [Next.js :3000]  (프론트엔드)
                  └── /api/   → [FastAPI :8000]  (백엔드 API)
```

Nginx 리버스 프록시 설정은 `nginx/default.conf`에 포함되어 있습니다.

### 배포 절차

```bash
# 1. EC2 인스턴스에 Docker 및 Docker Compose 설치

# 2. 프로젝트 클론
git clone <repository-url>
cd PedalRo

# 3. 환경 변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
# 각 파일에 프로덕션 API 키 입력

# 4. 전체 서비스 빌드 및 실행
docker compose up -d --build

# 5. Nginx 설정 적용
sudo cp nginx/default.conf /etc/nginx/conf.d/default.conf
sudo nginx -s reload
```

---

## 기대 효과

- **지역 상권 활성화**: 숨겨진 로컬 명소와 골목길을 이어주는 동선으로 소상공인 밀집 구역에 관광객 분산
- **탄소 중립 기여**: 자동차 대비 절감 탄소 배출량 시각화를 통한 친환경 관광 문화 선도
- **공공데이터 선순환**: 단일 데이터로 불가능했던 새 가치 창출 + 사용자 피드백 기반 추천 품질 지속 개선
- **AI 신뢰성 제고**: XAI 방식 추천 사유 제시로 공공 서비스 내 설명 가능한 AI 활용 모범 사례 구축
