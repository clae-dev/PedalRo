"use client";

import type { CourseResponse } from "@/types/course";

interface CourseResultProps {
  course: CourseResponse;
}

export default function CourseResult({ course }: CourseResultProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border p-6 space-y-4">
      <div>
        <h2 className="text-xl font-bold text-gray-900">{course.title}</h2>
        <div className="flex gap-4 mt-2 text-sm text-gray-500">
          {course.total_distance_km && (
            <span>총 {course.total_distance_km.toFixed(1)}km</span>
          )}
          {course.estimated_minutes && (
            <span>약 {course.estimated_minutes}분</span>
          )}
        </div>
      </div>

      {/* XAI 추천 사유 */}
      <div className="bg-blue-50 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-800 mb-2">
          AI 추천 사유
        </h3>
        <p className="text-sm text-blue-700 leading-relaxed">
          {course.explanation}
        </p>
      </div>

      {/* 경유지 목록 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">코스 경로</h3>
        <ol className="space-y-3">
          {course.waypoints.map((wp) => (
            <li key={wp.order} className="flex items-start gap-3">
              <span
                className={`flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                  wp.category === "bike_station"
                    ? "bg-green-500"
                    : "bg-blue-500"
                }`}
              >
                {wp.order}
              </span>
              <div>
                <p className="font-medium text-gray-900">{wp.name}</p>
                {wp.description && (
                  <p className="text-sm text-gray-500">{wp.description}</p>
                )}
                <span className="text-xs text-gray-400">
                  {wp.category === "bike_station" ? "자전거 대여소" : "관광지"}
                </span>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
