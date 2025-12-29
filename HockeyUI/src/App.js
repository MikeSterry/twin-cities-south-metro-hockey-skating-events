import { useEffect, useState } from "react";
import EventList from "./EventList";

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
    <>
      <div className="container">
        <img
          className="top-banner"
          src="images/banner.jpg"
          alt="Top banner"
        />
        <h1>Twin Cities - South Metro: Upcoming Hockey Events</h1>
        <EventList events={events} />
      </div>

      {/* FOOTER */}
      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-section">
            <h3>About</h3>
            <p>
              Community-maintained list of public hockey, open skate,
              and stick-and-puck events in the Twin Cities south metro area.
            </p>
          </div>

          <div className="footer-section">
            <h3>Links</h3>
            <ul>
              <li>
                <a
                  href="https://github.com/MikeSterry/twin-cities-south-metro-hockey-skating-events"
                  target="_blank"
                  rel="noreferrer"
                >
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href="http://allenphotoworks.com">
                  Paul Allen Photography
                </a>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Contact</h3>
            <p>
              Suggestions or corrections?
              Open an issue or submit a PR on GitHub.
            </p>
            <h3>Photo provided with permission by Paul Allen Photography.</h3>
            <p>
              Paul Allen is a professional photographer based in the Twin Cities South Metro area.
              He specializes in sports photography, family portraits, event photography, or capturing any of your memories.
              Visit&nbsp;
              <a href="http://allenphotoworks.com">allenphotoworks.com</a>
              Email&nbsp;
              <a href="mailto:paul@allenphotoworks.com">paul@allenphotoworks.com</a>
            </p>
          </div>
        </div>

        <div className="footer-bottom">
          © {new Date().getFullYear()} Twin Cities Hockey Events
        </div>
      </footer>
    </>
  );
}

export default App;
