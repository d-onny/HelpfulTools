(function(document){
    let accountName = document.getElementById("accountname");
    let tabIndex = document.getElementById("tabindex");
    let id = document.getElementById("sessID");

    grabPostData = function(){
        let combinedURL = "https://www.pathofexile.com/character-window/get-stash-items?league=Harvest&realm=pc&accountName=" + accountName 
                        + "&tabs=0&tabIndex=" + tabIndex;
        
        let request = new XMLHttpRequest();
        request.open("GET", combinedURL, false);
        request.setRequestHeader("cookie", "POESESSID" + id);
        request.send();
    }

}) (document);