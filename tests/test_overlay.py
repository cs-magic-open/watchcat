import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent))

from transparent_overlay.main import TransparentOverlay

@pytest.fixture
def app():
    """创建 QApplication 实例"""
    return QApplication([])

@pytest.fixture
def overlay(app):
    """创建 TransparentOverlay 实例"""
    with patch('transparent_overlay.main.mss') as mock_mss:
        with patch('transparent_overlay.main.TransparentOverlay.setup_signal_handling') as mock_signal:
            overlay = TransparentOverlay(app)
            # 模拟配置
            overlay.config = {
                "position": {"x": 100, "y": 100},
                "size": {"width": 200, "height": 200},
                "opacity": 1.0,
                "color": "#FF0000",
                "border": {"width": 2}
            }
            return overlay

def test_update_window_geometry(overlay):
    """测试窗口位置和大小更新"""
    # 记���初始状态
    initial_geometry = overlay.geometry()
    
    # 模拟匹配结果
    match_result = (300, 400, 500, 600)  # x, y, w, h
    
    # 调用更新方法
    overlay.update_window_geometry(match_result)
    
    # 验证配置更新
    assert overlay.config["position"]["x"] == 300
    assert overlay.config["position"]["y"] == 400
    assert overlay.config["size"]["width"] == 500
    assert overlay.config["size"]["height"] == 600
    
    # 验证窗口几何属性
    new_geometry = overlay.geometry()
    border_width = overlay.border_width
    
    assert new_geometry.x() == 300 - border_width
    assert new_geometry.y() == 400 - border_width
    assert new_geometry.width() == 500 + (border_width * 2)
    assert new_geometry.height() == 600 + (border_width * 2)
    
    # 验证窗口可见性
    if overlay.toggle_action.isChecked():
        assert overlay.isVisible()

def test_update_window_geometry_with_visibility(overlay):
    """测试窗口可见性控制"""
    # 设置初始状态为隐藏
    overlay.hide()
    overlay.toggle_action.setChecked(True)
    
    # 调用更新方法
    match_result = (300, 400, 500, 600)
    overlay.update_window_geometry(match_result)
    
    # 验证窗口变为可见
    assert overlay.isVisible()

def test_update_window_geometry_stays_hidden(overlay):
    """测试窗口保持隐藏状态"""
    # 设置初始状态为隐藏且 toggle_action 未选中
    overlay.hide()
    overlay.toggle_action.setChecked(False)
    
    # 调用更新方法
    match_result = (300, 400, 500, 600)
    overlay.update_window_geometry(match_result)
    
    # 验证窗口保持隐藏
    assert not overlay.isVisible()

def test_update_window_geometry_triggers_paint(overlay):
    """测试是否触发重绘"""
    # 模拟 update 方法
    overlay.update = MagicMock()
    
    # 调用更新方法
    match_result = (300, 400, 500, 600)
    overlay.update_window_geometry(match_result)
    
    # 验证是否调用了 update
    overlay.update.assert_called_once() 

def test_draw_border(overlay):
    """测试边框绘制"""
    # 创建模拟的 QPainter
    painter = MagicMock()
    
    # 创建测试用的矩形
    rect = QRect(10, 10, 100, 100)
    
    # 调用绘制方法
    overlay._draw_border(painter, rect)
    
    # 验证画笔设置
    painter.setBrush.assert_called_once_with(Qt.BrushStyle.NoBrush)
    painter.setPen.assert_called_once()
    painter.drawRect.assert_called_once_with(rect)
    
    # 验证画笔颜色和宽度
    pen = painter.setPen.call_args[0][0]
    assert pen.color().name() == overlay.config["color"]
    assert pen.width() == overlay.border_width