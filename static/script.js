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

function fetchStatsIntervall() {
	window.setInterval(fetchStats, 2000);
	fetchStats();
}

async function fetchStats() {
	let data = (await (await fetch(window.location + "/get-stats")).text()).toString();
	document.getElementById("statistics").innerHTML = data;
}