document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    
    // 点击选择文件按钮
    browseBtn.addEventListener('click', function() {
        fileInput.click();
    });
    
    // 文件选择变化
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            showFileInfo(this.files[0]);
        }
    });
    
    // 拖放事件 - 阻止默认行为
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // 拖放区域高亮
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('dragover');
    }
    
    function unhighlight() {
        dropArea.classList.remove('dragover');
    }
    
    // 处理拖放文件
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files && files.length) {
            fileInput.files = files;
            showFileInfo(files[0]);
        }
    }
    
    // 显示文件信息
    function showFileInfo(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        
        if (validTypes.includes(file.type)) {
            fileName.textContent = file.name;
            fileInfo.classList.remove('d-none');
        } else {
            alert('请选择有效的图片文件（JPG、JPEG、PNG）');
            fileInput.value = '';
            fileInfo.classList.add('d-none');
        }
    }
});