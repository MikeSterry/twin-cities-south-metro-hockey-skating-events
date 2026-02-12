import colorama
colorama.init = lambda *args, **kwargs: None  # Prevent tatsu/ics from repeatedly wrapping stdout

from flask import Flask, jsonify, make_response
from flask_caching import Cache
from handlers.Event_Handler import EventHandler

app = Flask(__name__)
config = {'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 43200}
cache = Cache(app, config=config)
app.json.sort_keys = False

@app.route('/api/get_events', methods=['GET'])
@cache.cached(timeout=43200)
def get_events():
    events = EventHandler().get_events()
    response = make_response(jsonify(events))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/api/clear_cache', methods=['GET'])
def clear_cache():
    print('Clearing cache...')
    cache.clear()
    return make_response("success")

if __name__ == "__main__":
    app.run(debug=True)