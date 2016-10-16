// Converts canvas to an image
// Specifically PNG base64
function convertCanvasToImage(canvas) {
  return canvas.toDataURL("image/png");
}

// Attempts to get the back camera if possible, otherwise the most ideal camera
function loadCamera() {
  var sources = [];
  function gotSources(sourceInfos) {
    sources = sourceInfos.filter((s) => s.kind === "video");
    var desiredSource;
    if (sources.length === 1) {
      desiredSource = sources[0];
    } else {
      var backCams = sources.filter((s) => s.label.includes("back"));
      if (backCams.length > 0) {
        desiredSource = backCams[0];
      }
      else {
        desiredSource = sources[0];
      }
    }
    startCamera(desiredSource);
  }

  if (typeof MediaStreamTrack === 'undefined' ||
      typeof MediaStreamTrack.getSources === 'undefined') {
    alert('This browser does not support MediaStreamTrack.\n\nTry Chrome.');
  } else {
    MediaStreamTrack.getSources(gotSources);
  }
}

function startCamera(source) {
  // Grab elements, create settings, etc.
  var video = document.getElementById('video');

  // Get access to the camera!
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    var videoSource = source.id;
    navigator.mediaDevices.getUserMedia({ video: {optional: [{sourceId: videoSource}]} }).then(function(stream) {
      video.src = window.URL.createObjectURL(stream);
      video.play();
    });
  }

  /* Legacy code below: getUserMedia
  else if(navigator.getUserMedia) { // Standard
      navigator.getUserMedia({ video: true }, function(stream) {
          video.src = stream;
          video.play();
      }, errBack);
  } else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
      navigator.webkitGetUserMedia({ video: true }, function(stream){
          video.src = window.webkitURL.createObjectURL(stream);
          video.play();
      }, errBack);
  } else if(navigator.mozGetUserMedia) { // Mozilla-prefixed
      navigator.mozGetUserMedia({ video: true }, function(stream){
          video.src = window.URL.createObjectURL(stream);
          video.play();
      }, errBack);
  }
  */

    // Elements for taking the snapshot
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var video = document.getElementById('video');

   // Trigger photo take
  document.getElementById("snap").addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480);
  });
}


$(function() {
  $(".hero-cta_button").on('click', function() {
    window.location.href = '/login';
  });
  // $(".hero-cta_button").on('click', function() {
  //   if (screenfull.enabled) {
  //     screenfull.request();
  //   } else {
  //     // Ignore or do something else
  //   }
  //
  //   setTimeout(function() {
  //     $(".hero").children(":not(.hero-cta)").addClass("transitioning");
  //
  //     $(".hero-cta_button").addClass("moving");
  //     setTimeout(function() {
  //       $(".hero-cta_button").addClass("moving_done");
  //       setTimeout(function() {
  //
  //         $(".hero-cta_button").addClass("button_transitioned");
  //         $(".hero").children(":not(.hero-cta)").remove();
  //         $(".SignupContent").removeClass("hidden");
  //         setTimeout(function() {
  //           $(".SignupContent").removeClass("transitioning");
  //           loadCamera();
  //         });
  //       }, 1);
  //     }, 1000);
  //   }, 100);
  // });
});
