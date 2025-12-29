import { useEffect, useState } from "react";
import EventList from "./EventList";
import { Footer } from "./Footer";

const API_URL = process.env.REACT_APP_API_URL || "/api/get_events";

function App() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) return <p>Loading events…</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <div className="container">
        <img
          className="top-banner"
          src="images/banner.jpg"
          alt="Top banner"
        />
        <h1>Twin Cities - South Metro: Upcoming Hockey Events</h1>
        <EventList events={events} />
        <Footer />
      </div>
    </div>
  );
}

export default App;
