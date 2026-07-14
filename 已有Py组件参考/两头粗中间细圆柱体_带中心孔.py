from pyp3d import *

# 定义参数化模型
class 两头粗中间细圆柱体_带中心孔(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        # 圆柱体基本参数
        self['总高度'] = Attr(2000.0, obvious=True)
        self['端部直径'] = Attr(500.0, obvious=True)
        self['中部直径'] = Attr(300.0, obvious=True)
        self['截面数量'] = Attr(15, obvious=True)
        # 中心孔参数
        self['中心孔直径'] = Attr(100.0, obvious=True)
        # 定位参数
        self['定位点X'] = Attr(0.0, obvious=True)
        self['定位点Y'] = Attr(0.0, obvious=True)
        self['定位点Z'] = Attr(0.0, obvious=True)
        self['旋转角度'] = Attr(0.0, obvious=True)
        # 模型显示参数
        self['两头粗中间细圆柱体_带中心孔'] = Attr(None, show=True)
        self.replace()
    
    @export
    # 模型造型
    def replace(self):
        # 设置变量，同时调用参数(简化书写过程)
        H = self['总高度']
        D_end = self['端部直径']
        D_mid = self['中部直径']
        num_sections = self['截面数量']
        D_hole = self['中心孔直径']
        x = self['定位点X']
        y = self['定位点Y']
        z = self['定位点Z']
        Angle = self['旋转角度']
        
        # 计算半径
        R_end = D_end / 2  # 端部半径（粗）
        R_mid = D_mid / 2  # 中部半径（细）
        R_hole = D_hole / 2  # 中心孔半径
        
        # ==================== 创建两头粗中间细的外轮廓圆柱体 ====================
        # 抛物线公式：R(z) = R_mid + (R_end - R_mid) * (2*z/H - 1)^2
        # 这是一个开口向上的抛物线
        # 在z=H/2处(t=0)达到最小值R_mid（中部细）
        # 在z=0和z=H处(t=±1)达到最大值R_end（两端粗）
        
        sections = []
        # 截面数量由用户参数控制，越多曲线越平滑
        
        for i in range(num_sections + 1):
            # 计算当前截面的Z位置（从0到H）
            z_pos = H * i / num_sections
            
            # 使用抛物线计算当前位置的半径
            # 将z位置归一化到[-1, 1]范围，中部为0，两端为±1
            t = 2 * z_pos / H - 1  # t在z=0时为-1，z=H/2时为0，z=H时为1
            
            # 抛物线曲线：t^2，在t=0(中部)时最小为0，在t=±1(两端)时最大为1
            parabola_factor = t * t  # t的平方，范围[0, 1]
            current_radius = R_mid + (R_end - R_mid) * parabola_factor
            
            # 创建当前位置的圆形截面
            current_section = translate(0, 0, z_pos) * Section(scale(current_radius) * Arc(2 * pi))
            sections.append(current_section)
        
        # 放样生成两头粗中间细的圆柱体外轮廓
        TaperedCylinder = Loft(*sections)
        
        # ==================== 创建中心孔圆柱体（用于布尔减运算） ====================
        # 中心孔是一个贯穿整个高度的圆柱体，使用Cone函数创建（当两端半径相同时即为圆柱）
        HoleCylinder = Cone(Vec3(0, 0, 0), Vec3(0, 0, H), R_hole, R_hole)
        
        # ==================== 布尔运算：外轮廓减去中心孔 ====================
        # 使用差集运算在圆柱体中间沿轴线方向开孔
        ResultGeometry = TaperedCylinder - HoleCylinder
        
        # 应用定位、旋转和颜色
        self['两头粗中间细圆柱体_带中心孔'] = translate(x, y, z) * rotation(pi/180 * Angle) * ResultGeometry.color(0.6, 0.8, 1.0, 0.8)

# 输出模型
if __name__ == "__main__":
    FinalGeometry = 两头粗中间细圆柱体_带中心孔()
    place(FinalGeometry)
