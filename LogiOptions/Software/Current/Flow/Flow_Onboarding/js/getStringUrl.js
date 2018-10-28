var brand   = "Logitech";
var website = "logitech.com/options";
        
        function after(string, delimiter)
        {
            var index = string.indexOf(delimiter);
            if ( index < 0 ) { return null; }
            
            return string.substr(index+1);
        }
        
        function query(key)
        {
            var address = String(window.location);
            if ( address == null ) { return null; }
            
            var fragment = after(address, '#');
            if ( fragment == null ) { return null; }
            
            var groups = fragment.split('&');
            if ( groups == null ) { return null; }
            
            for (var index=0; index<groups.length; index++)
            {
                var group = groups[index];
                var pair  = group.split('=');
                
                if ( pair.length > 0 )
                {
                    if ( pair[0] == key )
                    {
                        if ( pair.length == 1 )
                        {
                            return true;
                        }
                        else
                        {
                            if ( pair[1] == 'true' )
                            {
                                return true;
                            }
                            else
                            if ( pair[1] == 'false' )
                            {
                                return false;
                            }
                            else
                            {
                                return pair[1];
                            }
                        }
                    }
                }
            }
            
            return null;
        }
        
        function loadScript(url)
        {
            document.head.appendChild(document.createElement("script")).src = url;
        }
        
        function loadDefaultScript()
        {
            try
            {
                var locale   = query('locale');
                var logicool = query('logicool');
                
                brand   = ( ( logicool == true ) || locale.endsWith("_JP") ) ? "Logicool" : "Logitech";
                website = ( ( logicool == true ) || locale.endsWith("_JP") ) ? "logicool.co.jp/ja-jp/product/options" : "logitech.com/options";
                
                loadScript("localization/localization-" + ((locale!=null)?locale:'en') + ".js");

            }  
            catch (error)
            {
                loadScript("localization/localization-en.js");
                console.log("Error: Loading Default File");
            }  
        }

        loadDefaultScript();
