
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

// 绑定缩略图的点击事件，用于更换背景
document.addEventListener('DOMContentLoaded', () => {
  var modalBody = document.querySelector('.modal-body');
  modalBody.addEventListener('click', (event) => {
    var target = event.target;
    if (target.classList.contains('background-thumbnail')) {
      var fullImagePath = target.getAttribute('data-full-image');
      document.getElementById('background').style.backgroundImage = `url('${fullImagePath}')`;
      $('#backgroundModal').modal('hide');
    }
  });
});


document.addEventListener('DOMContentLoaded', (event) => {
  var fontcolor = document.getElementById('fontcolor');
  if(fontcolor) { // 确保元素存在
      fontcolor.addEventListener('click', changeTextColor);
  }
});

function changeTextColor() {
    console.log("改变文本颜色");
    // 创建一个随机颜色值
    var randomColor = '#' + Math.floor(Math.random()*16777215).toString(16);
    // 改变文本颜色
    document.body.style.color = randomColor;

}