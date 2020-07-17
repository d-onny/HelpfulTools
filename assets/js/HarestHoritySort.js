(function(document){

    grabPostData = function(){
        let request = new XMLHttpRequest();
        request.open("GET", combinedURL, false);
        request.setRequestHeader("Authorization", "POESESSID" + id); //check this
        request.send();
    }

}) (document);