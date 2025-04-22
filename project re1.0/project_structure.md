# 路面积水检测系统项目结构

## 目录结构

```
/
├── app.py                  # Flask应用主入口
├── static/                # 静态文件目录
│   ├── css/              # CSS样式文件
│   │   └── style.css     # 主样式文件
│   ├── js/               # JavaScript文件
│   │   └── main.js       # 主JS文件
│   ├── uploads/          # 用户上传的图片存储目录
│   └── results/          # 检测结果图片存储目录
├── templates/            # HTML模板目录
│   ├── index.html        # 主页面
│   └── result.html       # 结果展示页面
├── models/               # 模型目录
│   └── best.pt           # 训练好的YOLOv8模型
├── utils/                # 工具函数目录
│   └── detector.py       # 检测器类
├── train/                # 训练相关文件
│   ├── train.py          # 训练脚本
│   └── data.yaml         # 数据集配置文件
└── requirements.txt      # 项目依赖
```

## 功能模块

1. **前端界面**：提供用户友好的Web界面，允许用户上传图片并展示检测结果
2. **后端服务**：使用Flask处理HTTP请求，调用YOLOv8模型进行推理
3. **模型训练**：使用YOLOv8训练路面积水检测模型
4. **检测模块**：封装YOLOv8推理逻辑，处理上传的图片并返回检测结果