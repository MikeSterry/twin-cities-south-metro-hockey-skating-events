function formatICSDate(dateStr) {
  const d = new Date(dateStr.replace(" ", "T"));
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}T${pad(d.getHours())}${pad(d.getMinutes())}00`;
}

export function downloadICS(event) {
  const start = formatICSDate(event.start_time);
  const end = formatICSDate(event.end_time);
  const addr = event.arena.address;
  const location = `${event.arena.name}, ${addr.street}, ${addr.city}, ${addr.state} ${addr.zip_code}`;
  const description = [
    event.notes,
    event.cost?.cost != null ? `Cost: $${event.cost.cost}` : null,
  ]
    .filter(Boolean)
    .join("\\n");

  const lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//HockeyEvents//EN",
    "BEGIN:VEVENT",
    `DTSTART:${start}`,
    `DTEND:${end}`,
    `SUMMARY:${event.event_type} - ${event.arena.name}`,
    `LOCATION:${location}`,
  ];
  if (description) lines.push(`DESCRIPTION:${description}`);
  lines.push("END:VEVENT", "END:VCALENDAR");

  const blob = new Blob([lines.join("\r\n")], { type: "text/calendar" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${event.event_type.replace(/\s+/g, "_")}_${event.arena.name.replace(/\s+/g, "_")}.ics`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export function googleCalendarUrl(event) {
  const start = formatICSDate(event.start_time);
  const end = formatICSDate(event.end_time);
  const addr = event.arena.address;
  const location = `${event.arena.name}, ${addr.street}, ${addr.city}, ${addr.state} ${addr.zip_code}`;
  const details = [
    event.notes,
    event.cost?.cost != null ? `Cost: $${event.cost.cost}` : null,
  ]
    .filter(Boolean)
    .join("\n");

  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: `${event.event_type} - ${event.arena.name}`,
    dates: `${start}/${end}`,
    location,
    details,
  });
  return `https://calendar.google.com/calendar/render?${params}`;
}
