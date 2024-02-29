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
  