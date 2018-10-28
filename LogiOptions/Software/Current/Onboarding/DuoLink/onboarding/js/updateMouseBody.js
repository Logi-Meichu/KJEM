function updateMouseBody(){

	var divsDisplay;
	var channelDisplay;
	var mouseParam = (query('mouse') !=null) ? (query('mouse').toLowerCase()) : null;
	var mouseID = ( mouseParam != null ) ? ( mouseParam.split('_')[0] ) : null;
	var mice = document.getElementsByClassName('mouse');
	var arrows = document.getElementsByClassName('arrow');

	mouseIDTrackball = "0x0006b01d";
	
	for (var i = 0; i < mice.length; i++) {
		mice[i].style.display = 'none';	
	}
	for (var i = 0; i < arrows.length; i++) {
		arrows[i].style.display = 'none';	
	}

	if (mouseID == mouseIDTrackball) {
		divsDisplay = document.getElementsByClassName("id" + mouseIDTrackball);
	}
	else {
		divsDisplay = document.getElementsByClassName("default");
	}

	for (var i = 0; i < divsDisplay.length; i++) {
		divsDisplay[i].style.display = 'inline';
	}
	
}
