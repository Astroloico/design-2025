from flask import Flask, render_template
import statistics as stats
app = Flask(__name__)

database = []
id_counter = 0

class Research():
	id_number: int
	name: str
	password_hash: int
	data: list
	def __init__(self, name: str, password: str) -> None:
		global id_counter
		self.id_number = id_counter
		id_counter += 1
		self.name = name
		self.password_hash = hash(password)
		self.data = []
	def check_login(self, name, password) -> bool:
		return self.name == name and self.password_hash == hash(password)
	def get_processed_data(self) -> list:
		"""
		returns a list of lenght 3 with :
		index 0 : data as list[int]
		index 1 : list average as float
		index 2 : list median as float
		"""
		data = self.data if self.data else [0]
		return [data, stats.fmean(data), stats.median(data)]

def get_research_by_id(id_number):
	for r in database:
		if r.id_number == id_number:
			return r
		else:
			print(id_number, r.id_number)
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
def create_page(name, password):
	try:
		database.append(Research(name, password))
		return app.redirect(f"/research/{database[len(database) - 1].id_number}/overview/{get_key(database[len(database) - 1].password_hash)}")
	except Exception as e:
		return str(e)

@app.route("/research/<id_number>/overview/<key>")
@app.route("/research/<id_number>/overview.html/<key>")
def research_overview(id_number, key):
	try:
		r = get_research_by_id(int(id_number))
		if not r:
			return "404 - research not found"
		if get_key(r.password_hash) != int(key):
			return "lol nice try"
		return render_template("research-overview.html", research_id=r.id_number)
	except Exception as e:
		return str(e)

@app.route("/research/<id_number>/overview/<key>/get-stats")
@app.route("/research/<id_number>/overview.html/<key>/get-stats")
def get_stats(id_number, key):
	try:
		r = get_research_by_id(int(id_number))
		if not r:
			return "404 - research not found"
		if get_key(r.password_hash) != int(key):
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
	return render_template("login.html")

@app.route("/login-research/<name>/<password>/<id_number>")
def fetch_ketch(name, password, id_number):
	try:
		r = get_research_by_id(int(id_number))
		if not r:
			return "r"
		if get_key(r.password_hash) != int(get_key(hash(password))):
			return "p"
		return key(r.password_hash)
	except Exception as e:
		return "e " + str(e)

if __name__ == '__main__':
	app.run(debug = True)