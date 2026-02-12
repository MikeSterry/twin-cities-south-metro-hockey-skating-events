import React from "react";

export const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-grid">
        <div className="footer-section">
          <h3>About</h3>
          <p>
            Community-maintained list of public/open skate, and stick-and-puck
            events in the Twin Cities south metro area.
          </p>
        </div>

        <div className="footer-section">
          <h3>Contact</h3>
          <p>Suggestions or corrections?</p>
          <p>
            Open an issue or submit a PR on{" "}
            <a
              href="https://github.com/MikeSterry/twin-cities-south-metro-hockey-skating-events"
              target="_blank"
              rel="noreferrer"
            >
              GitHub
            </a>
          </p>
        </div>

        <div className="footer-section">
          <h3>Credits</h3>
          <h4>Photo provided with permission by Allen Photo Works.</h4>
          <p>
            Paul Allen is a professional photographer based in the Twin Cities
            South Metro area.
          </p>
          <p>
            He specializes in sports photography, family portraits, event
            photography, or capturing any of your memories.
          </p>
          <p>
            Visit:{" "}
            <a href="http://allenphotoworks.com" target="_blank" rel="noreferrer">
              allenphotoworks.com
            </a>
          </p>
          <p>
            Email:{" "}
            <a href="mailto:paul@allenphotoworks.com">
              paul@allenphotoworks.com
            </a>
          </p>
        </div>
      </div>

      <div className="footer-bottom">
        © {new Date().getFullYear()} Twin Cities South Metro Hockey Events
      </div>
    </footer>
  );
};
