from pyp3d import *
import math

# 定义参数化模型
class 单面切角长方体(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        # 长方体基本参数
        self['长度'] = Attr(1000.0, obvious=True)
        self['宽度'] = Attr(800.0, obvious=True)
        self['高度'] = Attr(600.0, obvious=True)
        # 切角参数
        self['切角尺寸'] = Attr(100.0, obvious=True)  # 切角在X和Y方向的尺寸
        # 定位参数
        self['定位点X'] = Attr(0.0, obvious=True)
        self['定位点Y'] = Attr(0.0, obvious=True)
        self['定位点Z'] = Attr(0.0, obvious=True)
        self['旋转角度'] = Attr(0.0, obvious=True)
        # 模型显示参数
        self['单面切角长方体'] = Attr(None, show=True)
        self.replace()
    
    @export
    # 模型造型
    def replace(self):
        # 设置变量，同时调用参数(简化书写过程)
        L = self['长度']
        W = self['宽度']
        H = self['高度']
        chamfer = self['切角尺寸']
        x = self['定位点X']
        y = self['定位点Y']
        z = self['定位点Z']
        Angle = self['旋转角度']
        
        # 限制切角尺寸不超过长宽的一半
        chamfer = min(chamfer, L/2 - 1, W/2 - 1)
        
        # ==================== 创建主体长方体 ====================
        MainBox = scale(L, W, H) * Cube()
        
        # ==================== 创建上表面四个切角切除体 ====================
        # 切角切除体是四个三棱柱，分别位于上表面的四个顶角
        # 三棱柱从顶角处向下切除，高度与长方体相同
        
        # 切角切除体的截面（直角三角形）
        triangle_section = Section(
            Vec2(0, 0),
            Vec2(chamfer, 0),
            Vec2(0, chamfer)
        )
        
        # 扫掠路径（沿Z轴向下）
        sweep_path = Line(Vec3(0, 0, H), Vec3(0, 0, 0))
        
        # ==================== 左下角切角切除体 ====================
        # 位于上表面左下角 (0, 0, H)
        cut1 = translate(0, 0, 0) * Sweep(triangle_section, sweep_path)
        
        # ==================== 右下角切角切除体 ====================
        # 位于上表面右下角 (L, 0, H)，需要旋转90度
        triangle_section_2 = Section(
            Vec2(0, 0),
            Vec2(0, chamfer),
            Vec2(-chamfer, 0)
        )
        cut2 = translate(L, 0, 0) * Sweep(triangle_section_2, sweep_path)
        
        # ==================== 右上角切角切除体 ====================
        # 位于上表面右上角 (L, W, H)，需要旋转180度
        triangle_section_3 = Section(
            Vec2(0, 0),
            Vec2(-chamfer, 0),
            Vec2(0, -chamfer)
        )
        cut3 = translate(L, W, 0) * Sweep(triangle_section_3, sweep_path)
        
        # ==================== 左上角切角切除体 ====================
        # 位于上表面左上角 (0, W, H)，需要旋转270度（或-90度）
        triangle_section_4 = Section(
            Vec2(0, 0),
            Vec2(0, -chamfer),
            Vec2(chamfer, 0)
        )
        cut4 = translate(0, W, 0) * Sweep(triangle_section_4, sweep_path)
        
        # ==================== 布尔运算：主体减去四个切角 ====================
        ResultGeometry = MainBox - cut1 - cut2 - cut3 - cut4
        
        # 应用定位、旋转和颜色
        self['单面切角长方体'] = translate(x, y, z) * rotation(pi/180 * Angle) * ResultGeometry.color(0.7, 0.85, 1.0, 1.0)

# 输出模型
if __name__ == "__main__":
    FinalGeometry = 单面切角长方体()
    place(FinalGeometry)
