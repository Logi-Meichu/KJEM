function btnDone(){
	var message =
	{
		command   : 'done',
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