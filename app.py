import flask
import redis
import time

app = flask.Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.ConnectionError as exc:
            if retries == 0:
                return exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    hits = get_hit_count()
    return "My hits is {}".format(hits)
    
