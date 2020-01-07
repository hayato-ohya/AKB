// DOM element where the Timeline will be attached
let container = document.getElementById("video-timeline");

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
    showCurrentTime: true,
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

// Load JSON data and set marker
let markers = [];
let marker_id = 0;
for (let i=0; i<chapters.length; i++){
    marker_id = i;
    timeline.addCustomTime(convertTime2Date(chapters[i].start_time), marker_id);
    timeline.setCustomTimeMarker(chapters[i].title, marker_id, true);
    markers.push({id: marker_id, time: convertTime2Date(chapters[i].start_time), title: chapters[i].title});
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


// Associate Player with custom bar
let timer;
player.on("timeupdate", moveCurrentBar);
function moveCurrentBar() {
    clearInterval(timer);
    timeline.setCurrentTime(convertTime2Date(player.currentTime()));
}
player.on("pause", stopCurrentBar);
function stopCurrentBar() {
    timer = setInterval(setIntervalWrapper, 10);
    console.log("Stop", player.currentTime());
}
function setIntervalWrapper() {
    timeline.setCurrentTime(convertTime2Date(player.currentTime()));
}

// Add the flag at the current time
function setCustomTime() {
    marker_id = marker_id + 1;
    timeline.addCustomTime(convertTime2Date(player.currentTime()), marker_id);
    timeline.setCustomTimeMarker("New Chapter", marker_id, true);
}

// Undo Redo
let commands = [];
let commandIdx = 0;
let groupCommand = null;

function recordCommand(name, params, funcDo, funcUndo) {
    // Add new command
    let newCommand = {"Name":name, "Params": params, "Do": funcDo, "Undo": funcUndo, };
    if (groupCommand) {
        groupCommand.commands.push(newCommand);
    } else {
        // Delete the last command
        if (commandIdx < commands.length){
            commands.splice(commandIdx, commands.length - commandIdx);
        }
        commands.push(newCommand);
        commandIdx++;
    }
    newCommand.Do();
}
function startGroupRecording(name) {
    groupCommand = {"name":name, "commands":[]};
}
function finishGroupRecording() {
    let name = groupCommand.name;
    let params = {"commands": groupCommand.commands};
    groupCommand = null;

    if (params.length <= 0){
        return;
    }
    recordCommand(
        name,
        params,
        function () {
            for (let i=0; i<this.Params.commands.length; i++){
                this.Params.commands[i].Do();
            }
        },
        function () {
            for (let i=0; i<this.Params.commands.length; i++){
                this.Params.commands[i].Undo();
            }
        }
    );
}

document.getElementById("button-undo").onclick = function () {
    if (commandIdx <= 0){
        return;
    }
    commandIdx--;
    commands[commandIdx].Undo();
};
document.getElementById("button-redo").onclick = function () {
    if (commands.length <= commandIdx){
        return;
    }
    commands[commandIdx].Do();
    commandIdx++;
};

timeline.on("timechanged", function (properties) {
    let prevTime = null;
    let i;
    for (i=0; i<markers.length; i++){
        if (markers[i].id == properties.id){
            prevTime = markers[i].time;
            break;
        }
    }

    recordCommand("Move",
        {id: properties.id, previousTime: prevTime, updateTime: properties.time},
        function (){
            timeline.setCustomTime(this.Params.updateTime, this.Params.id);
        },
        function (){
            timeline.setCustomTime(this.Params.previousTime, this.Params.id);
        });

    markers[i].time = properties.time;
});

timeline.on("markerchanged", function (properties) {
    let prevTitle = null;
    let i;
    for (i=0; i<markers.length; i++){
        if (markers[i].id == properties.id){
            prevTitle = markers[i].title;
            break;
        }
    }
    let tmpTitle = properties.title.replace("<br>", "");

    recordCommand("TitleChange",
        {id: properties.id, previousTitle: prevTitle, updateTitle: tmpTitle},
        function () {
            timeline.setCustomTimeMarker(this.Params.updateTitle, this.Params.id, true);
        },
        function () {
            timeline.setCustomTimeMarker(this.Params.previousTitle, this.Params.id, true);
        });

    markers[i].title = tmpTitle;
});

// データ書き出し