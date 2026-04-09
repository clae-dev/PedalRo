from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/pedalro"

    # External APIs
    ANTHROPIC_API_KEY: str = ""
    KAKAO_REST_API_KEY: str = ""
    TOUR_API_KEY: str = ""  # 한국관광공사 국문 관광정보 서비스 API 키

    # Bike station filter
    MIN_AVAILABLE_BIKES: int = 2  # 최소 대여 가능 자전거 수

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
