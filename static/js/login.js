
function login() {
    var number = $('#stdNumber');
    var password = $('#stdPassword');
    var btn = $('#loginbtn');
    var loading = $("#loading");
    var loading_icon = $('#loading_icon');
    var result = $('#result');
    number.parent('.mdui-textfield').removeClass('error');
    password.parent('.mdui-textfield').removeClass('error');
    if(number.val()==''){
        number.parent('.mdui-textfield').addClass('error');
        return;
    }
    if(password.val()==''){
        password.parent('.mdui-textfield').addClass('error');
        return;
    }
    var form = new FormData(document.getElementById('loginform'));
    btn.hide();
    loading.show();
    $.post(
        {
            url:'',
            data:form,
            dataType:'json',
            processData:false,
            contentType:false,
            success:function (data) {
                if(data.status=='200'){
                    window.setInterval(function () {
                        loading_icon.hide();
                        window.location.href='/'
                    },1000)
                }else{
                    window.setInterval(function () {
                        loading.hide();
                        btn.show();
                        password.parent('.mdui-textfield').addClass('error');
                    },1000)
                }
            },
            error:function (data) {
                window.setInterval(function () {
                        loading.hide();
                        btn.show();
                    },1000)
                alert('请求发生错误，请联系管理员')
            }
        }
    )
}