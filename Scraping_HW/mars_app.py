from flask import Flask, render_template
import datetime


app = Flask(__name__)

@app.route("/")
def main():
	return render_template("index.html", var_text="Hello and Welcome", var2="It's nice to see you again")

@app.route("/scrape")
def scrape():
	from mars_mission import setup, news, image, weather, facts, hemi, store
	setup()
	news()
	image()
	weather()
	facts()
	hemi()
	store()
	return(f'Fresh Data scraped at {datetime.datetime.now()}')


#@app.route("/<var_input>/<var2_input>")
#def variables(var_input, var2_input):
#	return render_template("index.html", var_text=var_input, var2=var2_input)


#@app.route("/classmates")
#def classmates():
#	class_list=['Ryan','Albert','Mark','Adam']
#	instr_list=['Vishal','Adam','Hussain']
#	return render_template("classmates.html", 
#		class_list=class_list, instr_list=instr_list)

if __name__ == "__main__":
    app.run(debug=True)
