"""코스 추천 API 라우터"""

from fastapi import APIRouter

from app.schemas.course import CourseRequest, CourseResponse
from app.services.bike_station import fetch_nearby_bike_stations, filter_available_stations
from app.services.tourism import fetch_nearby_tourism_spots, THEME_CONTENT_TYPE_MAP
from app.services.course_generator import generate_course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/recommend", response_model=CourseResponse)
async def recommend_course(request: CourseRequest):
    """
    사용자 취향 기반 자전거 관광 코스 추천

    1. 공공데이터 API 병렬 호출 (자전거 대여소 + 관광지)
    2. LangChain 3단계 체인으로 코스 생성
    3. XAI 방식 추천 사유와 함께 응답
    """
    import asyncio

    content_type_id = THEME_CONTENT_TYPE_MAP.get(request.theme)
    radius_m = int(request.radius_km * 1000)

    # 비동기 병렬 호출: 자전거 대여소 + 관광지 데이터
    bike_task = fetch_nearby_bike_stations(
        request.latitude, request.longitude, request.radius_km
    )
    tourism_task = fetch_nearby_tourism_spots(
        request.latitude, request.longitude, radius_m, content_type_id
    )
    bike_stations_raw, tourism_spots = await asyncio.gather(bike_task, tourism_task)

    # 대여 가능 자전거 2대 이상 필터링
    bike_stations = filter_available_stations(bike_stations_raw)

    # LangChain 3단계 체인 실행
    course = await generate_course(
        theme=request.theme,
        latitude=request.latitude,
        longitude=request.longitude,
        tourism_data=tourism_spots,
        bike_stations=bike_stations,
        max_waypoints=request.max_waypoints,
    )

    return course
