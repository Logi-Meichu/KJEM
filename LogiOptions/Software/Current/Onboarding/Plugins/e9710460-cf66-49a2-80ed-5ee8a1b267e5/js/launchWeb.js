function launchWeb(){
	var message =
	{
		command   : 'navigate',
		parameters:
		{
			url: 'http://www.logitech.com/options'
		}
	};
	
	try
	{
		window.external.NativeOnboarderSendMessage(JSON.stringify(message));
	}

	catch ( exception )
	{
		NativeOnboarder.sendMessage(JSON.stringify(message));
	}
}