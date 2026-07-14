from pyp3d import *

class 电磁控制盒(Component):
    def __init__(self):
        Component.__init__(self)
        
        self.setDrivenFeaturePoint('连盘底部圆心', SnapMode.GeometricCenter, '[X]', '[Y]', '[Z]')
        self.setDrivenFeaturePoint('电磁盒顶部圆心', SnapMode.GeometricCenter, '[X]', '[Y]', '[Z]+[连盘厚度]+[电磁盒直径]*0.8')
        self.setDrivenFeaturePoint('电磁接口外端面圆心', SnapMode.GeometricCenter, '[X]+[电磁盒直径]*0.7*cos([旋转角度]*pi/180)', '[Y]+[电磁盒直径]*0.7*sin([旋转角度]*pi/180)', '[Z]+[连盘厚度]+[电磁盒直径]*0.5')
        
        self['电磁盒直径'] = Attr(360.0, obvious=True, readonly=False)
        self['电磁盒高度'] = Attr(0.0, obvious=True, readonly=True)
        self['电磁接口直径'] = Attr(0.0, obvious=True, readonly=True)
        self['电磁接口长度'] = Attr(0.0, obvious=True, readonly=True)
        self['电磁中心高度'] = Attr(0.0, obvious=True, readonly=True)
        self['连盘直径'] = Attr(0.0, obvious=True, readonly=True)
        self['连盘厚度'] = Attr(50.0, obvious=True, readonly=False)
        self['紧固件直径'] = Attr(0.0, obvious=True, readonly=True)
        self['电磁控制盒'] = Attr(None, show=True)
        self['旋转角度'] = Attr(0, obvious=False)
        self['X'] = Attr(0.0, obvious=True)
        self['Y'] = Attr(0.0, obvious=True)
        self['Z'] = Attr(0.0, obvious=True)
        self.replace()
    
    @export
    def replace(self):
        D = self['电磁盒直径']
        t = self['连盘厚度']
        x = self['X']
        y = self['Y']
        z = self['Z']
        Angle = self['旋转角度']
        
        R = D / 2
        
        连盘直径 = 1.4 * D
        连盘半径 = 连盘直径 / 2
        电磁盒高度 = 0.8 * D
        电磁接口直径 = 0.4 * D
        电磁接口半径 = 电磁接口直径 / 2
        电磁接口长度 = 0.7 * D
        电磁中心高度 = 0.5 * D
        紧固件直径 = 0.2 * D
        紧固件半径 = 紧固件直径 / 2
        
        self['电磁盒高度'] = 电磁盒高度
        self['电磁接口直径'] = 电磁接口直径
        self['电磁接口长度'] = 电磁接口长度
        self['电磁中心高度'] = 电磁中心高度
        self['连盘直径'] = 连盘直径
        self['紧固件直径'] = 紧固件直径
        
        连盘 = Cone(Vec3(0, 0, 0), Vec3(0, 0, t), 连盘半径, 连盘半径)
        
        电磁盒 = Cone(Vec3(0, 0, t), Vec3(0, 0, t + 电磁盒高度), R, R)
        
        电磁接口 = Cone(Vec3(0, 0, t + 电磁中心高度), Vec3(电磁接口长度, 0, t + 电磁中心高度), 电磁接口半径, 电磁接口半径)
        
        紧固件1 = Cone(Vec3(连盘半径, 0, 0), Vec3(连盘半径, 0, t), 紧固件半径, 紧固件半径)
        紧固件2 = Cone(Vec3(0, 连盘半径, 0), Vec3(0, 连盘半径, t), 紧固件半径, 紧固件半径)
        紧固件3 = Cone(Vec3(-连盘半径, 0, 0), Vec3(-连盘半径, 0, t), 紧固件半径, 紧固件半径)
        紧固件4 = Cone(Vec3(0, -连盘半径, 0), Vec3(0, -连盘半径, t), 紧固件半径, 紧固件半径)
        
        连盘带紧固件 = 连盘 + 紧固件1 + 紧固件2 + 紧固件3 + 紧固件4
        
        电磁控制盒模型 = combine(连盘带紧固件, 电磁盒, 电磁接口)
        
        self['电磁控制盒'] = translate(x, y, z) * rotation(math.pi/180 * Angle) * 电磁控制盒模型

if __name__ == "__main__":
    FinalGeometry = 电磁控制盒()
    place(FinalGeometry)
