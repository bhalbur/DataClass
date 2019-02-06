from flask import Flask, render_template, redirect
import datetime
from flask_pymongo import PyMongo
import pandas as pd

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"
mongo = PyMongo(app)
last_update = ''

@app.route("/")
def main():
	news = mongo.db.variables.find({'type':'news'})[0]
	#featured_image = mongo.db.variables.find({'type':'featured_image'})[0]
	weather = mongo.db.variables.find({'type':'weather'})[0]
	plain_facts = mongo.db.variables.find_one({'type':'facts'})['content']
	facts_df = pd.DataFrame([plain_facts])
	facts = facts_df.to_html(index=False)
	hemi = mongo.db.variables.find({'type':'hemisphere'})
	
	return render_template("index.html", 
		last_update = last_update,
		news = news,
		featured_image = 'abc',
		weather = weather,
		facts = facts,
		hemi = hemi)


@app.route("/scrape")
def scrape():
	from mars_mission import news, image, weather, facts, hemi
	#news()
	#image()
	#weather()
	#facts()
	#hemi()
	last_update = datetime.datetime.now().strftime("%b %d, %Y at %H:%M")

	return redirect("/test")



@app.route("/test1")
def test1():
	plain_facts = mongo.db.variables.find_one({'type':'facts'})['content']
	facts_df = pd.DataFrame([plain_facts])
	facts = facts_df.to_html(index=False)

	return facts


if __name__ == "__main__":
    app.run(debug=True)
