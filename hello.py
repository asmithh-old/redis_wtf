from flask import Flask, render_template
app = Flask(__name__)
import os, redis
from flask import Response, json
from flask import request
import itertools

db = redis.StrictRedis('localhost')


@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/like_this', methods = ['GET', 'POST'])
def post_like_this():
    if request.method == 'POST':
        result = request.form
        why = result.values()[0]
        name = result.values()[1]
        db.lpush(name, why)
        db.sadd('users', name)
        users = db.smembers('users')
        users_list = list(users)
        reasons = []
        for u in users_list:
            for r in db.lrange(str(u), 0, -1):
                reasons.append((u, r))
        return render_template('like_this.html', reasons = reasons)

#@app.route('/like_this', methods = ['POST'])
#def like_this():
#    return render_template('like_this.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0')




