from flask import Flask, render_template, send_from_directory
import statistics as stats
import socket
from flask import request
from difflib import get_close_matches
app = Flask(__name__)

database = []

counties = [
	"alameda",
	"alpine",
	"amador",
	"butte",
	"calaveras",
	"colusa",
	"contra Costa",
	"del Norte",
	"el Dorado",
	"fresno",
	"glenn",
	"humboldt",
	"imperial",
	"inyo",
	"kern",
	"kings",
	"lake",
	"lassen",
	"los Angeles",
	"madera",
	"marin",
	"mariposa",
	"mendocino",
	"merced",
	"modoc",
	"mono",
	"monterey",
	"napa",
	"nevada",
	"orange",
	"placer",
	"plumas",
	"riverside",
	"sacramento",
	"san Benito",
	"san Bernardino",
	"san Diego",
	"san Francisco",
	"san Joaquin",
	"san Luis Obispo",
	"san Mateo",
	"santa Barbara",
	"santa Clara",
	"santa Cruz",
	"shasta",
	"sierra",
	"siskiyou",
	"solano",
	"sonoma",
	"stanislaus"
]

class Result():
	raw: str
	parsed: list[str]
	score: float
	media: str
	def __init__(self, anwser: str, media: str):
		print(media)
		self.raw = anwser
		self.parsed = anwser.lower().replace(" ", "").replace("\r", "").split("\n")
		counties_copy = counties.copy()
		self.media = media
		self.score = 0
		for item in self.parsed:
			if get_close_matches(item, counties_copy, 1, 0.9) != []:
				counties_copy.remove(get_close_matches(item, counties_copy, 1, 0.9)[0])
				self.score += 1

id_counter = 0
class Research():
	rid: int
	name: str
	password_hash: int
	key: str
	data: list[Result]
	def __init__(self, name: str, password: str) -> None:
		global id_counter
		self.rid = id_counter
		id_counter += 1
		self.name = name
		self.password_hash = hash(password)
		self.key = get_key(self.password_hash)
		self.data = []
	def get_processed_data(self) -> dict:
		desktop_scores = list(map(lambda x: x.score, filter(lambda x: x.media == "desktop", self.data)))
		mobile_scores = list(map(lambda x: x.score, filter(lambda x: x.media == "mobile", self.data)))
		return {
			"desktop_average": stats.fmean(desktop_scores if desktop_scores else [0]),
			"desktop_median": stats.median(desktop_scores if desktop_scores else [0]),
			"mobile_average": stats.fmean(mobile_scores if mobile_scores else [0]),
			"mobile_median": stats.median(mobile_scores if mobile_scores else [0])
		}

def get_research_by_id(rid):
	for r in database:
		if r.rid == rid:
			return r
	return None

def get_key(password):
	return str(hash(str(password))).removeprefix("-")

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
	return render_template("index.html")

@app.route("/research-creation")
@app.route("/research-creation.html")
def research_creation_page():
	return render_template("research-creation.html")

@app.route("/create-research/<name>/<password>")
def create_research(name, password):
	try:
		database.append(Research(name, password))
		return app.redirect(f"/research/{database[len(database) - 1].rid}/overview/{get_key(hash(password))}")
	except Exception as e:
		return str(e)

@app.route("/research/<rid>/overview/<key>")
@app.route("/research/<rid>/overview.html/<key>")
def research_overview(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if r.key != key:
			return "lol nice try"
		return render_template("research-overview.html", research_id=r.rid)
	except Exception as e:
		return str(e)

@app.route("/research/login/<rid>/<name>/<password>")
@app.route("/research/login.html/<rid>/<name>/<password>")
def research_login(rid, name, password):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return app.redirect("/research/login", error_pws_div_default = "incorrect, veuillez réessayer")
		if r.key != get_key(hash(password)):
			return app.redirect("/research/login", error_pws_div_default = "incorrect, veuillez réessayer")
		return app.redirect(f"/research/{rid}/overview/{r.key}")
	except Exception as e:
		return str(e)

@app.route("/research/<rid>/overview/<key>/get-stats")
@app.route("/research/<rid>/overview.html/<key>/get-stats")
def get_stats(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if r.key != key:
			return "lol nice try"
		return r.get_processed_data()
	except Exception as e:
		print(str(e))
		return str(e)

@app.route("/research/login")
@app.route("/research/login.html")
def login():
	return render_template("login.html")

@app.route("/login-research/<name>/<password>/<rid>")
def fetch_key(name, password, rid):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "r"
		if r.key != get_key(hash(password)):
			return "p"
		return get_key(r.password_hash)
	except Exception as e:
		return "e " + str(e)

@app.route("/research/<rid>", methods=["GET", "POST"])
def research_form(rid):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if request.method == "POST":
			r.data.append(Result(request.form.get("anwser"), request.form.get("devtype")))
			return app.redirect("/")
		return render_template("form-temp.html", url_rid=rid)
	except Exception as e:
		return str(e)

@app.route("/favicon.ico")
def logo():
	return send_from_directory("static/", "logo.ico")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
	database.append(Research('n', 'p'))
	app.run(debug = True, host = get_ip())