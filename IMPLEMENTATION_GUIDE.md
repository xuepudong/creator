# 🔧 RuijieDesk 自定义功能实现指南

## ✅ 第一阶段完成：配置键定义

已完成以下工作：
- ✅ 在 `libs/hbb_common/src/config.rs` 中添加13个新配置键
- ✅ 配置键已分配到正确的类别（BUILTIN/LOCAL/SETTINGS）
- ✅ 修改所有workflow文件使用 `xuepudong/RuijieDesk` 仓库
- ✅ 推送到GitHub

## 📋 配置键定义列表

```rust
// Line ~2661-2673 in libs/hbb_common/src/config.rs
pub const OPTION_HIDE_CHAT_VOICE: &str = "hide-chat-voice";
pub const OPTION_DISABLE_CHECK_UPDATE: &str = "disable-check-update";
pub const OPTION_HIDE_PASSWORD: &str = "hide-password";
pub const OPTION_HIDE_MENU_BAR: &str = "hide-menu-bar";
pub const OPTION_HIDE_QUIT: &str = "hide-quit";
pub const OPTION_ADD_COPY: &str = "add-copy";
pub const OPTION_APPLY_PRIVACY: &str = "apply-privacy";
pub const OPTION_PASS_POLICY: &str = "pass-policy";
pub const OPTION_HIDE_SERVICE_START_STOP: &str = "hide-service-start-stop";
pub const OPTION_NO_UNINSTALL: &str = "no-uninstall";
pub const OPTION_DISABLE_INSTALL: &str = "disable-install";
pub const OPTION_UNLOCK_PIN: &str = "unlock-pin";
pub const OPTION_PRIVACY_WALLPAPER: &str = "privacy-wallpaper";
```

---

## 🚀 第二阶段：功能实现计划

### 优先级1：UI隐藏功能（Flutter前端）

#### 1. hide-chat-voice - 隐藏聊天与语音按钮

**文件**: `flutter/lib/desktop/pages/remote_page.dart`

**实现位置**: 工具栏构建逻辑

```dart
// 搜索 "IconButton" 或 "chat" 找到聊天按钮
Widget buildToolbar() {
  final hideChat = bind.mainGetBuiltinOption(key: 'hide-chat-voice') == 'Y';

  return Row(
    children: [
      if (!hideChat) // 添加条件
        IconButton(
          icon: Icon(Icons.chat),
          onPressed: () => showChatOverlay(),
        ),
      // 其他按钮...
    ],
  );
}
```

**测试方法**:
1. 在custom.txt中添加: `"hide-chat-voice": "Y"`
2. 启动RustDesk
3. 连接远程桌面
4. 确认工具栏中没有聊天按钮

---

#### 2. hide-password - 隐藏临时密码面板

**文件**: `flutter/lib/desktop/pages/connection_page.dart`

**实现位置**: 主页ID输入区域

```dart
// 搜索 "password" 或 "连接密码" 找到密码显示组件
Widget buildConnectionCard() {
  final hidePassword = bind.mainGetBuiltinOption(key: 'hide-password') == 'Y';

  return Column(
    children: [
      // ID输入框
      TextField(...),

      // 密码显示区域
      if (!hidePassword) // 添加条件
        Container(
          child: Text('Your password: xxxxx'),
        ),
    ],
  );
}
```

---

#### 3. hide-menu-bar - 隐藏设置菜单

**文件**: `flutter/lib/desktop/pages/connection_page.dart`

**实现位置**: 顶部菜单栏

```dart
Widget buildMenuBar() {
  final hideMenu = bind.mainGetBuiltinOption(key: 'hide-menu-bar') == 'Y';

  if (hideMenu) {
    return SizedBox.shrink(); // 返回空widget
  }

  return MenuBar(...); // 原有菜单栏
}
```

---

#### 4. hide-quit - 隐藏退出按钮

**文件**: `flutter/lib/desktop/pages/remote_page.dart`

**实现位置**: 远程连接窗口的关闭按钮

```dart
Widget buildCloseButton() {
  final hideQuit = bind.mainGetBuiltinOption(key: 'hide-quit') == 'Y';

  if (hideQuit) {
    return SizedBox.shrink();
  }

  return IconButton(
    icon: Icon(Icons.close),
    onPressed: () => closeConnection(),
  );
}
```

---

#### 5. add-copy - 添加复制按钮

**文件**: `flutter/lib/desktop/pages/connection_page.dart`

**实现位置**: ID/密码显示区域旁边

```dart
Widget buildPasswordDisplay() {
  final addCopy = bind.mainGetBuiltinOption(key: 'add-copy') == 'Y';

  return Row(
    children: [
      Text('Password: $password'),
      if (addCopy)
        IconButton(
          icon: Icon(Icons.copy),
          onPressed: () {
            Clipboard.setData(ClipboardData(text: password));
            showToast('已复制到剪贴板');
          },
        ),
    ],
  );
}
```

---

#### 6. hide-service-start-stop - 隐藏服务启停按钮

**文件**: `flutter/lib/desktop/pages/server_page.dart`

**实现位置**: 服务器设置页面

```dart
Widget buildServiceControls() {
  final hideService = bind.mainGetBuiltinOption(key: 'hide-service-start-stop') == 'Y';

  if (hideService) {
    return SizedBox.shrink();
  }

  return Row(
    children: [
      ElevatedButton(
        child: Text('启动服务'),
        onPressed: () => startService(),
      ),
      ElevatedButton(
        child: Text('停止服务'),
        onPressed: () => stopService(),
      ),
    ],
  );
}
```

---

### 优先级2：功能逻辑修改

#### 7. disable-check-update - 禁用更新检查

**文件1**: `src/ui_interface.rs`

```rust
// 搜索 "check_software_update" 或类似函数
pub fn should_check_update() -> bool {
    // 添加这个检查
    if get_builtin_option("disable-check-update") == "Y" {
        return false;
    }

    // 原有逻辑
    Config::get_option("enable-check-update") != "N"
}
```

**文件2**: `flutter/lib/common/widgets/update.dart`

```dart
Future<void> checkUpdate() async {
  final disableUpdate = bind.mainGetBuiltinOption(key: 'disable-check-update') == 'Y';
  if (disableUpdate) {
    return; // 直接返回，不检查更新
  }

  // 原有更新检查逻辑
  final hasUpdate = await api.checkForUpdate();
  // ...
}
```

---

#### 8. apply-privacy - 禁止退出隐私模式

**文件**: `src/server/connection.rs`

```rust
// 搜索 "exit_privacy_mode" 或类似函数
pub fn can_exit_privacy_mode() -> bool {
    // 添加这个检查
    if get_builtin_option("apply-privacy") == "Y" {
        return false;
    }
    true
}

// 在退出隐私模式的函数中调用
pub fn exit_privacy_mode(&mut self) -> ResultType<()> {
    if !can_exit_privacy_mode() {
        bail!("Privacy mode is locked by administrator");
    }
    // 原有逻辑
}
```

---

#### 9. pass-policy - 允许简单密码

**文件**: `libs/hbb_common/src/password_security.rs`

```rust
// 搜索密码验证函数
pub fn validate_password(password: &str) -> ResultType<()> {
    // 添加这个检查
    if get_builtin_option("pass-policy") == "Y" {
        return Ok(()); // 允许任何密码
    }

    // 原有的复杂密码验证逻辑
    if password.len() < 8 {
        bail!("Password must be at least 8 characters");
    }
    // ...
}
```

---

#### 10. unlock-pin - 配置PIN码

**文件**: `src/ui_interface.rs`

```rust
// 在Config中添加PIN码验证函数
pub fn verify_unlock_pin(input_pin: &str) -> bool {
    let configured_pin = Config::get_option("unlock-pin");
    if configured_pin.is_empty() {
        return true; // 没有配置PIN，允许访问
    }
    input_pin == configured_pin
}
```

**Flutter端**: `flutter/lib/common/widgets/pin_input.dart`

```dart
Future<bool> showPinDialog() async {
  final configuredPin = bind.mainGetOption(key: 'unlock-pin');
  if (configuredPin.isEmpty) {
    return true; // 没有配置PIN
  }

  final inputPin = await showDialog<String>(
    context: context,
    builder: (context) => PinInputDialog(),
  );

  return inputPin == configuredPin;
}
```

---

### 优先级3：构建相关

#### 11. no-uninstall - 不创建卸载快捷方式

**文件**: `.github/workflows/generator-windows.yml`

**修改位置**: Windows打包步骤

```yaml
- name: Build installer
  if: env.UPLOAD_ARTIFACT == 'true'
  shell: bash
  run: |
    # 读取配置
    NO_UNINSTALL=$(echo "${{ inputs.custom }}" | base64 -d | jq -r '."no-uninstall" // "N"')

    pushd ./libs/portable
    pip3 install -r requirements.txt

    if [ "$NO_UNINSTALL" = "Y" ]; then
      # 不创建卸载快捷方式
      python3 ./generate.py --skip-uninstall
    else
      python3 ./generate.py
    fi

    popd
```

**或修改打包脚本**: `libs/portable/generate.py`

```python
import json
import base64
import sys

# 读取custom配置
custom_config = json.loads(base64.b64decode(os.environ.get('CUSTOM_CONFIG', '')))
no_uninstall = custom_config.get('no-uninstall') == 'Y'

if not no_uninstall:
    # 创建卸载快捷方式
    create_uninstall_shortcut()
```

---

#### 12. disable-install - 生成便携版

**文件**: `build.py`

```python
# 搜索 "portable" 或构建类型判断
def should_create_installer():
    custom_config = os.environ.get('CUSTOM_CONFIG', '')
    if custom_config:
        config = json.loads(base64.b64decode(custom_config))
        if config.get('disable-install') == 'Y':
            return False  # 只生成便携版，不生成安装程序
    return True

# 在构建逻辑中使用
if should_create_installer():
    build_installer()
else:
    # 只复制可执行文件，不打包安装程序
    shutil.copy('rustdesk.exe', f'{output_dir}/rustdesk-portable.exe')
```

---

#### 13. privacy-wallpaper - 隐私模式背景图

**文件**: `src/privacy_mode.rs`

```rust
use image::ImageReader;

pub fn get_privacy_wallpaper() -> Option<Vec<u8>> {
    // 1. 检查是否配置了自定义壁纸
    let wallpaper_url = get_builtin_option("privacy-wallpaper");
    if wallpaper_url.is_empty() || wallpaper_url == "false" {
        return None;
    }

    // 2. 下载壁纸（在构建时已下载到本地）
    let wallpaper_path = Path::new("resources/privacy_wallpaper.png");
    if !wallpaper_path.exists() {
        log::warn!("Privacy wallpaper not found: {:?}", wallpaper_path);
        return None;
    }

    // 3. 读取并返回图片数据
    match std::fs::read(wallpaper_path) {
        Ok(data) => Some(data),
        Err(e) => {
            log::error!("Failed to read privacy wallpaper: {}", e);
            None
        }
    }
}

// 在隐私模式激活时使用
pub fn enter_privacy_mode() {
    if let Some(wallpaper_data) = get_privacy_wallpaper() {
        set_wallpaper(&wallpaper_data);
    } else {
        // 使用默认黑色背景
        set_default_privacy_wallpaper();
    }
}
```

**构建时下载**: 在workflow中添加步骤

```yaml
- name: Download privacy wallpaper
  if: ${{ inputs.extras != '{}' }}
  run: |
    PRIVACY_LINK=$(echo '${{ inputs.extras }}' | jq -r '.privacylink // "false"')
    if [ "$PRIVACY_LINK" != "false" ]; then
      curl -o ./resources/privacy_wallpaper.png "$PRIVACY_LINK"
    fi
```

---

## 🧪 测试计划

### 1. 本地测试（开发环境）

```bash
# 1. 创建测试配置文件
cd /Users/xuepudong/kaifa/RuijieDesk
cat > custom.txt << 'EOF'
{
  "app-name": "RuijieDesk",
  "hide-chat-voice": "Y",
  "disable-check-update": "Y",
  "hide-password": "Y",
  "unlock-pin": "1234"
}
EOF

# 2. 构建并运行
python3 build.py --flutter --skip-portable-pack

# 3. 测试功能
./target/release/rustdesk
```

### 2. CI/CD测试（GitHub Actions）

触发一个测试构建：
```bash
cd /Users/xuepudong/kaifa/creator
# 通过Web界面提交一个配置，勾选所有新功能
# 检查GitHub Actions构建日志
```

---

## 📝 实现进度追踪

| 功能 | 配置键 | 状态 | 文件 | 备注 |
|------|--------|------|------|------|
| 配置键定义 | 所有 | ✅ 完成 | config.rs | 已推送到GitHub |
| Workflow更新 | - | ✅ 完成 | workflow/*.yml | 已使用RuijieDesk |
| 禁用更新检查 | disable-check-update | ✅ 完成 | src/updater.rs | 已实现并推送 |
| 允许简单密码 | pass-policy | ✅ 完成 | desktop_home_page.dart | 已实现并推送 |
| 禁止退出隐私 | apply-privacy | ✅ 完成 | server/connection.rs | 已实现并推送 |
| 隐藏聊天语音 | hide-chat-voice | ✅ 完成 | remote_toolbar.dart | 已实现并推送 |
| 隐藏退出按钮 | hide-quit | ✅ 完成 | remote_toolbar.dart | 已实现并推送 |
| 隐藏密码面板 | hide-password | ✅ 完成 | desktop_home_page.dart | 已实现并推送 |
| 添加复制按钮 | add-copy | ✅ 完成 | desktop_home_page.dart | 已实现并推送 |
| 隐藏设置菜单 | hide-menu-bar | ✅ 完成 | desktop_tab_page.dart | 已实现并推送 |
| 隐藏服务启停 | hide-service-start-stop | ✅ 完成 | connection_page.dart | 已实现并推送 |
| 配置PIN | unlock-pin | ⏳ 待实现 | ui_interface.rs + Flutter UI | 需要PIN输入对话框 |
| 不创建卸载 | no-uninstall | ⏳ 待实现 | workflow/*.yml | 需要修改打包逻辑 |
| 生成便携版 | disable-install | ⏳ 待实现 | build.py | 需要修改构建脚本 |
| 隐私背景图 | privacy-wallpaper | ⏳ 待实现 | privacy_mode.rs | 需要资源下载+应用 |

---

## 🎉 已完成功能详情

### 1. disable-check-update - 禁用更新检查
**文件**: `src/updater.rs`
**实现**:
- 在 `start_auto_update_check_()` 和 `check_update()` 函数开始处检查配置
- 读取 `BUILTIN_SETTINGS['disable-check-update']`
- 如果设置为 'Y'，直接返回，不执行更新检查

### 2. pass-policy - 允许简单密码
**文件**: `flutter/lib/desktop/pages/desktop_home_page.dart`
**实现**:
- 在 `setPasswordDialog()` 的 `submit()` 函数中添加检查
- 读取 `mainGetBuiltinOption('pass-policy')`
- 如果为 'Y'，跳过密码复杂度验证规则

### 3. apply-privacy - 禁止退出隐私模式
**文件**: `src/server/connection.rs`
**实现**:
- 在 `turn_off_privacy()` 函数开始处添加检查
- 读取 `BUILTIN_SETTINGS['apply-privacy']`
- 如果为 'Y'，返回错误消息，阻止退出隐私模式

### 4. hide-chat-voice - 隐藏聊天与语音按钮
**文件**: `flutter/lib/desktop/widgets/remote_toolbar.dart`
**实现**:
- 在工具栏构建逻辑中添加条件判断
- 只有当 `mainGetBuiltinOption('hide-chat-voice')` 不为 'Y' 时才添加 _ChatMenu 和 _VoiceCallMenu

### 5. hide-quit - 隐藏退出按钮
**文件**: `flutter/lib/desktop/widgets/remote_toolbar.dart`
**实现**:
- 在工具栏构建逻辑中添加条件判断
- 只有当 `mainGetBuiltinOption('hide-quit')` 不为 'Y' 时才添加 _CloseMenu

### 6. hide-password - 隐藏临时密码面板
**文件**: `flutter/lib/desktop/pages/desktop_home_page.dart`
**实现**:
- 在主页面布局中添加条件渲染
- 只有当 `mainGetBuiltinOption('hide-password')` 不为 'Y' 时才显示 buildPasswordBoard()

### 7. add-copy - 添加复制按钮
**文件**: `flutter/lib/desktop/pages/desktop_home_page.dart`
**实现**:
- 在密码显示区域添加复制按钮
- 当 `mainGetBuiltinOption('add-copy')` 为 'Y' 时显示
- 点击按钮复制密码到剪贴板

### 8. hide-menu-bar - 隐藏设置菜单
**文件**: `flutter/lib/desktop/pages/desktop_tab_page.dart`
**实现**:
- 在 Settings 按钮的 offstage 条件中添加检查
- 当 `mainGetBuiltinOption('hide-menu-bar')` 为 'Y' 时隐藏设置按钮

### 9. hide-service-start-stop - 隐藏服务启停按钮
**文件**: `flutter/lib/desktop/pages/connection_page.dart`
**实现**:
- 在 startServiceWidget() 的 offstage 条件中添加检查
- 当 `mainGetBuiltinOption('hide-service-start-stop')` 为 'Y' 时隐藏启动服务按钮

---

## 🎯 下一步行动

### 立即行动（今天）
1. ✅ 配置键定义 - 已完成
2. ✅ Workflow修改 - 已完成
3. 🔄 提交creator的修改到GitHub

### 明天开始
4. 实现UI隐藏功能（优先级1，6个功能）
5. 实现功能逻辑修改（优先级2，4个功能）
6. 实现构建相关功能（优先级3，3个功能）

### 推荐实现顺序
1. **disable-check-update** - 最简单，影响最大
2. **hide-password** - UI简单修改
3. **hide-chat-voice** - UI简单修改
4. **add-copy** - 添加新功能，用户友好
5. **hide-menu-bar** - UI修改
6. **unlock-pin** - 安全功能
7. **其他功能** - 按需实现

---

## 🚀 快速开始实现

想立即开始实现第一个功能吗？我建议从 **disable-check-update** 开始：

```bash
# 1. 打开文件
code /Users/xuepudong/kaifa/RuijieDesk/src/ui_interface.rs

# 2. 搜索 "check_software_update"

# 3. 添加判断逻辑（见上面的代码示例）

# 4. 测试
python3 build.py --flutter
```

**要不要现在开始实现这些功能？** 我可以逐个帮你实现！
