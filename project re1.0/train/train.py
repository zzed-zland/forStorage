from ultralytics import YOLO
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.detector import WaterDetector

def main():
    # 初始化模型
    # 使用预训练的YOLOv8模型作为基础
    model = YOLO('yolov8x.pt')
    
    # 配置训练参数
    # data.yaml文件包含了数据集的配置信息
    data_yaml = 'data.yaml'
    epochs = 100      # 训练轮数
    batch_size = 16   # 批次大小
    imgsz = 640      # 图像大小
    
    # 训练模型
    try:
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            batch=batch_size,
            imgsz=imgsz,
            patience=50,    # 早停参数
            save=True,      # 保存最佳模型
            device='0'      # 使用GPU训练
        )
        
        print("训练完成！")
        print(f"最佳模型保存在: {results.best}")
        
        # 将最佳模型复制到models目录
        best_model_path = results.best
        if os.path.exists(best_model_path):
            target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'best.pt')
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            import shutil
            shutil.copy2(best_model_path, target_path)
            print(f"最佳模型已复制到: {target_path}")
            
    except Exception as e:
        print(f"训练过程中出现错误: {str(e)}")

if __name__ == '__main__':
    main()