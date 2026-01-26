# 🚀 RustDesk 客户端构建器 - 完全汉化版

## ✨ 新功能总览

### 全新界面
- 🎨 现代化深色渐变背景
- ✨ 动态粒子效果
- 💎 玻璃态卡片设计
- 🌟 霓虹发光效果
- 📱 完全响应式设计

### 新增功能（40+ 个）
- ✅ Windows 32位支持
- ✅ UI 定制模式
- ✅ 隐私背景图
- ✅ 图像质量和帧率控制
- ✅ 主控端功能（7个）
- ✅ 被控端功能（9个）
- ✅ 通用功能（8个）

## 📋 开箱即用配置清单

### 1. 安装依赖
```bash
cd /path/to/creator
pip install -r requirements.txt
```

### 2. 配置环境变量
在服务器上设置以下环境变量：
```bash
export GHUSER="你的GitHub用户名"
export GHBEARER="你的GitHub Fine-grained Access Token"
```

或创建 `.env` 文件：
```env
GHUSER=你的GitHub用户名
GHBEARER=你的GitHub Fine-grained Access Token
```

### 3. 配置 GitHub Secrets
在你的 GitHub 仓库设置以下 Secrets：
- `GENURL` - 你的服务器地址（例如：example.com:8000）
- `SIGN_BASE_URL` - 代码签名服务器地址（可选）
- `SIGN_API_KEY` - 代码签名 API 密钥（可选）
- `WINDOWS_PFX_BASE64` - Windows 代码签名证书（可选）
- `WINDOWS_PFX_PASSWORD` - 证书密码（可选）
- `WINDOWS_PFX_SHA1_THUMBPRINT` - 证书指纹（可选）

### 4. 初始化数据库
```bash
python3 manage.py migrate
```

### 5. 启动服务器
```bash
# 开发环境
python3 manage.py runserver 0.0.0.0:8000

# 生产环境（使用 gunicorn）
gunicorn rdgen.wsgi:application --bind 0.0.0.0:8000
```

### 6. 创建 Systemd 服务（可选）
创建 `/etc/systemd/system/rdgen.service`：
```ini
[Unit]
Description=RustDesk 客户端构建器
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/rdgen
Environment="GHUSER=你的GitHub用户名"
Environment="GHBEARER=你的GitHub Token"
ExecStart=/opt/rdgen/venv/bin/python3 /opt/rdgen/manage.py runserver 0.0.0.0:8000
Restart=always
RestartSec=10
StandardOutput=file:/var/log/rdgen.log
StandardError=file:/var/log/rdgen.error

[Install]
WantedBy=multi-user.target
```

启用并启动服务：
```bash
sudo systemctl enable rdgen.service
sudo systemctl start rdgen.service
sudo systemctl status rdgen.service
```

## 🎯 支持的平台

| 平台 | Workflow 文件 | 状态 |
|------|---------------|------|
| Windows 64位 | `generator-windows.yml` | ✅ 已有 |
| **Windows 32位** | `generator-windows-x86.yml` | ✅ **新增** |
| Linux | `generator-linux.yml` | ✅ 已有 |
| Android | `generator-android.yml` | ✅ 已有 |
| macOS | `generator-macos.yml` | ✅ 已有 |

## 🔧 新增字段列表

### 平台相关
- `platform`: 新增 `windows-x86` 选项
- `ui_mode`: 启用定制版用户界面

### 外观设置
- `privacy_wallpaper`: 隐私模式背景图
- `image_quality`: 图像质量（最佳/平衡/低/自定义）
- `custom_fps`: 自定义帧率（30/60/90/120 FPS）

### 服务器配置
- `updateLink`: 在线更新链接
- `unlockPin`: 配置 PIN

### 安全设置
- `remove_preset_password_warning`: 隐藏密码警告
- `hide_account`: 隐藏账户设置

### 主控端功能（7个）
- `cycleMonitor`: 显示器切换按钮
- `xOffline`: 标记离线设备
- `hide_chat_voice`: 隐藏聊天与语音
- `viewOnly`: 默认浏览模式
- `collapse_toolbar`: 自动折叠工具栏
- `privacy_mode`: 默认隐私模式
- `hide_username_on_card`: 隐藏用户名

### 被控端功能（9个）
- `hideTray`: 隐藏托盘图标
- `hidePassword`: 隐藏临时密码面板
- `hideMenuBar`: 隐藏设置菜单
- `hideQuit`: 隐藏退出按钮
- `addcopy`: 添加复制按钮
- `applyprivacy`: 禁止退出隐私模式
- `passpolicy`: 允许简单密码
- `allowHostnameAsId`: 主机名作为 ID
- `hideService_Start_Stop`: 隐藏服务启停

### 通用功能（8个）
- `disable_check_update`: 禁用检查更新
- `no_uninstall`: 不创建卸载快捷方式
- `disable_install`: 生成便携版
- `allowD3dRender`: Direct3D 渲染
- `use_texture_render`: 纹理渲染
- `pre_elevate_service`: 自动提权
- `sync_init_clipboard`: 同步初始剪贴板
- `hide_powered_by_me`: 隐藏技术支持标识

## 🎨 界面特色

### 颜色主题
```css
主渐变: #667eea → #764ba2 (紫色)
副渐变: #f093fb → #f5576c (粉红)
成功色: #4facfe → #00f2fe (蓝青)
背景色: #0a0e27 (深蓝黑)
霓虹色: #00d4ff (蓝) / #bc13fe (紫)
```

### 交互效果
- 平台图标：悬停放大 + 发光
- 卡片：悬停上浮 + 边框发光
- 按钮：悬停放大 + 阴影加强
- 输入框：聚焦时霓虹边框
- 粒子：50个动态飘动粒子

## 📝 文件修改清单

### 已修改文件
1. ✅ `rdgenerator/forms.py` - 新增 40+ 字段
2. ✅ `rdgenerator/views.py` - 处理新字段逻辑
3. ✅ `rdgenerator/templates/generator.html` - 全新界面
4. ✅ `rdgenerator/templates/waiting.html` - 汉化
5. ✅ `rdgenerator/templates/generated.html` - 汉化
6. ✅ `.github/workflows/generator-windows-x86.yml` - **新建**

### 备份文件
- `rdgenerator/templates/generator_old.html` - 原始英文界面

## 🔍 测试清单

### 基础功能测试
- [ ] 访问 `http://localhost:8000/generator`
- [ ] 检查界面是否完全显示中文
- [ ] 检查动态粒子效果
- [ ] 测试保存/加载配置功能
- [ ] 测试所有新字段是否正常显示

### 构建测试
- [ ] 测试 Windows 64位构建
- [ ] 测试 Windows 32位构建
- [ ] 测试 Linux 构建
- [ ] 测试 Android 构建
- [ ] 测试 macOS 构建

### 功能测试
- [ ] 测试图标上传
- [ ] 测试 Logo 上传
- [ ] 测试隐私背景图上传
- [ ] 测试服务器配置
- [ ] 测试权限设置
- [ ] 测试所有附加功能

## ⚠️ 注意事项

### 安全配置
1. **生产环境必须启用 CSRF 保护**
   ```python
   # rdgen/settings.py
   MIDDLEWARE = [
       'django.middleware.csrf.CsrfViewMiddleware',  # 取消注释
       # ...
   ]
   ```

2. **修改 DEBUG 设置**
   ```python
   # rdgen/settings.py
   DEBUG = False  # 生产环境设为 False
   ```

3. **修改 SECRET_KEY**
   ```python
   # rdgen/settings.py
   SECRET_KEY = '你的随机密钥'  # 使用强随机密钥
   ```

4. **配置 ALLOWED_HOSTS**
   ```python
   # rdgen/settings.py
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

### 文件上传限制
- 图标和 Logo 大小限制：由表单验证控制
- 隐私背景图：建议最大 500KB，推荐 1920×1080

### GitHub Actions
- 构建时间：Windows 约 20-30 分钟
- 确保 GitHub Actions 有足够的配额
- 检查 workflow 状态：Actions 标签页

## 🆘 故障排除

### 1. 界面显示不正常
- 清除浏览器缓存
- 检查 Bootstrap 5 CDN 是否可访问
- 检查 Font Awesome CDN 是否可访问

### 2. 构建失败
- 检查 GitHub Actions logs
- 验证 GENURL 环境变量
- 确认 GitHub Token 权限正确

### 3. 文件上传失败
- 检查服务器磁盘空间
- 验证文件权限
- 检查上传文件大小

### 4. 数据库错误
```bash
# 重新创建数据库
rm db.sqlite3
python3 manage.py migrate
```

## 📚 参考链接

- [RustDesk 官方文档](https://rustdesk.com/docs/)
- [RustDesk GitHub](https://github.com/rustdesk/rustdesk)
- [Django 文档](https://docs.djangoproject.com/)
- [Bootstrap 5 文档](https://getbootstrap.com/docs/5.3/)

## 💡 使用技巧

### 快速开始
1. 选择平台（Windows 64/32位、Linux、Android、macOS）
2. 填写配置名称（必填）
3. 配置服务器信息
4. 上传图标和 Logo
5. 设置权限和安全选项
6. 选择需要的附加功能
7. 点击"开始构建客户端"

### 配置保存/加载
- **保存**：填写完表单后，点击右上角"保存配置"按钮
- **加载**：点击"加载配置"按钮，选择之前保存的 JSON 文件

### 批量构建
如需批量构建多个平台：
1. 保存一个基础配置
2. 对每个平台加载配置
3. 修改平台特定选项
4. 分别提交构建

## 🎉 完成！

现在你的 RustDesk 客户端构建器已经：
- ✅ 完全汉化
- ✅ 拥有超酷的现代化界面
- ✅ 支持 40+ 个新功能
- ✅ 支持 Windows 32位构建
- ✅ 开箱即用

访问 `http://yourdomain:8000/generator` 开始使用！

---

**如有问题，请检查日志文件：**
- 应用日志：`/var/log/rdgen.log`
- 错误日志：`/var/log/rdgen.error`
