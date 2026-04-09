export interface CourseRequest {
  latitude: number;
  longitude: number;
  theme: string;
  radius_km?: number;
  max_waypoints?: number;
}

export interface Waypoint {
  order: number;
  name: string;
  category: "bike_station" | "tourist_spot";
  latitude: number;
  longitude: number;
  description?: string;
}

export interface CourseResponse {
  title: string;
  theme: string;
  explanation: string;
  total_distance_km?: number;
  estimated_minutes?: number;
  waypoints: Waypoint[];
}

export type Theme = "자연" | "역사" | "맛집" | "힐링" | "문화";
