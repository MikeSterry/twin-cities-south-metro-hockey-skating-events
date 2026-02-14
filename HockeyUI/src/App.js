import { useEffect, useMemo, useState } from "react";
import EventList from "./EventList";
import { Footer } from "./Footer";
import MapView from "./MapView";

const API_URL = process.env.REACT_APP_API_URL || "/api/get_events";

function formatDateLabel(dateStr) {
  const [year, month, day] = dateStr.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

function getInitialTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "dark" || saved === "light") return saved;
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function getInitialFilters() {
  const params = new URLSearchParams(window.location.search);
  return {
    city: params.get("city") || "",
    date: params.get("date") || "",
    type: params.get("type") || "",
    sort: params.get("sort") || "time",
  };
}

function App() {
  const initial = getInitialFilters();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterCity, setFilterCity] = useState(initial.city);
  const [filterDate, setFilterDate] = useState(initial.date);
  const [filterType, setFilterType] = useState(initial.type);
  const [sortBy, setSortBy] = useState(initial.sort);
  const [viewMode, setViewMode] = useState("list");
  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  function toggleTheme() {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  }

  // Sync filter state to URL
  useEffect(() => {
    const params = new URLSearchParams();
    if (filterCity) params.set("city", filterCity);
    if (filterDate) params.set("date", filterDate);
    if (filterType) params.set("type", filterType);
    if (sortBy && sortBy !== "time") params.set("sort", sortBy);
    const qs = params.toString();
    const url = window.location.pathname + (qs ? `?${qs}` : "");
    window.history.replaceState(null, "", url);
  }, [filterCity, filterDate, filterType, sortBy]);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setEvents(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load events");
        setLoading(false);
      });
  }, []);

  const cities = useMemo(
    () =>
      [...new Set(events.map((e) => e.arena.address.city))].sort(),
    [events]
  );

  const dates = useMemo(
    () =>
      [...new Set(events.map((e) => e.start_time.split(" ")[0]))].sort(),
    [events]
  );

  const filteredEvents = useMemo(() => {
    const filtered = events.filter((e) => {
      if (filterCity && e.arena.address.city !== filterCity) return false;
      if (filterDate && !e.start_time.startsWith(filterDate)) return false;
      if (filterType && e.event_type !== filterType) return false;
      return true;
    });
    if (sortBy === "cost-asc") {
      return [...filtered].sort(
        (a, b) => (a.cost?.cost ?? Infinity) - (b.cost?.cost ?? Infinity)
      );
    }
    if (sortBy === "cost-desc") {
      return [...filtered].sort(
        (a, b) => (b.cost?.cost ?? -1) - (a.cost?.cost ?? -1)
      );
    }
    return filtered;
  }, [events, filterCity, filterDate, filterType, sortBy]);

  const hasActiveFilter = filterCity || filterDate || filterType || sortBy !== "time";

  function clearFilters() {
    setFilterCity("");
    setFilterDate("");
    setFilterType("");
    setSortBy("time");
  }

  if (loading)
    return (
      <div className="container">
        <div className="state-message">
          <p className="loading-dots">Loading events…</p>
        </div>
      </div>
    );

  if (error)
    return (
      <div className="container">
        <div className="state-message state-message--error">
          <p>{error}</p>
        </div>
      </div>
    );

  return (
    <div>
      <div className="container">
        <div className="hero">
          <img
            className="hero-banner"
            src="images/banner.jpg"
            alt="Hockey goalie guarding the net"
          />
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          >
            {theme === "dark" ? "\u2600\uFE0F" : "\uD83C\uDF19"}
          </button>
          <div className="hero-overlay">
            <h1 className="hero-title">
              Twin Cities South Metro: Upcoming Hockey &amp; Skating Events
            </h1>
          </div>
        </div>
        <div className="filter-bar">
          <div className="filter-group">
            <label className="filter-label" htmlFor="filter-city">City</label>
            <select
              id="filter-city"
              className="filter-select"
              value={filterCity}
              onChange={(e) => setFilterCity(e.target.value)}
            >
              <option value="">All Cities</option>
              {cities.map((city) => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label" htmlFor="filter-date">Date</label>
            <select
              id="filter-date"
              className="filter-select"
              value={filterDate}
              onChange={(e) => setFilterDate(e.target.value)}
            >
              <option value="">All Dates</option>
              {dates.map((d) => (
                <option key={d} value={d}>{formatDateLabel(d)}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <span className="filter-label">Event Type</span>
            <div className="filter-chips">
              {["", "Open Skate", "Stick and Puck"].map((type) => (
                <button
                  key={type}
                  className={`filter-chip${filterType === type ? " filter-chip--active" : ""}`}
                  onClick={() => setFilterType(type)}
                >
                  {type || "All"}
                </button>
              ))}
            </div>
          </div>

          <div className="filter-group">
            <label className="filter-label" htmlFor="filter-sort">Sort</label>
            <select
              id="filter-sort"
              className="filter-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="time">Time</option>
              <option value="cost-asc">Cost: Low to High</option>
              <option value="cost-desc">Cost: High to Low</option>
            </select>
          </div>

          <div className="filter-summary">
            <span>
              Showing {filteredEvents.length} of {events.length} events
            </span>
            {hasActiveFilter && (
              <button className="filter-clear" onClick={clearFilters}>
                Clear filters
              </button>
            )}
            <div className="view-toggle">
              <button
                className={`view-toggle-btn${viewMode === "list" ? " view-toggle-btn--active" : ""}`}
                onClick={() => setViewMode("list")}
                aria-label="List view"
              >
                ☰
              </button>
              <button
                className={`view-toggle-btn${viewMode === "map" ? " view-toggle-btn--active" : ""}`}
                onClick={() => setViewMode("map")}
                aria-label="Map view"
              >
                🗺
              </button>
            </div>
          </div>
        </div>

        {viewMode === "map" ? (
          <MapView events={filteredEvents} />
        ) : (
          <EventList events={filteredEvents} />
        )}
      </div>
      <Footer />
    </div>
  );
}

export default App;
