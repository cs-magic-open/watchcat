# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['transparent_overlay/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('default_config.json', '.'),
        ('resources', 'resources'),
        ('venv/lib/python3.12/site-packages/notifypy/os_notifiers/binaries/Notificator.app', 'notifypy/os_notifiers/binaries'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'cv2',
        'numpy',
        'mss',
        'plyer',
        'notifypy',
        'simpleaudio',
        'pydub'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WatchCat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WatchCat',
)
