var rec;
var soundStream;
var audioFile

document.getElementById("startRecord").disabled = false;
document.getElementById("stopRecord").disabled = true;
document.getElementById("submitRecord").disabled = true;

function startRecording() {
  document.getElementById("startRecord").disabled = true;
  document.getElementById("stopRecord").disabled = false;
  document.getElementById("recordedAudio").controls = false;
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(stream => {
    const aCtx = new AudioContext();
    const streamSource = aCtx.createMediaStreamSource(stream);
    rec = new Recorder(streamSource);
    rec.record();
    soundStream = stream;
  });
}

function stopRecording() {
  document.getElementById("startRecord").disabled = true;
  document.getElementById("stopRecord").disabled = true;
  document.getElementById("submitRecord").disabled = false;
  soundStream.getTracks().forEach(t => t.stop());
  rec.stop()
  rec.exportWAV((blob) => {
    const url = URL.createObjectURL(blob);
    let au = new Audio(url);
    au.controls = true;
    document.body.appendChild(au);
    au.play();
    let a = document.createElement('a');
    a.href = url;
    a.innerHTML = 'download';
    a.download = 'song.wav';
    document.body.appendChild(a);
    audioFile = blob;
  });
}

function submit() {
  var fd = new FormData();
  fd.append('file', audioFile, 'audio.wav');
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/sheet');
  xhr.send(fd)
  /*$.ajax({
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
  */
}