# 🚀 快速开始指南

## 第一步：安装依赖

```bash
cd /path/to/creator
python3 -m venv venv
source venv/bin/activate  # Windows 用: venv\Scripts\activate
pip install -r requirements.txt
```

## 第二步：配置环境

### 方法 1: 环境变量
```bash
export GHUSER="你的GitHub用户名"
export GHBEARER="你的GitHub Token"
```

### 方法 2: .env 文件
创建 `.env` 文件：
```env
GHUSER=你的GitHub用户名
GHBEARER=你的GitHub Token
```

## 第三步：GitHub Token 设置

1. 访问：https://github.com/settings/tokens?type=beta
2. 点击"Generate new token"
3. 选择"Fine-grained tokens"
4. 配置：
   - Token name: `rdgen`
   - Repository access: 选择你的 rdgen 仓库
   - Permissions:
     - Actions: Read and write ✅
     - Workflows: Read and write ✅

## 第四步：GitHub Secrets 设置

进入你的仓库 → Settings → Secrets and variables → Actions

添加以下 Secret：
- `GENURL`: 你的服务器地址（如：example.com:8000）

## 第五步：初始化数据库

```bash
python3 manage.py migrate
```

## 第六步：启动服务

```bash
python3 manage.py runserver 0.0.0.0:8000
```

## 第七步：访问界面

打开浏览器访问：`http://localhost:8000/generator`

## 🎉 完成！

现在你可以：
1. 选择构建平台
2. 填写配置信息
3. 上传图标和Logo
4. 选择功能选项
5. 点击"开始构建客户端"

## ⚡ 生产环境部署

### 使用 Systemd

创建服务文件 `/etc/systemd/system/rdgen.service`：

```ini
[Unit]
Description=RustDesk 客户端构建器
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/rdgen
Environment="GHUSER=你的GitHub用户名"
Environment="GHBEARER=你的Token"
ExecStart=/opt/rdgen/venv/bin/python3 manage.py runserver 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable rdgen
sudo systemctl start rdgen
sudo systemctl status rdgen
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## ❓ 常见问题

### Q: 构建失败？
A: 检查 GitHub Actions 日志，确认 Token 权限正确

### Q: 界面显示异常？
A: 清除浏览器缓存，检查 CDN 是否可访问

### Q: 上传图片失败？
A: 确保图片格式为 PNG，大小不超过 500KB

## 📱 支持平台

- ✅ Windows 64位
- ✅ Windows 32位
- ✅ Linux
- ✅ Android
- ✅ macOS

## 🆘 需要帮助？

查看完整文档：`README_CN.md`
