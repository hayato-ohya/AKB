// Read JSON file
function readTextFile(file)
{
    let rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                let allText = rawFile.responseText;
                alert(allText);
            }
        }
    };
    rawFile.send(null);
}
