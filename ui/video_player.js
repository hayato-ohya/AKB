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
let i, ul, li, a, chapterTitle;
ul = document.getElementById("ul-set-list");
for (i=0; i<chapters.length; i++){
    a = document.createElement("a");
    a.href = "javascript:void(0);";
    // a.onclick = "chapterClick();";
    li = document.createElement("li");
    li.id = chapters[i].id.toString();
    chapterTitle = document.createTextNode(chapters[i].title);

    a.append(chapterTitle);
    li.append(a);
    ul.append(li);
}

function chapterClick() {
    let target = document.getElementById("test");
    target.innerHTML = "hoge!";
}
