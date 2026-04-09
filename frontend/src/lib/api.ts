import type { CourseRequest, CourseResponse } from "@/types/course";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function recommendCourse(
  request: CourseRequest
): Promise<CourseResponse> {
  const response = await fetch(`${API_BASE}/api/v1/courses/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
