# WeChat-Mini-Program-Face-Recognition

微信小程序人脸识别助手，FastAPI 后端 + 微信小程序前端。

## 项目结构

```
├── server/                  # Python FastAPI 后端
│   ├── manage.py            # 入口：uvicorn 启动
│   ├── requirements.txt     # pip 依赖
│   └── app/
│       ├── __init__.py      # FastAPI 应用工厂 + lifespan
│       ├── configs.py       # 应用和 MongoDB 配置
│       ├── api/             # 小程序 API 接口
│       │   ├── index.py     # GET  /         API 首页
│       │   ├── user.py      # POST /user/    用户授权登录
│       │   ├── grid.py      # GET  /grid/    快捷导航菜单
│       │   └── match.py     # POST /match/   人脸识别上传
│       │                    # GET  /match/    查询结果/示例
│       ├── admin/           # 后台管理系统
│       │   ├── auth.py      # Cookie 认证
│       │   ├── login.py     # GET/POST /login/
│       │   ├── index.py     # GET  /admin/   仪表盘
│       │   ├── account.py   # CRUD /admin/account/
│       │   ├── face.py      # CRUD /admin/face/
│       │   └── loginlog.py  # 列表 /admin/loginlog/
│       ├── common/          # 公共模块
│       │   ├── face.py      # 人脸识别引擎 (face_recognition + dlib + OpenCV)
│       │   ├── check.py     # 账号密码验证
│       │   ├── forms.py     # WTForms 表单验证
│       │   ├── utils.py     # 通用工具类
│       │   ├── ip2Addr.py   # IP 地址解析
│       │   └── ip2Region.py # ip2region 数据库客户端
│       ├── templates/       # Jinja2 模板（后台页面）
│       └── static/          # 静态资源 (CSS, JS, 图片, ip2region.db)
│
├── weixin/                  # 微信小程序前端
│   ├── app.json             # 小程序配置 (4 个页面)
│   ├── pages/               # index, vision, match, about
│   └── static/style/        # WeUI 样式库
│
└── pyproject.toml           # uv 项目配置
```

## 功能特性

5 种人脸识别功能：
1. **人脸检测** — 红色矩形框标记人脸位置
2. **人脸勾勒** — 白色线条勾勒面部五官轮廓
3. **人脸截取** — 裁剪并提取每张人脸
4. **人脸化妆** — 虚拟化妆（眉毛、嘴唇、眼睛）
5. **人脸特征** — 68 个面部特征点标注

后台管理系统：
- 管理员登录/退出（Cookie 认证）
- 账号管理（CRUD）
- 人脸识别记录管理（列表、详情、审核）
- 用户授权日志查看

## 快速开始

### 环境要求

- Python >= 3.8
- MongoDB（默认 `127.0.0.1:27017`）
- dlib 人脸特征模型文件 `shape_predictor_68_face_landmarks.dat`
  - 下载后放入 `server/app/static/models/`

### 安装

```bash
git clone https://github.com/llxlr/WeChat-Mini-Program-Face-Recognition.git
cd WeChat-Mini-Program-Face-Recognition
git checkout fastapi

# 使用 uv 安装核心依赖
uv sync --python 3.12

# 安装人脸识别依赖（Windows 需要编译 dlib）
# 设置 DLIB_USE_CUDA=0 禁用 CUDA，PYTHONUTF8=1 修复编码问题
DLIB_USE_CUDA=0 PYTHONUTF8=1 uv pip install dlib face-recognition
uv pip install git+https://github.com/ageitgey/face_recognition_models
```

### 运行

```bash
cd server
uv run uvicorn app:create_app --host 0.0.0.0 --port 8003 --factory --reload
```

启动后访问：
- API 接口：`http://127.0.0.1:8003/`
- 后台管理：`http://127.0.0.1:8003/login/`
- API 文档：`http://127.0.0.1:8003/docs`

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | API 首页 |
| POST | `/user/` | 用户授权登录 |
| GET | `/grid/` | 快捷导航菜单 |
| POST | `/match/` | 上传图片进行人脸识别 |
| GET | `/match/` | 查询识别结果或获取示例 |

## 技术栈

- **后端**: FastAPI + uvicorn (Python)
- **数据库**: MongoDB (pymongo)
- **人脸识别**: face-recognition + dlib + OpenCV + Pillow
- **模板**: Jinja2
- **认证**: itsdangerous 签名 Cookie
- **表单**: WTForms + Werkzeug
- **依赖管理**: uv

## License

MIT
