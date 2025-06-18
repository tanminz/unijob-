import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(base_dir, 'static', 'licenses')
    ADMIN_VERIFICATION_CODE = 'ctsv2025'  # bạn đặt mã tùy ý
