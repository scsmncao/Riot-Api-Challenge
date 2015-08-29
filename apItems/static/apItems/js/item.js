var firstPatchData = {}
var secondPatchData = {}

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

function renderChampions(championList, elementToAppend) {
    _.each(championList, function() {
        $(elementToAppend).append()
    })
}

$(window).load(function() {
    var regexForNum = /[0-9]{4}/;
    itemId = parseInt(regexForNum.exec(window.location.pathname)[0]);
    $('.item-main-name').append(firstPatchData[itemId]['name'])
    var buyRateFirst = firstPatchData[itemId]['buy_rate'] * 100;
    var buyRateSecond = secondPatchData[itemId]['buy_rate'] * 100;
    var winRateFirst = firstPatchData[itemId]['win_rate'] * 100;
    var winRateSecond = secondPatchData[itemId]['win_rate'] * 100;
    if (buyRateFirst > buyRateSecond) {
        arrowBuy = 'https://upload.wikimedia.org/wikipedia/commons/0/04/Red_Arrow_Down.svg';
    }
    else if (Math.abs(buyRateFirst - buyRateSecond) < .0000001) {
        arrowBuy = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Neutral_icon_C.svg/2000px-Neutral_icon_C.svg.png';
    }
    else {
        arrowBuy = 'https://upload.wikimedia.org/wikipedia/commons/5/50/Green_Arrow_Up.svg';
    }
    if (winRateFirst > winRateSecond) {
        arrowWin = 'https://upload.wikimedia.org/wikipedia/commons/0/04/Red_Arrow_Down.svg';
    }
    else if (Math.abs(winRateFirst - winRateSecond) < .0000001) {
        arrowWin = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Neutral_icon_C.svg/2000px-Neutral_icon_C.svg.png';
    }
    else {
        arrowWin = 'https://upload.wikimedia.org/wikipedia/commons/5/50/Green_Arrow_Up.svg';
    }
    var buyRateDifference = buyRateSecond - buyRateFirst;
        var winRateDifference = winRateSecond - winRateFirst;
        if (buyRateDifference >= 0){
            var colorBuy = '#00FF00';
        }
        else {
            var colorBuy = '#FF3300';
        }
        if (winRateDifference >= 0){
            var colorWin = '#00FF00';
        }
        else {
            var colorWin = '#FF3300';
        }

        if (Math.abs(winRateDifference) > 2) {
            var highlight = '#000066';
        }
        else {
            var highlight = 'transparent';
        }
    $('.buy-rate-info').append('<div class="item-specific-page">' +
                                    '<div class="buy-rate">' +
                                        '<div class="patch-number left-patch">5.11</div>' +
                                        '<div class="item-buy-rate">' + buyRateFirst.toFixed(2) + '%</div>' + 
                                    '</div>' +
                                    '<div class="arrow-item-page"><img src="' + arrowBuy + '" height=20></div>' +
                                    '<div class="buy-rate">' +
                                        '<div class="patch-number right-patch">5.14</div>' +
                                        '<div class="item-buy-rate">' + buyRateSecond.toFixed(2) + '%</div>' +
                                    '</div>' +
                                '</div>'+
                                '<div class="item-difference-specific" style="color:' + colorBuy + '">' +
                                    buyRateDifference.toFixed(2) + '%' +
                                '</div>');
    $('.win-rate-info').append('<div class="item-specific-page">' +
                                    '<div class="buy-rate">' +
                                        '<div class="patch-number left-patch">5.11</div>' +
                                        '<div class="item-win-rate">' + winRateFirst.toFixed(2) + '%</div>' +
                                    '</div>' +
                                    '<div class="arrow-item-page"><img src="' + arrowWin + '" height=20></div>' + 
                                    '<div class="buy-rate">' +
                                        '<div class="patch-number right-patch">5.14</div>' +
                                        '<div class="item-win-rate">' + winRateSecond.toFixed(2) + '%</div>' +
                                    '</div>' +
                                '</div>'+
                                '<div class="item-difference-specific" style="color:' + colorWin + '">' +
                                    winRateDifference.toFixed(2) + '%' +
                                '</div>');
    $('.item-results').css('width', ($('.buy-rate-block').outerWidth() + $('.win-rate-block').outerWidth() + 45));
    var firstChampionList = firstPatchData[itemId]['champions'];
    var secondChampionList = secondPatchData[itemId]['champions'];
    for (var i = 0; i < firstChampionList.length; i++) {
        if (i === 7) {
            break;
        }
        else {
            $('.champion-list-firstpatch').append('<img src="http://ddragon.leagueoflegends.com/cdn/5.16.1/img/champion/' + firstChampionList[i] + '" height=50>')
        }
    }
    for (var i = 0; i < secondChampionList.length; i++) {
        if (i === 7) {
            break;
        }
        else {
            $('.champion-list-secondpatch').append('<img src="http://ddragon.leagueoflegends.com/cdn/5.16.1/img/champion/' + secondChampionList[i] + '" height=50>')
        }
    }
});