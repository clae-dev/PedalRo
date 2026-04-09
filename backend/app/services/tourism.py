"""한국관광공사 국문 관광정보 서비스 API 연동 서비스"""

import httpx

from app.core.config import settings

TOUR_API_BASE = "http://apis.data.go.kr/B551011/KorService1"


async def fetch_nearby_tourism_spots(
    latitude: float,
    longitude: float,
    radius_m: int = 5000,
    content_type_id: str | None = None,
) -> list[dict]:
    """
    한국관광공사 위치기반 관광정보 API를 호출하여 주변 관광지 목록을 반환합니다.

    Args:
        latitude: 위도
        longitude: 경도
        radius_m: 검색 반경 (미터)
        content_type_id: 관광 타입 (12=관광지, 14=문화시설, 39=음식점 등)
    """
    params = {
        "serviceKey": settings.TOUR_API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "PedalRo",
        "_type": "json",
        "mapX": str(longitude),
        "mapY": str(latitude),
        "radius": str(radius_m),
        "numOfRows": "50",
        "pageNo": "1",
    }
    if content_type_id:
        params["contentTypeId"] = content_type_id

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{TOUR_API_BASE}/locationBasedList1", params=params
        )
        response.raise_for_status()
        data = response.json()

    items = (
        data.get("response", {})
        .get("body", {})
        .get("items", {})
        .get("item", [])
    )
    return items if isinstance(items, list) else [items] if items else []


# 테마 → 관광 타입 매핑
THEME_CONTENT_TYPE_MAP = {
    "자연": "12",   # 관광지
    "역사": "14",   # 문화시설
    "맛집": "39",   # 음식점
    "힐링": "12",   # 관광지
    "문화": "14",   # 문화시설
}
