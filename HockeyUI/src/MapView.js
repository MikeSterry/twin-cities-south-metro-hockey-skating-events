import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import { arenaCoordinates } from "./arenaCoordinates";

// Fix Leaflet's default icon path issue with CRA/webpack
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function formatTime(value) {
  return new Date(value.replace(" ", "T")).toLocaleString(undefined, {
    weekday: "short",
    hour: "numeric",
    minute: "2-digit",
  });
}

function groupEventsByArena(events) {
  const groups = {};
  events.forEach((event) => {
    const name = event.arena.name;
    const coords = arenaCoordinates[name];
    if (!coords) return;
    if (!groups[name]) {
      groups[name] = {
        name,
        city: event.arena.address.city,
        coords,
        events: [],
      };
    }
    groups[name].events.push(event);
  });
  return Object.values(groups);
}

export default function MapView({ events }) {
  const arenas = groupEventsByArena(events);

  return (
    <div className="map-container">
      <MapContainer
        center={[44.78, -93.25]}
        zoom={11}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {arenas.map((arena) => (
          <Marker key={arena.name} position={arena.coords}>
            <Popup>
              <p className="map-popup-title">{arena.name}</p>
              <p className="map-popup-city">{arena.city}</p>
              <ul className="map-popup-events">
                {arena.events.map((event, i) => (
                  <li key={i} className="map-popup-event">
                    <span
                      className={`map-popup-badge ${
                        event.event_type === "Open Skate"
                          ? "map-popup-badge--skate"
                          : "map-popup-badge--puck"
                      }`}
                    >
                      {event.event_type}
                    </span>
                    {formatTime(event.start_time)} –{" "}
                    {formatTime(event.end_time)}
                    {event.cost?.cost != null && ` · $${event.cost.cost}`}
                  </li>
                ))}
              </ul>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
