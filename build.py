import os
import platform
from pathlib import Path
import PyInstaller.__main__
import cairosvg

def convert_svg_icons():
    """将SVG图标转换为各平台所需格式"""
    svg_path = Path("resources/icon.svg")
    
    if platform.system() == "Darwin":
        # macOS需要ICNS
        sizes = [16, 32, 64, 128, 256, 512, 1024]
        png_files = []
        
        for size in sizes:
            output_file = f"icon_{size}x{size}.png"
            cairosvg.svg2png(
                url=str(svg_path),
                write_to=output_file,
                output_width=size,
                output_height=size
            )
            png_files.append(output_file)
        
        os.makedirs("icon.iconset", exist_ok=True)
        for size, png_file in zip(sizes, png_files):
            os.rename(png_file, f"icon.iconset/icon_{size}x{size}.png")
        
        os.system("iconutil -c icns icon.iconset")
        os.system("rm -rf icon.iconset")

def build_app():
    """构建WatchCat应用程序"""
    
    # 转换图标
    convert_svg_icons()
    
    # 基础配置
    app_name = "WatchCat"
    entry_point = "src/main.py"
    icon_file = "icon.icns"
    
    # PyInstaller 参数
    args = [
        entry_point,
        "--name=%s" % app_name,
        "--windowed",
        "--clean",
        f"--icon={icon_file}",
        "--add-data=resources:resources",
        "--collect-submodules=src",
        "--noupx",  # 禁用UPX压缩以提升启动速度
        "--noconfirm",  # 自动覆盖输出目录
    ]
    
    # macOS 特定配置
    if platform.system() == "Darwin":
        args.extend([
            "--osx-bundle-identifier=com.cs-magic.watchcat",
            "--codesign-identity=",  # 空字符串表示跳过签名
            "--osx-entitlements-file=",  # 空字符串表示不使用授权文件
        ])
        
    # 运行 PyInstaller
    PyInstaller.__main__.run(args)
    
    # 清理临时文件
    if os.path.exists(icon_file):
        os.remove(icon_file)

if __name__ == "__main__":
    build_app()