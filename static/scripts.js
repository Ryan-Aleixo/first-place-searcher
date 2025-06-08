let HDButtonState = 0;
let HRButtonState = 0;
let DTButtonState = 0;
let FLButtonState = 0;
let resultDiv = document.getElementById('result');
let resultCount = document.getElementById('count');
let data;
const idList = ["pp-min", "pp-max", "ar-min", "ar-max", "od-min", "od-max", "cs-min", "cs-max",
    "sr-min", "sr-max", "length-min", "length-max", "combo-min", "combo-max", "bpm-min", "bpm-max",
    "acc-min", "acc-max", "pc-min", "pc-max"];
let inputList = [];
let name;
let namesList = [];

function toggleHD() {
    HDButtonState = (HDButtonState + 1) % 2;
    updateButtonState('toggleHD', HDButtonState);
}

function toggleHR() {
    HRButtonState = (HRButtonState + 1) % 2;
    updateButtonState('toggleHR', HRButtonState);
}

function toggleDT() {
    DTButtonState = (DTButtonState + 1) % 2;
    updateButtonState('toggleDT', DTButtonState);
}

function toggleFL() {
    FLButtonState = (FLButtonState + 1) % 2;
    updateButtonState('toggleFL', FLButtonState);
}

function updateButtonState(buttonId, Toggle) {
    const button = document.getElementById(buttonId);
    if (Toggle === 1) {
        button.classList.add('orange-bg');
    } else {
        button.classList.remove('orange-bg');
    }

    search();
}


function getFromInputs() {
    inputList = [];

    for (let i = 0; i < idList.length; i++) {
        inputList.push(document.getElementById(idList[i]).value);
    }
    // add names list other time
    return inputList.concat([HDButtonState, HRButtonState, DTButtonState, FLButtonState]);
}

function search() {
    const xhr = new XMLHttpRequest();
    const inputListJSON = JSON.stringify(getFromInputs());
    console.log(inputListJSON);

    xhr.open('GET', `/search?inputList=${inputListJSON}`, true); // use /search now

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            resultDiv = document.getElementById('result');

            resultDiv.innerHTML = "";
            resultCount.innerHTML = "";
            data = JSON.parse(xhr.responseText);
            if (data.length === 0) {
                resultDiv.innerHTML = "Your search didn't return anything"
                return;
            }
            resultCount.innerText = "Results: " + data.length;
            const firstItems = data.slice(0, 5);
            data.splice(0, 5);
            firstItems.forEach(item => {
                addHTML(item);
            });
        }
    };
    xhr.send();

}


function addHTML(item) {
    resultDiv.innerHTML += `
        <div class="map_display">
            <img src="https://assets.ppy.sh/beatmaps/${item['MapsetID']}/covers/list.jpg" alt="No Background">
            <a href="${item['mapURL']}" class="link_text" target="_blank">${item['artistName']} - ${item['mapTitle']} [${item['DiffName']}]</a>
            <div class="info_box">
                <p class="other">Playcount: ${item['MapsetPlaycount']}</p>
                <p class="other">Curr #1: ${item['player']}</p>
                <p class="other">Accuracy: ${item['accuracy']}%</p>
                <p class="other">Year Ranked: ${item['DateRanked']}</p>
            </div>
        </div>`

}

window.addEventListener('scroll', () => {
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight * 0.9) {
        loadData();
    }
})

function loadData() {
    resultDiv = document.getElementById('result');
    items = data.slice(0, 5);
    data.splice(0, 5);
    items.forEach(item => {
        addHTML(item);
    });
}
