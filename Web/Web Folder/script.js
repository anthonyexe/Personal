// Ant
var songQuotes = new Array();
var songCount = 0;

let artist = document.getElementById("artist");
let currentIndex, currentSong, currentQuote;
let correctCount = 0;
let para = document.getElementById("Quote");
let score = document.getElementById("Score");
let concurrentScore = document.getElementById("concurrentScore");

let wrongGuesses = new Array();

async function playButton() {
    //Disable the play button for selected artist
    artist.disabled = "disabled";
    //Gray out the play button
    artist.style.background = "grey";
    //Store the artist's name from HTML element
    let artistName = artist.name;
    //Pass artistName variable to the jsonData method to extract the songs/quotes from
    //the specified artist's JSON file
    await jsonData(artistName);
    //Call the createButtons method to display the user's song options
    createButtons();
    currentIndex = 0;
    //Set currentSong variable to the first song title in the songQuotes array
    currentSong = songQuotes[0][0];
    //Set currentQuote variable to the first song quote in the songQuotes array
    currentQuote = songQuotes[0][1];
    //Set the para element's inner HTML to the currentQuote value to display
    //the first quote to the user
    para.innerHTML = currentQuote;
}

async function jsonData(artistName) {
    //Create artistFile variable to hold the JSON file name for the specified artist
    const artistFile = artistName + '.json';
    //Variable for Promise returned by fetching of the JSON file
    const response = await fetch(artistFile);
    //Data variable to hold JSON objects
    const data = await response.json();
    //Results variable to hold stringified JSON objects
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
    //Shuffle the songQuotes array
    songQuotes = shuffleSongs(songQuotes);
}

function shuffleSongs(arr) {
    //Set shuffleIndex equal to total number of songs
    let shuffleIndex = songCount;
    while (shuffleIndex != 0) {
        //Compute a random index from 0:(shuffleIndex - 1)
        let randomIndex = Math.floor(Math.random() * shuffleIndex--);
        //Store the current arr value at the shuffleIndex in a temp variable
        let temp = arr[shuffleIndex];
        //Set the current arr value at the shuffleIndex to the arr value at the randomIndex
        arr[shuffleIndex] = arr[randomIndex];
        //"Swap" the values by setting the arr value at the randomIndex to the temp value from above
        arr[randomIndex] = temp;
    }
    return arr;
}

function createButtons() {
    //Create empty array to store a copy of the song titles
    let titlesCopy = [];
    //Loop through the songQuotes array and store each song title in the titlesCopy array
    for (let i = 0; i < songCount; i++) {
        titlesCopy[i] = songQuotes[i][0];
    }
    //Shuffle the titlesCopy array so the buttons/song choices for the user are random
    titlesCopy = shuffleSongs(titlesCopy);
    //Create an HTML div element variable
    const newDiv = document.createElement("div");
    //Loop through titlesCopy array to get song titles for each button
    for (let i = 0; i < songCount; i++) {
        //Create an HTML button element variable
        const newButton = document.createElement('button');
        //Set the button text to the current song title
        newButton.textContent = titlesCopy[i];
        //Give the button an "onclick" attribute that enables it to call the guess method
        newButton.setAttribute("onclick", "guess(this)");
        //Set the button's class to "songChoices" for CSS effects
        newButton.className = "songChoices";
        //Append the button to the div element
        newDiv.appendChild(newButton);
    }
    //Set the div class to "buttonDiv" for CSS effects
    newDiv.className = "buttonDiv";
    //Set the div id to "buttonDiv" for accessing later in JavaScript
    newDiv.id = "buttonDiv";
    //Get "buttonContainer" div element and append the button div
    document.getElementById("buttonContainer").appendChild(newDiv);
}

/*
function listQuotes() {
    const docFrag = document.createDocumentFragment();
    for (let i = 0; i < songCount; i++) {
        var entry = document.createElement('li');
        entry.textContent = songQuotes[i][1];
        docFrag.appendChild(entry);
    }
    document.body.appendChild(docFrag);
}
*/

function checkAnswer(element) {
    //Take the given HTML element and check if the inner HTML value is equal to the currentSong value
    if (element.innerHTML == currentSong) {
        //If yes, increment correctCount, disable the button, and change the background color to green
        correctCount++;
        element.disabled = "disabled";
        element.style.background='linear-gradient(to bottom right, #6eef4780, #42f80a80)';
    }
    else {
        //If not, call buttonShake style animation and push the current song title into wrongGuesses array
        element.style.animation="buttonShake .4s";
        wrongGuesses.push(currentSong);
    }
}

function disableWrongGuesses() {
    //Query all elements with the songChoices class and store them in buttons variable
    var buttons = document.querySelectorAll(".songChoices");
    buttons.forEach(element => {
        //For each button element, loop through the wrongGuesses array
        for (let i = 0; i < wrongGuesses.length; i++) {
            //If current button element's innerHTML is equal to current song title in wrongGuesses, disable that button
            if (element.innerHTML == wrongGuesses[i])
                element.disabled = "disabled";
        }
    })
}

function guess(element) {
    if(currentIndex == 0 || (currentIndex + 1 < songCount)) {
        checkAnswer(element);
        currentIndex++;
        //Update currentSong variable to next song title
        currentSong = songQuotes[currentIndex][0];
        //Update currentQuote variable to next song quote
        currentQuote = songQuotes[currentIndex][1];
        //Update the quote displayed to the user to reflect the next song quote
        para.innerHTML = currentQuote;
    }
    else { //Last guess
        checkAnswer(element);
        //Call disableWrongGuesses method to make sure the user cannot select the remaining buttons from their incorrect guesses
        disableWrongGuesses();
        //Calculate user score rounded to nearest whole number expressed as a percentage
        //Change the 'score' element's innerHTML to reflect user's score
        score.innerHTML = Math.round(((correctCount / songCount) * 100)) + "%";
    }
    //Update concurrent score expressed as a fraction
    concurrentScore.innerHTML = correctCount + "/" + songCount;
}

function replay() {
    //Remove song choice buttons from previous game
    document.getElementById("buttonDiv").remove();
    //Reset songQuotes to empty array
    songQuotes = [];
    //Reset current index, song, and quote variables to be null
    currentIndex, currentSong, currentQuote = null;
    //Reset correctCount
    correctCount = 0;
    //Set score element's innerHTML to empty string
    score.innerHTML = "";
    //Set concurrentScore element's innerHTML to empty string
    concurrentScore.innerHTML = "";
    //Call playButton method to start new game
    playButton();
}
