import streamlit as st

def render_interpretation_guide():
    """Render a comprehensive, keyword-agnostic guide for interpreting dashboard charts and metrics."""
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin: 0.5rem 0 1rem 0;">
            <span style="font-size: 1.5rem;">📖</span>
            <h3 style="margin: 0; font-weight: 800; color: #1E1B4B; letter-spacing: -0.02em;">마켓 인사이트 차트 & 데이터 해석 가이드북</h3>
            <span style="background: #EEF2FF; color: #4F46E5; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; border: 1px solid #C7D2FE;">EDA FRAMEWORK</span>
        </div>
        <p style="color: #64748B; font-size: 0.9rem;">
            어떤 검색어를 입력하더라도 <strong>네이버의 수치와 그래프를 통해 시장의 성격, 소비자의 행동 단계, 바이럴 흐름을 스스로 해석</strong>할 수 있는 범용 프레임워크입니다.
        </p>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 1. 트렌드 시계열 차트",
        "🏢 2. 채널별 점유율 & 성격",
        "🔍 3. 소비자 구매 여정(CDJ)",
        "📋 4. EDA 분석 체크리스트"
    ])

    with tab1:
        st.markdown("""
        #### 📈 데이터랩 상대 검색지수(0~100) 해석 가이드
        네이버 데이터랩은 절대 검색 건수가 아닌, **선택 기간 내 최다 검색량(100)을 기준으로 한 상대적 관심도**를 보여줍니다.

        - **🔥 피크(Peak, 100) 발생 지점**:
          - 특정 날짜에 검색량이 급증한 원인을 파악하세요. (신제품 발표, 공중파 방송 노출, 할인 프로모션, 사건·사고 등)
          - 피크 이후 관심도가 **원래 수준으로 급락**하는지, 아니면 **높아진 베이스라인을 유지**하는지 확인하여 일시적 반짝 유행인지 지속적 수요인지 판별합니다.
        - **📊 키워드 간 상대적 격차**:
          - 여러 키워드를 동시 비교할 때, 한 키워드가 압도적(100 부근)이고 다른 키워드가 바닥(10 미만)에 머문다면 **대중적 인지도 격차가 매우 큰 상태**입니다.
        - **〰️ 주기성 및 변동성 (표준편차)**:
          - 주말/주중 패턴이나 계절성(여름, 명절, 연말 등)이 있는지 확인하세요.
        """)

    with tab2:
        st.markdown("""
        #### 🏢 8개 채널별 문서량 분포로 보는 시장 특성
        어느 채널에 문서가 집중되어 있는지에 따라 **시장의 현재 속성과 커뮤니케이션 타깃**을 파악할 수 있습니다.

        | 채널명 | 주된 성격 | 높은 비중이 의미하는 시장 상황 |
        | :--- | :--- | :--- |
        | **📰 뉴스** | 공신력, 보도자료, B2B, 정책 | 산업 동향, 기업 이슈, 신기술 발표 등 공식 미디어 중심의 관심 |
        | **✍️ 블로그** | 개인 경험, 제품 리뷰, 정보성 롱폼 | 소비자의 **실제 구매 후기 및 꼼꼼한 정보 탐색**이 활발한 시장 |
        | **☕ 카페글** | 커뮤니티, 찐팬/실사용자 소통, Q&A | 특정 매니아층, 맘카페, 동호회 등 **진성 커뮤니티 바이럴** 중심 |
        | **🙋 지식iN** | 직관적 질문, 문제 해결, 고민 상담 | 소비자가 **가격, 부작용, 비교 추천 등 구체적 고민**을 겪고 있는 단계 |
        | **🌐 웹문서** | 공식 웹사이트, 블로그, 포럼 등 | 전반적인 웹상의 누적 정보량 및 SEO 인덱싱 규모 |
        | **🖼️ 이미지** | 시각적 비주얼, 디자인, 패션/인테리어 | 패션, 뷰티, 여행, 맛집 등 **비주얼 중심의 탐색**이 중요한 분야 |
        | **📍 지역(플레이스)** | 오프라인 매장, 병원, 학원, 맛집 | 로컬 상권 기반의 방문/예약 중심 비즈니스 |
        | **📚 백과사전** | 학술, 전문 용어, 개념 정의 | 전문 용어이거나 학문/역사적 배경이 있는 정형화된 개념 |
        """)

    with tab3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%); border: 1.5px solid #E0E7FF; border-radius: 14px; padding: 1.25rem; margin: 1rem 0;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; text-align: center;">
                <div style="background: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); border-top: 3px solid #4F46E5;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #4F46E5;">1. 인지 (Awareness)</div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">뉴스 / 트렌드 피크</div>
                </div>
                <div style="background: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); border-top: 3px solid #7C3AED;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #7C3AED;">2. 탐색 (Consideration)</div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">지식iN / 검색어</div>
                </div>
                <div style="background: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); border-top: 3px solid #059669;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #059669;">3. 검증 (Validation)</div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">블로그 후기 / 카페글</div>
                </div>
                <div style="background: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); border-top: 3px solid #E11D48;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #E11D48;">4. 전환 (Action)</div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">지역(플레이스) / 웹</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        #### 📋 시장 분석(EDA) 실전 체크리스트
        새로운 키워드를 넣었을 때 아래 4가지 질문을 던져보세요:

        1. **[수요 vs 공급]** 트렌드 검색량(수요)에 비해 블로그/카페 문서 수(공급)가 충분한가, 아니면 아직 블루오션인가?
        2. **[바이럴 채널]** 카페와 블로그 중 어디에서 더 활발하게 언급되는가? (체험단 vs 커뮤니티 침투 전략 결정)
        3. **[고객의 페인포인트]** 지식iN 탭의 질문 제목들을 보았을 때 소비자가 가장 궁금해하는 핵심 의문은 무엇인가?
        4. **[피쟁 키워드 비교]** 경쟁 브랜드나 대체재 키워드와 비교했을 때, 우리 키워드의 점유율과 트렌드 추세는 어떠한가?
        """)
