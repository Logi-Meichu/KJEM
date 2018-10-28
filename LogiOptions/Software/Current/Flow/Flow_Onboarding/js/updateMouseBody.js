function updateMouseBody(){

	var mouseDisplay;
	var channelDisplay;
	var mouseParam = (query('mouse') !=null) ? (query('mouse').toLowerCase()) : null;
	var mouseID = ( mouseParam != null ) ? ( mouseParam.split('_')[0] ) : null;
	var mice = document.getElementsByClassName('mouse');
	var channel = document.getElementsByClassName('channel');

	
	
	for (var i = 0; i < mice.length; i++) {
		mice[i].style.display = 'none';	
	}
	
	for (var i = 0; i < channel.length; i++) {
		channel[i].style.display = 'none';	
	}
	
	if (mouseID == '0x0006b01a' || mouseID == '0x0006b019' || mouseID == "0x0006b019_0x0001" || mouseID == "0x0006b019_0x0002") {
		mouseDisplay = document.getElementsByClassName(mouseID);
		for (var i = 0; i < mouseDisplay.length; i++) {
			mouseDisplay[i].style.display = 'inline';
		}
		
		channelDisplay = document.getElementsByClassName('channel1');
		for (var i = 0; i < channelDisplay.length; i++) {
			channelDisplay[i].style.display = 'inline';
		}
	}
	
		
	else if (mouseID == '0x0006b01d' || mouseID == '0x0006b01b') {
		mouseDisplay = document.getElementsByClassName(mouseID);
		for (var i = 0; i < mouseDisplay.length; i++) {
			mouseDisplay[i].style.display = 'inline';
		}
		
		channelDisplay = document.getElementsByClassName('channel2');
		for (var i = 0; i < channelDisplay.length; i++) {
			channelDisplay[i].style.display = 'inline';
		}
	}
	
	
	else if (mouseID == '0x0006b015') {
		mouseDisplay = document.getElementsByClassName('0x0006b015');
		for (var i = 0; i < mouseDisplay.length; i++) {
			mouseDisplay[i].style.display = 'inline';
		}
		
		channelDisplay = document.getElementsByClassName('channel3');
		for (var i = 0; i < channelDisplay.length; i++) {
			channelDisplay[i].style.display = 'inline';
		}
	}
	
	// DEFAULT
	
	else {
		mouseDisplay = document.getElementsByClassName('0x0006b01b');
		for (var i = 0; i < mouseDisplay.length; i++) {
			mouseDisplay[i].style.display = 'inline';
		}
		
		channelDisplay = document.getElementsByClassName('channel2');
		for (var i = 0; i < channelDisplay.length; i++) {
			channelDisplay[i].style.display = 'inline';
		}
	
	}
}
