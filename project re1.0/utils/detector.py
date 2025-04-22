import os
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

class WaterDetector:
    def __init__(self, model_path):
        """
        初始化水检测器
        
        Args:
            model_path: YOLOv8模型路径
        """
        # 检查模型文件是否存在
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")
            
        # 加载YOLOv8模型
        self.model = YOLO(model_path)
        
    def detect(self, image_path, output_path=None):
        """
        检测图像中的积水
        
        Args:
            image_path: 输入图像路径
            output_path: 输出图像路径（可选）
            
        Returns:
            检测结果字典，包含检测到的积水区域信息
        """
        # 检查图像文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图像文件不存在: {image_path}")
        
        # 使用YOLOv8进行预测
        results = self.model(image_path)
        
        # 处理检测结果
        detection_results = []
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for i, box in enumerate(boxes):
                # 获取边界框坐标
                x1, y1, x2, y2 = box.xyxy[0].astype(int)
                # 获取置信度
                confidence = float(box.conf[0])
                # 获取类别
                cls = int(box.cls[0])
                cls_name = result.names[cls]
                
                detection_results.append({
                    'id': i,
                    'class': cls_name,
                    'confidence': confidence,
                    'bbox': [int(x1), int(y1), int(x2), int(y2)]
                })
        
        # 如果指定了输出路径，保存标注后的图像
        if output_path:
            # 获取原始图像
            img = cv2.imread(image_path)
            
            # 在图像上绘制检测结果
            for det in detection_results:
                x1, y1, x2, y2 = det['bbox']
                conf = det['confidence']
                cls_name = det['class']
                
                # 绘制边界框
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # 绘制标签
                label = f"{cls_name}: {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # 保存结果图像
            cv2.imwrite(output_path, img)
        
        return detection_results
    
    def train(self, data_yaml, epochs=100, batch_size=16, imgsz=640):
        """
        训练YOLOv8模型
        
        Args:
            data_yaml: 数据集配置文件路径
            epochs: 训练轮数
            batch_size: 批次大小
            imgsz: 图像大小
            
        Returns:
            训练结果
        """
        # 使用YOLOv8进行训练
        results = self.model.train(
            data=data_yaml,
            epochs=epochs,
            batch=batch_size,
            imgsz=imgsz,
            patience=50,
            save=True
        )
        
        return results