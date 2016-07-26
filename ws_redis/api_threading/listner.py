
import redis
import json
import time

r = redis.StrictRedis(host='178.18.31.65', port=6666, db=0)
p = r.pubsub()

p.subscribe('api_channel')
while True:
    message = p.get_message()
    if message:
        print("in my handler function")
        print(message["data"])
    time.sleep(0.001)  # be nice to the system :)