from flask import Blueprint, render_template, request, jsonify
from backend.app import db

# 创建蓝图
blueprint = Blueprint('main', __name__)

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API路由 - 获取舆情数据
@blueprint.route('/api/sentiment', methods=['GET'])
def get_sentiment_data():
    # 这里将从数据库获取数据并返回
    # 临时返回一些示例数据
    data = {
        'positive': 60,
        'neutral': 30,
        'negative': 10
    }
    return jsonify(data)