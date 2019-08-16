//There is some glitchy behavior with key repeating, so I am using a set to solve the issue
var pressedKeys = {}

//the ajax should be changed to POST eventually but there is an issue with JQuery
function keydown(e) {
	if(e.keyCode in pressedKeys && pressedKeys[e.keyCode] == true) return;
	
	pressedKeys[e.keyCode] = true
	console.log(e.keyCode)
	$.get("/keyPressed/", {"key": e.keyCode})
	
}

function keyup(e) {
	pressedKeys[e.keyCode] = false
	$.get("/keyReleased/", {"key": e.keyCode})
}
window.addEventListener('keyup',this.keyup,false);
window.addEventListener('keydown',this.keydown,false);

//on load
$(function(){

	$("#start_button").click(function(){
		console.log("start")
		f = $.get("/startNavigation/", {})
		console.log(f)
	})
	$("#stop_button").click(function(){
		console.log("stop")
		$.get("/stopNavigation/", {})
	})

	setInterval(function(){
		console.log("LOOP")
		$("#map_img").attr('src', "/latestMap.jpg?" + new Date().getTime());
	}, 2500)
})
