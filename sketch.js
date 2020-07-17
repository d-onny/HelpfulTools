let accountName = document.getElementById("accountname");
let tabIndex = document.getElementById("tabindex");
let id = document.getElementById("sessID");

let filteredData;

function setup() {
  frameRate(60);
}

// Main "Game" Loop, occurs 60 times a second according to frameRate()
function draw() {
  // https://p5js.org/reference/#/p5/createButton
  // https://p5js.org/reference/#/p5/createInput
  // https://p5js.org/reference/#/p5/httpGet
  // https://p5js.org/reference/#/p5/createElement
}

function getRequest() {
  let combinedURL = "https://www.pathofexile.com/character-window/get-stash-items?league=Harvest&realm=pc&accountName=" + accountName 
                + "&tabs=0&tabIndex=" + tabIndex;
  let data;
  httpGet(combinedURL, 'jsonp', false, function(response){
    data = response;
  });

  console.log(data);
}