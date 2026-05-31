# -*- coding: utf-8 -*-
import os
import datetime
import uuid

from fastapi import APIRouter, Request, UploadFile, File, Form, Query
from app import get_db
from app.common.utils import CommonUtils
from app.common.face import Face
from bson.objectid import ObjectId

router = APIRouter()


def make_upload_dir():
    """创建上传目录"""
    upload_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'static', 'uploads'
    )
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)
    return upload_path


def image_name():
    """生成图片名称"""
    prefix1 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    prefix2 = uuid.uuid4().hex
    return prefix1 + prefix2


def save_image(upload_path, file_content, filename, site_url):
    """保存图片并返回HTTP路径"""
    newname = image_name() + os.path.splitext(filename)[-1]
    img_path = os.path.join(upload_path, newname)
    with open(img_path, 'wb') as f:
        f.write(file_content)
    return newname, site_url + '/static/uploads/{}'.format(newname)


@router.post('/match/')
async def match_post(
    request: Request,
    img: UploadFile = File(...),
    cate: int = Form(...),
):
    """人脸识别上传"""
    res = {'code': 0}
    upload_path = make_upload_dir()
    site_url = CommonUtils.site_url

    # 读取上传文件
    file_content = await img.read()
    imgs_name, imgs_http = save_image(upload_path, file_content, img.filename, site_url)

    # 人脸识别
    fm = Face(upload_path, imgs_name, upload_path)
    known_image = None

    if cate == 1:
        known_image = fm.face_box()
        name = '人脸检测'
    elif cate == 2:
        known_image = fm.face_sense()
        name = '人脸勾勒'
    elif cate == 3:
        known_image = fm.face_find()
        name = '人脸截取'
    elif cate == 4:
        known_image = fm.face_makeup()
        name = '人脸化妆'
    elif cate == 5:
        known_image = fm.face_68_point()
        name = '人脸特征'

    # 保存记录到数据库
    db = get_db()
    record = db.image.insert_one(dict(
        unknown_image=[imgs_http],
        known_image=list(map(
            lambda v: site_url + '/static/uploads/{}'.format(v),
            known_image
        )),
        name=name,
        cate=cate,
        status=0,
        **CommonUtils.common_params(request.client.host, request.headers)
    ))

    last_id = record.inserted_id
    if last_id:
        res = {'code': 1, 'cate': cate, 'uuid': str(last_id)}

    return res


@router.get('/match/')
async def match_get(
    uuid: str = Query(None),
    cate: int = Query(1),
):
    """查询识别结果或示例"""
    site_url = CommonUtils.site_url

    if uuid:
        # 根据uuid查询记录
        db = get_db()
        record = db.image.find_one({'_id': ObjectId(uuid)})
        if record:
            return {
                'name': record['name'],
                'cate': record['cate'],
                'unknown_image': record['unknown_image'],
                'known_image': record['known_image'],
            }
        return {'code': 0, 'msg': '未找到记录'}

    # 返回示例数据
    data = {
        1: {
            'cate': 1,
            'name': '人脸检测示例',
            'unknown_image': [site_url + '/static/images/exp/g.png'],
            'known_image': [site_url + '/static/images/exp/g_box.png']
        },
        2: {
            'cate': 2,
            'name': '人脸勾勒示例',
            'unknown_image': [site_url + '/static/images/exp/g.png'],
            'known_image': [site_url + '/static/images/exp/g_sense.png']
        },
        3: {
            'cate': 3,
            'name': '人脸截取示例',
            'unknown_image': [site_url + '/static/images/exp/g.png'],
            'known_image': [
                site_url + '/static/images/exp/g1.png',
                site_url + '/static/images/exp/g2.png',
                site_url + '/static/images/exp/g3.png',
                site_url + '/static/images/exp/g4.png'
            ]
        },
        4: {
            'cate': 4,
            'name': '人脸化妆示例',
            'unknown_image': [site_url + '/static/images/exp/g.png'],
            'known_image': [site_url + '/static/images/exp/g_makeup.png']
        },
        5: {
            'cate': 5,
            'name': '人脸特征示例',
            'unknown_image': [site_url + '/static/images/exp/face_68.jpg'],
            'known_image': [site_url + '/static/images/exp/face_68_feature.png']
        }
    }
    return data.get(cate, data[1])
