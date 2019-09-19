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
		var my_image = new Image()
		var img_url = "/latestMap.jpg?" + new Date().getTime()
		my_image.src = img_url
		my_image.onload = () => {
			$("#map_img").attr('src', img_url)
		}
	}, 2500)
})

