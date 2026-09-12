# ⚡ 네이버 마켓 인사이트 스튜디오 (Naver Market Insight Studio)

> 네이버 공식 오픈 API(8개 채널)와 데이터랩 검색어 트렌드 API를 기반으로 시장 트렌드와 미디어 반응도를 실시간 교차 분석하는 **탐색적 데이터 분석(EDA) 인터랙티브 대시보드**입니다.

---

## 🧭 프로젝트 개요

* **목적**: 키워드에 대한 대중의 검색 관심도(수요)와 8대 미디어 채널의 콘텐츠 발행량(공급)을 다각도로 분석하여 마케팅 및 시장 인사이트를 도출합니다.
* **핵심 분석 채널 (8대 채널)**:
  * 📝 블로그 (`blog`)
  * ☕ 카페글 (`cafearticle`)
  * 📰 뉴스 (`news`)
  * 🌐 웹문서 (`webkr`)
  * 💡 지식iN (`kin`)
  * 🖼️ 이미지 (`image`)
  * 📍 지역/플레이스 (`local`)
  * 📚 백과사전 (`encyc`)

---

## 🌟 주요 기능 및 탭 구성

### 1. 상단 핵심 KPI 요약 카드
* 키워드별 누적 총 콘텐츠 발행량, 검색어 트렌드 평균 지수, 최고 검색일 및 1위 점유 채널을 실시간 카드 형태로 한눈에 요약

### 2. 5대 핵심 분석 탭

| 탭 | 주요 기능 및 분석 내용 |
| :--- | :--- |
| **📊 1. 마켓 점유율 & 채널 분석** | 8개 채널별 발행 규모 비교 바 차트 및 키워드별 채널 점유율 도넛 차트 |
| **📈 2. 시계열 트렌드 랩** | 네이버 데이터랩 일/주/월 단위 상대 검색량 인터랙티브 시계열 차트, 7일 이동평균선(MA-7) 및 변동계수(CV) 분석 |
| **🔮 3. 심층 EDA 랩** | • **8채널 레이더 차트**: 키워드별 채널 침투력 비교<br>• **수요-공급 4분면 매트릭스**: 대중 관심도 vs 콘텐츠 공급 포지셔닝<br>• **주간 검색 리듬 히트맵**: 요일별 관심도 집중 패턴 분석 |
| **🔎 4. 채널별 콘텐츠 탐색기** | 8개 채널별 실제 검색 결과 카드형 열람, 채널별 CSV 다운로드 및 **전체 통합 Excel 보고서** 다운로드 |
| **📖 5. 마켓 인사이트 가이드북** | 소비자 의사결정 여정(CDJ) 및 데이터 기반 의사결정 프레임워크 가이드 |

---

## 🛠️ 기술 스택

* **Frontend**: Streamlit
* **Interactive Charting**: Plotly, Matplotlib
* **Data Processing**: Pandas, OpenPyXL
* **Package Manager**: `uv` (Fast Python Package Installer)
* **APIs**: NAVER API HUB (Search API & Datalab Trend API)

---

## 💻 로컬 실행 방법

```bash
# 1. 패키지 설치
uv sync

# 2. 스트림릿 대시보드 실행
uv run streamlit run app.py
```

---

## 🔑 환경 변수 설정 (`.env`)

네이버 클라우드 플랫폼(NAVER API HUB) 또는 네이버 개발자 센터의 인증 키를 프로젝트 루트의 `.env` 파일에 설정합니다.

```env
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here
```
