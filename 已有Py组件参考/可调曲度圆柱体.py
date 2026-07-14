from pyp3d import *

# 定义参数化模型
class 可调曲度圆柱体(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        # 圆柱体基本参数
        self['总高度'] = Attr(2000.0, obvious=True)
        self['端部直径'] = Attr(500.0, obvious=True)
        self['中部直径'] = Attr(300.0, obvious=True)
        self['截面数量'] = Attr(15, obvious=True)
        # 曲度控制参数：1.0为抛物线，越大越尖，越小越平缓
        self['曲度系数'] = Attr(2.0, obvious=True)
        # 定位参数
        self['定位点X'] = Attr(0.0, obvious=True)
        self['定位点Y'] = Attr(0.0, obvious=True)
        self['定位点Z'] = Attr(0.0, obvious=True)
        self['旋转角度'] = Attr(0.0, obvious=True)
        # 模型显示参数
        self['可调曲度圆柱体'] = Attr(None, show=True)
        self.replace()
    
    @export
    # 模型造型
    def replace(self):
        # 设置变量，同时调用参数(简化书写过程)
        H = self['总高度']
        D_end = self['端部直径']
        D_mid = self['中部直径']
        num_sections = self['截面数量']
        curvature = self['曲度系数']
        x = self['定位点X']
        y = self['定位点Y']
        z = self['定位点Z']
        Angle = self['旋转角度']
        
        # 计算半径
        R_end = D_end / 2  # 端部半径（粗）
        R_mid = D_mid / 2  # 中部半径（细）
        
        # ==================== 使用可调曲度函数创建侧边过渡 ====================
        # 曲度公式：R(z) = R_mid + (R_end - R_mid) * |t|^curvature
        # t = 2*z/H - 1，范围[-1, 1]，中部为0，两端为±1
        # curvature控制曲度：
        #   - curvature = 1.0：线性过渡（直线）
        #   - curvature = 2.0：抛物线（默认，向内凹）
        #   - curvature > 2.0：更尖锐的曲线（腰部更细）
        #   - 1.0 < curvature < 2.0：更平缓的曲线
        #   - curvature < 1.0：向外凸的曲线
        
        sections = []
        # 截面数量由用户参数控制，越多曲线越平滑
        
        for i in range(num_sections + 1):
            # 计算当前截面的Z位置（从0到H）
            z_pos = H * i / num_sections
            
            # 将z位置归一化到[-1, 1]范围，中部为0，两端为±1
            t = 2 * z_pos / H - 1  # t在z=0时为-1，z=H/2时为0，z=H时为1
            
            # 使用可调曲度公式计算当前位置的半径
            # |t|^curvature：在t=0(中部)时为0，在t=±1(两端)时为1
            # 公式：R(z) = R_mid + (R_end - R_mid) * |t|^curvature
            # 中部(t=0)：半径 = R_mid（细）
            # 两端(t=±1)：半径 = R_end（粗）
            curvature_factor = pow(abs(t), curvature)
            current_radius = R_mid + (R_end - R_mid) * curvature_factor
            
            # 创建当前位置的圆形截面
            current_section = translate(0, 0, z_pos) * Section(scale(current_radius) * Arc(2 * pi))
            sections.append(current_section)
        
        # ==================== 放样生成可调曲度的圆柱体 ====================
        TaperedCylinder = Loft(*sections)
        
        # 应用定位、旋转和颜色
        self['可调曲度圆柱体'] = translate(x, y, z) * rotation(pi/180 * Angle) * TaperedCylinder.color(0.6, 0.8, 1.0, 0.8)

# 输出模型
if __name__ == "__main__":
    FinalGeometry = 可调曲度圆柱体()
    place(FinalGeometry)
