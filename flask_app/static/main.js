function lightDark() {
	var a = document.getElementById("body");
	// var b = document.getElementById(" ");
	// var c = document.getElementById(" ");
	// var d = document.getElementById(" ");

	if (a.style.backgroundColor !== "var(--dark-charc)") {
		a.style.backgroundColor = "var(--dark-charc)";
    } else {
    		a.style.backgroundColor = "rgb(225, 225, 225)";
    }

}

function navDropdown() {
    var x = document.getElementById("navDropdown");
    var a = document.getElementById("navDropdownBtn");
    var c = document.getElementById("downArrow");

    x.style.display = "block";
    x.style.transition = "display ease-in 2s";
    a.style.backgroundColor = "#3c3c3c";
}

function navDropdownRehide() {
	var x = document.getElementById("navDropdown");
	var a = document.getElementById("navDropdownBtn");
	x.style.display = "none";
	a.style.backgroundColor = "#282828";
}

function showArtistsTab() {
	var artistsContent = document.getElementById("favoriteArtists");
	var tracksContent = document.getElementById("favoriteTracks");
	var artistsTab = document.getElementById("artistsTab");
	var tracksTab = document.getElementById("tracksTab");

	artistsContent.classList.add("activeTab");
	tracksContent.classList.remove("activeTab");

	tracksContent.classList.add("hidden");
	artistsContent.classList.remove("hidden");

	artistsTab.classList.add("activeTab");
	tracksTab.classList.remove("activeTab");
}

function showTracksTab() {
	var artistsContent = document.getElementById("favoriteArtists");
	var tracksContent = document.getElementById("favoriteTracks");
	var artistsTab = document.getElementById("artistsTab");
	var tracksTab = document.getElementById("tracksTab");

	artistsContent.classList.remove("activeTab");
	tracksContent.classList.add("activeTab");

	artistsContent.classList.add("hidden");
	tracksContent.classList.remove("hidden");

	artistsTab.classList.remove("activeTab");
	tracksTab.classList.add("activeTab");
}