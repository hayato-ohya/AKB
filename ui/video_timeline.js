// DOM element where the Timeline will be attached
let container = document.getElementById("video-timeline");

// Create a DataSet (allows two way data-binding)
let items = new vis.DataSet([
    { id: 1, content: "item 1",
        start: new Date(2000, 1, 1, 1, 0, 0, 1),
    end: new Date(2000, 1, 1, 1, 10, 1, 0)},
    { id: 2, content: "item 2",
        start: new Date(2000, 1, 1, 1, 15, 0, 1),
        end: new Date(2000, 1, 1, 1, 20, 1, 0)},
]);

// Configuration for the Timeline
let options = {
    align: "center",
    editable: true,
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
};

// Create a Timeline
let timeline = new vis.Timeline(container, items, options);
