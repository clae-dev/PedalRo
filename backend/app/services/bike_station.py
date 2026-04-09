"""공영자전거 실시간 대여소 정보 API 연동 서비스"""

import httpx

from app.core.config import settings


async def fetch_nearby_bike_stations(
    latitude: float, longitude: float, radius_km: float = 5.0
) -> list[dict]:
    """
    행정안전부/지자체 공영자전거 실시간 API를 호출하여
    반경 내 대여 가능 수량이 MIN_AVAILABLE_BIKES 이상인 대여소를 반환합니다.
    """
    # TODO: 실제 공공데이터 API 엔드포인트 연동
    # 현재는 인터페이스 정의만 해둔 상태
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 예시: 서울시 따릉이 API 호출 구조
        # response = await client.get(
        #     "http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/1/1000/",
        # )
        pass

    # TODO: 응답 파싱 후 MIN_AVAILABLE_BIKES 필터링
    return []


def filter_available_stations(stations: list[dict]) -> list[dict]:
    """대여 가능 자전거가 기준치 이상인 대여소만 필터링"""
    return [
        s for s in stations
        if s.get("available_bikes", 0) >= settings.MIN_AVAILABLE_BIKES
    ]
