import json
import oauth2 as oauth
from secret import keys 
from flask import (Flask, jsonify, render_template)
from model import (connect_to_db, db, Tweet)
#import pprint    pp = pprint.PrettyPrinter(indent=4) pp.pprint(stufftoprint)
import time



app = Flask(__name__)
app.secret_key = "miau"


def authorize():
    """authorize w/ twitter api and fetch recent codenewbie tweets, return a json"""

    consumer = oauth.Consumer(key=keys["consumer_key"], secret=keys["consumer_secret"])
    access_token = oauth.Token(key=keys["access_token"], secret=keys["access_secret"])
    client = oauth.Client(consumer, access_token)
    test_url = "https://api.twitter.com/1.1/search/tweets.json?q=%23codenewbie&result_type=mixed&count=100&include_entities=false"
    response, data = client.request(test_url)

    return json.loads(data)


def format_tweets():
    """return a list of tuples of recent codenewbie tweets"""

    tweet = None
    time_created = None
    retweets = None
    results = authorize()["statuses"]
    output = []

    for result in results:
        if result['text'][0:2] != 'RT':
            tweet = result['text']
            time_created =  time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(result['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            handle = result['user']['screen_name']
            if 'retweeted_status' in result:
                retweets = result['retweeted_status']['retweet_count']
            output.append((handle, time_created, tweet, retweets))

    return output


@app.route("/")
def homepage():
    """Display tweets"""
    
    output = format_tweets()



    return render_template("home.html", output=output)




if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "postgresql:///newb")
    app.run(port=5000)
