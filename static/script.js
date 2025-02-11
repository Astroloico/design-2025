function createResearch() {
	document.getElementById("error-psw-div").innerHTML = "";
	let nameField = document.getElementById("name").value;
	if (nameField.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuilez entrer un nom de recherche";
		return "name non-existence error";
	}
	let psw = document.getElementById("psw1").value;
	if (psw.length == 0) {
		document.getElementById("error-psw-div").innerHTML = "Veuillex rentrer un mot de passe";
		return "password non-existence error";
	}
	if (document.getElementById("psw2").value != psw) {
		document.getElementById("error-psw-div").innerHTML = "Les mots de passe ne sont pas les mêmes";
		return "passwords not matching error";
	}
	location.replace("/create-research/" + nameField + "/" + psw + "")
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
	window.location.assign("/research/" + rid + "/overview/" + key)
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