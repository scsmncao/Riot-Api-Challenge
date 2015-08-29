var patches = ['5.11', '5.14']
var servers = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
var modes = ['NORMAL_5X5', 'RANKED_SOLO']

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

$(window).load(function() {
    $('.inner-container').append('<div class="patches-compared">' +
                                    'Patch ' + patches[0] + ' vs Patch ' + patches[1] +
                                '</div>'
                                )
    $('.inner-container').append('<div class="labels">' + 
                                '<div class="name-of-item label-for-chart">' +
                                    'Item Name' +
                                '</div>' +
                                '<div class="rates-container-buy rate-container label-for-chart">' +
                                    'Buy Rate' +
                                '</div>' +
                                '<div class="rates-container-win rate-container label-for-chart win-container-label">' +
                                    'Win Rate' +
                                '</div>' +
                            '</div>');
    _.each(Object.keys(firstPatchData), function(item) {
        var buyRateFirst = firstPatchData[item]['buy_rate'] * 100;
        var buyRateSecond = secondPatchData[item]['buy_rate'] * 100;
        var winRateFirst = firstPatchData[item]['win_rate'] * 100;
        var winRateSecond = secondPatchData[item]['win_rate'] * 100;
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

        var appendItem = '<div class="item-description" style="background-color:' + highlight + '">' + 
                            '<a href="' + item + '" class="link-to-item">' +
                            '<div class="item-img">' +
                                '<img src="http://ddragon.leagueoflegends.com/cdn/5.16.1/img/item/' + item + '.png"' + 'height="50">' +
                            '</div>' + 
                            '<div class="name-of-item">' +
                                firstPatchData[item]['name'] +
                            '</div>' +
                            '<div class="rates-container-buy rate-container">' +
                                '<span class="buy-rate-first rate">' + buyRateFirst.toFixed(2) + '%</span>' + 
                                '<span class="arrow"><img src="' + arrowBuy + '" height=10></span>' + 
                                '<span class="buy-rate-second rate">' + buyRateSecond.toFixed(2) + '%</span>' +
                            '</div>' +
                            '<div class="rate-difference buy-difference" style="color:' + colorBuy + '">' +
                                buyRateDifference.toFixed(2) + '%' +
                            '</div>' +
                            '<div class="rates-container-win rate-container">' +
                                '<span class="win-rate-first rate">' + winRateFirst.toFixed(2) + '%</span>' + 
                                '<span class="arrow"><img src="' + arrowWin + '" height=10></span>' + 
                                '<span class="win-rate-second rate">' + winRateSecond.toFixed(2) + '%</span>' +
                            '</div>' +
                            '<div class="rate-difference win-difference" style="color:' + colorWin + '">' +
                                winRateDifference.toFixed(2) + '%' +
                            '</div></a>' +
                        '</div>';
        $('.inner-container').append(appendItem);

    });
});