// DOM element where the Timeline will be attached
let container = document.getElementById("video-timeline");
let customDate = new Date();

// Create a DataSet (allows two way data-binding)
let items = new vis.DataSet();

// Configuration for the Timeline
let options = {
    align: "center",
    format: {
        minorLabels: {},
        majorLabels: {
            millisecond:'HH:mm:ss',
            second:     'HH:mm:ss',
            minute:     'HH:mm:ss',
            hour:       'HH:mm:ss'
        }
    },
    stack: false,
    min: new Date(2000, 1, 1, 0, 0, 0, 0),
    max: new Date(2000, 1, 1, 23, 59, 59, 0),
    zoomMin: 10000,
    zoomFriction: 30,
};

function convertTime2Date(inputTime) {
    inputTime = Number(inputTime);
    let h = Math.floor(inputTime / 3600);
    let m = Math.floor((inputTime - 3600 * h) / 60);
    let s = Math.floor(((inputTime - 3600 * h) - 60 * m));
    let ms = Number((inputTime - Math.floor(inputTime)).toFixed(3) * 1000);
    let d = new Date(2000, 1, 1, 0, 0, 0, 0);
    d.setHours(d.getHours() + h);
    d.setMinutes(d.getMinutes() + m);
    d.setSeconds(d.getSeconds() + s);
    d.setMilliseconds(d.getMilliseconds() + ms);
    return d;
}

function convertDate2Time(inputDate) {
    if (Object.prototype.toString.call(inputDate) == "[object Date]"){
        let h = inputDate.getHours();
        let m = inputDate.getMinutes();
        let s = inputDate.getSeconds();
        let ms = inputDate.getMilliseconds();
        let ret = (h * 3600) + (m * 60) + s + (ms / 1000);
        return ret;
    } else {
        return -1;
    }
}

options.max = convertTime2Date(Number(chapters[chapters.length -1].end_time));  // End of the video

// Create a Timeline
let timeline = new vis.Timeline(container, items, options);

let marker_id = 0;
for (let i=0; i<chapters.length; i++){
    marker_id = i;
    timeline.addCustomTime(convertTime2Date(chapters[i].start_time), marker_id);
    timeline.setCustomTimeMarker(chapters[i].title, marker_id, true);
}

timeline.on("doubleClick",
    function (properties) {
        let eventProps = timeline.getEventProperties(properties.event);
        if(eventProps.what === "custom-time"){
            timeline.removeCustomTime(eventProps.customTime);
        } else {
            marker_id = marker_id + 1;
            timeline.addCustomTime(eventProps.time, marker_id);
            timeline.setCustomTimeMarker("New Chapter", marker_id, true);
        }
    });


// Playerとcustom barの連携
player.on("timeupdate", hoge);
function hoge() {
    console.log("player.currentTime()", player.currentTime());
}