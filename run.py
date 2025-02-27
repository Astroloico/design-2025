from flask import Flask, render_template, send_from_directory, send_file
import statistics as stats
import socket
from flask import request
from difflib import get_close_matches, SequenceMatcher
import time
import markupsafe
flask_app = Flask(__name__)

database = []

counties = [
	"alameda",
	"alpine",
	"amador",
	"butte",
	"calaveras",
	"colusa",
	"contra costa",
	"delnorte",
	"eldorado",
	"fresno",
	"glenn",
	"humboldt",
	"imperial",
	"inyo",
	"kern",
	"kings",
	"lake",
	"lassen",
	"losangeles",
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
	"sanbenito",
	"sanbernardino",
	"sandiego",
	"sanfrancisco",
	"sanjoaquin",
	"sanluis obispo",
	"sanmateo",
	"santa barbara",
	"santaclara",
	"santacruz",
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
	good: list[str]
	matches: list[str]
	sim_scores: list[float]
	score: float
	media: str
	date: time.struct_time
	def __init__(self, anwser: str = "", media: str = ""):
		self.raw = anwser
		self.parsed = anwser.lower().replace(" ", "").replace("\r", "").split("\n", 50)
		while self.parsed.count(""):
			self.parsed.remove("")
		counties_copy = counties.copy()
		self.media = media
		self.score = 0
		self.date = time.localtime()
		self.good = []
		self.matches = []
		self.sim_scores = []
		for item in self.parsed:
			self.sim_scores.append(SequenceMatcher(None, item, get_close_matches(item, counties_copy, 1, 0)[0]).ratio())
			m = get_close_matches(item, counties_copy, 1, 0.75)
			if len(m) > 0:
				self.good.append(item)
				self.matches.append(m[0])
				counties_copy.remove(m[0])
				self.score += 1

id_counter = 0
class Research():
	rid: int
	name: str
	password_hash: int
	key: str
	data: list[Result]
	send: int
	did_counter: int
	start_date: time.struct_time
	def __init__(self, name: str, password: str) -> None:
		global id_counter
		self.rid = id_counter
		id_counter += 1
		self.name = name
		self.password_hash = hash(password)
		self.key = get_key(self.password_hash)
		self.data = []
		self.sent = 0
		self.did_counter = 0
		self.start_date = time.gmtime()
	def get_graph_y(self, stat_type, media) -> list[float]:
		"""stat_type == True || 1 => average
		stat_type == False || 0 => median"""
		try:
			timeline = self.data.copy()
			incremental_list = []
			ouput = []
			j = 0
			for i in timeline:
				if i.media == media:
					incremental_list.append(i.score)
				if stat_type:
					ouput.append(abs(stats.fmean(incremental_list if incremental_list else [0])))
				else:
					ouput.append(abs(stats.median(incremental_list if incremental_list else [0])))
				j += 1
			return ouput if ouput else [0]
		except Exception as e:
			print(str(e))
			return [0]
	def get_new_ones(self) -> str:
		try:
			new_ones = self.data[self.sent : len(self.data)]
			self.sent = len(self.data)
			s = ""
			for r in new_ones:
				s = render_template("notif-template.html", score=r.score, media=r.media, num=self.did_counter) + s
				self.did_counter += 1
			return s
		except Exception as e:
			print(e)
			return(e)
	def get_processed_data(self) -> dict:
		desktop_scores = list(map(lambda x: x.score, filter(lambda x: x.media == "desktop", self.data)))
		mobile_scores = list(map(lambda x: x.score, filter(lambda x: x.media == "mobile", self.data)))
		return {
			"desktop_average": stats.fmean(desktop_scores if desktop_scores else [0]),
			"desktop_median": stats.median(desktop_scores if desktop_scores else [0]),
			"mobile_average": stats.fmean(mobile_scores if mobile_scores else [0]),
			"mobile_median": stats.median(mobile_scores if mobile_scores else [0]),
			"chart_x": [i for i in range(len(desktop_scores) + len(mobile_scores))],
			"chart_y_0": self.get_graph_y(1, "desktop"),
			"chart_y_1": self.get_graph_y(0, "desktop"),
			"chart_y_2": self.get_graph_y(1, "mobile"),
			"chart_y_3": self.get_graph_y(0, "mobile"),
			"desktop_quartiles":
				[min(desktop_scores if desktop_scores else [0])] +
				stats.quantiles(desktop_scores if len(desktop_scores) >= 2 else [0, 0], n=6, method="inclusive") +
				[max(desktop_scores if desktop_scores else [0])],
			"mobile_quartiles":
				[min(mobile_scores if mobile_scores else [0])] +
				stats.quantiles(mobile_scores if len(mobile_scores) >= 2 else [0, 0], n=6, method="inclusive") +
				[min(mobile_scores if mobile_scores else [0])]
		}

def get_research_by_id(rid):
	for r in database:
		if r.rid == rid:
			return r
	return None

def get_key(password):
	return str(hash(str(password))).removeprefix("-")

@flask_app.route("/")
@flask_app.route("/index")
@flask_app.route("/index.html")
def index():
	return render_template("index.html")

@flask_app.route("/research-creation")
@flask_app.route("/research-creation.html")
def research_creation_page():
	return render_template("research-creation.html")

@flask_app.route("/create-research/<name>/<password>")
def create_research(name, password):
	try:
		database.append(Research(name, password))
		return flask_app.redirect(f"/research/{database[len(database) - 1].rid}/overview/{get_key(hash(password))}")
	except Exception as e:
		return str(e)

@flask_app.route("/research/<rid>/overview/<key>")
@flask_app.route("/research/<rid>/overview.html/<key>")
def research_overview(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if r.key != key:
			return "lol nice try"
		return render_template("research-overview.html", research_id=r.rid, key=r.key)
	except Exception as e:
		return str(e)

@flask_app.route("/research/login/<rid>/<name>/<password>")
@flask_app.route("/research/login.html/<rid>/<name>/<password>")
def research_login(rid, name, password):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return flask_app.redirect("/research/login", error_pws_div_default = "incorrect, veuillez réessayer")
		if r.key != get_key(hash(password)):
			return flask_app.redirect("/research/login", error_pws_div_default = "incorrect, veuillez réessayer")
		return flask_app.redirect(f"/research/{rid}/overview/{r.key}")
	except Exception as e:
		return str(e)

@flask_app.route("/research/<rid>/overview/<key>/get-stats")
@flask_app.route("/research/<rid>/overview.html/<key>/get-stats")
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

@flask_app.route("/research/<rid>/overview/<key>/get-new-data")
def get_new_data(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if r.key != key:
			return "lol nice try"
		return r.get_new_ones()
	except Exception as e:
		print(str(e))
		return str(e)

@flask_app.route("/research/login")
@flask_app.route("/research/login.html")
def login():
	return render_template("login.html")

@flask_app.route("/login-research/<name>/<password>/<rid>")
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

@flask_app.route("/research/<rid>", methods=["GET", "POST"])
def research_form(rid):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if request.method == "POST":
			r.data.append(Result(request.form.get("anwser"), request.form.get("devtype")))
			return flask_app.redirect("/")
		return render_template("form-temp.html", url_rid=rid)
	except Exception as e:
		print(e)
		return str(e)

@flask_app.route("/favicon.ico")
def logo():
	return send_from_directory("static/", "logo.ico")

@flask_app.route("/debugdata/<media>/<num>")
def debugdata(num, media):
	database[0].data.append(Result("\n".join(counties[0 : int(num)]), "desktop" if (media == "d") else "mobile"))
	return flask_app.redirect("/")

@flask_app.route("/research/<rid>/overview/<key>/download/resultats.html")
def download_results(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if r.key != key:
			return "lol nice try"
		desktop = list(filter(lambda x: x.media == "desktop", r.data))
		mobile = list(filter(lambda x: x.media == "mobile", r.data))
		desktop_scores = list(map(lambda x: x.score, r.data))
		mobile_scores = list(map(lambda x: x.score, r.data))
		full_results = ""
		n = 1
		for i in r.data:
			full_results += render_template(
				"df-result-template.html",
				num=n,
				date=time.asctime(i.date),
				media=("Ordinateur" if i.media == "desktop" else "Téléphone"),
				score=i.score,
				raw=i.raw,
				parsed="\n".join(i.parsed),
				good="\n".join(i.good),
				matches="\n".join(i.matches),
				sim_scores="\n".join(map(str, i.sim_scores))
			)
			full_results += "<br>"
			n += 1
			with open("resultats.html", "w") as file:
				file.write(render_template(
					"download-file.html",
					name=r.name,
					date=time.asctime(r.start_date),
					lenght=len(r.data),
					desktop_average=stats.fmean(desktop_scores if desktop_scores else [0]),
					desktop_median=stats.median(desktop_scores if desktop_scores else [0]),
					desktop_len=len(desktop),
					mobile_average=stats.fmean(mobile_scores if mobile_scores else [0]),
					mobile_median=stats.median(mobile_scores if mobile_scores else [0]),
					mobile_len=len(mobile),
					full_data=markupsafe.Markup(full_results)
				))
		return send_file("resultats.html")
	except Exception as e:
		print("error2: " + str(e))
		return str(e)


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
	flask_app.run(debug = True, host = get_ip())