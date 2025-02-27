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
		return "rid non-existance error";
	}
	key = await fetchKey(rid, nameField, psw);
	if (key == "r") {
		document.getElementById("error-psw-div").innerHTML = "Aucune recherche correspondante";
		return "rid not matching db error";
	}
	if (key == "p") {
		document.getElementById("error-psw-div").innerHTML = "Mauvais nom / mot de passe";
		return "nice try error";
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
	let deskAvr = document.getElementById("deskAvr");
	let deskMed = document.getElementById("deskMed");
	let moblAvr = document.getElementById("moblAvr");
	let moblMed = document.getElementById("moblMed");
	let chartdatadivs = [
		document.getElementById("chartdata0"),
		document.getElementById("chartdata1"),
		document.getElementById("chartdata2"),
		document.getElementById("chartdata3"),
		document.getElementById("chartdatax"),
		document.getElementById("deskquarts"),
		document.getElementById("moblquarts")
	];
	let ntflist = document.getElementById("ntflist");
	let response = await fetch(window.location + "/get-stats");
	let data = await response.json();
	deskMed.innerHTML = data.desktop_median;
	deskAvr.innerHTML = data.desktop_average;
	moblAvr.innerHTML = data.mobile_average;
	moblMed.innerHTML = data.mobile_median;
	chartdatadivs[0].innerHTML = data.chart_y_0;
	chartdatadivs[1].innerHTML = data.chart_y_1;
	chartdatadivs[2].innerHTML = data.chart_y_2;
	chartdatadivs[3].innerHTML = data.chart_y_3;
	chartdatadivs[4].innerHTML = data.chart_x;
	chartdatadivs[5].innerHTML = data.desktop_quartiles;
	chartdatadivs[6].innerHTML = data.mobile_quartiles;
	response = await fetch(window.location + "/get-new-data");
	data = await response.text();
	if (data != "") {
		ntflist.innerHTML = data + ntflist.innerHTML;
		ntflist.childNodes.forEach(element => {
			if (element.classList.contains("nlist-animate")) {
				element.classList.remove("nlist-animate");
			}
			element.classList.add("nlist-animate");
		});
	}
}

function startTimer() {
	let timer = 20000;
	document.getElementById("start-button").style.display = "none";
	document.getElementById("list").style.display = "inline";
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
	let intervalID = window.setInterval(function() {
		if (timer - (Date.now() - startTime) <= 0) {
			window.clearInterval(intervalID);
			return undefined;
		}
		ctx.fillStyle = "#008800";
		ctx.strokeStyle = ctx.fillStyle;
		ctx.beginPath();
		ctx.arc(
			256 + Math.sin((Date.now() - startTime - 40) / timer * Math.PI * 2) * 184,
			256 - Math.cos((Date.now() - startTime - 40) / timer * Math.PI * 2) * 184,
			35, 0, 2 * Math.PI
		);
		ctx.fill();
		ctx.stroke();
		ctx.fillStyle = "#888888";
		ctx.strokeStyle = "#000000";
		ctx.beginPath();
		ctx.arc(
			256 + Math.sin((Date.now() - startTime) / timer * Math.PI * 2) * 184,
			256 - Math.cos((Date.now() - startTime) / timer * Math.PI * 2) * 184,
			32, 0, 2 * Math.PI
		);
		ctx.fill();
		ctx.stroke();
		ctx.font = "128px Arial";
		ctx.clearRect(184, 310, 156, -128);
		if (Date.now() - startTime < 19000) {
			ctx.fillText((timer - (Date.now() - startTime)).toString().slice(0, 2), 184, 300);
		} else {
			ctx.fillText("0".concat((timer - (Date.now() - startTime)).toString().slice(0, 1)), 184, 300);
		}
		if (Date.now() - startTime > 10000) {
			ctx.fillRect(250, 290, 10, 10);
		}
	}, Math.floor(1000 / 30));
	window.setTimeout(function() {
		document.getElementById("list").style.display = "none";
		document.getElementById("form").style.display = "inline";
		devTypeCheck()
	}, timer);
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
function qdchart() {
	console.log("got here");
	function fitToContainer(canvas){
		canvas.style.width ='100%';
		canvas.style.height ='100%';
		canvas.width  = canvas.offsetWidth;
		canvas.height = canvas.offsetHeight;
	}
	let c = document.getElementById("qdgraph");
	fitToContainer(c);
	let ctx = c.getContext("2d");
	let w = c.width;
	let h = c.height;
	ctx.fillStyle = "#000000";
	ctx.strokeStyle = "#000000"
	ctx.lineWidth = 8;
	function drawLine(x1, y1, x2, y2) {
		ctx.moveTo(x1, y1);
		ctx.lineTo(x2, y2);
	}
	window.setInterval(function() {
		ctx.clearRect(0, 0, w, h);
		let deskquarts = JSON.parse("[" + document.getElementById("deskquarts").innerHTML + "]");
		let moblquarts = JSON.parse("[" + document.getElementById("moblquarts").innerHTML + "]");
		let d1 = {
			min: deskquarts[0],
			q1: deskquarts[1],
			q2: deskquarts[2],
			q3: deskquarts[3],
			q4: deskquarts[4],
			max: deskquarts[5]
		};
		let d2 = {
			min: moblquarts[0],
			q1: moblquarts[1],
			q2: moblquarts[2],
			q3: moblquarts[3],
			q4: moblquarts[4],
			max: moblquarts[5]
		};
		function qxtocx(value) {
			let min = Math.min(d1.min, d2.min);
			let max = Math.max(d1.max, d2.max);
			if (min == max) {
				return 4;
			}
			return (value - min) / (max - min) * (w - 8) + 4;
		}
		ctx.beginPath();
		drawLine(qxtocx(d1.min), 4, qxtocx(d1.min), h / 2 - 4);
		drawLine(qxtocx(d2.min), h / 2 - 4, qxtocx(d2.min), h - 4);
		drawLine(qxtocx(d1.min), h / 4, qxtocx(d1.q1), h / 4);
		drawLine(qxtocx(d2.min), h * 0.75, qxtocx(d2.q1), h * 0.75);
		drawLine(qxtocx(d1.q3), h / 4, qxtocx(d1.max), h / 4);
		drawLine(qxtocx(d2.q3), h * 0.75, qxtocx(d2.max), h * 0.75);
		drawLine(qxtocx(d1.q2), 4, qxtocx(d1.q2), h / 2 - 4);
		drawLine(qxtocx(d2.q2), h / 2 + 4, qxtocx(d2.q2), h - 4);
		drawLine(qxtocx(d1.max), 4, qxtocx(d1.max), h / 2 - 4);
		drawLine(qxtocx(d2.max), h / 2 + 4, qxtocx(d2.max), h - 4);
		ctx.rect(qxtocx(d1.q1), 4, qxtocx(d1.q3) - qxtocx(d1.q1), h / 2 - 8);
		ctx.rect(qxtocx(d2.q1), h / 2 + 4, qxtocx(d2.q3) - qxtocx(d2.q1), h / 2 - 8);
		ctx.stroke();
	}, 10);
}