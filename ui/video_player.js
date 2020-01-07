// import $ from 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'

// Read JSON file
const jsonUrl = "nmb2_1.json";
let jsonData;
$.ajax({
    url: jsonUrl,
    dataType: 'json',
    async: false,
    data: {"data": "data"},
    success: function (json) {
        jsonData = json;
    }
});
let chapters = jsonData.chapters;
let videoName = jsonData.video_name;
let videoDate = jsonData.video_date;

// Display video name into script
let divVideoTitle = document.getElementById("video-title");
divVideoTitle.append(videoName);
let divVideoDate = document.getElementById("video-date");
divVideoDate.append(videoDate);

// Display information into list
let i, ul, li, a, ic, chapterTitle;
let repeatFlg = false;
ul = document.getElementById("ul-set-list");
for (i=0; i<chapters.length; i++){
    ic = document.createElement("i");
    ic.className = "fas fa-stop";
    ic.id = "icon-" + chapters[i].id.toString();

    a = document.createElement("a");
    a.href = "javascript:void(0);";

    li = document.createElement("li");
    li.id = chapters[i].id.toString();
    li.onclick = chapterClick;
    chapterTitle = document.createTextNode(chapters[i].title);

    a.append(ic);
    a.append(" ");
    a.append(chapterTitle);
    li.append(a);
    ul.append(li);
}

// Video Player
let player = videojs("video-player");
let currentTime;
let repeatID = null;
player.volume(0.5);

function chapterClick() {
    currentTime = player.currentTime();
    let start_time = Number(chapters[this.id].start_time);
    let end_time = Number(chapters[this.id].end_time);

    if (currentTime != 0 &&  start_time <= currentTime && currentTime <= end_time){
        repeatFlg = true;
        repeatID = this.id;
    }else {
        repeatFlg = false;
        repeatID = null;
    }
    console.log(repeatFlg);

    player.ready(function () {
        player.currentTime(start_time);
        player.play();

    });
}

function changeSetListState () {
    let start_time, end_time, icon_elem, list_elem;
    currentTime = player.currentTime();
    // console.log(currentTime);
    for (i=0; i<chapters.length; i++){
        start_time = Number(chapters[i].start_time);
        end_time = Number(chapters[i].end_time);
        icon_elem = document.getElementById("icon-" + chapters[i].id.toString());
        list_elem = document.getElementById(chapters[i].id.toString());
        if (repeatFlg && start_time <= currentTime && currentTime < end_time){
            icon_elem.className = "fa fa-repeat video-playing";
            list_elem.className = "video-playing";
        }else if (currentTime !== 0 && start_time <= currentTime && currentTime < end_time){
            icon_elem.className = "fas fa-play video-playing";
            list_elem.className = "video-playing";
        }else {
            icon_elem.className = "fas fa-stop video-not-playing";
            list_elem.className = "video-not-playing";
        }

    }
};

function repeatProcess (){
    if (repeatFlg){
        currentTime = player.currentTime();
        if (currentTime >= Number(chapters[repeatID].end_time) - 0.2){ // adjust the repeat frame
            player.currentTime(Number(chapters[repeatID].start_time));
            player.play();
        }
    }
    changeSetListState();
}

player.on("timeupdate", repeatProcess);
// let timer = setInterval(repeatProcess, 200); // 0.2s
// clearInterval(timer);
