import React from "react";
import { isIOS, isMacOs } from "react-device-detect";

function mapLink(address) {
  if (isIOS || isMacOs) {
    return (
      "https://maps.apple.com/?q=" +
      encodeURIComponent(
        address.street +
          ", " +
          address.city +
          ", " +
          address.state +
          " " +
          address.zip_code
      )
    );
  }
  return (
    "https://www.google.com/maps/search/?api=1&query=" +
    encodeURIComponent(
      address.street +
        ", " +
        address.city +
        ", " +
        address.state +
        " " +
        address.zip_code
    )
  );
}

function formatDateTime(value) {
  return new Date(value.replace(" ", "T")).toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function badgeClass(eventType) {
  if (eventType === "Open Skate") return "event-badge event-badge--skate";
  return "event-badge event-badge--puck";
}

export default function EventList({ events }) {
  return (
    <ul className="event-list">
      {events.map((event, i) => (
        <li key={i} className="event-card">
          <div className="card-header">
            <span className={badgeClass(event.event_type)}>
              {event.event_type}
            </span>
            <h2>
              <a
                href={mapLink(event.arena.address)}
                target="_blank"
                rel="noreferrer"
              >
                {event.arena.name}
              </a>
            </h2>
          </div>
          <div className="card-body">
            <div className="card-info-row">
              <span aria-hidden="true">📍</span>
              <span>{event.arena.address.city}</span>
            </div>
            <div className="card-info-row">
              <span aria-hidden="true">🕐</span>
              <span>
                {formatDateTime(event.start_time)} –{" "}
                {formatDateTime(event.end_time)}
              </span>
            </div>
            {event.notes && <p className="card-notes">{event.notes}</p>}
          </div>
          <div className="card-footer">
            <p className="card-cost">
              ${event.cost?.cost ?? "Cost Unknown"}
            </p>
          </div>
        </li>
      ))}
    </ul>
  );
}
