from flask import Flask, render_template
import statistics as stats
import socket
from flask import request
app = Flask(__name__)

database = []
id_counter = 0

class Research():
	rid: int
	name: str
	password_hash: int
	data: list
	def __init__(self, name: str, password: str) -> None:
		global id_counter
		self.rid = id_counter
		id_counter += 1
		self.name = name
		self.password_hash = hash(password)
		self.data = []
	def get_processed_data(self) -> list:
		"""
		returns a list of lenght 3 with :
		index 0 : data as list[int]
		index 1 : list average as float
		index 2 : list median as float
		"""
		data = self.data if self.data else [0]
		return [data, stats.fmean(data), stats.median(data)]

def get_research_by_id(rid):
	for r in database:
		if r.rid == rid:
			return r
		else:
			print(rid, r.rid)
	return None

def get_key(password):
	return str(hash(password))

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
		return app.redirect(f"/research/{database[len(database) - 1].rid}/overview/{get_key(database[len(database) - 1].password_hash)}")
	except Exception as e:
		return str(e)

@app.route("/research/<rid>/overview/<key>")
@app.route("/research/<rid>/overview.html/<key>")
def research_overview(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if get_key(r.password_hash) != key:
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
			return "404 - research not found"
		key = hash(r.password_hash)
		if hash(r.password_hash) != key:
			return app.redirect("/research/login", error_pws_div_default = "incorrect, veuillez réessayer")
		return app.redirect(f"/research/{rid}/overview/{str(key)}")
	except Exception as e:
		return str(e)

@app.route("/research/<rid>/overview/<key>/get-stats")
@app.route("/research/<rid>/overview.html/<key>/get-stats")
def get_stats(rid, key):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		if get_key(r.password_hash) != key:
			return "lol nice try"
		processed = r.get_processed_data()
		return render_template("stats.html",
			average=str(processed[1]),
			median=str(processed[2]),
			data=str(processed[0]))
	except Exception as e:
		return str(e)

@app.route("/research/login")
@app.route("/research/login.html")
def login():
	print("form :")
	print(request.form)
	return render_template("login.html")

@app.route("/login-research/<name>/<password>/<rid>")
def fetch_key(name, password, rid):
	try:
		r = get_research_by_id(int(rid))
		if not r:
			return "r"
		if get_key(r.password_hash) != get_key(hash(password)):
			return "p"
		return get_key(r.password_hash)
	except Exception as e:
		return "e " + str(e)

@app.route("/research/<rid>", methods=["GET", "POST"])
def research_form(rid):
	try:
		if request.method == "POST":
			print(request.form.get("textinput1"))
			return app.redirect("/")
		r = get_research_by_id(int(rid))
		if not r:
			return "404 - research not found"
		return render_template("form-temp.html", url_rid=rid)
	except Exception as e:
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
	app.run(debug = True, host = get_ip())