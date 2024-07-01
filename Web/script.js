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
const songQuotes = new Map();
var songCount = 0;
var songTitles = new Array();

async function buttonPress(element) {
    const artistName = element.name;
    const flag = await jsonData(artistName);
    createButtons();
    listQuotes();
}

async function jsonData(artistName) {
    const artistFile = artistName + '.json';
    const response = await fetch(artistFile);
    const data = await response.json();
    var results = JSON.parse(JSON.stringify(data));
        
    for (var x in results) {
        for (let i = 0; i < results[x].length; i++) {
            console.log(results[x][i]["title"]);
            //Generate random number for quote array index
            var randomQuoteIndex = Math.floor(Math.random() * results[x][i]["quotes"].length);
                //console.log(randomQuoteIndex);
                //console.log((results[x][i]["quotes"][randomQuoteIndex].quote));
            //Set current song title value as the key and a random quote from that song as the associated value
            songQuotes.set(results[x][i]["title"], results[x][i]["quotes"][randomQuoteIndex].quote);
            for (let j = 0; j < results[x][i]["quotes"].length; j++) {
                console.log(results[x][i]["quotes"][j]["quote"]);
            }
        }
    }
    //Set songTitles array equal to array of songQuotes key values
    songTitles = Array.from(songQuotes.keys());
    console.log(songTitles);
        
    //Set songCount equal to value of songTitles length
    songCount = songTitles.length;
    console.log(songCount + " songs");

    //Print contents of songQuotes map
    const iter = songQuotes.entries();
    let next = iter.next();
    while (!next.done) {
        console.log(next.value);
        next = iter.next();
    }
}

function createButtons() {
    var docFrag = document.createDocumentFragment();
    for (let i = 0; i < songCount; i++) {
        const newButton = document.createElement('button');
        newButton.textContent = songTitles[i];
        docFrag.appendChild(newButton);
    }
    document.body.appendChild(docFrag);
}

function listQuotes() {
    var docFrag = document.createDocumentFragment();
    const iter = songQuotes.entries();
    for (let [key, value] of songQuotes) {
        console.log(value);
        var entry = document.createElement('li');
        entry.textContent = value;
        docFrag.appendChild(entry);
    }

    songQuotes.forEach((val, key) => {
        console.log(val);
    })
    document.body.appendChild(docFrag);
}