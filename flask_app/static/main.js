function lightDark() {
	let a = document.getElementById("body");
	let b = document.getElementById("lightDarkIconBtn");
	let c = document.getElementById("lightBtnCase");
	let d = document.getElementById("darkBtnCase");

	var legal = document.getElementById("legal");

	if (a.style.backgroundColor !== "var(--dark-charc)") {
		a.style.backgroundColor = "var(--dark-charc)";
		b.style.backgroundColor = "var(--light-btn)"
		c.style.display = "none";
		d.style.display = "inline-block";
		legal.style.backgroundColor = "rgb(100,100,100)"
    } else {
    a.style.backgroundColor = "rgb(225, 225, 225)";
    b.style.backgroundColor = "var(--purple)"
		c.style.display = "inline-block";
		d.style.display = "none";
		legal.style.backgroundColor = "#111111"
    }

}

function navDropdown() {
    let x = document.getElementById("navDropdown");
    let a = document.getElementById("navDropdownBtn");
    let c = document.getElementById("downArrow");

    x.style.display = "block";
    x.style.transition = "display ease-in 2s";
    a.style.backgroundColor = "#3c3c3c";
}

function navDropdownRehide() {
	let x = document.getElementById("navDropdown");
	let a = document.getElementById("navDropdownBtn");
	x.style.display = "none";
	a.style.backgroundColor = "#282828";
}

function showArtistsTab() {
	let artistsContent = document.getElementById("favoriteArtists");
	let tracksContent = document.getElementById("favoriteTracks");
	let artistsTab = document.getElementById("artistsTab");
	let tracksTab = document.getElementById("tracksTab");

	// artistsContent.classList.add("activeTab");
	// tracksContent.classList.remove("activeTab");

	tracksContent.classList.add("hidden");
	artistsContent.classList.remove("hidden");

	artistsTab.classList.add("activeTab");
	tracksTab.classList.remove("activeTab");
}

function showTracksTab() {
	let artistsContent = document.getElementById("favoriteArtists");
	let tracksContent = document.getElementById("favoriteTracks");
	let artistsTab = document.getElementById("artistsTab");
	let tracksTab = document.getElementById("tracksTab");

	// artistsContent.classList.remove("activeTab");
	// tracksContent.classList.add("activeTab");

	artistsContent.classList.add("hidden");
	tracksContent.classList.remove("hidden");

	artistsTab.classList.remove("activeTab");
	tracksTab.classList.add("activeTab");
}


function shortStatsTab() {
	let a = document.getElementById("shortStatsTab");
	let b = document.getElementById("medStatsTab");
	let c = document.getElementById("longStatsTab");

	a.classList.add("activeStatsTab");
	b.classList.remove("activeStatsTab");
	c.classList.remove("activeStatsTab");
}

function medStatsTab() {
	let a = document.getElementById("shortStatsTab");
	let b = document.getElementById("medStatsTab");
	let c = document.getElementById("longStatsTab");

	b.classList.add("activeStatsTab");
	c.classList.remove("activeStatsTab");
	a.classList.remove("activeStatsTab");
}

function longStatsTab() {
	let a = document.getElementById("shortStatsTab");
	let b = document.getElementById("medStatsTab");
	let c = document.getElementById("longStatsTab");

	c.classList.add("activeStatsTab");
	b.classList.remove("activeStatsTab");
	a.classList.remove("activeStatsTab");
}