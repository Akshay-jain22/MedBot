var content = document.getElementById("dynamic-content");
var status = document.getElementById("status");
var medicine = '';
var schedule = '';
var Possible_Schedule = {
    "001": "Evening",
    "010": "Afternoon",
    "011": "Afternoon, Evening",
    "100": "Morning",
    "101": "Morning, Evening",
    "110": "Morning, Afternoon",
    "111": "Morning, Afternoon, Evening"
};

Medicines = [];
Schedules = [];
var isPaused = true;

// Sequence of Code Execution :-
// wishMe -> InputName -> InputSchedule -> verify -> update_data -> SaveFile

function wishMe() {
    document.getElementById("status").innerHTML = "Medbot is running...";
    var text = 'Hello Sir, I am MedBot';

    console.log('DOM is Loaded Successfully');

    speak(text);

    wait = (funcName = 'wishMe') => {
        if (isPaused) {
            console.log('wait : ' + funcName);
            setTimeout(function() {
                wait(funcName);
            }, 100);
        } else {
            InputName('CONTINUE');
        }
    }
    wait();
}


function InputName(text = 'STOP') {
    isPaused = true;
    speak('Tell the Medicine Name');

    wait = (funcName = 'InputName') => {
        if (isPaused) {
            console.log('wait : ' + funcName);
            setTimeout(function() {
                wait(funcName);
            }, 100);
        } else {
            listenMedicine(text);
        }
    }
    wait();
}

function InputSchedule(text = 'STOP') {
    isPaused = true;
    speak('Tell the Schedule');

    wait = (funcName = 'InputSchedule') => {
        if (isPaused) {
            console.log('wait : ' + funcName);
            setTimeout(function() {
                wait(funcName);
            }, 100);
        } else {
            listenSchedule(text);
        }
    }
    wait();
}

function replaceAt(temp, index, replacement) {
    return temp.substr(0, index) + replacement + temp.substr(index + replacement.length);
}

function verify() {
    isPaused = true;
    document.getElementById("update").disabled = true;

    medicine = document.getElementById('Medicine').value;
    temp = "000";
    if (document.getElementById('morning').checked)
        temp = replaceAt(temp, 0, "1");
    if (document.getElementById('afternoon').checked)
        temp = replaceAt(temp, 1, "1");
    if (document.getElementById('evening').checked)
        temp = replaceAt(temp, 2, "1");
    schedule = Possible_Schedule[temp];

    speak('Are the details correct?')

    details = "</br>Medicine Name : " + medicine + "</br>Schedule : " + schedule;
    content.innerHTML += details;

    wait = (funcName = 'verify') => {
        if (isPaused) {
            console.log('wait : ' + funcName);
            setTimeout(function() {
                wait(funcName);
            }, 100);
        } else {
            listenVerify()
        }
    }
    wait();
}


function update_data() {
    isPaused = true;

    medicine = document.getElementById('Medicine').value;
    temp = "000";
    if (document.getElementById('morning').checked)
        temp = replaceAt(temp, 0, "1");
    if (document.getElementById('afternoon').checked)
        temp = replaceAt(temp, 1, "1");
    if (document.getElementById('evening').checked)
        temp = replaceAt(temp, 2, "1");
    console.log(temp);
    schedule = Possible_Schedule[temp];

    Medicines.push(medicine);
    Schedules.push(schedule);

    speak("Great. Do you want to add more medicines ?")
    wait = (funcName = 'update_data') => {
        if (isPaused) {
            console.log('wait : ' + funcName);
            setTimeout(function() {
                wait(funcName);
            }, 100);
        } else {
            listenUpdateData();
        }
    }
    wait();
}

function check(id) {
    document.getElementById(id).checked = true;
}

function uncheck(id) {
    document.getElementById(id).checked = false;
}

function setSchedule(query, text) {
    uncheck('morning');
    uncheck('afternoon');
    uncheck('evening');

    isKey = query in Possible_Schedule;
    if (isKey) {
        if (query[0] == '1')
            check('morning');
        if (query[1] == '1')
            check('afternoon');
        if (query[2] == '1')
            check('evening');
        schedule = Possible_Schedule[query];

        if (text == 'CONTINUE')
            verify();
    } else {
        content.innerHTML = 'Incorrect Schedule : ' + query + ', Try Again!';
        InputSchedule(text);
    }
}


function SaveFile() {
    document.getElementById("status").innerHTML = "Saving File...";
    alert("Saving File ...");

    $.getJSON('/save', {
        name: JSON.stringify(Medicines),
        schedule: JSON.stringify(Schedules),
    }, function(data) {
        message = data.result;
        alert(message);
        document.getElementById("status").innerHTML = message;
        Medicines = [];
        Schedules = [];
    });
}


/*----------------------------------
    Text to Speech Functionality
----------------------------------*/

async function speak(text) {
    isPaused = true;
    //update the content of dynamicBox
    content.innerHTML = text;

    await getNextAudio(text);
    async function getNextAudio(sentence) {
        const speech = new SpeechSynthesisUtterance(sentence);
        speech.volume = 1;
        speech.rate = 1;
        speech.pitch = 1;
        window.speechSynthesis.speak(speech);

        return new Promise(resolve => {
            speech.onend = () => {
                resolve;
                isPaused = false;
            }
        });
    }
};


/*----------------------------------
    Speech to Text Functionality
----------------------------------*/

try {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognition = new SpeechRecognition();
} catch (e) {
    console.error(e);
    $('.no-browser-support').show();
    $('.app').hide();
}

recognition.onstart = function() {
    content.innerHTML = 'Listening...';
}

recognition.onspeechend = function() {
    status.innerHTML = 'You were quiet for a while so voice recognition turned itself off.';
}

recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
        content.innerHTML = 'No speech was detected. Try again.';
    };
}

async function listenMedicine(text) {
    isPaused = true;
    recognition.start();
    recognition.continuous = true;

    recognition.onresult = function(data) {
        //get the currentLine captured by the SpeechRecognition object data.
        var current = data.resultIndex;

        //get it's transcript
        var query = data.results[current][0].transcript;
        recognition.stop();
        console.log(query);
        status.innerHTML = 'Voice Recognition Stopped';

        var mobileRepeatBug = (current == 1 && query == event.results[0][0].transcript);
        isPaused = false;
        if (!mobileRepeatBug) {
            document.getElementById('Medicine').value = query;
            medicine = query;
            if (text == 'CONTINUE')
                InputSchedule(text);
        } else {
            content.innerHTML = 'Some Error Occured, Try Again!';
            InputName(text);
        }
    };
}

async function listenSchedule(text) {
    isPaused = true;
    recognition.start();
    recognition.continuous = true;

    recognition.onresult = function(data) {
        //get the currentLine captured by the SpeechRecognition object data.
        var current = data.resultIndex;

        //get it's transcript
        var query = data.results[current][0].transcript;
        recognition.stop();
        console.log(query);
        content.innerHTML = 'Voice recognition stopped';

        var mobileRepeatBug = (current == 1 && query == event.results[0][0].transcript);
        isPaused = false;
        if (!mobileRepeatBug) {
            setSchedule(query, text);
        } else {
            content.innerHTML = 'Some Error Occured, Try Again!';
            InputSchedule(text);
        }
    };
}

async function listenVerify() {
    isPaused = true;
    recognition.start();
    recognition.continuous = true;

    recognition.onresult = function(data) {
        //get the currentLine captured by the SpeechRecognition object data.
        var current = data.resultIndex;

        //get it's transcript
        var query = data.results[current][0].transcript;
        recognition.stop();
        console.log(query);
        content.innerHTML = 'Voice recognition stopped';

        var mobileRepeatBug = (current == 1 && query == event.results[0][0].transcript);
        isPaused = false;
        if (!mobileRepeatBug) {
            if (query.includes('no')) {
                content.innerHTML = "Sorry for inconvenience, Try editing through website";
                document.getElementById("update").disabled = false;
            } else {
                update_data()
            }
        } else {
            content.innerHTML = 'Some Error Occured, Try Again!';
            verify();
        }
    };
}

async function listenUpdateData() {
    isPaused = true;
    recognition.start();
    recognition.continuous = true;

    recognition.onresult = function(data) {
        //get the currentLine captured by the SpeechRecognition object data.
        var current = data.resultIndex;

        //get it's transcript
        var query = data.results[current][0].transcript;
        recognition.stop();
        console.log(query);
        content.innerHTML = 'Voice recognition stopped';

        var mobileRepeatBug = (current == 1 && query == event.results[0][0].transcript);
        isPaused = false;
        if (!mobileRepeatBug) {
            if (!query.includes('yes')) {
                content.innerHTML = "Ohk Sir, Thanks for using Medbot";
                SaveFile();
            } else {
                InputName('CONTINUE');
            }
        } else {
            content.innerHTML = 'Some Error Occured, Try Again!';
            Medicines.pop();
            Schedules.pop();
            update_data();
        }
    };
}