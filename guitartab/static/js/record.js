navigator.mediaDevices.getUserMedia({audio:true})
  .then(stream => {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
      audio.push(e.data);
      if (rec.state == "inactive"){
        let blob = new Blob(audio,{type:'audio/x-mpeg-3'});
        recordedAudio.src = URL.createObjectURL(blob);
        recordedAudio.controls = true;
        submit(blob);
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

function submit(blob) {
  /*
  var http = new XMLHttpRequest();
  var url = "/";
  http.open("POST", url, true);

  console.log("FormData:");
  console.log(blob);
  var formData = new FormData();
  formData.append('file', blob);

  http.setRequestHeader("Content-Type", "multipart/form-data");
  http.send(formData);
  */
  var fd = new FormData();
  fd.append('file', blob, 'audio.mp3');
  $.ajax({
      type: 'POST',
      url: '/',
      data: fd,
      cache: false,
      processData: false,
      contentType: false,
      enctype: 'multipart/form-data'
  }).done(function(data) {
         console.log(data);
  });
}