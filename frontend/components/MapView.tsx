"use client";

import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { Project } from "@/app/page";
import { useTheme } from "next-themes";

// Fix missing marker icons in Next.js / webpack builds
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Status → colour mapping for custom marker icons
const STATUS_COLORS: Record<string, string> = {
  Active: "#22c55e",
  Abandoned: "#ef4444",
  Completed: "#3b82f6",
};

function getStatusIcon(status: string) {
  const color = STATUS_COLORS[status] ?? "#6b7280";
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="40" viewBox="0 0 28 40">
    <path fill="${color}" stroke="white" stroke-width="2"
      d="M14 0C6.268 0 0 6.268 0 14c0 9.333 14 26 14 26S28 23.333 28 14C28 6.268 21.732 0 14 0z"/>
    <circle fill="white" cx="14" cy="14" r="6"/>
  </svg>`;
  return L.divIcon({
    html: svg,
    iconSize: [28, 40],
    iconAnchor: [14, 40],
    popupAnchor: [0, -40],
    className: "",
  });
}

interface MapViewProps {
  projects: Project[];
  onSelectProject: (p: Project) => void;
}

export default function MapView({ projects, onSelectProject }: MapViewProps) {
  const { resolvedTheme } = useTheme();
  // Use a stable key to prevent "Map container already initialized" on HMR
  const mapKey = useRef(`map-${Date.now()}`);

  const tileUrl =
    resolvedTheme === "dark"
      ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

  const attribution =
    resolvedTheme === "dark"
      ? '© <a href="https://carto.com/">CartoDB</a>'
      : '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';

  return (
    <MapContainer
      key={mapKey.current}
      center={[9.082, 8.6753]}
      zoom={6}
      className="w-full h-full z-0"
    >
      <TileLayer attribution={attribution} url={tileUrl} />

      {projects.map((proj) => (
        <Marker
          key={proj.id}
          position={[proj.location.lat, proj.location.lng]}
          icon={getStatusIcon(proj.status)}
          eventHandlers={{
            click: () => onSelectProject(proj),
          }}
        >
          <Popup>
            <div className="font-semibold text-gray-900">{proj.name}</div>
            <div className="text-sm text-gray-500">{proj.location.label}</div>
            <div
              className="text-xs font-medium mt-1"
              style={{ color: STATUS_COLORS[proj.status] ?? "#6b7280" }}
            >
              {proj.status}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
