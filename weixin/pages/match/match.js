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
        this.setData({
            uuid: options.uuid,
            cate: options.cate,
            pg: 0
        });
        var self = this;
        wx.request({
            url: app.globalData.url + '/match/',
            method: "GET",
            header: {
                'Content-Type': 'application/json'
            },
            data: {
                cate: options.cate,
                uuid: options.uuid
            },
            success: function(res) {
                //console.log(res);
                self.setData({
                    data: res.data
                });
            }
        })
    },
    chooseImage: function() {
        var self = this;
        wx.chooseImage({
            count: 1,
            sizeType: ['original', 'compressed'],
            sourceType: ['album', 'camera'],
            success: function(res) {
                //console.log(res);
                wx.showLoading({
                    title: '正在上传识别',
                });
                //图片临时地址
                var img_src = res.tempFilePaths[0];
                //定义上传和进度条
                const upload_task = wx.uploadFile({
                    url: app.globalData.url + '/match/',
                    filePath: img_src,
                    name: 'img',
                    formData: {
                        cate: self.options.cate
                    },
                    success: function(res) {
                        //console.log(res);
                        wx.showToast({
                            title: '上传识别成功',
                            icon: 'success',
                            duration: 1500
                        });
                        self.setData({
                            img_src
                        });
                        //跳转到识别结果的页面
                        var data = JSON.parse(res.data);
                        var url = "match?cate=" + data.cate + "&uuid=" + data.uuid;
                        setTimeout(function() {
                            wx.redirectTo({
                                url: url,
                            })
                        });
                    }
                });
                //定义进度条
                upload_task.onProgressUpdate((res) => {
                    self.setData({
                        pg: res.progress
                    });
                });
            },
        });
    }


})