import { useEffect, useState } from "react";
import EventList from "./EventList";

const API_URL = process.env.REACT_APP_API_URL || "http://192.168.1.56:5600/api/public_skate_events";

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
    <div className="container">
      <h1>Twin Cities - South Metro: Upcoming Hockey Events</h1>
// ToDo: Add this image. I'd love to have it proportionally resize with the window.
//      <div className="flex-container">
//        <img src="images/HockeyBench.png" alt="bench with hockey skates, stick and a puck" />
//      </div>
      <EventList events={events} />
    </div>
  );
}

export default App;
