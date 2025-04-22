import os
import sys
import argparse

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.xml_to_yolo import convert_directory

def main(args):
    # 转换训练集标注
    print("正在转换训练集XML标注文件...")
    convert_directory(
        input_dir=os.path.join(args.base_dir, 'train'),
        output_dir=os.path.join(args.base_dir, 'yolo_labels_train')
    )
    
    # 转换验证集标注
    print("正在转换验证集XML标注文件...")
    convert_directory(
        input_dir=os.path.join(args.base_dir, 'valid'),
        output_dir=os.path.join(args.base_dir, 'yolo_labels_valid')
    )
    
    # 转换测试集标注
    print("正在转换测试集XML标注文件...")
    convert_directory(
        input_dir=os.path.join(args.base_dir, 'test'),
        output_dir=os.path.join(args.base_dir, 'yolo_labels_test')
    )
    
    print("所有标注文件转换完成！")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='转换XML标注文件为YOLO格式')
    parser.add_argument('--base_dir', type=str, default='.', help='项目根目录')
    
    args = parser.parse_args()
    main(args) 