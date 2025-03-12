import torch
import kagglehub
from torchvision import datasets, transforms

# 数据预处理
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 下载数据集
def download_dataset():
    path = kagglehub.dataset_download("sshikamaru/car-object-detection")
    return path

# 加载数据集并自动获取类别数量
def get_data_loaders(batch_size=32):
    data_dir = download_dataset()
    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    num_classes = len(dataset.classes)
    train_size = int(0.8 * len(dataset))
    valid_size = len(dataset) - train_size
    train_dataset, valid_dataset = torch.utils.data.random_split(dataset, [train_size, valid_size])
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_loader = torch.utils.data.DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, valid_loader, num_classes

__all__ = ['get_data_loaders']

