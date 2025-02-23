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
	ctx.lineWidth = 12;
	ctx.strokeStyle = "#000000";
	ctx.beginPath();
	ctx.arc(256, 256, 128, 0, 2 * Math.PI);
	ctx.stroke();
	ctx.beginPath();
	ctx.arc(256, 256, 240, 0, 2 * Math.PI);
	ctx.stroke();
	ctx.lineWidth = 8;
	setInterval(function() {
		ctx.fillStyle = "#008800";
		ctx.strokeStyle = ctx.fillStyle;
		ctx.beginPath();
		ctx.arc(
			256 + Math.sin((Date.now() - startTime - 40) / 20000 * Math.PI * 2) * 184,
			256 - Math.cos((Date.now() - startTime - 40) / 20000 * Math.PI * 2) * 184,
			35, 0, 2 * Math.PI
		);
		ctx.fill();
		ctx.stroke();
		ctx.fillStyle = "#888888";
		ctx.strokeStyle = "#000000";
		ctx.beginPath();
		ctx.arc(
			256 + Math.sin((Date.now() - startTime) / 20000 * Math.PI * 2) * 184,
			256 - Math.cos((Date.now() - startTime) / 20000 * Math.PI * 2) * 184,
			32, 0, 2 * Math.PI
		);
		ctx.fill();
		ctx.stroke();
		ctx.font = "128px Arial";
		ctx.clearRect(184, 310, 156, -128);
		if (Date.now() - startTime < 19000) {
			ctx.fillText((20000 - (Date.now() - startTime)).toString().slice(0, 2), 184, 300);
		} else {
			ctx.fillText("0".concat((20000 - (Date.now() - startTime)).toString().slice(0, 1)), 184, 300);
		}
		if (Date.now() - startTime > 10000) {
			ctx.fillRect(250, 290, 10, 10);
		}
	}, Math.floor(1000 / 30));
}

function questionTime() {
	document.getElementById("list").style.display = "none";
	document.getElementById("form").style.display = "inline";
	devTypeCheck()
}

function checkTextareaLineCount() {
	let textarea = document.getElementById("anwser");
	let numOfLines = textarea.value.split("\n").length;
	console.info([textarea.value.split("\n").length, textarea.value]);
	if (numOfLines > 50) {
		while (textarea.value.split("\n").length > 50) {
			textarea.value = textarea.value.substring(0, textarea.value.length - 1);
		}
	}
}

function devTypeCheck() {
	let output = document.getElementById("devtype");
	if (navigator.userAgent.match(/Android|BlackBerry|iPhone|iPad|iPod|Opera Mini|IEMobile/i)) {
		output.value = "mobile";
	} else {
		output.value = "desktop";
	}
}