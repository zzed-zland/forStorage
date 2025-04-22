from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from utils.detector import WaterDetector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['RESULT_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'results')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# 确保上传和结果目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# 初始化检测器
detector = WaterDetector(model_path='models/best.pt')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加唯一标识符，避免文件名冲突
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # 保存上传的图片
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)
        
        # 进行检测
        result_filename = f"result_{unique_filename}"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        
        # 调用检测器进行检测
        detection_results = detector.detect(upload_path, result_path)
        
        # 返回结果页面
        return render_template('result.html', 
                              original_image=url_for('static', filename=f'uploads/{unique_filename}'),
                              result_image=url_for('static', filename=f'results/{result_filename}'),
                              detection_results=detection_results)
    
    flash('不支持的文件类型')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)