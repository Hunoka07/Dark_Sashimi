# -*- coding: utf-8 -*-

PROJECT_NAME = 'Tonu Project'
VERSION = '1.0.0'
CREATOR = 'System Developer'

SECRET_KEY = 'secret-key-that-must-be-changed'
DEBUG = False
TESTING = False

DATABASE_URI = 'sqlite:///application.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

PROXY_SOURCES = []
REQUEST_TIMEOUT = 30

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1000 * 1000

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = None

ITEMS_PER_PAGE = 25
DEFAULT_LANGUAGE = 'vi'
SUPPORTED_LANGUAGES = ['en', 'vi']

