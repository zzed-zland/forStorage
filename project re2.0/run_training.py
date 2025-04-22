import os
import sys
import argparse
import subprocess

def main(args):
    # 项目根目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 步骤1: 转换XML标注文件为YOLO格式
    print("\n=== 步骤1: 转换XML标注文件为YOLO格式 ===")
    convert_cmd = [
        sys.executable,
        os.path.join(base_dir, 'convert_labels.py'),
        '--base_dir', base_dir
    ]
    subprocess.run(convert_cmd, check=True)
    
    # 步骤2: 训练模型
    print("\n=== 步骤2: 训练模型 ===")
    train_cmd = [
        sys.executable,
        os.path.join(base_dir, 'train', 'train.py'),
        '--model', args.model,
        '--data', os.path.join(base_dir, args.data),
        '--epochs', str(args.epochs),
        '--batch_size', str(args.batch_size),
        '--img_size', str(args.img_size),
        '--patience', str(args.patience),
        '--device', args.device
    ]
    subprocess.run(train_cmd, check=True)
    
    print("\n=== 训练流程完成! ===")
    print(f"最佳模型保存在: {os.path.join(base_dir, 'models', 'best.pt')}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='水积检测训练流程')
    parser.add_argument('--model', type=str, default='yolov8n.pt', help='预训练模型路径')
    parser.add_argument('--data', type=str, default='data.yaml', help='数据配置文件路径')
    parser.add_argument('--epochs', type=int, default=10, help='训练轮数')
    parser.add_argument('--batch_size', type=int, default=10, help='批次大小')
    parser.add_argument('--img_size', type=int, default=640, help='图像大小')
    parser.add_argument('--patience', type=int, default=50, help='早停参数')
    parser.add_argument('--device', type=str, default='0', help='训练设备，例如：0表示第一个GPU')
    
    args = parser.parse_args()
    main(args) 