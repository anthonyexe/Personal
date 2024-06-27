// Ant
//-------------------- Button Testing ---------------
var button = document.getElementById("submit");

function myFunc() {
    if (button.innerHTML === "Submit") {
        button.innerHTML = Date();
    }
    else {
        button.innerHTML = "Submit";
    }
}

button.addEventListener("click", myFunc);
//---------------------------------------------------

//------------------ Quiz Testing -------------------
function buttonPress(element) {
    const artistName = element.name;
    jsonData(artistName);
}

async function jsonData(artistName) {
    const artistFile = artistName + '.json';
    const response = await fetch(artistFile);
    const data = await response.json();
    var results = JSON.parse(JSON.stringify(data));
    
    for (var x in results) {
        for (let i = 0; i < results[x].length; i++) {
            console.log(results[x][i]["title"]);
            for (let j = 0; j < results[x][i]["quotes"].length; j++) {
                console.log(results[x][i]["quotes"][j]["quote"]);
            }
        }
    }
    
}

//jsonData();
