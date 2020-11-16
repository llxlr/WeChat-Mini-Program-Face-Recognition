/*
* url：请求的地址
* fields：提交的字段
* redirect_url：跳转的地址
* jquery语法
* */

function request(url, fields, redirect_url) {
    $("#btn-sub").click(function () {
        //对表单数据序列化
        var data = $("#form-data").serialize();
        //执行异步ajax请求
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: data,
            success: function (res) {
                //console.log(res);
                if (res.code == 1) {
                    //成功跳转
                    location.href = redirect_url;
                } else {
                    //失败错误信息展示
                    var error = res.data;
                    for (var index in fields) {
                        var key = fields[index];
                        if (typeof error[key] === 'undefined') {
                            $("#error_" + key).empty();
                        } else {
                            $("#error_" + key).empty();
                            $("#error_" + key).append(
                                error[key]
                            );
                        }
                    }
                }
            }
        })
    });
}
