function closeBtn(){
	var message =
	{
		command   : 'close',
		parameters: null
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