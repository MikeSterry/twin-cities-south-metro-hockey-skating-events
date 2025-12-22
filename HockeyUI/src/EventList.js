import React from "react";

function mapLink(address) {
  return "https://www.google.com/maps/search/?api=1&query=" +
    encodeURIComponent(address.street + ", " + address.city + ", " + address.state + " " + address.zip_code);
}

function formatDateTime(value) {
  return new Date(value.replace(" ", "T")).toLocaleString();
}

export default function EventList({ events }) {
  return (
    <ul className="event-list">
      {events.map((event, i) => (
        <li key={i} className="event-card">
          <h2>
            <a href={mapLink(event.arena.address)} target="_blank" rel="noreferrer">
              {event.arena.name}
            </a>
          </h2>
          <p><strong>City:</strong> {event.arena.address.city}</p>
          <p><strong>Event Type:</strong> {event.event_type}</p>
          <p><strong>Start:</strong> {formatDateTime(event.start_time)}</p>
          <p><strong>End:</strong> {formatDateTime(event.end_time)}</p>
          <p><strong>Cost:</strong> ${event.cost?.cost ?? "Cost Unknown"}</p>
          <p>{event.notes}</p>
        </li>
      ))}
    </ul>
  );
}
