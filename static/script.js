function createResearch() {
	document.getElementById("error-psw-div").innerHTML = "";
	let nameField = document.getElementById("name").value;
	if (nameField.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuilez entrer un nom de recherche";
		return "name non-existence error";
	}
	let psw = document.getElementById("psw1").value;
	if (psw.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuillex entrer un mot de passe";
		return "password non-existence error";
	}
	if (document.getElementById("psw2").value != psw) {
		document.getElementById("error-psw-div").innerHTML = "Les mots de passe ne sont pas les mêmes";
		return "passwords not matching error";
	}
	window.location.replace("/create-research/" + nameField + "/" + psw + "")
}

async function loginResearch() {
	document.getElementById("error-psw-div").innerHTML = "";
	let nameField = document.getElementById("name").value;
	if (nameField.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuilez entrer un nom de recherche";
		return "name non-existence error";
	}
	let psw = document.getElementById("psw").value;
	if (psw.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuillez entrer un mot de passe";
		return "password non-existence error";
	}
	let rid = document.getElementById("rid").value
	if (rid.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuillez entrer un identifiant";
		return "rid not matching error";
	}
	key = await fetchKey(rid, nameField, psw);
	if (key == "r") {
		document.getElementById("error-psw-div").innerHTML = "Aucune recherche correspondante";
		return "rid not matching db error";
	}
	if (key == "p") {
		document.getElementById("error-psw-div").innerHTML = "Mauvais nom / mot de passe";
		return "nive try error";
	}
	if (key[0] == "e") {
		document.getElementById("error-psw-div").innerHTML = "Une erreure est survenue";
		console.log(key);
		return "server-side error";
	}
	window.location.replace("/research/" + rid + "/overview/" + key)
}

async function fetchKey(rid, name, password) {
	let key = (await (await fetch("/login-research/" + name + "/" + password + "/" + rid)).text());
	return key;
}

function fetchStatsIntervall() {
	window.setInterval(fetchStats, 2000);
	fetchStats();
}

async function fetchStats() {
	let data = (await (await fetch(window.location + "/get-stats")).text()).toString();
	document.getElementById("statistics").innerHTML = data;
}

function startTimer() {
	document.getElementById("start-button").style.display = "none";
	document.getElementById("list").style.display = "inline";
	window.setTimeout(questionTime, 20 * 1000);
	startStopwatch();
}

function startStopwatch() {
	let c = document.getElementById("stopwatch");
	let ctx = c.getContext("2d");
	let startTime = Date.now();
	setInterval(function() {
		let width = c.width;
		ctx.clearRect(0, 0, width, width);
		ctx.fillColor = "#0000ff";
		let x = Math.sin((Date.now() - startTime) / 1000) * 0.75 / 2 + 0.5;
		let y = Math.cos((Date.now() - startTime) / 1000) * 0.75 / 2 + 0.5;
		ctx.fillRect(x * width - 5, -y * width - 5, 10, 10);
	}, 10);
}

function questionTime() {
	document.getElementById("list").style.display = "none";
	document.getElementById("form").style.display = "inline";
}