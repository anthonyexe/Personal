// Anthony D'Alessandro
var wordLength = 0;
var wordLengthString = '';
var letterChoice = '';
var timeSelection = 0;
const inputWords = new Map();
const letterMap = new Map();

const letterElements = document.getElementsByClassName("letterChoices");
const wordLengthElements = document.querySelectorAll("#three_letter_words, #four_letter_words, #five_letter_words");
const timerElements = document.querySelectorAll('#one_minute, #two_minutes, #three_minutes');


function letterSelect(element) {
    letterChoice = element.id;
    console.log(letterChoice);
    for (let i = 0; i < letterElements.length; i++) {
        var currentButton = letterElements.item(i);
        if (element.id === currentButton.id) {
            currentButton.style.color = 'white';
            currentButton.style.opacity = '1.0';
        }
        else {
            currentButton.style.color = 'grey';
            currentButton.style.opacity = '0.5';
        }
            
    }
}

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
        }
        else {
            currentElement.style.color = 'grey';
            currentElement.style.opacity = '0.5';
        }
    }
}

function setTimer(element, time) {
    timeSelection = time;
    console.log(timeSelection);
    for (let i = 0; i < timerElements.length; i++) {
        var currentElement = timerElements.item(i);
        if (element.id === currentElement.id) {
            currentElement.style.color = 'white';
            currentElement.style.opacity = '1.0';
        }
        else {
            currentElement.style.color = 'grey';
            currentElement.style.opacity = '0.5';
        }
    }
}

async function jsonData() {
    const fileName = wordLengthString + '.json';
    console.log(fileName);
    const response = await fetch(fileName);
    const data = await response.json();
    var results = JSON.parse(JSON.stringify(data));

    for (var x in results) {
        if (x.charAt(0) === letterChoice)
            letterMap.set(x, 1);
    }

    console.log(letterMap.size);
}

function checkInput() {
    var input = document.getElementById("userInput").value;
    console.log(input);
    if (!inputWords.has(input) && letterMap.has(input)) {
        inputWords.set(input, 1);
    }
    else {
        console.log("wrong/repeat word");
    }
    document.getElementById("userInput").value='';
    console.log(inputWords);
}

function timer() {
    let paragraph = document.createElement("p");
    paragraph.id = "timer";
    document.getElementById("timerDiv").append(paragraph);
    var sec = 60;
    var timer = setInterval(function() {
        document.getElementById("timer").innerHTML = '00:' + sec;
        sec--;
        if (sec < 0) {
            clearInterval(timer);
        }
    }, 1000);
}

function newTimer() {
    let paragraph = document.createElement("p");
    paragraph.id = "newTimer";
    document.getElementById("timerDiv").append(paragraph);
    
    var timer = setInterval(function() {
        const minutes = Math.floor(timeSelection / 60);
        let seconds = timeSelection % 60;
        if (seconds < 0)
            clearInterval(timer);
        if (seconds < minutes)
            seconds = '0' + seconds;
        document.getElementById("newTimer").innerHTML = `${minutes}:${seconds}`;
        timeSelection--;
    }, 1000);
}

function play() {
    var gameCriteria = document.getElementById("gameCriteria");
    gameCriteria.innerHTML = "" + wordLength + " letter words that start with " + "'" + letterChoice.toUpperCase() + "'";
    document.getElementById("letter-buttons").remove();
    document.getElementById("word-length-buttons").remove();
    document.getElementById("timer-buttons").remove();
    document.getElementById("play").remove();
    var instructionElements = document.querySelectorAll("#instruction1, #instruction2, #instruction3");
    console.log(instructionElements);

    for (let i = 0; i < instructionElements.length; i++) {
        var currentElement = instructionElements.item(i);
        currentElement.remove();
    }

    var userInput = document.getElementById("userInput");
    userInput.disabled = false;
    userInput.setAttribute("maxlength", wordLength);
    userInput.addEventListener('keyup', function(e) {
        if (this.value.length === wordLength)
            checkInput();
    });
    jsonData();
    //newTimer();
}

function getResults() {
    for (const [key, value] of inputWords.entries()) {
        console.log(key);
    }

    var stringResults = "";
    var results = document.createElement("p");
    var totalWordCount = document.createElement("p");
    totalWordCount.innerHTML = inputWords.size;

    var inputWordsSize = inputWords.size;
    var counter = 0;
    inputWords.forEach((value, key) => {
        if (counter == inputWordsSize - 1)
            stringResults += key;
        else
            stringResults += key + ", ";
        counter++;
    })
    
    results.innerHTML = stringResults;

    document.getElementById("resultsDiv").append(totalWordCount);
    document.getElementById("resultsDiv").append(results);
}