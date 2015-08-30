var patches = ['5.11', '5.14']

var firstPatchData = {}
var secondPatchData = {}

// ajax calls to get the data
$.ajax({
  url: "static/apItems/final_data/5.11/combined_data.json",
  dataType: 'json',
  async: false,
  success: function(data) {
    firstPatchData = data;
  }
});

$.ajax({
  url: "static/apItems/final_data/5.14/combined_data.json",
  dataType: 'json',
  async: false,
  success: function(data) {
    secondPatchData = data;
  }
});

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

// function to render the champions
function renderChampions(championList, elementToAppend) {
    for (var i = 0; i < championList.length; i++) {
        if (i === 7) {
            break;
        }
        else {
            $(elementToAppend).append('<img src="http://ddragon.leagueoflegends.com/cdn/5.16.1/img/champion/' + championList[i] + '" height=50>')
        }
    }
}

// function to append the rates
function appendRates(elementToAppendTo, firstRate, secondRate) {
    // this will determine what kind of arrow to use
    if (firstRate > secondRate) {
        arrow = 'https://upload.wikimedia.org/wikipedia/commons/0/04/Red_Arrow_Down.svg';
    }

    // checks for equality, since they are floats, need a delta
    else if (Math.abs(firstRate - secondRate) < .0000001) {
        arrow = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Neutral_icon_C.svg/2000px-Neutral_icon_C.svg.png';
    }
    else {
        arrow = 'https://upload.wikimedia.org/wikipedia/commons/5/50/Green_Arrow_Up.svg';
    }
    var rateDifference = secondRate - firstRate;
    if (rateDifference >= 0){
        var color = '#00FF00';
    }
    else {
        var color = '#FF3300';
    }
    $(elementToAppendTo).append('<div class="item-specific-page">' +
                                    '<div class="buy-rate">' +
                                        '<div class="patch-number left-patch">' + patches[0] + '</div>' +
                                        '<div class="item-buy-rate">' + firstRate.toFixed(2) + '%</div>' +
                                    '</div>' +
                                    '<div class="arrow-item-page"><img src="' + arrow + '" height=20></div>' + 
                                    '<div class="buy-rate">' +
                                        '<div class="patch-number right-patch">' + patches[1] + '</div>' +
                                        '<div class="item-buy-rate">' + secondRate.toFixed(2) + '%</div>' +
                                    '</div>' +
                                '</div>'+
                                '<div class="item-difference-specific" style="color:' + color + '">' +
                                    rateDifference.toFixed(2) + '%' +
                                '</div>');
}

function appendTreeItems(elementToAppendTo, itemList, type) {
    _.each(itemList, function(item) {
        if (firstPatchData.hasOwnProperty(item)) {
            $(elementToAppendTo).append('<a class="build-items" href="/' + item + '">' + '<img src="http://ddragon.leagueoflegends.com/cdn/5.16.1/img/item/' + item +'.png" height=30></a>');
        }
    });
    if (itemList.length === undefined) {
        $(elementToAppendTo).append('This item does not build ' + type + ' any AP Item');
    }
}

// get the item number from the url
var regexForNum = /[0-9]{4}/;
itemId = parseInt(regexForNum.exec(window.location.pathname)[0]);

// checking for injection attacks just in case django doesn't catch them
if (itemId % 1 !== 0 && itemId.toString().length != 4) {
    window.location.replace("/index.html");
    alert('Stop trying to hack the site');
}

//redirect if item id doesn't exist
else {
    if (!firstPatchData.hasOwnProperty(itemId)) {
        window.location.replace("/index.html");
    }
}

$(window).load(function() {

    appendTreeItems('.from-items', firstPatchData[itemId]['from'], 'from');
    appendTreeItems('.into-items', secondPatchData[itemId]['into'], 'into');

    //append the name of the item
    $('.item-main-name').append(firstPatchData[itemId]['name'])

    // calculate the buy rate and win rate percentages of each
    var buyRateFirst = firstPatchData[itemId]['buy_rate'] * 100;
    var buyRateSecond = secondPatchData[itemId]['buy_rate'] * 100;
    var winRateFirst = firstPatchData[itemId]['win_rate'] * 100;
    var winRateSecond = secondPatchData[itemId]['win_rate'] * 100;

    appendRates('.buy-rate-info', buyRateFirst, buyRateSecond);
    appendRates('.win-rate-info', winRateFirst, winRateSecond);
    
    // determines the width of the item results div in order to center it with margin: 0 auto
    $('.item-results').css('width', ($('.buy-rate-block').outerWidth() + $('.win-rate-block').outerWidth() + 45));

    // gets the champions list
    var firstChampionList = firstPatchData[itemId]['champions'];
    var secondChampionList = secondPatchData[itemId]['champions'];

    // adds the champions to the list and at most has 7
    renderChampions(firstChampionList, '.champion-list-firstpatch');
    renderChampions(secondChampionList, '.champion-list-secondpatch');
});