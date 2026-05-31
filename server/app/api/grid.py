# -*- coding: utf-8 -*-
from fastapi import APIRouter
from app.common.utils import CommonUtils

router = APIRouter()


@router.get('/grid/')
async def grid():
    """快捷导航菜单"""
    site_url = CommonUtils.site_url
    grid_data = {
        'style': 'width:50%;',
        'logo': site_url + '/static/images/bg.png',
        'name': '快捷导航',
        'data': [
            {
                'name': '人脸检测',
                'image': site_url + '/static/images/g1-1.png',
                'url': '/pages/match/match?cate=1&uuid='
            },
            {
                'name': '人脸勾勒',
                'image': site_url + '/static/images/g1-2.png',
                'url': '/pages/match/match?cate=2&uuid='
            },
            {
                'name': '人脸截取',
                'image': site_url + '/static/images/g1-3.png',
                'url': '/pages/match/match?cate=3&uuid='
            },
            {
                'name': '人脸化妆',
                'image': site_url + '/static/images/g1-4.png',
                'url': '/pages/match/match?cate=4&uuid='
            },
            {
                'name': '人脸特征',
                'image': site_url + '/static/images/g1-5.png',
                'url': '/pages/match/match?cate=5&uuid='
            },
            {
                'name': '关于作者',
                'image': site_url + '/static/images/g1-6.png',
                'url': '/pages/about/about'
            }
        ]
    }
    return grid_data
