$('#summernote').summernote({
    placeholder: 'Hello stand alone ui',
    tabsize: 2,
    height: 120,
    tooltip: true,
    toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'underline', 'clear']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video']],
        ['view', ['fullscreen', 'codeview', 'help']]
    ],
    colorButton: {
        foreColor: 'red',
        backColor: 'transparent'
    }
    });

var review = document.getElementById('submit_review');
var submit = document.getElementById('submit')

review.addEventListener('click', function() {
    // 获取Summernote编辑器中的内容
    var contentWithTags = $('#summernote').summernote('code');

    // 创建一个临时元素，用于提取纯文本内容
    var tempElement = document.createElement('div');
    tempElement.innerHTML = contentWithTags;

    // 使用innerText或textContent属性获取纯文本内容
    var pureTextContent = tempElement.innerText || tempElement.textContent;

    // 现在pureTextContent中包含了没有HTML标签的纯文本内容
    var feeling= document.getElementById('review');
    var content = document.getElementById('content');
    if(content){
        $("#content").val(pureTextContent);
    }
    if(feeling){
        $("#review").val(pureTextContent);
    
    }
});

