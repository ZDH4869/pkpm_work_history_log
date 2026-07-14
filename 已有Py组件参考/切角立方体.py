from pyp3d import *

class 切角立方体(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['长度L'] = Attr(750.0, obvious=True, readonly=False)
        self['宽度W'] = Attr(480.0, obvious=True, readonly=False)
        self['切角长度C'] = Attr(75.0, obvious=True, readonly=False)
        self['厚度T'] = Attr(160.0, obvious=True, readonly=False)
        self['法兰内径D'] = Attr(400.0, obvious=True, readonly=False)
        self['法兰底边高B'] = Attr(25.0, obvious=True, readonly=False)
        
        self['切角立方体'] = Attr(None, show=True)
        self['旋转角度'] = Attr(0, obvious=False)
        self['X'] = Attr(0.0, obvious=False, readonly=True)
        self['Y'] = Attr(0.0, obvious=False, readonly=True)
        self['Z'] = Attr(0.0, obvious=False, readonly=True)
        
        self.setDrivenFeaturePoint('顶面后左角', SnapMode.EndPoint, '0', '0', '[长度L]')
        self.setDrivenFeaturePoint('顶面后右角', SnapMode.EndPoint, '0', '[宽度W]', '[长度L]')
        self.setDrivenFeaturePoint('顶面前左角', SnapMode.EndPoint, '[厚度T]', '0', '[长度L]')
        self.setDrivenFeaturePoint('顶面前右角', SnapMode.EndPoint, '[厚度T]', '[宽度W]', '[长度L]')
        self.setDrivenFeaturePoint('顶面中心', SnapMode.GeometricCenter, '[厚度T]/2', '[宽度W]/2', '[长度L]')
        self.setDrivenFeaturePoint('法兰孔几何中心', SnapMode.EndPoint, '[厚度T]/2', '[法兰底边高B]+[法兰内径D]/2', '[长度L]-[宽度W]/2')
        self.setDrivenFeaturePoint('法兰孔顶面圆心', SnapMode.EndPoint, '[厚度T]', '[法兰底边高B]+[法兰内径D]/2', '[长度L]-[宽度W]/2')
        self.setDrivenFeaturePoint('法兰孔底面圆心', SnapMode.EndPoint, '0', '[法兰底边高B]+[法兰内径D]/2', '[长度L]-[宽度W]/2')
        
        self.replace()
    
    @export
    def replace(self):
        L = self['长度L']
        W = self['宽度W']
        C = self['切角长度C']
        T = self['厚度T']
        D = self['法兰内径D']
        B = self['法兰底边高B']
        x = self['X']
        y = self['Y']
        z = self['Z']
        Angle = self['旋转角度']
        
        ratio = C / 2**0.5
        
        section = Section(
            Vec2(0, L),
            Vec2(W, L),
            Vec2(W, ratio),
            Vec2(W - ratio, 0),
            Vec2(ratio, 0),
            Vec2(0, ratio)
        )
        
        path = Line(Vec3(0, 0, 0), Vec3(0, 0, T))
        
        main_body = Sweep(section, path)
        
        hole_circle = Section(scale(D/2) * Arc(2 * math.pi))
        hole_circle_transformed = translate(W/2, B + D/2, 0) * hole_circle
        hole_cylinder = Sweep(hole_circle_transformed, path)
        
        final_geometry = substract(main_body, hole_cylinder)
        
        self['切角立方体'] = translate(x, y, z) * rotation(math.pi/180 * Angle) * rotate(Vec3(1, 0, 0), math.pi/2) * final_geometry

if __name__ == "__main__":
    FinalGeometry = 切角立方体()
    place(FinalGeometry)
