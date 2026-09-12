# 🚀 네이버 마켓 인사이트 EDA 대시보드 (Naver Market Insight Dashboard)

네이버 공식 오픈 API(뉴스, 블로그, 웹문서, 이미지, 지식iN, 지역, 카페글, 백과사전) 및 데이터랩 검색어 트렌드 API를 기반으로 시장 트렌드를 다각도로 분석하는 인터랙티브 탐색적 데이터 분석(EDA) 대시보드입니다.

---

## 🌟 주요 기능

1. **다중 검색어 비교 분석**:
   - 콤마(`,`)로 구분된 다중 키워드(예: `인공지능, 빅데이터, 클라우드`)를 동시에 수집 및 비교

2. **네이버 데이터랩 검색어 트렌드 시계열 EDA**:
   - 기간(일/주/월 단위)별 상대 검색량 추이 인터랙티브 차트 (Plotly)
   - 7일 이동평균선(MA-7) 토글 및 최고 검색일, 평균 지수, 변동계수(CV) 요약

3. **8대 검색 채널 누적 검색량(Total) 비교**:
   - 뉴스·블로그·웹문서·이미지·지식iN·지역·카페글·백과사전 발행 규모 및 점유율 파이/도넛 차트

4. **다차원 심층 분석 (Advanced Analytics)**:
   - **8개 채널 레이더 스파이더 차트**: 키워드별 미디어 채널 침투력 비교
   - **수요-공급 4분면 매트릭스**: 대중 관심도(수요) vs 콘텐츠 발행량(공급) 포지셔닝 분석
   - **주간 검색 리듬 히트맵**: 요일/주차별 관심도 집중 패턴 시각화

5. **원본 데이터 열람 및 엑셀/CSV 내보내기**:
   - 8개 채널별 세부 검색 결과 카드 및 개별 CSV 다운로드
   - 전체 채널 통합 Excel 보고서 원클릭 다운로드 지원

6. **하이브리드 모드 지원 (Mock & Real API)**:
   - `.env`에 네이버 API 키가 없어도 즉시 모든 기능을 체험할 수 있는 정교한 데모(Mock) 모드 자동 지원

---

## 🛠️ 기술 스택

* **Frontend / Framework**: Streamlit (v1.40+)
* **Data Visualization**: Plotly, Matplotlib
* **Data Processing**: Pandas, OpenPyXL
* **Package & Environment Manager**: `uv` (Fast Python Package Installer)

---

## 🚀 로컬 실행 방법

```bash
# 1. 패키지 설치
uv sync

# 2. 대시보드 실행
uv run streamlit run app.py
```

---

## 🔑 환경 변수 설정 (`.env`)

네이버 클라우드 플랫폼(NAVER API HUB) 또는 네이버 개발자 센터에서 발급받은 키를 `.env` 파일에 등록합니다.

```env
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here
```
