const app = getApp();

Page({

    /**
     * 页面的初始数据
     */
    data: {

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
        //获取用户信息
        //自动跳转
        var that = this;
        wx.getSetting({
            success: res => {
                if (res.authSetting['scope.userInfo']) {
                    // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
                    wx.getUserInfo({
                        lang: 'zh_CN',
                        success: res => {
                            that.setUserInfoAndNext(res.userInfo)
                        }
                    })
                }
            }
        })
    },

    bindGetUserInfo: function(e) {
        //console.log(e);
        if (e.detail.userInfo) {
            //用户按了允许的按钮
            var that = this;
            that.setUserInfoAndNext(e.detail.userInfo);
        } else {
            //用户按了拒绝的按钮
            wx.showModal({
                title: '警告',
                content: '您点击了拒绝授权，将无法进入小程序，请授权之后再进入！',
                showCancel: false,
                confirmText: '返回授权',
                success: function(res) {
                    if (res.confirm) {
                        console.log("用户点击了“返回授权”")
                    }
                }
            })
        }
    },
    setUserInfoAndNext: function(user_info) {
        wx.showLoading({
            title: '登录授权跳转！',
        });
        //请求服务器，把授权用户信息提交到服务端
        //头像，城市，国家，性别，语言，昵称，省份
        wx.request({
            url: app.globalData.url + '/user/',
            data: {
                avatarUrl: user_info.avatarUrl,
                city: user_info.city,
                country: user_info.country,
                gender: user_info.gender,
                language: user_info.language,
                nickName: user_info.nickName,
                province: user_info.province
            },
            method: 'POST',
            header: {
                'content-type': 'application/json'
            },
            success: function(res) {
                console.log(res);
                if (res.data.code == 1) {
                    //跳转到快捷导航
                    setTimeout(() => {
                        wx.reLaunch({
                            url: '../vision/vision',
                        })
                    }, 1000);
                }
            }
        });
    }
})