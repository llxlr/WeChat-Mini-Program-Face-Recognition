const app = getApp();

Page({

    /**
     * 页面的初始数据
     */
    data: {
        grids: null
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
        var self = this;
        wx.request({
            url: app.globalData.url + '/grid/',
            header: {
                'content-type': 'application/json'
            },
            method: 'GET',
            success: function(res) {
                //console.log(res);
                self.setData({
                    grids: res.data
                })
            }
        })
    },
})