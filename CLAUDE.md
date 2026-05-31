# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

WeChat-Mini-Program-Face-Recognition is a face recognition service with:
- **FastAPI** backend (`server/`) — REST API + admin panel
- **WeChat Mini Program** frontend (`weixin/`) — 4 pages mobile app
- **MongoDB** database — stores accounts, login logs, face records
- 5 face processing modes: detection, outline, crop, makeup, 68-point landmarks

## Architecture

```
WeChat Mini Program ──HTTP──> FastAPI server (:8003) ──> MongoDB (:27017)
                                    │
                              ┌─────┴─────┐
                          api/ routes   admin/ routes
                          (REST JSON)   (Jinja2 HTML templates)
```

## Key Files

| File | Role |
|------|------|
| `server/app/__init__.py` | FastAPI app factory, lifespan (MongoDB connect/disconnect), static mount |
| `server/app/configs.py` | App config (debug, site_url, cookie_secret) + MongoDB config |
| `server/app/api/router.py` | Aggregates all API sub-routers |
| `server/app/admin/router.py` | Aggregates all admin sub-routers |
| `server/app/admin/auth.py` | Cookie auth via itsdangerous URLSafeSerializer |
| `server/app/common/face.py` | Face recognition engine (face_recognition, dlib, cv2, PIL) |
| `server/app/common/utils.py` | CommonUtils: site_url, current_time, common_params |
| `server/app/common/forms.py` | WTForms: LoginForm, AccountAddForm with custom validators |
| `server/app/common/check.py` | MongoDB credential verification |
| `server/manage.py` | Entry point: `uvicorn app:create_app --factory` |
| `pyproject.toml` | uv project config, dependencies, bfsu mirror index |

## Route Map

### API Routes (for WeChat Mini Program)
- `GET /` → `api/index.py` — Returns client IP, address, headers
- `POST /user/` → `api/user.py` — WeChat user login record → `loginlog` collection
- `GET /grid/` → `api/grid.py` — 6-item navigation menu with icons
- `POST /match/` → `api/match.py` — Upload image (`img` field) + `cate` form field, runs face processing, saves to `image` collection
- `GET /match/` → `api/match.py` — Query by `uuid` or return demo data by `cate` (1-5)

### Admin Routes (Jinja2 HTML pages)
- `/login/` GET/POST → `admin/login.py` — Login page with WTForms validation, sets signed cookie
- `/admin/logout/` → `admin/login.py` — Clears cookie, redirects to login
- `/admin/` → `admin/index.py` — Dashboard with counts (image_total, image_check, loginlog_total)
- `/admin/account/` → `admin/account.py` — List accounts
- `/admin/account/add/` GET/POST → `admin/account.py` — Add account (hashes password via werkzeug)
- `/admin/account/delete/` → `admin/account.py` — Delete by `_id`
- `/admin/face/` → `admin/face.py` — Paginated face record list (15/page), sorted by createdAt desc
- `/admin/face/detail/` → `admin/face.py` — Single record detail view
- `/admin/face/delete/` → `admin/face.py` — Delete by `_id`
- `/admin/face/status/` → `admin/face.py` — Set status=1 (approved)
- `/admin/loginlog/` → `admin/loginlog.py` — Paginated login log list
- `/admin/loginlog/detail/` → `admin/loginlog.py` — Single log detail

## MongoDB Collections

Database: `face_project` (configurable in configs.py)

| Collection | Fields |
|-----------|--------|
| `account` | name, pwd (hashed), createdAt, updatedAt |
| `loginlog` | nickName, avatarUrl, country, province, city, gender, language, ip, addr, headers, createdAt |
| `image` | unknown_image[], known_image[], name, cate, status (0/1), ip, addr, headers, createdAt |

## Auth Flow

- Admin auth uses `itsdangerous.URLSafeSerializer` with `cookie_secret` from configs
- `admin/auth.py` provides `set_admin_cookie()`, `get_admin_name()`, `clear_admin_cookie()`, `login_required()`
- Each admin route checks `login_required(request)` and redirects to `/login/` if unauthenticated
- API routes have no auth (they serve the WeChat Mini Program)

## Development

```bash
# Install deps
uv sync --python 3.12

# Install face recognition (Windows)
DLIB_USE_CUDA=0 PYTHONUTF8=1 uv pip install dlib face-recognition
uv pip install git+https://github.com/ageitgey/face_recognition_models

# Run server
cd server && uv run uvicorn app:create_app --host 0.0.0.0 --port 8003 --factory --reload

# API docs
open http://127.0.0.1:8003/docs

# Admin panel
open http://127.0.0.1:8003/login/
```

## Key Dependencies

- `fastapi`, `uvicorn[standard]` — Web framework & ASGI server
- `pymongo` — MongoDB driver
- `face-recognition`, `opencv-python`, `Pillow` — Image processing
- `dlib` — 68-point face landmark detection (requires `shape_predictor_68_face_landmarks.dat` model file)
- `itsdangerous` — Signed cookie auth
- `Werkzeug` — Password hashing (`generate_password_hash`, `check_password_hash`), `MultiDict`
- `WTForms` — Form validation
- `jinja2` — Template rendering
- `python-multipart` — File upload parsing
- `aiofiles` — Async file operations

## Notes

- Default port: **8003**
- Static files mounted at `/static`
- The `face.py` module requires `dlib` and `face_recognition` at module level — these must be installed
- `ip2region.db` binary database is used for IP geolocation
- `weixin/` directory is the WeChat Mini Program frontend (not Python), deployed separately via WeChat DevTools
- The `master` branch contains the original Tornado implementation; `fastapi` is the current branch
