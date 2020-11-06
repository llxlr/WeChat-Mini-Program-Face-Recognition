# -*- coding: utf-8 -*-
import cv2
import dlib
import os
import datetime
import uuid
import face_recognition  # 导入人类识别库
from PIL import Image, ImageDraw


# 人类识别程序
class Face:
    # 定义一个初始化构造方法
    def __init__(self, directory_path, picture_name, save_path):
        # 把外部参数赋值实例属性
        self.dir_path = directory_path  # 图片目录
        self.pic_name = picture_name  # 图片名称
        self.save_path = save_path  # 保存路径

    @property
    def image_init(self):
        # 加载图片，对图片进行初始化
        # 就把图片转化为像素矩阵
        image = face_recognition.load_image_file(
            os.path.join(
                self.dir_path,
                self.pic_name
            )
        )
        return image

    # 获取图像中人脸位置
    def get_face_locations(self):
        # 初始化
        image = self.image_init
        # 查找人类位置，位置算法，基于轮廓算法
        # [(56, 683, 146, 593), (86, 354, 176, 265), (116, 494, 206, 404), (116, 155, 206, 66)]
        # 左上角点、右下角点
        face_locations = face_recognition.face_locations(image)
        return image, face_locations

    # 获取图像中人类特征
    def get_face_landmarks(self):
        # 初始化
        image = self.image_init
        # 通过特征算法获取所有的特征点
        face_landmarks_list = face_recognition.face_landmarks(image)
        return image, face_landmarks_list

    # 时间
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 保存名称定义
    @property
    def image_name(self):
        # 名称构成：时间+唯一字符串
        prefix1 = self.dt
        prefix2 = uuid.uuid4().hex
        return prefix1 + prefix2

    # 保存识别结果方法，pillow
    def save_pil_face(self, pil_image):
        # 如果保存目录不存在，则创建
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # 定义图片完整名称
        filename = "{}.png".format(
            self.image_name
        )
        # 保存图片至指定的位置
        pil_image.save(os.path.join(self.save_path, filename), 'png')
        return filename

    # 1.框选人脸功能
    def face_box(self):
        # 获取人脸的位置
        image, face_locations = self.get_face_locations()
        # 将图片转化为图像数组
        pil_image = Image.fromarray(image)
        # 把图像数组转化为可绘制的对象
        draw = ImageDraw.Draw(pil_image)
        # 循环遍历人脸上、右、下、左位置
        # 颜色遵循三原色原理
        # RGB => R：红，G：绿，B：蓝，色值0~255
        for (top, right, bottom, left) in face_locations:
            # 绘制矩形框
            draw.rectangle(
                (
                    (left, top),
                    (right, bottom)
                ),
                outline=(255, 0, 0),
                width=5
            )
        # 显示图像
        # pil_image.show()
        # 保存图像
        filename = self.save_pil_face(pil_image)
        return [filename]

    # 2.人脸勾勒功能
    def face_sense(self):
        # 获取图像和人脸特征
        image, face_landmarks_list = self.get_face_landmarks()
        # 定义获取脸部特征的列表，键
        facial_features = [
            'chin',
            'left_eyebrow',
            'right_eyebrow',
            'nose_bridge',
            'nose_tip',
            'left_eye',
            'right_eye',
            'top_lip',
            'bottom_lip'
        ]
        # 将图像转化为图像数组
        pil_image = Image.fromarray(image)
        # 将图像数组转化为可绘制的对象
        draw = ImageDraw.Draw(pil_image)
        # 遍历所有特征点
        for face_landmark in face_landmarks_list:
            # 遍历特征列表
            for facial_feature in facial_features:
                # 绘制描线
                draw.line(face_landmark[facial_feature], width=5, fill=(255, 255, 255))
        # 显示图像
        # pil_image.show()
        # 保存图像
        filename = self.save_pil_face(pil_image)
        return [filename]

    # 3.截取人脸功能
    def face_find(self):
        # 获取图像和人脸位置
        image, face_locations = self.get_face_locations()
        result = []
        # 循环遍历人脸位置
        for face_location in face_locations:
            # 获取上右下左位置
            top, right, bottom, left = face_location
            # 框选图片中所有的人脸位置
            face_image = image[top:bottom, left:right]
            # 把框选出来的结果转化为一个图像数组
            pil_image = Image.fromarray(face_image)
            # 保存图片
            filename = self.save_pil_face(pil_image)
            # 把最终结果追加到头像列表
            result.append(
                filename
            )
        # 返回头像列表
        return result

    # 4.人脸化妆
    def face_makeup(self):
        # 获取图像和人脸位置
        image, face_landmarks_list = self.get_face_landmarks()
        # 将图像转化为图像数组
        pil_image = Image.fromarray(image)
        # 将图像数组转化为可绘制的对象
        draw = ImageDraw.Draw(pil_image, 'RGBA')
        # 循环遍历人脸特征
        for face_landmark in face_landmarks_list:
            # 绘制左右眉毛
            # 形状
            draw.polygon(face_landmark['left_eyebrow'], fill=(68, 54, 39, 128))
            draw.polygon(face_landmark['right_eyebrow'], fill=(68, 54, 39, 128))
            # 线条
            draw.line(face_landmark['left_eyebrow'], fill=(68, 54, 39, 150), width=3)
            draw.line(face_landmark['right_eyebrow'], fill=(68, 54, 39, 150), width=3)
            # 绘制上下嘴唇
            # 形状
            draw.polygon(face_landmark['top_lip'], fill=(150, 0, 0, 128))
            draw.polygon(face_landmark['bottom_lip'], fill=(150, 0, 0, 128))
            # 线条
            draw.line(face_landmark['top_lip'], fill=(150, 0, 0, 64), width=3)
            draw.line(face_landmark['bottom_lip'], fill=(150, 0, 0, 64), width=3)
            # 绘制左右眼睛
            # 形状
            draw.polygon(face_landmark['left_eye'], fill=(255, 255, 255, 30))
            draw.polygon(face_landmark['right_eye'], fill=(255, 255, 255, 30))
            # 线条
            draw.line(face_landmark['left_eye'] + [face_landmark['left_eye'][0]], fill=(0, 0, 0, 110), width=2)
            draw.line(face_landmark['right_eye'] + [face_landmark['right_eye'][0]], fill=(0, 0, 0, 110), width=2)
        # 显示图片
        # pil_image.show()
        # 保存图片
        filename = self.save_pil_face(pil_image)
        return [filename]

    # 5.人脸68个特征点获取
    def face_68_point(self):
        # 读取图片
        image = cv2.imread(os.path.join(self.dir_path, self.pic_name))
        # 使用特征提取器
        detector = dlib.get_frontal_face_detector()
        # 定义模型的路径
        model_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/models/shape_predictor_68_face_landmarks.dat'
        )
        # 定义预测器
        predictor = dlib.shape_predictor(model_path)
        # 实例化特征提取器
        dets = detector(image, 1)
        for k, d in enumerate(dets):
            # 利用预测器预测
            shape = predictor(image, d)
            # 标出68个点
            for i in range(68):
                # 画圆点，圆心、半径、颜色、实心
                cv2.circle(
                    image,
                    (shape.part(i).x, shape.part(i).y),
                    2,
                    (255, 0, 0),
                    -1,
                )
                # 画文字，文字、坐标、风格、大小、颜色
                cv2.putText(
                    image,
                    str(i),
                    (shape.part(i).x, shape.part(i).y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    (0, 255, 0)
                )
        # 显示图像
        # cv2.imshow('68.png', image)
        # cv2.waitKey(0)
        # 保存图像
        filename = self.save_cv2_face(image)
        return [filename]

    # 使用opencv保存图片
    def save_cv2_face(self, image):
        # 如果保存目录不存在，则创建
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # 定义图片完整名称
        filename = "{}.png".format(
            self.image_name
        )
        # 保存图片至指定的位置
        cv2.imwrite(os.path.join(self.save_path, filename), image)
        return filename


if __name__ == "__main__":
    root_path = os.path.dirname(
        os.path.dirname(__file__)
    )
    face = Face(
        directory_path=os.path.join(root_path, 'static/images/exp'),
        picture_name='g.png',
        save_path=os.path.join(root_path, 'static/uploads')
    )
    # print(face.get_face_locations())
    # print(face.get_face_landmarks())
    # print(face.face_box())
    # print(face.face_sense())
    # print(face.face_find())
    # print(face.face_makeup())
    print(face.face_68_point())
