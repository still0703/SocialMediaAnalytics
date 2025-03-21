from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# 初始化Flask应用
app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/social_media_analytics'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# 初始化SQLAlchemy
db = SQLAlchemy(app)

#导入模型
from backend.models import *

# 导入路由（确保在创建app和db之后导入，避免循环导入问题）
from backend.routes import main_routes

# 注册蓝图
app.register_blueprint(main_routes.blueprint)

# 测试路由
@app.route('/test')
def test():
    return "Flask应用正常运行!"

# 如果直接运行此文件
if __name__ == '__main__':
    app.run(debug=True)