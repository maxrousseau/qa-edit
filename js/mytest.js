// @NOTE :: this works! I could simply use this to perform any necessary updates of the data. Im
// trying to understand if HTML forms would be preferable for this purpose or no...
function sendPost() {
    var url = "http://127.0.0.1:8000/posting/"
    // here just get the context, context_id, question, answer, label and topic
    var x = document.getElementById("context").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }};

    const qid = parseInt(document.getElementById('qid').textContent.trim());
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const context = document.getElementById('context').value;
    const context_id = parseInt(document.getElementById('context_id').value);
    const label = document.getElementById('label').value;
    const topic = document.getElementById('topic').value;


    xhr.send(JSON.stringify({"qid": qid,
                             "question": question,
                             "answer": answer,
                             "context": context,
                             "context_id": context_id,
                             "label": label,
                             "topic" : topic}));
    // @TODO :: @BUG :: if there is an invalid field the post request fails to
    // save the changes, therefore we should wait to have a 200 response from
    // the post before moving on? xhr.status
    //  https://stackoverflow.com/questions/3760319/how-to-force-a-program-to-wait-until-an-http-request-is-finished-in-javascript
}


function next() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/sample/"
    var qid = parseInt(document.getElementById('qid').textContent.trim());
    qid += 1;//@BUG check if out of bound...
    qid = qid.toString();
    url = url + qid
    window.location.href = url
}

function prev() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/sample/"
    var qid = parseInt(document.getElementById('qid').textContent.trim());
    qid -= 1; //@BUG check if out of bound...
    qid = qid.toString();
    url = url + qid
    window.location.href = url
}

function goto() {
    sendPost(); // save current question before leaving
    var url = "http://127.0.0.1:8000/sample/"
    var qid = document.getElementById('qid_select').value.toString();
    url = url + qid
    window.location.href = url
}

function callAdd(){

    var url = "http://127.0.0.1:8000/new/"
    // here just get the context, context_id, question, answer, label and topic
    var x = document.getElementById("context").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }};

    const qid = parseInt(document.getElementById('qid').textContent.trim());
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const context = document.getElementById('context').value;
    const context_id = parseInt(document.getElementById('context_id').value);
    const label = document.getElementById('label').value;
    const topic = document.getElementById('topic').value;

    xhr.send(JSON.stringify({"qid": qid,
                             "question": question,
                             "answer": answer,
                             "context": context,
                             "context_id": context_id,
                             "label": label,
                             "topic" : topic}));
    // @TODO :: @BUG :: if there is an invalid field the post request fails to
    // save the changes, therefore we should wait to have a 200 response from
    // the post before moving on? xhr.status
    //  https://stackoverflow.com/questions/3760319/how-to-force-a-program-to-wait-until-an-http-request-is-finished-in-javascript

    const new_id = xhr.response
    var url = "http://127.0.0.1:8000/sample/"
    url = url + new_id
    window.location.href = url

}

function callSave(){
    var url = "http://127.0.0.1:8000/serialize/"
    // here just get the context, context_id, question, answer, label and topic
    var x = document.getElementById("context").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }};

    const qid = parseInt(document.getElementById('qid').textContent.trim());
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const context = document.getElementById('context').value;
    const context_id = parseInt(document.getElementById('context_id').value);
    const label = document.getElementById('label').value;
    const topic = document.getElementById('topic').value;

    xhr.send(JSON.stringify({"qid": qid,
                             "question": question,
                             "answer": answer,
                             "context": context,
                             "context_id": context_id,
                             "label": label,
                             "topic" : topic}));
}


function callExport(){
    var url = "http://127.0.0.1:8000/export/"
    // here just get the context, context_id, question, answer, label and topic
    var x = document.getElementById("context").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }};

    const qid = parseInt(document.getElementById('qid').textContent.trim());
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const context = document.getElementById('context').value;
    const context_id = parseInt(document.getElementById('context_id').value);
    const label = document.getElementById('label').value;
    const topic = document.getElementById('topic').value;

    xhr.send(JSON.stringify({"qid": qid,
                             "question": question,
                             "answer": answer,
                             "context": context,
                             "context_id": context_id,
                             "label": label,
                             "topic" : topic}));
}

function callUpdateName() {}

function promptEditName() {}
