if (localStorage.applyHistory === undefined) {
	localStorage.applyHistory = "{}";
}

function logHistory(historyType) {
	var applyTime = new Date().getTime()
	var date = new Date(applyTime).setHours(0, 0, 0, 0); // Date with 0 time
															// elements

	var applyHistory = localStorage.applyHistory;
	applyHistory = JSON.parse(applyHistory);

	if (applyHistory[date] === undefined) {
		applyHistory[date] = {
			"apply_history" : [],
			"view_history" : [],
			"search_history" : []
		};
	}

	applyHistory[date][historyType].push({
		"time" : applyTime,
		"title" : localStorage.jobTitle
	});
	localStorage.applyHistory = JSON.stringify(applyHistory);
}