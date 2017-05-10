navigator.mediaDevices.getUserMedia({audio:true})
  .then(stream => {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
      audio.push(e.data);
      if (rec.state == "inactive"){
        let blob = new Blob(audio,{type:'audio/x-mpeg-3'});
        recordedAudio.src = URL.createObjectURL(blob);
        recordedAudio.controls = true;
     }
    }
  })
  .catch(e=>console.log(e));

function startRecording() {
  startRecord.disabled = true;
  stopRecord.disabled = false;
  audio = [];
  recordedAudio.controls = false;
  rec.start();
}

function stopRecording() {
  startRecord.disabled = false;
  stopRecord.disabled = true;
  rec.stop();

  if (document.getElementById('submitDiv') != null) {
    return;
  }

  var submitBtn = document.createElement("input");
  submitBtn.id = "submitBtn";
  submitBtn.type = "button";
  submitBtn.value = "Submit"
  submitBtn.onclick = submit;

  var submitDiv = document.createElement("div");
  submitDiv.id = "submitDiv";
  submitDiv.appendChild(submitBtn);

  // TODO: Maybe reset button?

  document.getElementById('audio').appendChild(submitDiv);
}

function submit() {
  var http = new XMLHttpRequest();
  var url = "";
  var params = "src=" + recordedAudio.src;
  http.open("POST", url, true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.send(params);
}

function resetRecord() {
  recordedAudio = null;
  startRecord.disabled = false;
  stopRecord.disabled = true;
  resetRecord.disabled = true;
}