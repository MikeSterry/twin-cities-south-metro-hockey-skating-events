import React from "react";
import { isIOS, isMacOs } from "react-device-detect";
import { downloadICS, googleCalendarUrl } from "./calendarUtils";

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

function isHappeningNow(startTime, endTime) {
  const now = new Date();
  const start = new Date(startTime.replace(" ", "T"));
  const end = new Date(endTime.replace(" ", "T"));
  return now >= start && now <= end;
}

export default function EventList({ events }) {
  return (
    <ul className="event-list">
      {events.map((event, i) => {
        const live = isHappeningNow(event.start_time, event.end_time);
        return (
          <li
            key={i}
            className={`event-card${live ? " event-card--live" : ""}`}
          >
            <div className="card-header">
              <div className="card-badges">
                <span className={badgeClass(event.event_type)}>
                  {event.event_type}
                </span>
                {live && <span className="live-badge">LIVE</span>}
              </div>
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
              <div className="card-actions">
                {isIOS || isMacOs ? (
                  <button
                    className="card-action-btn"
                    onClick={() => downloadICS(event)}
                    title="Add to Calendar"
                  >
                    📅 Add to Calendar
                  </button>
                ) : (
                  <a
                    className="card-action-btn"
                    href={googleCalendarUrl(event)}
                    target="_blank"
                    rel="noreferrer"
                    title="Add to Google Calendar"
                  >
                    📅 Add to Calendar
                  </a>
                )}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
