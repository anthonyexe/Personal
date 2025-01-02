// Anthony D'Alessandro
const inputWords = new Map();
const threeLetterMap = new Map();

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

async function jsonData(length) {
    const fileName = length.id + '.json';
    console.log(fileName);
    const response = await fetch(fileName);
    const data = await response.json();
    var results = JSON.parse(JSON.stringify(data));

    for (var x in results) {
        threeLetterMap.set(x, 1);
    }

    console.log(threeLetterMap.size);
}

function checkInput() {
    var input = document.getElementById("userInput").value;
    console.log(input);

    var resultButton = document.getElementById("submit");
    if (!inputWords.has(input) && threeLetterMap.has(input)) {
        inputWords.set(input, 1);
        resultButton.style.background = 'linear-gradient(to bottom right, #6eef4780, #42f80a80)';
        setTimeout(function() {
            resultButton.style.background = 'linear-gradient(to bottom right, #EF4765, #FF9A5A)';
        }, 125);
    }
    else {
        resultButton.classList.remove("gameButtons");
        void resultButton.offsetWidth;
        resultButton.classList.add("gameButtons");
        //resultButton.style.animation = "buttonShake .2s";
        console.log("wrong/repeat word");
        
    }
    document.getElementById("userInput").value='';
    console.log(inputWords);
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