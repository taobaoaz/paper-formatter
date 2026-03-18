# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['核心模块/main.py'],
    pathex=['功能模块', '核心模块'],
    binaries=[],
    datas=[('功能模块/parsers', 'parsers'), ('功能模块/rules', 'rules')],
    hiddenimports=['parsers', 'rules'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='论文排版优化器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
