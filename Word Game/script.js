// Anthony D'Alessandro
var letterChoice = '';
var letterBoolean = false;
var wordLength = 0;
var wordLengthString = '';
var wordLengthBoolean = false;
var timeSelection = 0;
var timeBoolean = false;
const inputWords = new Set();
const wordSet = new Set();

const letterElements = document.getElementsByClassName("letterChoices");
const wordLengthElements = document.querySelectorAll("#three_letter_words, #four_letter_words, #five_letter_words");
const timerElements = document.querySelectorAll('#five_seconds, #one_minute, #two_minutes, #three_minutes');
const playButton = document.getElementById("play");

function reloadPage() {
    window.location.reload();
}

//Handle when a user selects the letter that the words will start with.
function letterSelect(element) {
    letterChoice = element.id;
    console.log(letterChoice);
    for (let i = 0; i < letterElements.length; i++) {
        var currentButton = letterElements.item(i);
        if (element.id === currentButton.id) {
            currentButton.style.color = 'white';
            currentButton.style.opacity = '1.0';
            letterBoolean = true;
        }
        else {
            currentButton.style.color = 'black';
            currentButton.style.opacity = '0.5';
        }
            
    }
    if (letterBoolean && wordLengthBoolean && timeBoolean) {
        playButton.disabled = false;
        playButton.style.background = 'linear-gradient(to bottom right, #47b1ef, #785aff)';
    }
        
}
//Handle when a user selects the length that the words will be.
function wordLengthSelect(element, charLimit) {
    wordLengthString = element.id;
    wordLength = charLimit;
    console.log(wordLengthString);
    console.log(wordLength);

    for (let i = 0; i < wordLengthElements.length; i++) {
        var currentElement = wordLengthElements.item(i);
        if (element.id === currentElement.id) {
            currentElement.style.color = 'white';
            currentElement.style.opacity = '1.0';
            wordLengthBoolean = true;
        }
        else {
            currentElement.style.color = 'black';
            currentElement.style.opacity = '0.5';
        }
    }
    if (letterBoolean && wordLengthBoolean && timeBoolean) {
        playButton.disabled = false;
        playButton.style.background = 'linear-gradient(to bottom right, #47b1ef, #785aff)';
    }
        
}
//Handle when a user selects the duration of the challenge.
function setTimer(element, time) {
    timeSelection = time;
    console.log(timeSelection);
    for (let i = 0; i < timerElements.length; i++) {
        var currentElement = timerElements.item(i);
        if (element.id === currentElement.id) {
            currentElement.style.color = 'white';
            currentElement.style.opacity = '1.0';
            timeBoolean = true;
        }
        else {
            currentElement.style.color = 'black';
            currentElement.style.opacity = '0.5';
        }
    }
    if (letterBoolean && wordLengthBoolean && timeBoolean) {
        playButton.disabled = false;
        playButton.style.background = 'linear-gradient(to bottom right, #47b1ef, #785aff)';
    }
        
}
/*Access the appropriate JSON file depending on the word length that the user selected.
  This function also parses through the aforementioned list of words and adds each one
  that starts with the letter specified be the user to a hashset.
*/
async function jsonData() {
    const fileName = wordLengthString + '.json';
    const response = await fetch(fileName);
    const data = await response.json();
    var results = JSON.parse(JSON.stringify(data));

    for (var x in results) {
        if (x.charAt(0) === letterChoice)
            wordSet.add(x);
    }

    console.log(wordSet.size);
}
//Creates the game timer and counts down from the time specified by the user.
function newTimer() {
    let paragraph = document.createElement("p");
    paragraph.id = "newTimer";
    document.getElementById("timerDiv").append(paragraph);
    
    var timer = timeSelection;
    var minutes, seconds;
    var timeInterval = setInterval(function() {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById("newTimer").innerHTML = minutes + ": " + seconds;

        if (--timer < 0) {
            clearInterval(timeInterval);
            endGame();
        }
    }, 1000);
}
//Handle each guess/answer from the user during the game and displays it for the user to see.
function checkInput() {
    var input = document.getElementById("userInput").value;
    var currentWord = document.createElement("span");
    currentWord.append(input + ", ");
    document.getElementById("guesses").append(currentWord);
    document.getElementById("userInput").value='';
}
/*This function essentially "starts" the game and removes/sets up the necessary elements.
*/
function play() {
    //Start game timer and call jsonData function to create the set of possible words for the game.
    newTimer();
    jsonData();
    var gameCriteria = document.getElementById("gameCriteria");
    gameCriteria.innerHTML = "" + wordLength + " letter words that start with " + "'" + letterChoice.toUpperCase() + "'";
    var userInput = document.getElementById("userInput");
    userInput.hidden = false;
    userInput.disabled = false;
    userInput.focus();
    document.getElementById("letter-buttons").remove();
    document.getElementById("word-length-buttons").remove();
    document.getElementById("timer-buttons").remove();
    document.getElementById("play").remove();
    var guesses = document.createElement("p");
    guesses.id = "guesses";
    document.getElementById("resultsDiv").append(guesses);
    var score = document.createElement("p");
    score.id = "score";
    document.getElementById("resultsDiv").append(score);
    var instructionElements = document.querySelectorAll("#instruction1, #instruction2, #instruction3");

    for (let i = 0; i < instructionElements.length; i++) {
        var currentElement = instructionElements.item(i);
        currentElement.remove();
    }

    userInput.setAttribute("maxlength", wordLength);
    userInput.addEventListener('keyup', function(e) {
        if (this.value.length === wordLength)
            checkInput();
    });
}
function getResults() {
    var resultElements = document.getElementById("guesses").querySelectorAll("*");
    var count = 0;
    resultElements.forEach(element => {
        let currentWord = element.innerHTML.replace(/,/g, "");
        currentWord = currentWord.trim();
        if (count == resultElements.length - 1)
            element.innerHTML = currentWord;
        if (!inputWords.has(currentWord) && wordSet.has(currentWord)) {
            inputWords.add(currentWord);
            element.style.color = 'green';
        }
        else {
            element.style.textDecoration = 'line-through';
        }
        count++;
    });
    
    document.getElementById("score").append("Score: " + inputWords.size + " words in " + timeSelection / 60 + " minute(s)");
}
/*This function is called when the game timer runs out and disables the input form and
  removes the timer.
*/
function endGame() {
    document.getElementById("userInput").disabled = true;
    document.getElementById("newTimer").remove();
    getResults();

    var replayButton = document.createElement("button");
    replayButton.className = "wordLengthChoices";
    replayButton.id = "replay";
    replayButton.innerHTML = "Replay";
    replayButton.addEventListener('click', replay);

    var newGameButton = document.createElement("button");
    newGameButton.className = "wordLengthChoices";
    newGameButton.id = "newGame";
    newGameButton.innerHTML = "New Game";
    newGameButton.addEventListener('click', reloadPage);

    document.getElementById("endButtons").append(replayButton);
    document.getElementById("endButtons").append(newGameButton);
}

function replay() {
    inputWords.clear();
    document.getElementById("replay").remove();
    document.getElementById("newGame").remove();

    document.getElementById("guesses").innerHTML = "";
    document.getElementById("score").innerHTML = "";

    document.getElementById("userInput").disabled = false;
    document.getElementById("userInput").focus();
    newTimer();
}