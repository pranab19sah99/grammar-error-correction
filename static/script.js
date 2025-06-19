// Main function that sends data to our flask backend
// It is a post message with one line of text as contetn
function sendData(inputValue) {
    fetch('/process_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ value: inputValue })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('outtxt').value += (data.message + "\n");
    })
    .catch(error => console.error('Error:', error));
}

// This function just takes content from textarea on UI
// Sends the data using above funciton to backend
function checkText() {
    const inputValue = document.getElementById('txt').value;
    sendData(inputValue);
}

// This function will open a dialog for the user to get a filename
// then open it and then read line by line and feed it the backend
function checkFile() {
    var input = document.createElement('input');
    input.type = 'file';

    input.onchange = e => { 
        var file = e.target.files[0]; // Pick file

        var reader = new FileReader();
        reader.readAsText(file,'UTF-8');

        reader.onload = readerEvent => {
            var content = readerEvent.target.result; // Extract content
            lines = content.split(/\r?\n/); // this regex for end of line split

            // Now we have individual lines that can be fed to the backend flask
            for (const line of lines) {
                console.log(line); // this was just for debug
                sendData(line); // send to backend
            }
        }
    }

    input.click();
}
