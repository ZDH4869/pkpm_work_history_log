from pyp3d import *
import math

# 定义参数化模型
class 上粗下细凸曲线圆柱体(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        # 圆柱体基本参数
        self['总高度'] = Attr(400.0, obvious=True)
        self['顶部直径'] = Attr(600.0, obvious=True)
        self['底部直径'] = Attr(300.0, obvious=True)
        self['截面数量'] = Attr(40, obvious=True)
        # 曲线控制参数 - 控制下凹上凸的曲线形状
        self['曲线指数'] = Attr(0.4, obvious=True)  # 指数小于1时，曲线下凹；大于1时，曲线上凹
        # 中心孔参数
        self['中心孔直径'] = Attr(200.0, obvious=True)
        # 定位参数
        self['定位点X'] = Attr(0.0, obvious=True)
        self['定位点Y'] = Attr(0.0, obvious=True)
        self['定位点Z'] = Attr(0.0, obvious=True)
        self['旋转角度'] = Attr(0.0, obvious=True)
        # 模型显示参数
        self['上粗下细凸曲线圆柱体'] = Attr(None, show=True)
        self.replace()
    
    @export
    # 模型造型
    def replace(self):
        # 设置变量，同时调用参数(简化书写过程)
        H = self['总高度']
        D_top = self['顶部直径']
        D_bottom = self['底部直径']
        num_sections = self['截面数量']
        curve_exp = self['曲线指数']
        D_hole = self['中心孔直径']
        x = self['定位点X']
        y = self['定位点Y']
        z = self['定位点Z']
        Angle = self['旋转角度']
        
        # 计算半径
        R_top = D_top / 2      # 顶部半径（粗）
        R_bottom = D_bottom / 2  # 底部半径（细）
        R_hole = D_hole / 2    # 中心孔半径
        
        # ==================== 创建上粗下细带下凹凸曲线的外轮廓圆柱体 ====================
        # 使用幂函数创建下凹上凸的曲线效果
        # 公式：R(z) = R_bottom + (R_top - R_bottom) * t^curve_exp
        # 当 curve_exp < 1 时，曲线呈下凹形状（类似你提供的图片）
        # 当 curve_exp = 1 时，为直线（圆锥）
        # 当 curve_exp > 1 时，曲线呈上凹形状
        
        sections = []
        
        for i in range(num_sections + 1):
            # 计算当前截面的Z位置（从0到H）
            z_pos = H * i / num_sections
            
            # 计算归一化高度 t [0, 1]，0为底部，1为顶部
            t = z_pos / H
            
            # 使用幂函数计算半径
            # t^curve_exp 当 curve_exp < 1 时，t较小时增长快，t较大时增长慢
            # 这样形成下凹的曲线形状
            if curve_exp > 0:
                curve_factor = math.pow(t, curve_exp)
            else:
                curve_factor = t  # 防止负数或零指数出错
            
            # 当前位置的半径
            current_radius = R_bottom + (R_top - R_bottom) * curve_factor
            
            # 创建当前位置的圆形截面
            current_section = translate(0, 0, z_pos) * Section(scale(current_radius) * Arc(2 * pi))
            sections.append(current_section)
        
        # 放样生成带凸曲线的圆柱体外轮廓
        CurvedCylinder = Loft(*sections)
        
        # ==================== 创建中心孔圆柱体（用于布尔减运算） ====================
        # 中心孔是一个贯穿整个高度的圆柱体
        HoleCylinder = Cone(Vec3(0, 0, 0), Vec3(0, 0, H), R_hole, R_hole)
        
        # ==================== 布尔运算：外轮廓减去中心孔 ====================
        # 使用差集运算在圆柱体中间沿轴线方向开孔
        ResultGeometry = CurvedCylinder - HoleCylinder
        
        # 应用定位、旋转和颜色
        self['上粗下细凸曲线圆柱体'] = translate(x, y, z) * rotation(pi/180 * Angle) * ResultGeometry.color(0.6, 0.8, 1.0, 0.9)

# 输出模型
if __name__ == "__main__":
    FinalGeometry = 上粗下细凸曲线圆柱体()
    place(FinalGeometry)
