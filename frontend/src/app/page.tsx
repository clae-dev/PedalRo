"use client";

import { useState } from "react";
import ThemeSelector from "@/components/ThemeSelector";
import CourseResult from "@/components/CourseResult";
import KakaoMap from "@/components/KakaoMap";
import { recommendCourse } from "@/lib/api";
import type { Theme, CourseResponse } from "@/types/course";

export default function Home() {
  const [theme, setTheme] = useState<Theme | null>(null);
  const [course, setCourse] = useState<CourseResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRecommend = async () => {
    if (!theme) return;
    setLoading(true);
    setError(null);

    try {
      // 사용자 위치 가져오기 (기본값: 서울 시청)
      let lat = 37.5665;
      let lng = 126.978;

      if (navigator.geolocation) {
        try {
          const pos = await new Promise<GeolocationPosition>(
            (resolve, reject) =>
              navigator.geolocation.getCurrentPosition(resolve, reject, {
                timeout: 5000,
              })
          );
          lat = pos.coords.latitude;
          lng = pos.coords.longitude;
        } catch {
          // 위치 권한 거부 시 기본값 사용
        }
      }

      const result = await recommendCourse({
        latitude: lat,
        longitude: lng,
        theme,
      });
      setCourse(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "코스 추천에 실패했습니다."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="bg-white border-b px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-900">
          페달로
          <span className="text-blue-600 ml-1 text-sm font-normal">
            PedalRo
          </span>
        </h1>
        <p className="text-sm text-gray-500 mt-1">
          AI 기반 자전거 관광 코스 큐레이션
        </p>
      </header>

      <main className="flex-1 flex flex-col lg:flex-row">
        {/* 사이드 패널 */}
        <aside className="w-full lg:w-[420px] p-6 space-y-6 overflow-y-auto">
          {/* 테마 선택 */}
          <section>
            <h2 className="text-lg font-semibold text-gray-800 mb-3">
              테마 선택
            </h2>
            <ThemeSelector selected={theme} onSelect={setTheme} />
          </section>

          {/* 추천 버튼 */}
          <button
            onClick={handleRecommend}
            disabled={!theme || loading}
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "코스 생성 중..." : "코스 추천받기"}
          </button>

          {error && (
            <p className="text-sm text-red-600 bg-red-50 p-3 rounded-lg">
              {error}
            </p>
          )}

          {/* 추천 결과 */}
          {course && <CourseResult course={course} />}
        </aside>

        {/* 지도 영역 */}
        <div className="flex-1 min-h-[400px] lg:min-h-0">
          <KakaoMap
            waypoints={course?.waypoints ?? []}
            center={
              course?.waypoints?.[0]
                ? {
                    lat: course.waypoints[0].latitude,
                    lng: course.waypoints[0].longitude,
                  }
                : undefined
            }
          />
        </div>
      </main>
    </div>
  );
}
