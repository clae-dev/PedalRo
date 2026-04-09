"use client";

import type { Theme } from "@/types/course";

const THEMES: { value: Theme; label: string; icon: string }[] = [
  { value: "자연", label: "자연", icon: "🌿" },
  { value: "역사", label: "역사", icon: "🏛️" },
  { value: "맛집", label: "맛집", icon: "🍽️" },
  { value: "힐링", label: "힐링", icon: "💆" },
  { value: "문화", label: "문화", icon: "🎭" },
];

interface ThemeSelectorProps {
  selected: Theme | null;
  onSelect: (theme: Theme) => void;
}

export default function ThemeSelector({
  selected,
  onSelect,
}: ThemeSelectorProps) {
  return (
    <div className="flex gap-3 flex-wrap">
      {THEMES.map(({ value, label, icon }) => (
        <button
          key={value}
          onClick={() => onSelect(value)}
          className={`flex items-center gap-2 px-4 py-2 rounded-full border-2 transition-all ${
            selected === value
              ? "border-blue-500 bg-blue-50 text-blue-700"
              : "border-gray-200 hover:border-gray-300 text-gray-600"
          }`}
        >
          <span>{icon}</span>
          <span className="font-medium">{label}</span>
        </button>
      ))}
    </div>
  );
}
