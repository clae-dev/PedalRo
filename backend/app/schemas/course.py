from pydantic import BaseModel, Field


class CourseRequest(BaseModel):
    """코스 추천 요청"""
    latitude: float = Field(..., description="사용자 현재 위도")
    longitude: float = Field(..., description="사용자 현재 경도")
    theme: str = Field(..., description="테마 (자연, 역사, 맛집, 힐링, 문화)")
    radius_km: float = Field(default=5.0, description="탐색 반경 (km)")
    max_waypoints: int = Field(default=5, ge=2, le=10, description="최대 경유지 수")


class WaypointResponse(BaseModel):
    order: int
    name: str
    category: str
    latitude: float
    longitude: float
    description: str | None = None


class CourseResponse(BaseModel):
    """코스 추천 응답"""
    title: str
    theme: str
    explanation: str  # XAI 추천 사유
    total_distance_km: float | None = None
    estimated_minutes: int | None = None
    waypoints: list[WaypointResponse]


class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None
