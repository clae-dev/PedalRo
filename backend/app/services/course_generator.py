"""LangChain 기반 XAI 테마 큐레이션 엔진 — 프롬프트 체이닝 + RAG"""

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings
from app.schemas.course import CourseResponse, WaypointResponse

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=settings.ANTHROPIC_API_KEY,
    temperature=0.3,
)

# [1단계] 테마별 관광지 필터링
STEP1_FILTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "당신은 자전거 관광 코스 큐레이터입니다."),
    ("human", """다음 관광지 목록에서 '{theme}' 테마에 가장 적합한 장소를 최대 {max_waypoints}개 선별하세요.

관광지 데이터:
{tourism_data}

JSON 배열로 응답하세요. 각 항목: {{"name": "장소명", "latitude": 위도, "longitude": 경도, "description": "한줄 설명", "relevance_score": 0~100}}
"""),
])

# [2단계] 자전거 대여소 연계 코스 생성
STEP2_COURSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "당신은 자전거 경로 최적화 전문가입니다."),
    ("human", """선별된 관광지와 주변 자전거 대여소 데이터를 결합하여 최적의 자전거 관광 코스를 생성하세요.

선별 관광지:
{filtered_spots}

주변 자전거 대여소 (잔여 자전거 2대 이상):
{bike_stations}

사용자 위치: 위도 {latitude}, 경도 {longitude}

JSON으로 응답하세요:
{{"title": "코스 제목", "waypoints": [{{"order": 순서, "name": "장소명", "category": "bike_station|tourist_spot", "latitude": 위도, "longitude": 경도, "description": "설명"}}], "total_distance_km": 총거리, "estimated_minutes": 예상시간}}
"""),
])

# [3단계] XAI 추천 사유 생성
STEP3_EXPLAIN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "당신은 설명 가능한 AI(XAI) 전문가입니다. 추천 근거를 데이터에 기반하여 투명하게 설명합니다."),
    ("human", """다음 자전거 관광 코스의 추천 사유를 작성하세요.

테마: {theme}
코스 정보:
{course_data}

관광지 데이터 근거:
{tourism_data}

자전거 대여소 현황:
{bike_stations}

다음 내용을 포함하여 3~5문장으로 추천 사유를 작성하세요:
1. 해당 테마와의 관련성 (데이터 기반 수치 포함)
2. 경로 효율성 및 자전거 대여소 접근성
3. 특별히 추천하는 포인트
"""),
])


async def generate_course(
    theme: str,
    latitude: float,
    longitude: float,
    tourism_data: list[dict],
    bike_stations: list[dict],
    max_waypoints: int = 5,
) -> CourseResponse:
    """3단계 LangChain LCEL 체인으로 코스를 생성합니다."""
    json_parser = JsonOutputParser()

    # Step 1: 테마별 관광지 필터링
    step1_chain = STEP1_FILTER_PROMPT | llm | json_parser
    filtered_spots = await step1_chain.ainvoke({
        "theme": theme,
        "max_waypoints": max_waypoints,
        "tourism_data": str(tourism_data),
    })

    # Step 2: 코스 생성
    step2_chain = STEP2_COURSE_PROMPT | llm | json_parser
    course_data = await step2_chain.ainvoke({
        "filtered_spots": str(filtered_spots),
        "bike_stations": str(bike_stations),
        "latitude": latitude,
        "longitude": longitude,
    })

    # Step 3: XAI 추천 사유 생성
    step3_chain = STEP3_EXPLAIN_PROMPT | llm
    explanation_result = await step3_chain.ainvoke({
        "theme": theme,
        "course_data": str(course_data),
        "tourism_data": str(tourism_data),
        "bike_stations": str(bike_stations),
    })

    return CourseResponse(
        title=course_data.get("title", f"{theme} 자전거 코스"),
        theme=theme,
        explanation=explanation_result.content,
        total_distance_km=course_data.get("total_distance_km"),
        estimated_minutes=course_data.get("estimated_minutes"),
        waypoints=[
            WaypointResponse(**wp) for wp in course_data.get("waypoints", [])
        ],
    )
