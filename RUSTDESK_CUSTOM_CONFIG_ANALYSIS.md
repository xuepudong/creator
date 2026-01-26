# RuijieDesk 配置支持分析报告

## 📊 总览

基于 RustDesk 官方代码分析（libs/hbb_common/src/config.rs），我们添加的配置项中：

- **✅ 已支持**: 20个配置项
- **❌ 需魔改**: 13个配置项
- **总计**: 33个新增配置项

---

## ✅ 官方RustDesk已支持的配置（无需魔改）

这些配置可以直接使用，会被RustDesk正确识别和应用：

### 1. **显示设置**（KEYS_DISPLAY_SETTINGS）
| 配置键 | 功能 | forms.py字段 |
|--------|------|--------------|
| `view-only` | 仅浏览模式 | viewOnly |
| `collapse-toolbar` | 折叠工具栏 | collapse_toolbar |
| `privacy-mode` | 隐私模式 | privacy_mode |
| `image-quality` | 图像质量 | image_quality |
| `custom-fps` | 自定义帧率 | custom_fps |
| `sync-init-clipboard` | 同步初始剪贴板 | sync_init_clipboard |

### 2. **本地设置**（KEYS_LOCAL_SETTINGS）
| 配置键 | 功能 | forms.py字段 |
|--------|------|--------------|
| `use-texture-render` | 纹理渲染 | use_texture_render |
| `allow-d3d-render` | D3D渲染 | allowD3dRender |
| `pre-elevate-service` | 自动提权 | pre_elevate_service |

### 3. **服务器设置**（KEYS_SETTINGS）
| 配置键 | 功能 | forms.py字段 |
|--------|------|--------------|
| `enable-keyboard` | 启用键盘 | enableKeyboard |
| `enable-clipboard` | 启用剪贴板 | enableClipboard |
| `enable-file-transfer` | 启用文件传输 | enableFileTransfer |
| `enable-audio` | 启用音频 | enableAudio |
| `enable-tunnel` | 启用TCP隧道 | enableTCP |
| `enable-remote-restart` | 启用远程重启 | enableRemoteRestart |
| `enable-record-session` | 启用会话录制 | enableRecording |
| `enable-block-input` | 启用输入锁定 | enableBlockingInput |
| `allow-remote-config-modification` | 允许远程修改配置 | enableRemoteModi |
| `enable-remote-printer` | 启用远程打印 | enablePrinter |
| `enable-camera` | 启用摄像头 | enableCamera |
| `enable-terminal` | 启用终端 | enableTerminal |
| `enable-lan-discovery` | 启用局域网发现 | denyLan (反向) |
| `direct-server` | 直接服务器 | enableDirectIP |
| `allow-auto-disconnect` | 允许自动断开 | autoClose |
| `allow-remove-wallpaper` | 允许移除壁纸 | removeWallpaper |
| `approve-mode` | 认证方式 | passApproveMode |

### 4. **内建设置**（KEYS_BUILDIN_SETTINGS）
| 配置键 | 功能 | forms.py字段 |
|--------|------|--------------|
| `remove-preset-password-warning` | 移除密码警告 | remove_preset_password_warning |
| `hide-security-settings` | 隐藏安全设置 | hideSecuritySettings |
| `hide-network-settings` | 隐藏网络设置 | hideNetworkSettings |
| `hide-server-settings` | 隐藏服务器设置 | hideServerSettings |
| `hide-proxy-settings` | 隐藏代理设置 | hideProxySettings |
| `hide-remote-printer-settings` | 隐藏远程打印设置 | hideRemotePrinterSettings |
| `hide-websocket-settings` | 隐藏WebSocket设置 | hideWebsocketSettings |
| `hide-username-on-card` | 隐藏用户名 | hide_username_on_card |
| `hide-tray` | 隐藏托盘图标 | hideTray |
| `allow-hostname-as-id` | 主机名作为ID | allowHostnameAsId |
| `hide-powered-by-me` | 隐藏技术支持标识 | hide_powered_by_me |

---

## ❌ 需要魔改RustDesk的配置

这些配置目前在RustDesk源码中**不存在**，需要我们添加代码支持：

### 优先级1：UI相关（前端修改）

| 配置键 | 功能 | forms.py字段 | 需要修改的文件 |
|--------|------|--------------|----------------|
| `hide-chat-voice` | 隐藏聊天与语音 | hide_chat_voice | flutter/lib/desktop/pages/remote_page.dart |
| `hide-password` | 隐藏临时密码面板 | hidePassword | flutter/lib/desktop/pages/connection_page.dart |
| `hide-menu-bar` | 隐藏设置菜单 | hideMenuBar | flutter/lib/desktop/pages/connection_page.dart |
| `hide-quit` | 隐藏退出按钮 | hideQuit | flutter/lib/desktop/pages/connection_page.dart |
| `add-copy` | 添加复制按钮 | addcopy | flutter/lib/desktop/pages/connection_page.dart |
| `hide-service-start-stop` | 隐藏服务启停 | hideService_Start_Stop | flutter/lib/desktop/pages/server_page.dart |

### 优先级2：功能逻辑（后端修改）

| 配置键 | 功能 | forms.py字段 | 需要修改的文件 |
|--------|------|--------------|----------------|
| `disable-check-update` | 禁用检查更新 | disable_check_update | src/ui_interface.rs, flutter/lib/common/widgets/update.dart |
| `apply-privacy` | 禁止退出隐私模式 | applyprivacy | src/server/connection.rs |
| `pass-policy` | 允许简单密码 | passpolicy | libs/hbb_common/src/password_security.rs |
| `unlock-pin` | 配置PIN | unlockPin | src/ui_interface.rs, flutter/lib/common/widgets/pin_input.dart |

### 优先级3：安装相关（构建脚本修改）

| 配置键 | 功能 | forms.py字段 | 需要修改的文件 |
|--------|------|--------------|----------------|
| `no-uninstall` | 不创建卸载快捷方式 | no_uninstall | .github/workflows/generator-*.yml, build.py |
| `disable-install` | 生成便携版 | disable_install | build.py, res/msi/Package.wxs |

### 优先级4：资源文件（需要特殊处理）

| 配置键 | 功能 | forms.py字段 | 需要修改的文件 |
|--------|------|--------------|----------------|
| `privacy-wallpaper` | 隐私背景图 | privacy_wallpaper | src/privacy_mode.rs, 资源打包 |

---

## 🔧 实现方案

### 方案A：最小修改（推荐）
**只保留官方支持的配置，删除需要魔改的13个**

**优点：**
- ✅ 无需修改RustDesk源码
- ✅ 稳定可靠，兼容性好
- ✅ 易于维护，跟随官方更新

**缺点：**
- ❌ 功能较少

**实施步骤：**
1. 修改 `rdgenerator/forms.py`，删除13个不支持的字段
2. 修改 `rdgenerator/views.py`，删除对应的处理逻辑
3. 修改 `rdgenerator/templates/generator.html`，删除对应的UI元素
4. 测试验证

### 方案B：完整魔改（功能完整）
**Fork RustDesk并添加所有功能支持**

**优点：**
- ✅ 功能完整，所有配置都可用
- ✅ 完全自主可控

**缺点：**
- ❌ 开发工作量大（约3-5天）
- ❌ 需要维护魔改分支
- ❌ 跟随官方更新困难

**实施步骤：**
1. 在你的 RuijieDesk 仓库中添加功能支持
2. 修改 `.github/workflows/generator-*.yml` 使用你的仓库
3. 测试所有功能
4. 定期合并官方更新

### 方案C：混合方案（平衡）
**保留关键功能，删除不重要的**

**保留的魔改功能（约5-7个高优先级）：**
- hide-chat-voice
- disable-check-update
- hide-password
- hide-menu-bar
- privacy-wallpaper

**删除的功能（低优先级）：**
- hide-quit, add-copy, apply-privacy, pass-policy
- hide-service-start-stop, no-uninstall, disable-install

---

## 📝 魔改代码模板

### 示例1: 添加 `hide-chat-voice` 支持

#### 1. 在 config.rs 中添加配置键：
```rust
// libs/hbb_common/src/config.rs Line ~2660
pub const OPTION_HIDE_CHAT_VOICE: &str = "hide-chat-voice";

// 添加到 KEYS_BUILDIN_SETTINGS 数组中 Line ~2836
pub const KEYS_BUILDIN_SETTINGS: &[&str] = &[
    // ... 其他配置
    OPTION_HIDE_CHAT_VOICE,
];
```

#### 2. 在 Flutter UI 中使用：
```dart
// flutter/lib/desktop/pages/remote_page.dart
import 'package:get/get.dart';

// 在工具栏构建逻辑中：
Widget _buildToolbar() {
  final hideChat = bind.mainGetBuiltinOption(key: 'hide-chat-voice') == 'Y';

  return Row(
    children: [
      if (!hideChat) IconButton(
        icon: Icon(Icons.chat),
        onPressed: () => _showChatDialog(),
      ),
      // 其他按钮...
    ],
  );
}
```

### 示例2: 添加 `disable-check-update` 支持

#### 1. 在 config.rs 中添加配置键：
```rust
// libs/hbb_common/src/config.rs Line ~2694
pub const OPTION_DISABLE_CHECK_UPDATE: &str = "disable-check-update";

// 添加到 KEYS_LOCAL_SETTINGS
```

#### 2. 在更新检查逻辑中使用：
```rust
// src/ui_interface.rs
pub fn should_check_update() -> bool {
    if get_builtin_option("disable-check-update") == "Y" {
        return false;
    }
    Config::get_bool_option("enable-check-update")
}
```

---

## 🎯 我的建议

**建议采用方案C（混合方案）：**

1. **第一阶段**（立即实施）：
   - 保留20个官方支持的配置
   - 删除13个需要魔改的配置
   - 确保系统稳定运行

2. **第二阶段**（2-3周后）：
   - 评估用户反馈，确定最需要的5-7个功能
   - 在RuijieDesk中逐步实现这些功能
   - 充分测试后发布

3. **长期维护**：
   - 保持与官方RustDesk同步更新
   - 维护最小化的魔改补丁集

---

## 📋 下一步行动

### 选择方案A（推荐）：
```bash
# 1. 立即清理不支持的配置
cd /Users/xuepudong/kaifa/creator

# 2. 我可以帮你自动删除这13个字段
# 3. 测试验证
# 4. 提交代码
```

### 选择方案B：
```bash
# 1. 开始魔改RuijieDesk
cd /Users/xuepudong/kaifa/RuijieDesk

# 2. 我可以帮你逐个实现这些功能
# 3. 修改workflow指向你的仓库
```

### 选择方案C：
```bash
# 1. 先清理低优先级的8个配置
# 2. 保留5个高优先级的功能待实现
# 3. 分阶段开发测试
```

**你倾向于哪个方案？** 我可以立即帮你开始实施。
