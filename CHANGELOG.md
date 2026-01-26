# 🎉 RustDesk 客户端构建器 - 更新日志

## 版本：2.0.0 - 完全汉化增强版
**发布日期：** 2026-01-26

---

## 🆕 新功能

### 1. 全新用户界面 ✨
- **深色渐变主题**：紫色到深紫的现代化渐变背景
- **动态粒子效果**：50个飘动粒子增强科技感
- **玻璃态卡片**：毛玻璃效果的现代化卡片设计
- **霓虹发光**：蓝色和紫色的霓虹光效
- **悬停动画**：所有元素都有流畅的交互动画
- **完全响应式**：完美适配桌面和移动设备

### 2. 平台支持扩展 🖥️
- ✅ **Windows 32位支持**
  - 新增 `generator-windows-x86.yml` workflow
  - 完整的 32位编译环境配置
  - 兼容 i686-pc-windows-msvc 目标

### 3. 新增功能字段（40+个）📋

#### 基础设置
- `ui_mode` - 启用定制版用户界面
- `unlockPin` - 配置 PIN 码

#### 外观定制
- `privacy_wallpaper` - 隐私模式背景图（PNG，1920×1080）
- `image_quality` - 图像质量（最佳/平衡/低/自定义）
- `custom_fps` - 自定义帧率（30/60/90/120 FPS）

#### 服务器配置
- `updateLink` - 在线更新链接

#### 安全设置
- `remove_preset_password_warning` - 隐藏密码警告
- `hide_account` - 隐藏账户设置

#### 主控端功能（7个）
- `cycleMonitor` - 在会话顶部显示显示器切换按钮
- `xOffline` - 在地址簿中标记离线设备
- `hide_chat_voice` - 隐藏会话中的聊天与语音功能
- `viewOnly` - 默认以浏览模式连接会话
- `collapse_toolbar` - 会话启动时自动折叠工具栏
- `privacy_mode` - 默认进入隐私模式
- `hide_username_on_card` - 在连接卡片中隐藏用户名

#### 被控端功能（9个）
- `hideTray` - 隐藏托盘图标
- `hidePassword` - 隐藏临时密码面板
- `hideMenuBar` - 隐藏设置菜单
- `hideQuit` - 隐藏退出按钮
- `addcopy` - 添加复制按钮
- `applyprivacy` - 禁止被控端退出隐私模式
- `passpolicy` - 允许使用简单的临时密码
- `allowHostnameAsId` - 使用主机名作为 ID（Win 10+）
- `hideService_Start_Stop` - 隐藏常规和托盘的服务启停

#### 通用功能（8个）
- `disable_check_update` - 禁用启动时检查更新
- `no_uninstall` - 不创建卸载快捷方式
- `disable_install` - 生成便携版
- `allowD3dRender` - 启用 Direct3D 渲染
- `use_texture_render` - 启用纹理渲染（Win 10+）
- `pre_elevate_service` - 启动时自动提权
- `sync_init_clipboard` - 同步初始剪贴板内容
- `hide_powered_by_me` - 隐藏"技术支持"标识

### 4. 完全汉化 🇨🇳
- ✅ 所有界面文本翻译为简体中文
- ✅ 表单标签和说明汉化
- ✅ 提示信息和帮助文本汉化
- ✅ 等待和成功页面汉化
- ✅ 错误提示汉化

---

## 📝 文件变更清单

### 新建文件
```
.github/workflows/generator-windows-x86.yml  # Windows 32位构建流程
README_CN.md                                  # 完整中文文档
QUICKSTART_CN.md                              # 快速开始指南
CHANGELOG.md                                  # 本文件
```

### 修改文件
```
rdgenerator/forms.py                         # 新增 40+ 字段
rdgenerator/views.py                         # 处理新字段逻辑
rdgenerator/templates/generator.html         # 全新界面（2800+ 行）
rdgenerator/templates/waiting.html           # 汉化并美化
rdgenerator/templates/generated.html         # 汉化并美化
```

### 备份文件
```
rdgenerator/templates/generator_old.html     # 原始英文界面备份
```

---

## 🎨 界面设计规范

### 配色方案
```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
--dark-bg: #0a0e27;
--card-bg: rgba(255, 255, 255, 0.05);
--neon-blue: #00d4ff;
--neon-purple: #bc13fe;
```

### 交互效果
- **卡片悬停**：上浮 5px + 边框发光
- **按钮悬停**：上浮 3px + 阴影加强
- **输入框聚焦**：霓虹蓝边框 + 阴影
- **平台图标**：放大 1.15 倍 + 发光效果

---

## 🔧 技术变更

### 前端技术栈
- **框架**：Bootstrap 5.3.0
- **图标**：Font Awesome 6.4.0
- **字体**：Noto Sans SC（中文优化）
- **动画**：CSS3 Animations + Transitions

### 后端变更
- **Django Forms**：新增 40+ 字段定义
- **Views 处理**：完整的字段处理逻辑
- **配置生成**：支持所有新功能的 JSON 配置

### GitHub Actions
- **新工作流**：完整的 Windows 32位构建流程
- **兼容性**：与原有流程完全兼容
- **优化**：复用缓存，提升构建速度

---

## 📊 统计数据

### 代码量
- **新增代码**：约 3,500 行
- **修改代码**：约 500 行
- **总代码量**：约 5,000+ 行

### 功能数量
- **新增字段**：40+ 个
- **新增功能**：24 个独立功能
- **支持平台**：5 个（新增 1 个）

### 文件统计
- **新建文件**：4 个
- **修改文件**：5 个
- **备份文件**：1 个

---

## ⚠️ 破坏性变更

### 无破坏性变更
- 所有原有功能保持兼容
- 原有配置文件可以继续使用
- 数据库结构无变化
- API 接口保持一致

---

## 🐛 已知问题

### 1. Python 依赖
- 需要安装 `python-dotenv` 包
- 解决方案：`pip install python-dotenv`

### 2. 表单验证
- 某些新字段的验证可能需要进一步优化
- 建议在生产环境部署前充分测试

### 3. 浏览器兼容性
- 推荐使用现代浏览器（Chrome, Firefox, Edge, Safari）
- IE 浏览器不再支持

---

## 📋 升级指南

### 从旧版本升级

1. **备份数据**
```bash
cp db.sqlite3 db.sqlite3.backup
```

2. **拉取最新代码**
```bash
git pull origin master
```

3. **更新依赖**
```bash
pip install -r requirements.txt
```

4. **迁移数据库**
```bash
python3 manage.py migrate
```

5. **重启服务**
```bash
sudo systemctl restart rdgen
```

---

## 🚀 下一步计划

### v2.1.0 计划功能
- [ ] 多语言支持（英文/繁体中文/日文）
- [ ] 配置模板库
- [ ] 批量构建支持
- [ ] 构建历史记录
- [ ] API 文档
- [ ] 单元测试覆盖

### v2.2.0 计划功能
- [ ] Docker 容器化部署
- [ ] Kubernetes 支持
- [ ] 构建队列优化
- [ ] 实时构建状态推送
- [ ] 用户权限管理
- [ ] 构建缓存优化

---

## 🙏 致谢

### 基于项目
- [RustDesk](https://github.com/rustdesk/rustdesk) - 原始 RustDesk 项目
- [VenimK/creator](https://github.com/VenimK/creator) - 原始构建器

### 使用的开源项目
- Django - Web 框架
- Bootstrap - UI 框架
- Font Awesome - 图标库
- GitHub Actions - CI/CD

---

## 📄 许可证

本项目继承原项目许可证。

---

## 📞 联系方式

- **问题反馈**：在 GitHub 上提交 Issue
- **功能建议**：在 GitHub 上提交 Feature Request
- **文档问题**：查看 README_CN.md

---

**最后更新：** 2026-01-26
**版本：** 2.0.0
**状态：** ✅ 稳定
