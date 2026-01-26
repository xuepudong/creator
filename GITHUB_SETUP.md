# 🔧 GitHub配置指南

## ✅ 已完成的功能（10个）

以下功能已经完全实现并推送到 `xuepudong/RuijieDesk` 仓库：

### 后端功能（4个）
1. ✅ **disable-check-update** - 禁用更新检查
2. ✅ **pass-policy** - 允许简单密码
3. ✅ **apply-privacy** - 禁止退出隐私模式
4. ✅ **no-uninstall** - 不创建卸载快捷方式

### 前端UI功能（6个）
5. ✅ **hide-chat-voice** - 隐藏聊天与语音按钮
6. ✅ **hide-quit** - 隐藏退出按钮
7. ✅ **hide-password** - 隐藏临时密码面板
8. ✅ **add-copy** - 添加复制按钮
9. ✅ **hide-menu-bar** - 隐藏设置菜单
10. ✅ **hide-service-start-stop** - 隐藏服务启停按钮

---

## 📋 GitHub需要做的配置

### 1. Creator仓库（Web前端）

#### 仓库：`https://github.com/VenimK/creator`

**问题**：当前用户 `xuepudong` 没有push权限

**需要做的**：
```bash
# 方法1: 如果VenimK是你的另一个账号，切换到那个账号
cd /Users/xuepudong/kaifa/creator
git remote set-url origin https://github.com/VenimK/creator.git
git push origin master

# 方法2: Fork到xuepudong账号
# 在GitHub上fork VenimK/creator 到 xuepudong/creator
git remote set-url origin https://github.com/xuepudong/creator.git
git push origin master

# 方法3: 添加VenimK账号的GitHub token
git remote set-url origin https://<TOKEN>@github.com/VenimK/creator.git
git push origin master
```

**需要push的内容**：
- `IMPLEMENTATION_GUIDE.md` - 实现进度文档（已更新到10/13）
- `.github/workflows/*.yml` - 已修改为使用 `xuepudong/RuijieDesk`

---

### 2. RuijieDesk仓库（RustDesk源代码）

#### 仓库：`https://github.com/xuepudong/RuijieDesk`

✅ **状态**：已完成，所有代码已推送

**提交历史**：
```
290f51a - Implement no-uninstall feature
706f697 - Implement hide-menu-bar and hide-service-start-stop UI features
55e288e - Implement hide-quit, hide-password, and add-copy UI features
1ebcdd4 - Implement apply-privacy and hide-chat-voice features
6c70872 - Implement disable-check-update and pass-policy features
1462fcf - Add 13 new configuration keys to config.rs
```

**修改的文件**：
- `libs/hbb_common/src/config.rs` - 新增13个配置键
- `src/updater.rs` - 禁用更新检查
- `src/server/connection.rs` - 禁止退出隐私模式
- `src/platform/windows.rs` - 不创建卸载快捷方式
- `flutter/lib/desktop/pages/desktop_home_page.dart` - 密码相关UI
- `flutter/lib/desktop/pages/desktop_tab_page.dart` - 隐藏设置菜单
- `flutter/lib/desktop/pages/connection_page.dart` - 隐藏服务按钮
- `flutter/lib/desktop/widgets/remote_toolbar.dart` - 工具栏UI

---

## 🧪 测试步骤

### 1. 确认Creator可以访问

访问你的Creator Web界面：`http://localhost:21114` 或部署的URL

### 2. 提交测试构建

在Creator界面填写表单：

**基础配置**：
- App Name: `TestDesk`
- Server: `你的服务器地址`
- Key: `你的密钥`

**自定义功能** (勾选测试)：
- ✅ 禁用启动时检查更新
- ✅ 允许简单密码
- ✅ 禁止退出隐私模式
- ✅ 隐藏聊天与语音功能
- ✅ 隐藏关闭按钮
- ✅ 隐藏临时密码面板
- ✅ 显示密码复制按钮
- ✅ 隐藏设置菜单
- ✅ 隐藏服务启停按钮
- ✅ 不创建卸载快捷方式

**平台**：选择 Windows

### 3. 查看构建结果

1. 进入GitHub Actions页面
2. 找到刚触发的workflow run
3. 等待构建完成（约15-30分钟）
4. 下载生成的exe文件

### 4. 验证功能

安装并运行生成的客户端，验证：

- ✅ 启动时不检查更新
- ✅ 可以设置简单密码（如"123"）
- ✅ 远程工具栏没有聊天、语音、关闭按钮
- ✅ 主页没有临时密码面板，或有复制按钮
- ✅ 没有设置菜单按钮
- ✅ 开始菜单没有"Uninstall XXX"快捷方式
- ✅ 隐私模式无法被远程用户退出
- ✅ 没有服务启动/停止按钮

---

## 🔄 同步Creator和RuijieDesk的步骤

### Creator → RuijieDesk 数据流

```
用户在Creator填写表单
    ↓
生成custom.txt配置 (Base64 + JSON)
    ↓
通过GitHub API触发Actions
    ↓
Actions checkout xuepudong/RuijieDesk
    ↓
将custom.txt放入构建目录
    ↓
编译时读取配置并应用
    ↓
生成自定义客户端
```

### 关键代码位置

**Creator (Django)**：
- `rdgenerator/views.py` - 处理表单并调用GitHub API
- `rdgenerator/forms.py` - 表单字段定义
- `.github/workflows/*.yml` - workflow定义

**RuijieDesk (Rust/Flutter)**：
- `libs/hbb_common/src/config.rs` - 配置键定义
- `src/common.rs` - 读取custom.txt的load_custom_client()
- 各功能实现文件（见上述修改文件列表）

---

## ⚠️ 重要提示

### 配置键映射

Creator表单字段 → custom.txt JSON键 → RustDesk config常量：

| Creator字段 | custom.txt键 | config.rs常量 |
|------------|--------------|---------------|
| disable_check_update | "disable-check-update" | OPTION_DISABLE_CHECK_UPDATE |
| pass_policy | "pass-policy" | OPTION_PASS_POLICY |
| hide_chat_voice | "hide-chat-voice" | OPTION_HIDE_CHAT_VOICE |
| hide_quit | "hide-quit" | OPTION_HIDE_QUIT |
| hide_password | "hide-password" | OPTION_HIDE_PASSWORD |
| hide_menu_bar | "hide-menu-bar" | OPTION_HIDE_MENU_BAR |
| add_copy | "add-copy" | OPTION_ADD_COPY |
| apply_privacy | "apply-privacy" | OPTION_APPLY_PRIVACY |
| hide_service_start_stop | "hide-service-start-stop" | OPTION_HIDE_SERVICE_START_STOP |
| no_uninstall | "no-uninstall" | OPTION_NO_UNINSTALL |

### 配置值格式

所有布尔配置使用字符串：
- 启用：`"Y"`
- 禁用：`"N"` 或不设置

读取示例：
```rust
// Rust
let is_enabled = config::BUILTIN_SETTINGS
    .read()
    .unwrap()
    .get(config::keys::OPTION_XXX)
    .map(|v| v == "Y")
    .unwrap_or(false);
```

```dart
// Flutter
final isEnabled = bind.mainGetBuiltinOption(key: 'option-name') == 'Y';
```

---

## 📦 下一步开发（剩余3个功能）

### 11. unlock-pin - 配置PIN码 ⏳
**难度**：中等
**需要**：
- Flutter PIN输入对话框UI
- 启动时验证逻辑
- 设置界面PIN配置

**实现位置**：
- `flutter/lib/common/widgets/pin_dialog.dart` (新建)
- `src/ui_interface.rs` - 验证逻辑
- `flutter/lib/desktop/pages/desktop_home_page.dart` - 启动验证

### 12. disable-install - 只生成便携版 ⏳
**难度**：低
**需要**：
- Workflow检测配置
- 跳过安装程序生成步骤

**实现位置**：
- `.github/workflows/generator-windows*.yml`
- 修改artifact上传逻辑

### 13. privacy-wallpaper - 隐私模式背景图 ⏳
**难度**：高
**需要**：
- Workflow下载图片到resources
- 隐私模式激活时设置壁纸
- Windows API调用

**实现位置**：
- `.github/workflows/*.yml` - 下载步骤
- `src/privacy_mode.rs` - 应用壁纸
- `src/privacy_mode/win_topmost_window.rs` - Windows实现

---

## 🎉 总结

✅ **10个核心功能已完成**，覆盖了：
- 所有UI隐藏/显示功能
- 密码策略和权限控制
- 更新检查控制
- 安装卸载控制

🔄 **Creator需要push权限**才能完成部署

📝 **详细文档**：见 `IMPLEMENTATION_GUIDE.md`

💡 **测试建议**：先测试已完成的10个功能，确认workflow和配置系统正常工作，再继续开发剩余3个功能
