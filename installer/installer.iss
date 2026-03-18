; Inno Setup 安装脚本
; 论文排版优化器 v2.0.0
; 
; 使用方法：
; 1. 下载并安装 Inno Setup: https://jrsoftware.org/isdl.php
; 2. 用 Inno Setup Compiler 打开此文件
; 3. 编译生成安装包

[Setup]
; 基本设置
AppName=论文排版优化器
AppVersion=2.0.0
AppPublisher=开发小助手
AppPublisherURL=https://github.com/taobaoaz/paper-formatter
AppSupportURL=https://github.com/taobaoaz/paper-formatter/issues
AppUpdatesURL=https://github.com/taobaoaz/paper-formatter/releases

; 安装目录
DefaultDirName={autopf}\论文排版优化器
DefaultGroupName=论文排版优化器
DisableProgramGroupPage=yes

; 输出设置
OutputDir=installer_output
OutputBaseFilename=论文排版优化器安装程序_v2.0.0
SetupIconFile=installer\app_icon.ico
UninstallDisplayIcon={app}\论文排版优化器.exe

; 压缩设置
Compression=lzma2/max
SolidCompression=yes

; 权限
PrivilegesRequired=admin

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 主程序
Source: "dist\论文排版优化器.exe"; DestDir: "{app}"; Flags: ignoreversion

; 启动文件
Source: "启动文件\*"; DestDir: "{app}\启动文件"; Flags: ignoreversion recursesubdirs

; 功能模块
Source: "功能模块\*"; DestDir: "{app}\功能模块"; Flags: ignoreversion recursesubdirs

; 核心模块
Source: "核心模块\*"; DestDir: "{app}\核心模块"; Flags: ignoreversion recursesubdirs

; 文档
Source: "文档资料\*.md"; DestDir: "{app}\文档"; Flags: ignoreversion

[Icons]
; 开始菜单
Name: "{group}\论文排版优化器"; Filename: "{app}\论文排版优化器.exe"
Name: "{group}\检查更新"; Filename: "{app}\论文排版优化器.exe"; Parameters: "--check-update"
Name: "{group}\GitHub 仓库"; Filename: "https://github.com/taobaoaz/paper-formatter"

; 桌面图标
Name: "{autodesktop}\论文排版优化器"; Filename: "{app}\论文排版优化器.exe"; Tasks: desktopicon

[Run]
; 安装完成后运行
Filename: "{app}\论文排版优化器.exe"; Description: "{cm:LaunchProgram,论文排版优化器}"; Flags: nowait postinstall skipifsilent

[Code]
// 安装向导自定义代码
var
  UpdateCheckLabel: TLabel;

procedure InitializeWizard;
begin
  // 自定义欢迎信息
  WizardForm.WelcomeLabel1.Caption := '欢迎安装 论文排版优化器 v2.0.0';
  WizardForm.WelcomeLabel2.Caption := '此向导将引导您完成安装过程。'#13#10'建议在继续之前关闭其他所有应用程序。';
end;
