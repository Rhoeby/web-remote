//There is some glitchy behavior with key repeating, so I am using a set to solve the issue
var pressedKeys = {}

//the ajax should be changed to POST eventually but there is an issue with JQuery
window.addEventListener('keydown',this.keydown,false);
function keydown(e) {
	if(e.keyCode in pressedKeys && pressedKeys[e.keyCode] == true) return;
	
	pressedKeys[e.keyCode] = true
	$.get("/keyPressed/", {"key": e.keyCode})
	
}

window.addEventListener('keyup',this.keyup,false);
function keyup(e) {
	pressedKeys[e.keyCode] = false
    $.get("/keyReleased/", {"key": e.keyCode})
}