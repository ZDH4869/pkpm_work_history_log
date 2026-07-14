from pyp3d import *

class 圆角柱体(Component):
    def __init__(self):
        Component.__init__(self)
        self['半径'] = Attr(500.0, obvious=True, readonly=False)
        self['高度'] = Attr(2000.0, obvious=True, readonly=False)
        self['圆角半径'] = Attr(100.0, obvious=True, readonly=False)
        self['圆角柱体'] = Attr(None, show=True)
        self['旋转角度'] = Attr(0, obvious=True)
        self['X'] = Attr(0.0, obvious=True)
        self['Y'] = Attr(0.0, obvious=True)
        self['Z'] = Attr(0.0, obvious=True)
        self.replace()
    
    @export
    def replace(self):
        R = self['半径']
        H = self['高度']
        r = self['圆角半径']
        x = self['X']
        y = self['Y']
        z = self['Z']
        Angle = self['旋转角度']
        
        arc1 = translate(R-r, r, 0) * scale(r) * Arc(-0.5*math.pi)
        arc2 = translate(R-r, H-r, 0) * scale(r) * Arc(0.5*math.pi)
        
        section = Section(
            Vec2(0, 0),
            Vec2(R-r, 0),
            arc1,
            Vec2(R, r),
            Vec2(R, H-r),
            arc2,
            Vec2(R-r, H),
            Vec2(0, H)
        )
        
        section_rotated = rotate(Vec3(1, 0, 0), -0.5*math.pi) * section
        
        line_path = Line(Arc(2*pi))
        
        rounded_cylinder = Sweep(section_rotated, line_path)
        
        self['圆角柱体'] = translate(x, y, z) * rotation(math.pi/180 * Angle) * rounded_cylinder

if __name__ == "__main__":
    FinalGeometry = 圆角柱体()
    place(FinalGeometry)
