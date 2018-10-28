function btnBack(){
	var message =
	{
		command   : 'back',
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