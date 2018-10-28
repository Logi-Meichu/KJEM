function replaceString(){

/* REPLACE TEXT */ 
	
	var btns = document.getElementsByClassName('btn_cancel');
	for (var i = 0; i < btns.length; i++) {
  
  		replaceStr(btns[i],btn_cancel);
	}
	
	var btns = document.getElementsByClassName('btn_continue');
	for (var i = 0; i < btns.length; i++) {
 
  		replaceStr(btns[i],btn_continue);	
	}

	var btns = document.getElementsByClassName('btn_back');
	for (var i = 0; i < btns.length; i++) {
 
  		replaceStr(btns[i],btn_back);
	}
	
	var btns = document.getElementsByClassName('error');
	for (var i = 0; i < btns.length; i++) {

  		replaceStr(btns[i],window["error"+i]);
	}

	var btns = document.getElementsByClassName('btn_next');
	for (var i = 0; i < btns.length; i++) {

  		replaceStr(btns[i],btn_next);
	}

	var btns = document.getElementsByClassName('btn_done');
	for (var i = 0; i < btns.length; i++) {
 
  		replaceStr(btns[i],btn_done);
	}

	var btns = document.getElementsByClassName('link_website');
	for (var i = 0; i < btns.length; i++) {

  		replaceWebsite(btns[i],link_website);
	}

	var btns = document.getElementsByClassName('link_howToPair');
	for (var i = 0; i < btns.length; i++) {
		replaceStr(btns[i],link_howToPair);
	}

	var btns = document.getElementsByClassName('btn_howTo');
	for (var i = 0; i < btns.length; i++) {
		replaceStr(btns[i],btn_howTo);
	}

	var btns = document.getElementsByClassName('btn_enableFlow');
	for (var i = 0; i < btns.length; i++) {
		replaceStr(btns[i],btn_enableFlow);
	}

	var btns = document.getElementsByClassName('btn_retry');
	for (var i = 0; i < btns.length; i++) {
		replaceStr(btns[i],btn_retry);
	}

	var titles = document.getElementsByClassName('title');
	for (var i = 0; i < titles.length; i++) {
  		replaceStr(titles[i],window["title"+i]);
  		/* ALIGN TEXT AT BOTTOM OF DIV */

		titles[i].parentElement.style.height = "60px"; 
		titles[i].style.height = "auto"; 
  		titles[i].style.bottom = "20px"; 
	}
	
	var descs = document.getElementsByClassName('desc');
	for (var i = 0; i < descs.length; i++) {
		replaceStr(descs[i],window["desc"+i]);
	}
	
	function replaceStr(className, stringName) {
		var newString = stringName.replace("%LogiBrand%", brand).replace("%logibrand%", brand.toLowerCase()).replace("%LOGIBRAND%", brand.toUpperCase());
  		className.innerHTML = newString;

	}
	
	function replaceWebsite(className, stringName) {
		var newString = stringName.replace("%logiwebsite%", website);
  		className.innerHTML = newString;
	}


	/* POSITION BTN X */
	
	var btns_align = document.getElementsByClassName('center');
	for (var i = 0; i < btns_align.length; i++) {
  		positionX(btns_align[i], "center");
	}
	
	var btns_align = document.getElementsByClassName('left');
	for (var i = 0; i < btns_align.length; i++) {
  		positionX(btns_align[i], "left");
	}
	
	var btns_align = document.getElementsByClassName('right');
	for (var i = 0; i < btns_align.length; i++) {
  		positionX(btns_align[i], "right");
	}

	/* POSITION BTN Y */

	var btns_align = document.getElementsByClassName('up');
	for (var i = 0; i < btns_align.length; i++) {
  		positionY(btns_align[i], "up");
	}

	function positionX(div, positionX) {
		var posX;
		div.style.width = "auto";
		div.style.minWidth = "100px";
		div.style.paddingLeft = div.style.paddingRight = "15px";
		
		if (positionX === "center")
		{
			posX = 500 - (div.clientWidth/2);
  			div.style.transform = "translateX(0px) translateY(0px)";
  			div.style.left = posX+"px";
  		}
  		else if (positionX === "left")
		{
			posX = 500 - (div.clientWidth) - 10;
  			div.style.transform = "translateX(0px) translateY(0px)";
  			div.style.left = posX+"px";
  		}
  	  	else if (positionX === "right")
		{
			posX = 510;
  			div.style.transform = "translateX(0px) translateY(0px)";
  			div.style.left = posX+"px";
  		}
  		
	}
	
	function positionY(div, positionY) {
		var posY;

		if (positionY === "up")
		{
			posY = 524;
  			div.style.top = posY+"px";
  		}
  		
  		else if (positionY === "down")
		{
			posY = 580;
  			div.style.top = posY+"px"; 
  		}
	}
	
}