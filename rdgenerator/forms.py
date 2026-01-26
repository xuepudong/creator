from django import forms
from django.utils.safestring import mark_safe
from PIL import Image

class GenerateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为所有字段添加 form-control 类
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.URLInput, forms.NumberInput, forms.Textarea, forms.Select)):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.PasswordInput):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.FileInput):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.CheckboxInput):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-check-input'
                else:
                    field.widget.attrs['class'] = 'form-check-input'

    #Platform
    platform = forms.ChoiceField(choices=[
        ('windows','Windows 64位'),
        ('windows-x86','Windows 32位'),
        ('linux','Linux'),
        ('android','Android'),
        ('macos','macOS')
    ], initial='windows')
    version = forms.ChoiceField(
        choices=[('master','master'),('1.4.5','1.4.5'),('1.4.4','1.4.4'),('1.4.3','1.4.3'),('1.4.2','1.4.2'),('1.4.1','1.4.1'),('1.4.0','1.4.0'),('1.3.9','1.3.9'),('1.3.8','1.3.8'),('1.3.7','1.3.7'),('1.3.6','1.3.6'),('1.3.5','1.3.5'),('1.3.4','1.3.4'),('1.3.3','1.3.3')],
        initial='1.4.5',
        help_text=mark_safe("如果构建失败，请在 GitHub 上报告问题")
    )
    ui_mode = forms.BooleanField(label="启用定制版用户界面", initial=True, required=False)
    delayFix = forms.BooleanField(label="修复连接延迟", initial=True, required=False)

    #General
    exename = forms.CharField(label="配置名称（仅限英文字符）", required=True)
    appname = forms.CharField(label="应用名称", required=False)
    slogan = forms.CharField(label="自定义标语", required=False, initial="", help_text="留空则使用默认标语")
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('incoming', '仅被控'),
        ('outgoing', '仅主控'),
        ('both', '双向控制')
    ], initial='incoming')
    installation = forms.ChoiceField(label="安装行为", choices=[
        ('installationY', '否，启用安装'),
        ('installationN', '是，禁用安装')
    ], initial='installationY')
    settings = forms.ChoiceField(label="设置权限", choices=[
        ('settingsY', '否，启用设置'),
        ('settingsN', '是，禁用设置'),
        ('settingsGranular', '细粒度控制')
    ], initial='settingsY')
    androidappid = forms.CharField(label="安卓客户端标识符", required=False)

    # Granular hide settings options - Tabs
    hideGeneralSettings = forms.BooleanField(label="隐藏常规设置", initial=False, required=False)
    hideSecuritySettings = forms.BooleanField(label="隐藏安全设置", initial=False, required=False)
    hideNetworkSettings = forms.BooleanField(label="隐藏网络设置", initial=False, required=False)
    hideDisplaySettings = forms.BooleanField(label="隐藏显示设置", initial=False, required=False)
    hideAccountSettings = forms.BooleanField(label="隐藏账户设置", initial=False, required=False)
    hidePluginSettings = forms.BooleanField(label="隐藏插件设置", initial=False, required=False)
    hideRemotePrinterSettings = forms.BooleanField(label="隐藏远程打印设置", initial=False, required=False)
    # Sub-sections
    hideServerSettings = forms.BooleanField(label="隐藏服务器设置", initial=False, required=False)
    hideProxySettings = forms.BooleanField(label="隐藏代理设置", initial=False, required=False)
    hideWebsocketSettings = forms.BooleanField(label="隐藏 WebSocket 设置", initial=False, required=False)

    #  New fields
    hide_account = forms.BooleanField(label="隐藏账户设置", initial=False, required=False)
    remove_preset_password_warning = forms.BooleanField(label="隐藏密码警告", initial=True, required=False)

    #Custom Server
    serverIP = forms.CharField(label="服务器地址", required=False)
    apiServer = forms.CharField(label="API 地址", required=False)
    key = forms.CharField(label="密钥", required=False)
    urlLink = forms.CharField(label="门户网站", required=False)
    downloadLink = forms.CharField(label="更新下载链接", required=False)
    updateLink = forms.CharField(label="在线更新链接", required=False)
    compname = forms.CharField(label="公司名称", required=False)

    #Visual
    iconfile = forms.FileField(label="应用图标（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    logofile = forms.FileField(label="品牌标识（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    privacy_wallpaper = forms.FileField(label="隐私模式背景图（PNG 格式，1920×1080）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    iconbase64 = forms.CharField(required=False)
    logobase64 = forms.CharField(required=False)
    privacy_wallpaper_base64 = forms.CharField(required=False)
    theme = forms.ChoiceField(choices=[
        ('light', '浅色主题'),
        ('dark', '深色主题'),
        ('system', '跟随系统')
    ], initial='system')
    themeDorO = forms.ChoiceField(choices=[('default', '默认设置'),('override', '强制覆盖')], initial='default')
    image_quality = forms.ChoiceField(label="图像质量", choices=[
        ('best', '最佳'),
        ('balanced', '平衡'),
        ('low', '低'),
        ('custom', '自定义')
    ], initial='balanced', required=False)
    custom_fps = forms.ChoiceField(label="自定义帧率", choices=[
        ('30', '30 FPS'),
        ('60', '60 FPS'),
        ('90', '90 FPS'),
        ('120', '120 FPS')
    ], initial='30', required=False)

    #Security
    passApproveMode = forms.ChoiceField(label="认证方式", choices=[('password','通过密码接受会话'),('click','通过点击接受会话'),('password-click','两者均可')],initial='password-click')
    permanentPassword = forms.CharField(label="预设密码", widget=forms.PasswordInput(), required=False)
    unlockPin = forms.CharField(label="配置PIN", widget=forms.PasswordInput(), required=False)
    denyLan = forms.BooleanField(label="隐藏于局域网", initial=True, required=False)
    enableDirectIP = forms.BooleanField(label="启用IP访问", initial=True, required=False)
    autoClose = forms.BooleanField(label="自动关闭会话", initial=True, required=False)

    #Permissions
    permissionsDorO = forms.ChoiceField(label="权限设置模式", choices=[('default', '默认设置'),('override', '强制覆盖')], initial='default')
    permissionsType = forms.ChoiceField(label="权限预设", choices=[('custom', '自定义'),('full', '完全访问'),('view','仅共享屏幕')], initial='custom')
    enableKeyboard = forms.BooleanField(label="启用键盘控制", initial=True, required=False)
    enableClipboard = forms.BooleanField(label="启用剪贴板同步", initial=True, required=False)
    enableFileTransfer = forms.BooleanField(label="启用文件传输", initial=True, required=False)
    enableAudio = forms.BooleanField(label="启用音频传输", initial=False, required=False)
    enableTCP = forms.BooleanField(label="启用 TCP 隧道", initial=True, required=False)
    enableRemoteRestart = forms.BooleanField(label="启用远程重启", initial=True, required=False)
    enableRecording = forms.BooleanField(label="启用会话录制", initial=True, required=False)
    enableBlockingInput = forms.BooleanField(label="启用输入锁定", initial=True, required=False)
    enableRemoteModi = forms.BooleanField(label="允许远程修改配置", initial=False, required=False)
    enablePrinter = forms.BooleanField(label="启用远程打印", initial=False, required=False)
    enableCamera = forms.BooleanField(label="启用摄像头访问", initial=True, required=False)
    enableTerminal = forms.BooleanField(label="启用终端访问", initial=True, required=False)

    #Other
    removeWallpaper = forms.BooleanField(label="远程会话期间移除桌面壁纸", initial=False, required=False)

    defaultManual = forms.CharField(label="默认设置（用户可修改）", widget=forms.Textarea, required=False)
    overrideManual = forms.CharField(label="覆盖设置（用户不可修改）", widget=forms.Textarea, required=False)

    # 主控端功能
    cycleMonitor = forms.BooleanField(label="在会话顶部显示显示器切换按钮", initial=False, required=False)
    xOffline = forms.BooleanField(label="在地址簿中标记离线设备", initial=False, required=False)
    hide_chat_voice = forms.BooleanField(label="隐藏会话中的聊天与语音功能", initial=False, required=False)
    viewOnly = forms.BooleanField(label="默认以浏览模式连接会话", initial=False, required=False)
    collapse_toolbar = forms.BooleanField(label="会话启动时自动折叠工具栏", initial=False, required=False)
    privacy_mode = forms.BooleanField(label="默认进入隐私模式", initial=False, required=False)
    hide_username_on_card = forms.BooleanField(label="在连接卡片中隐藏用户名", initial=False, required=False)

    # 被控端功能
    hideTray = forms.BooleanField(label="隐藏托盘图标", initial=False, required=False)
    hidePassword = forms.BooleanField(label="隐藏临时密码面板", initial=False, required=False)
    hideMenuBar = forms.BooleanField(label="隐藏设置菜单", initial=False, required=False)
    hideQuit = forms.BooleanField(label="隐藏退出按钮", initial=False, required=False)
    addcopy = forms.BooleanField(label="添加复制按钮", initial=False, required=False)
    applyprivacy = forms.BooleanField(label="禁止被控端退出隐私模式", initial=False, required=False)
    passpolicy = forms.BooleanField(label="允许使用简单的临时密码", initial=False, required=False)
    allowHostnameAsId = forms.BooleanField(label="使用主机名作为 ID（Windows 10 及以上）", initial=False, required=False)
    hideService_Start_Stop = forms.BooleanField(label="隐藏常规和托盘的服务启停", initial=False, required=False)

    # 通用功能
    disable_check_update = forms.BooleanField(label="禁用启动时检查更新", initial=True, required=False)
    no_uninstall = forms.BooleanField(label="不创建卸载快捷方式", initial=False, required=False)
    disable_install = forms.BooleanField(label="生成便携版", initial=False, required=False)
    allowD3dRender = forms.BooleanField(label="启用 Direct3D 渲染", initial=False, required=False)
    use_texture_render = forms.BooleanField(label="启用纹理渲染（Windows 10 及以上）", initial=False, required=False)
    pre_elevate_service = forms.BooleanField(label="启动时自动提权", initial=False, required=False)
    sync_init_clipboard = forms.BooleanField(label="同步初始剪贴板内容", initial=False, required=False)
    hide_powered_by_me = forms.BooleanField(label="隐藏'技术支持'标识", initial=True, required=False)

    # 保留旧功能
    hidecm = forms.BooleanField(label="隐藏连接管理窗口", initial=False, required=False)
    statussort = forms.BooleanField(label="允许按在线状态排序", initial=False, required=False)
    removeNewVersionNotif = forms.BooleanField(label="移除版本更新通知", initial=False, required=False)

    def clean_iconfile(self):
        print("checking icon")
        image = self.cleaned_data['iconfile']
        if image:
            try:
                # Open the image using Pillow
                img = Image.open(image)

                # Check if the image is a PNG (optional, but good practice)
                if img.format != 'PNG':
                    raise forms.ValidationError("Only PNG images are allowed.")

                # Get image dimensions
                width, height = img.size

                # Check for square dimensions
                if width != height:
                    raise forms.ValidationError("Custom App Icon dimensions must be square.")
                
                return image
            except OSError:  # Handle cases where the uploaded file is not a valid image
                raise forms.ValidationError("Invalid icon file.")
            except Exception as e: # Catch any other image processing errors
                raise forms.ValidationError(f"Error processing icon: {e}")