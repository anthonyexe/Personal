// Ant
//------------------ Quiz Testing -------------------
var songQuotes = new Array();
var songCount = 0;

let artist = document.getElementById("artist");
let currentIndex, currentSong, currentQuote;
let correctCount = 0;
let para = document.getElementById("Quote");
let result = document.getElementById("Result");
let score = document.getElementById("Score");
let concurrentScore = document.getElementById("concurrentScore");

let wrongGuesses = new Array();

async function buttonPress() {
    artist.disabled = "disabled";
    artist.style.background = "grey";
    artistName = artist.name;
    await jsonData(artistName);
    //songQuotes = shuffleSongs(songQuotes);
    createButtons();
    currentIndex = 0;
    currentSong = songQuotes[0][0];
    currentQuote = songQuotes[0][1];
    para.innerHTML = currentQuote;
}

async function jsonData(artistName) {
    const artistFile = artistName + '.json';
    const response = await fetch(artistFile);
    const data = await response.json();
    var results = JSON.parse(JSON.stringify(data));
        
    for (var x in results) {
        //Set songCount equal to value of results
        songCount = results[x].length;
        for (let i = 0; i < results[x].length; i++) {
            //Generate random number for quote array index
            var randomQuoteIndex = Math.floor(Math.random() * results[x][i]["quotes"].length);
            //Set current song title value as the key and a random quote from that song as the associated value
            songQuotes.push([results[x][i]["title"], results[x][i]["quotes"][randomQuoteIndex].quote]);
        }
    }

    songQuotes = shuffleSongs(songQuotes);
    for (let i = 0; i < songQuotes.length; i++) {
        for (let j = 0; j < songQuotes[i].length; j++) {
            console.log(songQuotes[i][j]);
        }
    }
}

function shuffleSongs(arr) {
    let currentIndex = songCount;
    while (currentIndex != 0) {
        let randomIndex = Math.floor(Math.random() * currentIndex--);
        //console.log("random = " + randomIndex)
        //console.log("current = " + currentIndex);
        
        let temp = arr[currentIndex];
        //console.log(temp);
        arr[currentIndex] = arr[randomIndex];
        arr[randomIndex] = temp;
        
    }
    return arr;
}

function createButtons() {
    let titlesCopy = [];
    for (let i = 0; i < songCount; i++) {
        titlesCopy[i] = songQuotes[i][0];
    }
    titlesCopy = shuffleSongs(titlesCopy);

    const newDiv = document.createElement("div");
    for (let i = 0; i < songCount; i++) {
        const newButton = document.createElement('button');
        newButton.textContent = titlesCopy[i];
        newButton.setAttribute("onclick", "guess(this)");
        newButton.className = "songChoices";
        newDiv.appendChild(newButton);
    }
    newDiv.className = "buttonDiv";
    newDiv.id = "buttonDiv";
    document.getElementById("buttonContainer").appendChild(newDiv);
}

function listQuotes() {
    const docFrag = document.createDocumentFragment();
    for (let i = 0; i < songCount; i++) {
        var entry = document.createElement('li');
        entry.textContent = songQuotes[i][1];
        docFrag.appendChild(entry);
    }
    document.body.appendChild(docFrag);
}

function checkAnswer(element) {
    if (element.innerHTML == currentSong) {
        result.innerHTML = "Correct";
        //console.log("Correct");
        correctCount++;
        element.disabled = "disabled";
        element.style.background='linear-gradient(to bottom right, #6eef4780, #42f80a80)';
    }
    else {
        result.innerHTML = "Incorrect";
        wrongGuesses.push(currentSong);
        //console.log("Incorrect");
    }
}

function disableWrongGuesses() {
    var buttons = document.querySelectorAll(".songChoices");
    buttons.forEach(element => {
        for (let i = 0; i < wrongGuesses.length; i++) {
            if (element.innerHTML == wrongGuesses[i])
                element.disabled = "disabled";
        }
    })
}

function guess(element) {
    if (currentIndex == 0) {
        checkAnswer(element);
        currentIndex++;
        currentSong = songQuotes[currentIndex][0];
        currentQuote = songQuotes[currentIndex][1];
        para.innerHTML = currentQuote;
    }

    else if(currentIndex + 1 < songCount) {
        checkAnswer(element);
        currentIndex++;
        currentSong = songQuotes[currentIndex][0];
        currentQuote = songQuotes[currentIndex][1];
        para.innerHTML = currentQuote;
    }
    else {
        checkAnswer(element);
        disableWrongGuesses();
        score.innerHTML = ((correctCount / songCount) * 100) + "%";
    }
    concurrentScore.innerHTML = correctCount + "/" + songCount;
}

function replay() {
    document.getElementById("buttonDiv").remove();
    songQuotes = [];
    currentIndex, currentSong, currentQuote = null;
    correctCount = 0;
    result.innerHTML = "";
    score.innerHTML = "";
    concurrentScore.innerHTML = "";
    buttonPress();
}