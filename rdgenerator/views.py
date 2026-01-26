import io
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
import os
import re
import requests
import base64
import json
import uuid
from django.conf import settings as _settings
from django.db.models import Q
from .forms import GenerateForm
from .models import GithubRun
from PIL import Image
from urllib.parse import quote
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def generator_view(request):
    if request.method == 'POST':
        form = GenerateForm(request.POST, request.FILES)
        if form.is_valid():
            platform = form.cleaned_data['platform']
            version = form.cleaned_data['version']
            ui_mode = form.cleaned_data['ui_mode']
            delayFix = form.cleaned_data['delayFix']
            cycleMonitor = form.cleaned_data['cycleMonitor']
            xOffline = form.cleaned_data['xOffline']
            hidecm = form.cleaned_data['hidecm']
            statussort = form.cleaned_data['statussort']
            removeNewVersionNotif = form.cleaned_data['removeNewVersionNotif']
            server = form.cleaned_data['serverIP']
            key = form.cleaned_data['key']
            apiServer = form.cleaned_data['apiServer']
            urlLink = form.cleaned_data['urlLink']
            downloadLink = form.cleaned_data['downloadLink']
            updateLink = form.cleaned_data.get('updateLink', '')
            unlockPin = form.cleaned_data.get('unlockPin', '')
            image_quality = form.cleaned_data.get('image_quality', 'balanced')
            custom_fps = form.cleaned_data.get('custom_fps', '30')
            if not server:
                server = 'rs-ny.rustdesk.com' #default rustdesk server
            if not key:
                key = 'OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=' #default rustdesk key
            if not apiServer:
                apiServer = server+":21114"
            if not urlLink:
                urlLink = "https://rustdesk.com"
            if not downloadLink:
                downloadLink = "https://rustdesk.com/download"
            direction = form.cleaned_data['direction']
            installation = form.cleaned_data['installation']
            settings = form.cleaned_data['settings']
            hideGeneralSettings = form.cleaned_data['hideGeneralSettings']
            hideSecuritySettings = form.cleaned_data['hideSecuritySettings']
            hideNetworkSettings = form.cleaned_data['hideNetworkSettings']
            hideDisplaySettings = form.cleaned_data['hideDisplaySettings']
            hideAccountSettings = form.cleaned_data['hideAccountSettings']
            hidePluginSettings = form.cleaned_data['hidePluginSettings']
            hideRemotePrinterSettings = form.cleaned_data['hideRemotePrinterSettings']
            hideServerSettings = form.cleaned_data['hideServerSettings']
            hideProxySettings = form.cleaned_data['hideProxySettings']
            hideWebsocketSettings = form.cleaned_data['hideWebsocketSettings']
            appname = form.cleaned_data['appname']
            filename = form.cleaned_data['exename']
            compname = form.cleaned_data['compname']
            if not compname:
                compname = "Purslane Ltd"
            androidappid = form.cleaned_data['androidappid']
            if not androidappid:
                androidappid = "com.carriez.flutter_hbb"
            compname = compname.replace("&","\\&")
            permPass = form.cleaned_data['permanentPassword']
            theme = form.cleaned_data['theme']
            themeDorO = form.cleaned_data['themeDorO']
            #runasadmin = form.cleaned_data['runasadmin']
            passApproveMode = form.cleaned_data['passApproveMode']
            denyLan = form.cleaned_data['denyLan']
            enableDirectIP = form.cleaned_data['enableDirectIP']
            #ipWhitelist = form.cleaned_data['ipWhitelist']
            autoClose = form.cleaned_data['autoClose']
            permissionsDorO = form.cleaned_data['permissionsDorO']
            permissionsType = form.cleaned_data['permissionsType']
            enableKeyboard = form.cleaned_data['enableKeyboard']
            enableClipboard = form.cleaned_data['enableClipboard']
            enableFileTransfer = form.cleaned_data['enableFileTransfer']
            enableAudio = form.cleaned_data['enableAudio']
            enableTCP = form.cleaned_data['enableTCP']
            enableRemoteRestart = form.cleaned_data['enableRemoteRestart']
            enableRecording = form.cleaned_data['enableRecording']
            enableBlockingInput = form.cleaned_data['enableBlockingInput']
            enableRemoteModi = form.cleaned_data['enableRemoteModi']
            removeWallpaper = form.cleaned_data['removeWallpaper']
            defaultManual = form.cleaned_data['defaultManual']
            overrideManual = form.cleaned_data['overrideManual']
            slogan = form.cleaned_data['slogan']
            enablePrinter = form.cleaned_data['enablePrinter']
            enableCamera = form.cleaned_data['enableCamera']
            enableTerminal = form.cleaned_data['enableTerminal']

            # 新增主控端功能
            hide_chat_voice = form.cleaned_data.get('hide_chat_voice', False)
            viewOnly = form.cleaned_data.get('viewOnly', False)
            collapse_toolbar = form.cleaned_data.get('collapse_toolbar', False)
            privacy_mode = form.cleaned_data.get('privacy_mode', False)
            hide_username_on_card = form.cleaned_data.get('hide_username_on_card', False)

            # 新增被控端功能
            hideTray = form.cleaned_data.get('hideTray', False)
            hidePassword = form.cleaned_data.get('hidePassword', False)
            hideMenuBar = form.cleaned_data.get('hideMenuBar', False)
            hideQuit = form.cleaned_data.get('hideQuit', False)
            addcopy = form.cleaned_data.get('addcopy', False)
            applyprivacy = form.cleaned_data.get('applyprivacy', False)
            passpolicy = form.cleaned_data.get('passpolicy', False)
            allowHostnameAsId = form.cleaned_data.get('allowHostnameAsId', False)
            hideService_Start_Stop = form.cleaned_data.get('hideService_Start_Stop', False)

            # 新增通用功能
            disable_check_update = form.cleaned_data.get('disable_check_update', True)
            no_uninstall = form.cleaned_data.get('no_uninstall', False)
            disable_install = form.cleaned_data.get('disable_install', False)
            allowD3dRender = form.cleaned_data.get('allowD3dRender', False)
            use_texture_render = form.cleaned_data.get('use_texture_render', False)
            pre_elevate_service = form.cleaned_data.get('pre_elevate_service', False)
            sync_init_clipboard = form.cleaned_data.get('sync_init_clipboard', False)
            hide_powered_by_me = form.cleaned_data.get('hide_powered_by_me', True)
            remove_preset_password_warning = form.cleaned_data.get('remove_preset_password_warning', True)
            hide_account = form.cleaned_data.get('hide_account', False)

            filename = re.sub(r'[^\w\s-]', '_', filename).strip()
            myuuid = str(uuid.uuid4())
            protocol = _settings.PROTOCOL
            host = request.get_host()
            full_url = f"{protocol}://{host}"
            try:
                iconfile = form.cleaned_data.get('iconfile')
                if not iconfile:
                    iconfile = form.cleaned_data.get('iconbase64')
                iconlink = save_png(iconfile,myuuid,full_url,"icon.png")
            except:
                print("failed to get icon, using default")
                iconlink = "false"
            try:
                logofile = form.cleaned_data.get('logofile')
                if not logofile:
                    logofile = form.cleaned_data.get('logobase64')
                logolink = save_png(logofile,myuuid,full_url,"logo.png")
            except:
                print("failed to get logo")
                logolink = "false"

            try:
                privacy_wallpaper = form.cleaned_data.get('privacy_wallpaper')
                if not privacy_wallpaper:
                    privacy_wallpaper = form.cleaned_data.get('privacy_wallpaper_base64')
                if privacy_wallpaper:
                    privacylink = save_png(privacy_wallpaper,myuuid,full_url,"privacy_wallpaper.png")
                else:
                    privacylink = "false"
            except:
                print("failed to get privacy wallpaper")
                privacylink = "false"

            ###create the custom.txt json here and send in as inputs below
            decodedCustom = {}
            if direction != "Both":
                decodedCustom['conn-type'] = direction
            if installation == "installationN":
                decodedCustom['disable-installation'] = 'Y'
            
            # Handle settings control
            if settings == "settingsN":
                # Global disable - hides ALL settings
                decodedCustom['disable-settings'] = 'Y'
            elif settings == "settingsGranular":
                # Granular hide settings - only add the ones that are checked
                # Main tabs
                if hideGeneralSettings:
                    decodedCustom['hide-general-settings'] = 'Y'
                if hideSecuritySettings:
                    decodedCustom['hide-security-settings'] = 'Y'
                if hideNetworkSettings:
                    decodedCustom['hide-network-settings'] = 'Y'
                if hideDisplaySettings:
                    decodedCustom['hide-display-settings'] = 'Y'
                if hideAccountSettings:
                    decodedCustom['hide-account-settings'] = 'Y'
                if hidePluginSettings:
                    decodedCustom['hide-plugin-settings'] = 'Y'
                if hideRemotePrinterSettings:
                    decodedCustom['hide-remote-printer-settings'] = 'Y'
                # Network sub-sections
                if hideServerSettings:
                    decodedCustom['hide-server-settings'] = 'Y'
                if hideProxySettings:
                    decodedCustom['hide-proxy-settings'] = 'Y'
                if hideWebsocketSettings:
                    decodedCustom['hide-websocket-settings'] = 'Y'
            if appname.upper != "rustdesk".upper and appname != "":
                decodedCustom['app-name'] = appname
            decodedCustom['override-settings'] = {}
            decodedCustom['default-settings'] = {}
            if permPass != "":
                decodedCustom['password'] = permPass
            if theme != "system":
                if themeDorO == "default":
                    decodedCustom['default-settings']['theme'] = theme
                elif themeDorO == "override":
                    decodedCustom['override-settings']['theme'] = theme
            decodedCustom['approve-mode'] = passApproveMode
            decodedCustom['enable-lan-discovery'] = 'N' if denyLan else 'Y'
            decodedCustom['direct-server'] = 'Y' if enableDirectIP else 'N'
            decodedCustom['allow-auto-disconnect'] = 'Y' if autoClose else 'N'
            decodedCustom['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
            if permissionsDorO == "default":
                decodedCustom['default-settings']['access-mode'] = permissionsType
                decodedCustom['default-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['default-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['default-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['default-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['default-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['default-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['default-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['default-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['default-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'
                decodedCustom['default-settings']['hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['default-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['default-settings']['approve-mode'] = passApproveMode
                if hidecm:
                    decodedCustom['locked-verification-method'] = 'Y'
                decodedCustom['default-settings']['allow-hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['default-settings']['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
                decodedCustom['default-settings']['enable-remote-printer'] = 'Y' if enablePrinter else 'N'
                decodedCustom['default-settings']['enable-camera'] = 'Y' if enableCamera else 'N'
                decodedCustom['default-settings']['enable-terminal'] = 'Y' if enableTerminal else 'N'
            else:
                decodedCustom['override-settings']['access-mode'] = permissionsType
                decodedCustom['override-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['override-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['override-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['override-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['override-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['override-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['override-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['override-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['override-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'
                decodedCustom['override-settings']['direct-server'] = 'Y' if enableDirectIP else 'N'
                decodedCustom['override-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['override-settings']['approve-mode'] = passApproveMode
                if hidecm:
                    decodedCustom['locked-verification-method'] = 'Y'
                decodedCustom['override-settings']['allow-hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['override-settings']['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
                decodedCustom['override-settings']['enable-remote-printer'] = 'Y' if enablePrinter else 'N'
                decodedCustom['override-settings']['enable-camera'] = 'Y' if enableCamera else 'N'
                decodedCustom['override-settings']['enable-terminal'] = 'Y' if enableTerminal else 'N'

            # Add server configuration to override-settings (more reliable than sed)
            decodedCustom['override-settings']['custom-rendezvous-server'] = server
            decodedCustom['override-settings']['key'] = key
            decodedCustom['override-settings']['api-server'] = apiServer

            for line in defaultManual.splitlines():
                k, value = line.split('=')
                decodedCustom['default-settings'][k.strip()] = value.strip()

            for line in overrideManual.splitlines():
                k, value = line.split('=')
                decodedCustom['override-settings'][k.strip()] = value.strip()

            # 添加新功能字段
            if unlockPin:
                decodedCustom['unlock-pin'] = unlockPin

            if image_quality:
                if permissionsDorO == "default":
                    decodedCustom['default-settings']['image-quality'] = image_quality
                else:
                    decodedCustom['override-settings']['image-quality'] = image_quality

            if custom_fps and int(custom_fps) > 30:
                if permissionsDorO == "default":
                    decodedCustom['default-settings']['custom-fps'] = custom_fps
                else:
                    decodedCustom['override-settings']['custom-fps'] = custom_fps

            # 主控端功能
            if hide_chat_voice:
                decodedCustom['hide-chat-voice'] = 'Y'
            if viewOnly:
                if permissionsDorO == "default":
                    decodedCustom['default-settings']['view-only'] = 'Y'
                else:
                    decodedCustom['override-settings']['view-only'] = 'Y'
            if collapse_toolbar:
                if permissionsDorO == "default":
                    decodedCustom['default-settings']['collapse-toolbar'] = 'Y'
                else:
                    decodedCustom['override-settings']['collapse-toolbar'] = 'Y'
            if privacy_mode:
                if permissionsDorO == "default":
                    decodedCustom['default-settings']['privacy-mode'] = 'Y'
                else:
                    decodedCustom['override-settings']['privacy-mode'] = 'Y'
            if hide_username_on_card:
                decodedCustom['hide-username-on-card'] = 'Y'

            # 被控端功能
            if hideTray:
                decodedCustom['hide-tray'] = 'Y'
            if hidePassword:
                decodedCustom['hide-password'] = 'Y'
            if hideMenuBar:
                decodedCustom['hide-menu-bar'] = 'Y'
            if hideQuit:
                decodedCustom['hide-quit'] = 'Y'
            if addcopy:
                decodedCustom['add-copy'] = 'Y'
            if applyprivacy:
                decodedCustom['apply-privacy'] = 'Y'
            if passpolicy:
                decodedCustom['pass-policy'] = 'Y'
            if allowHostnameAsId:
                decodedCustom['allow-hostname-as-id'] = 'Y'
            if hideService_Start_Stop:
                decodedCustom['hide-service-start-stop'] = 'Y'

            # 通用功能
            if disable_check_update:
                decodedCustom['disable-check-update'] = 'Y'
            if no_uninstall:
                decodedCustom['no-uninstall'] = 'Y'
            if disable_install:
                decodedCustom['disable-install'] = 'Y'
            if allowD3dRender:
                decodedCustom['allow-d3d-render'] = 'Y'
            if use_texture_render:
                decodedCustom['use-texture-render'] = 'Y'
            if pre_elevate_service:
                decodedCustom['pre-elevate-service'] = 'Y'
            if sync_init_clipboard:
                decodedCustom['sync-init-clipboard'] = 'Y'
            if hide_powered_by_me:
                decodedCustom['hide-powered-by-me'] = 'Y'
            if remove_preset_password_warning:
                decodedCustom['remove-preset-password-warning'] = 'Y'
            if hide_account:
                decodedCustom['hide-account'] = 'Y'
            
            decodedCustomJson = json.dumps(decodedCustom)

            string_bytes = decodedCustomJson.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            encodedCustom = base64_bytes.decode("ascii")

            #github limits inputs to 10, so lump extras into one with json
            extras = {}
            extras['genurl'] = _settings.GENURL
            extras['urlLink'] = urlLink
            extras['downloadLink'] = downloadLink
            extras['updateLink'] = updateLink if updateLink else downloadLink
            extras['delayFix'] = 'true' if delayFix else 'false'
            extras['version'] = version
            extras['rdgen'] = 'true'
            extras['cycleMonitor'] = 'true' if cycleMonitor else 'false'
            extras['xOffline'] = 'true' if xOffline else 'false'
            extras['hidecm'] = 'true' if hidecm else 'false'
            extras['statussort'] = 'true' if statussort else 'false'
            extras['removeNewVersionNotif'] = 'true' if removeNewVersionNotif else 'false'
            extras['compname'] = compname
            extras['androidappid'] = androidappid
            extras['slogan'] = slogan if slogan else f"Developed By {appname}"
            extras['ui_mode'] = 'true' if ui_mode else 'false'
            extras['privacylink'] = privacylink
            extra_input = json.dumps(extras)

            ####from here run the github action, we need user, repo, access token.
            if platform == 'windows':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'
            elif platform == 'windows-x86':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows-x86.yml/dispatches'
            elif platform == 'linux':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-linux.yml/dispatches'
            elif platform == 'android':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-android.yml/dispatches'
            elif platform == 'macos':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-macos.yml/dispatches'
            else:
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'
                
            
            #url = 'https://api.github.com/repos/'+_settings.GHUSER+'/rustdesk/actions/workflows/test.yml/dispatches'  
            data = {
                "ref":"master",
                "inputs":{
                    "server":server,
                    "key":key,
                    "apiServer":apiServer,
                    "custom":encodedCustom,
                    "uuid":myuuid,
                    #"iconbase64":iconbase64.decode("utf-8"),
                    #"logobase64":logobase64.decode("utf-8") if logobase64 else "",
                    "iconlink":iconlink,
                    "logolink":logolink,
                    "appname":appname,
                    "extras":extra_input,
                    "filename":filename
                }
            } 
            #print(data)
            print(f"=== GitHub Workflow Dispatch Debug ===")
            print(f"URL: {url}")
            print(f"Platform: {platform}")
            print(f"Version: {version}")
            print(f"App Name: {appname}")
            print(f"UUID: {myuuid}")
            
            headers = {
                'Accept':  'application/vnd.github+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+_settings.GHBEARER,
                'X-GitHub-Api-Version': '2022-11-28'
            }
            create_github_run(myuuid)
            response = requests.post(url, json=data, headers=headers)
            print(f"GitHub API Response Status: {response.status_code}")
            print(f"GitHub API Response Body: {response.text}")
            print(f"=== End Debug ===")
            if response.status_code == 204:
                return render(request, 'waiting.html', {'filename':filename, 'uuid':myuuid, 'status':"Starting generator...please wait", 'platform':platform})
            else:
                error_detail = response.json() if response.text else {"message": "Unknown error"}
                return JsonResponse({
                    "error": "GitHub workflow dispatch failed",
                    "status_code": response.status_code,
                    "details": error_detail
                })
    else:
        form = GenerateForm()
    return render(request, 'generator.html', {'form': form})


def check_for_file(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    platform = request.GET['platform']
    gh_run = GithubRun.objects.filter(Q(uuid=uuid)).first()
    status = gh_run.status

    #if file_exists:
    if status == "Success":
        return render(request, 'generated.html', {'filename': filename, 'uuid':uuid, 'platform':platform})
    else:
        return render(request, 'waiting.html', {'filename':filename, 'uuid':uuid, 'status':status, 'platform':platform})

def download(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    file_path = os.path.join('exe',uuid,filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def get_png(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    file_path = os.path.join('png',uuid,filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def create_github_run(myuuid):
    new_github_run = GithubRun(
        uuid=myuuid,
        status="Starting generator...please wait"
    )
    new_github_run.save()

def update_github_run(request):
    data = json.loads(request.body)
    myuuid = data.get('uuid')
    mystatus = data.get('status')
    GithubRun.objects.filter(Q(uuid=myuuid)).update(status=mystatus)
    return HttpResponse('')

def resize_and_encode_icon(imagefile):
    maxWidth = 200
    try:
        with io.BytesIO() as image_buffer:
            for chunk in imagefile.chunks():
                image_buffer.write(chunk)
            image_buffer.seek(0)

            img = Image.open(image_buffer)
            imgcopy = img.copy()
    except (IOError, OSError):
        raise ValueError("Uploaded file is not a valid image format.")

    # Check if resizing is necessary
    if img.size[0] <= maxWidth:
        with io.BytesIO() as image_buffer:
            imgcopy.save(image_buffer, format=imagefile.content_type.split('/')[1])
            image_buffer.seek(0)
            return_image = ContentFile(image_buffer.read(), name=imagefile.name)
        return base64.b64encode(return_image.read())

    # Calculate resized height based on aspect ratio
    wpercent = (maxWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    # Resize the image while maintaining aspect ratio using LANCZOS resampling
    imgcopy = imgcopy.resize((maxWidth, hsize), Image.Resampling.LANCZOS)

    with io.BytesIO() as resized_image_buffer:
        imgcopy.save(resized_image_buffer, format=imagefile.content_type.split('/')[1])
        resized_image_buffer.seek(0)

        resized_imagefile = ContentFile(resized_image_buffer.read(), name=imagefile.name)

    # Return the Base64 encoded representation of the resized image
    resized64 = base64.b64encode(resized_imagefile.read())
    #print(resized64)
    return resized64
 
#the following is used when accessed from an external source, like the rustdesk api server
def startgh(request):
    #print(request)
    data_ = json.loads(request.body)
    ####from here run the github action, we need user, repo, access token.
    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-'+data_.get('platform')+'.yml/dispatches'  
    data = {
        "ref":"master",
        "inputs":{
            "server":data_.get('server'),
            "key":data_.get('key'),
            "apiServer":data_.get('apiServer'),
            "custom":data_.get('custom'),
            "uuid":data_.get('uuid'),
            "iconlink":data_.get('iconlink'),
            "logolink":data_.get('logolink'),
            "appname":data_.get('appname'),
            "extras":data_.get('extras'),
            "filename":data_.get('filename')
        }
    } 
    headers = {
        'Accept':  'application/vnd.github+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+_settings.GHBEARER,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response)
    return HttpResponse(status=204)

def save_png(file, uuid, domain, name):
    file_save_path = "png/%s/%s" % (uuid, name)
    Path("png/%s" % uuid).mkdir(parents=True, exist_ok=True)

    if isinstance(file, str):  # Check if it's a base64 string
        try:
            header, encoded = file.split(';base64,')
            decoded_img = base64.b64decode(encoded)
            file = ContentFile(decoded_img, name=name) # Create a file-like object
        except ValueError:
            print("Invalid base64 data")
            return None  # Or handle the error as you see fit
        except Exception as e:  # Catch general exceptions during decoding
            print(f"Error decoding base64: {e}")
            return None
        
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    imageJson = {}
    imageJson['url'] = domain
    imageJson['uuid'] = uuid
    imageJson['file'] = name
    #return "%s/%s" % (domain, file_save_path)
    return json.dumps(imageJson)

def save_custom_client(request):
    file = request.FILES['file']
    myuuid = request.POST.get('uuid')
    file_save_path = "exe/%s/%s" % (myuuid, file.name)
    Path("exe/%s" % myuuid).mkdir(parents=True, exist_ok=True)
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return HttpResponse("File saved successfully!")
