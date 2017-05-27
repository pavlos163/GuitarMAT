navigator.mediaDevices.getUserMedia({audio:true})
  .then(stream => {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
      audio.push(e.data);
      if (rec.state == "inactive"){
        let blob = new Blob(audio,{type:'audio/x-mpeg-3'});
        recordedAudio.src = URL.createObjectURL(blob);
        recordedAudio.controls = true;
        audioDownload.href = recordedAudio.src;
        audioDownload.download = 'audio.mp3';
        audioDownload.innerHTML = 'Download';
        // submit(blob);
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
  /*
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
  */
}

// TODO: This needs work. Submit button currently does not do anything.
// Also, page does not get reloaded and therefore the results are not shown.
// The POST request has to be done without AJAX.

/*
function submit(blob) {
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
*/