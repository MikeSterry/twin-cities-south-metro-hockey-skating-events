from datetime import datetime, timedelta
from flask import Flask, jsonify, make_response
from flask_caching import Cache
from models.Event import Event
from location_handlers.AppleValley import AppleValley
from location_handlers.Burnsville import Burnsville
from location_handlers.Lakeville import Lakeville
from location_handlers.Eagan import Eagan
from location_handlers.Rosemount import Rosemount
from location_handlers.Bloomington import Bloomington
from location_handlers.Edina import Edina
from location_handlers.InverGroveHeights import InverGroveHeights
from location_handlers.Richfield import Richfield
from location_handlers.SouthStPaul import SouthStPaul

app = Flask(__name__)
config = {'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 43200}
cache = Cache(app, config=config)
app.json.sort_keys = False

apple_valley_handler = AppleValley()
burnsville_handler = Burnsville()
lakeville_handler = Lakeville()
eagan_handler = Eagan()
rosemount_handler = Rosemount()
bloomington_handler = Bloomington()
edina_handler = Edina()
inver_grove_heights_handler = InverGroveHeights()
richfield_handler = Richfield()
south_st_paul_handler = SouthStPaul()

@app.route('/api/public_skate_events', methods=['GET'])
@cache.cached(timeout=43200)
def get_public_skate_events():
    events = get_events()
    response = make_response(jsonify(events))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/api/clear_cache', methods=['GET'])
def clear_cache():
    print('Clearing cache...')
    cache.clear()
    return make_response("success")

def get_events() -> list[Event]:
    events = get_location_events()
    print(f'Total events fetched: {len(events)}')
    filtered_events = filter_events_next_24_hours(events)
    print(f'Total events after filtering: {len(filtered_events)}')
    ordered_events = sort_events_by_start_time(filtered_events)

    if ordered_events:
        events_json = []
        for event in ordered_events:
            event_data = {
                "arena": {
                    "name": event.arena.name,
                    "address": {
                        "street": event.arena.address.street,
                        "city": event.arena.address.city,
                        "state": event.arena.address.state,
                        "zip_code": event.arena.address.zip_code
                    },
                    "notes": event.arena.notes
                },
                "event_type": event.event_type.value,
                "start_time": event.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": event.end_time.strftime("%Y-%m-%d %H:%M"),
                "notes": event.notes,
                "cost": {
                    "cost": event.cost.get_cost()
                }
            }
            events_json.append(event_data)
        return events_json
    else:
        return []

def get_location_events() -> list[Event]:
    events = []
    events.extend(apple_valley_handler.get_events())
    events.extend(burnsville_handler.get_events())
    events.extend(lakeville_handler.get_events())
    events.extend(eagan_handler.get_events())
    events.extend(rosemount_handler.get_events())
    events.extend(bloomington_handler.get_events())
    events.extend(inver_grove_heights_handler.get_events())
    events.extend(richfield_handler.get_events())
    events.extend(south_st_paul_handler.get_events())

    # events.extend(edina_handler.get_events())                 # Todo: Finish Edina handler
    # Farmington handler not implemented yet
    # Mistic Lake handler not implemented yet
    # Shakopee handler not implemented yet
    # Highland handler not implemented yet
    # Pleasant handler not implemented yet
    # West St Paul handler not implemented yet

    return events

"""
Filter events by date range (optional) - next 24 hours
"""
def filter_events_next_24_hours(events: list[Event]) -> list[Event]:
    now = datetime.now()
    next_24_hours = now + timedelta(hours=48)
    return filter_events_by_date_range(events, now, next_24_hours)

"""
Filter events by date range
"""
def filter_events_by_date_range(events: list[Event], start_date, end_date) -> list[Event]:
    filtered_events = []
    for event in events:
        # print(f'Event start time: {event.start_time}, Filter range: {start_date} - {end_date}')
        if start_date <= event.start_time <= end_date:
            # print(f'{event.start_time} is greater than {start_date} and less than {end_date}')
            filtered_events.append(event)
    return filtered_events

"""
Sort events by start time
"""
def sort_events_by_start_time(events: list[Event]) -> list[Event]:
    return sorted(events, key=lambda event: event.start_time)


if __name__ == "__main__":
    app.run(debug=True)