# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['transparent_overlay/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('default_config.json', '.'),
        ('resources', 'resources'),
        ('*/site-packages/notifypy/os_notifiers/binaries/Notificator.app', 'notifypy/os_notifiers/binaries'),
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
    excludes=['tkinter', 'matplotlib', 'PIL'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
    collect_submodules=['PyQt6.QtCore', 'PyQt6.QtGui'],
    collect_data_files=[('PyQt6', '.')],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WatchCat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  
    disable_windowed_traceback=False,
    argv_emulation=False,  
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
