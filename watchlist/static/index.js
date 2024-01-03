
document.addEventListener('DOMContentLoaded', function() {
    var player = document.getElementById("player")
    var music = document.getElementById("music");
    player.addEventListener('click', function() {

        if(music.paused){
            music.play();
        }else{
            music.pause();
        }

    });
  });

