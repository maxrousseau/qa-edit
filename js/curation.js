// @DONE
// load next/previous (check boundaries before) Ok
// save a modified sample Ok
// add new sample Ok
// export function Ok
// edit name Ok

// @TODO
// delete function

// @NOTE :: this works! I could simply use this to perform any necessary updates of the data. Im
// trying to understand if HTML forms would be preferable for this purpose or no...
function sendPost() {
    var url = "http://127.0.0.1:8000/post-curate/";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }};

    const loc = parseInt(document.getElementById('index').textContent.trim());
    const qid = parseInt(document.getElementById('qid').textContent.trim());
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const context = document.getElementById('context').value;
    const topic = document.getElementById('topic').value;


    xhr.send(JSON.stringify({"loc": loc,
                             "qid": qid,
                             "question": question,
                             "answer": answer,
                             "context": context,
                             "topic" : topic}));
    // @TODO :: @BUG :: if there is an invalid field the post request fails to
    // save the changes, therefore we should wait to have a 200 response from
    // the post before moving on? xhr.status
    //  https://stackoverflow.com/questions/3760319/how-to-force-a-program-to-wait-until-an-http-request-is-finished-in-javascript
}

function next() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/curate/";
    var loc = parseInt(document.getElementById('index').textContent.trim());
    var min = 0;
    var max = parseInt(document.getElementById('limit').textContent.trim());
    console.log(loc);
    loc += 1;//@BUG check if out of bound...
    if (loc <= max) {
        loc = loc.toString();
        url = url + loc;
        window.location.href = url;
    }
}

function prev() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/curate/";
    var loc = parseInt(document.getElementById('index').textContent.trim());
    console.log(loc);
    if (loc > 0) {
        loc -= 1;//@BUG check if out of bound...
        loc = loc.toString();
        url = url + loc;
        window.location.href = url;
    }
}

function goto() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/curate/"
    var loc = document.getElementById('qid_select').value.toString();
    var max = parseInt(document.getElementById('limit').textContent.trim());

    if (loc >= 0 && loc <= max) {
        url = url + loc;
        window.location.href = url;
    }
}

function add() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/new-curate/";
    var curate_url = "http://127.0.0.1:8000/curate/";
    var xhr = new XMLHttpRequest();
    var loc = parseInt(document.getElementById('index').textContent.trim());
    var max = parseInt(document.getElementById('limit').textContent.trim());
    var new_loc = max + 1

    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }};

    xhr.send(JSON.stringify({"loc": loc}));
    window.location.href = curate_url + new_loc;

}

function exportDataset() {
    sendPost(); // save current question in-memory before exporting
    fetch("http://127.0.0.1:8000/export-curate/");
}

function rename() {
    var current_name = document.getElementById('dataset-name').textContent;
    let new_name = prompt("Change dataset name", current_name);

    if (new_name != null) {
        fetch("http://127.0.0.1:8000/rename/"+new_name);
        document.getElementById("dataset-name").innerHTML = new_name;
  }
}
