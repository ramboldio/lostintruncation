//INTERPRETATION OF QUESTIONS ARE BEING STORED AND SENT TO THE CHIP

//HTW IP Adressen
//var ipImage = 'http://192.168.50.201:5000/submit';
//var ipText = 'http://192.168.50.201:5000/submit_text';

var ipImage = '/submit';
var ipText = '/submit_text';

var showing = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var slides = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'];

function next() {
    var qElems = [];
    for (var i = 0; i < slides.length; i++) {
        qElems.push(document.getElementById(slides[i]));   
    }
    for (var i = 0; i < showing.length; i++) {
        if (showing[i] == 1) {
            qElems[i].style.display = 'none';
            showing[i] = 0;
            if (i == showing.length - 1) {
                qElems[0].style.display = 'block';
                showing[0] = 1;
            } else {
                qElems[i + 1].style.display = 'block';
                showing[i + 1] = 1;
            }
            break;
        }
    }      
}

//WAIT A BIT AFTER GOING FROM PHOTO TO QUESTIONS
function timeFunction() {
	setTimeout(function() { next(); }, 3000);
}

//from information "takes a few seconds" to "your data will be safe with us"
function timeFunction2() {
	setTimeout(function() { next(); }, 480000);
}

//reload
function timeFunction3() {
	setTimeout(function() { location.reload(); }, 580000);
}

function showloading() {
	document.getElementById("ring").classList.add('show-ring');
	document.getElementById("ring").classList.remove('hide');
}

function hideTemplate() {
	document.getElementById("template").classList.add('hide');
}


//STORE TEXT IN VARIABLE
function storeVar(el) {
	var value = el.getAttribute('value'); 
	console.log(value);

	const formData = new FormData();
	formData.append('text', value);

	fetch(ipText, { 
		method: 'POST',
		body: formData
	}).then(
		success => console.log(success)
	).catch(
		error => console.log(error) 
	);	
}

//WEBCAM TURNS ON + SNAPSHOT IS BEING SENT TO CHIP

const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('canvas');
const snapSoundElement = document.getElementById('snapSound');
const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);

webcam.start()
	.then(() => {
		console.log("webcam started");
	})
	.catch(err => {
		console.log(err);
	});

//document.querySelector('#download-photo').href = picture;
//console.log(picture);

webcam.stop();

// Select your input type file and store it in a variable
const input = document.getElementById('fileinput');

// This will upload the file after having read it
function upload() {
	canvasElement.toBlob(function (blob) {
		const imgFile = new File([blob], 'test.png', {
			type: 'image/png'
		});
		const formData = new FormData();
		formData.append('file', imgFile);

		fetch(ipImage, { // Your POST endpoint 
			method: 'POST',
			body: formData
		}).then(
			response => response.json() // if the response is a JSON object
		).then(
			success => console.log(success) // Handle the success response object
		).catch(
			error => console.log(error) // Handle the error response object
		);
	});
}

// Event handler executed when a file is selected
const onSelectFile = () => upload(input.files[0]);

// Add a listener on your input
// It will be triggered when a file will be selected
//input.addEventListener('change', onSelectFile, false);

