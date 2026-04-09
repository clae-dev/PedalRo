"use client";

import { useEffect, useRef } from "react";
import type { Waypoint } from "@/types/course";

declare global {
  interface Window {
    kakao: any;
  }
}

interface KakaoMapProps {
  waypoints: Waypoint[];
  center?: { lat: number; lng: number };
}

export default function KakaoMap({ waypoints, center }: KakaoMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!window.kakao?.maps || !mapRef.current) return;

    const mapCenter = center
      ? new window.kakao.maps.LatLng(center.lat, center.lng)
      : new window.kakao.maps.LatLng(37.5665, 126.978); // 서울 시청 기본값

    const map = new window.kakao.maps.Map(mapRef.current, {
      center: mapCenter,
      level: 5,
    });

    // 마커 표시
    const markers = waypoints.map((wp) => {
      const position = new window.kakao.maps.LatLng(wp.latitude, wp.longitude);
      const marker = new window.kakao.maps.Marker({ map, position });

      const infowindow = new window.kakao.maps.InfoWindow({
        content: `<div style="padding:5px;font-size:12px;"><strong>${wp.name}</strong><br/>${wp.description || ""}</div>`,
      });

      window.kakao.maps.event.addListener(marker, "click", () => {
        infowindow.open(map, marker);
      });

      return marker;
    });

    // Polyline 경로 표시
    if (waypoints.length >= 2) {
      const path = waypoints.map(
        (wp) => new window.kakao.maps.LatLng(wp.latitude, wp.longitude)
      );

      new window.kakao.maps.Polyline({
        map,
        path,
        strokeWeight: 4,
        strokeColor: "#3B82F6",
        strokeOpacity: 0.8,
        strokeStyle: "solid",
      });

      // 경로에 맞게 지도 범위 조정
      const bounds = new window.kakao.maps.LatLngBounds();
      path.forEach((p: any) => bounds.extend(p));
      map.setBounds(bounds);
    }
  }, [waypoints, center]);

  return <div ref={mapRef} className="w-full h-full rounded-lg" />;
}
