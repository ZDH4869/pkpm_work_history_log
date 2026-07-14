from pyp3d import *
import math

class 平焊法兰(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['压力等级'] = Attr('PN10', obvious=True)
        
        self['公称尺寸'] = Attr('DN15', obvious=True, combo=['DN10', 'DN15'])
        
        self['法兰内径系列'] = Attr('系列1', obvious=True, combo=['系列1', '系列2'])
        
        self['法兰外径'] = Attr(95.0, obvious=True, readonly=True)
        
        self['螺栓孔中心圆直径'] = Attr(65.0, obvious=True, readonly=True)
        
        self['螺纹孔直径'] = Attr(14, obvious=True, readonly=True)
        
        self['螺纹数量'] = Attr(4, obvious=True, readonly=True)
        
        self['螺纹规格'] = Attr('M12', obvious=True, readonly=True)
        
        self['法兰厚度'] = Attr(14.0, obvious=True, readonly=True)
        
        self['密封面类型'] = Attr('突面-RF', obvious=True, combo=['平面-FF', '突面-RF'])
        
        self['密封面直径'] = Attr(45.0, obvious=True, readonly=True)
        
        self['密封面厚度'] = Attr(2.0, obvious=True, readonly=True)
        
        self['平焊法兰'] = Attr(None, show=True)
        
        self.replace()
    
    def get_spec_data(self):
        DN = self['公称尺寸']
        series = self['法兰内径系列']
        
        spec_data = {
            'DN10': {
                '系列1': {
                    '法兰内径': 18.0,
                    '法兰外径': 90.0,
                    '螺栓孔中心圆直径': 60.0,
                    '螺纹孔直径': 14,
                    '螺纹数量': 4,
                    '螺纹规格': 'M12',
                    '法兰厚度': 14.0,
                    '密封面直径': 40.0,
                    '密封面厚度': 2.0
                },
                '系列2': {
                    '法兰内径': 15.0,
                    '法兰外径': 90.0,
                    '螺栓孔中心圆直径': 60.0,
                    '螺纹孔直径': 14,
                    '螺纹数量': 4,
                    '螺纹规格': 'M12',
                    '法兰厚度': 14.0,
                    '密封面直径': 40.0,
                    '密封面厚度': 2.0
                }
            },
            'DN15': {
                '系列1': {
                    '法兰内径': 22.0,
                    '法兰外径': 95.0,
                    '螺栓孔中心圆直径': 65.0,
                    '螺纹孔直径': 14,
                    '螺纹数量': 4,
                    '螺纹规格': 'M12',
                    '法兰厚度': 14.0,
                    '密封面直径': 45.0,
                    '密封面厚度': 2.0
                },
                '系列2': {
                    '法兰内径': 19.0,
                    '法兰外径': 95.0,
                    '螺栓孔中心圆直径': 65.0,
                    '螺纹孔直径': 14,
                    '螺纹数量': 4,
                    '螺纹规格': 'M12',
                    '法兰厚度': 14.0,
                    '密封面直径': 45.0,
                    '密封面厚度': 2.0
                }
            }
        }
        
        return spec_data[DN][series]
    
    def update_parameters(self):
        spec_data = self.get_spec_data()
        
        self['法兰外径'] = spec_data['法兰外径']
        self['螺栓孔中心圆直径'] = spec_data['螺栓孔中心圆直径']
        self['螺纹孔直径'] = spec_data['螺纹孔直径']
        self['螺纹数量'] = spec_data['螺纹数量']
        self['螺纹规格'] = spec_data['螺纹规格']
        self['法兰厚度'] = spec_data['法兰厚度']
        self['密封面直径'] = spec_data['密封面直径']
        self['密封面厚度'] = spec_data['密封面厚度']
    
    @export
    def replace(self):
        self.update_parameters()
        
        spec_data = self.get_spec_data()
        
        D = spec_data['法兰外径']
        D1 = spec_data['螺栓孔中心圆直径']
        d = spec_data['螺纹孔直径']
        n = spec_data['螺纹数量']
        C = spec_data['法兰厚度']
        d1 = spec_data['法兰内径']
        d4 = spec_data['密封面直径']
        f1 = spec_data['密封面厚度']
        
        seal_type = self['密封面类型']
        
        outer_radius = D / 2
        inner_radius = d1 / 2
        
        flange_main = Cone(Vec3(0, 0, 0), Vec3(0, 0, C), outer_radius, outer_radius)
        flange_main = flange_main - Cone(Vec3(0, 0, -1), Vec3(0, 0, C + 1), inner_radius, inner_radius)
        
        bolt_hole_radius = d / 2
        bolt_circle_radius = D1 / 2
        
        bolt_holes = None
        for i in range(n):
            angle = 2 * math.pi * i / n
            hole_x = bolt_circle_radius * math.cos(angle)
            hole_y = bolt_circle_radius * math.sin(angle)
            hole = translate(Vec3(hole_x, hole_y, 0)) * Cone(Vec3(0, 0, -1), Vec3(0, 0, C + 1), bolt_hole_radius, bolt_hole_radius)
            if bolt_holes is None:
                bolt_holes = hole
            else:
                bolt_holes = bolt_holes + hole
        
        if bolt_holes is not None:
            flange_main = flange_main - bolt_holes
        
        if seal_type == '突面-RF':
            seal_radius = d4 / 2
            seal_ring = Cone(Vec3(0, 0, C), Vec3(0, 0, C + f1), seal_radius, seal_radius)
            seal_ring = seal_ring - Cone(Vec3(0, 0, C - 1), Vec3(0, 0, C + f1 + 1), inner_radius, inner_radius)
            flange_main = flange_main + seal_ring
        
        self['平焊法兰'] = flange_main.color(0.7, 0.7, 0.7, 1)

if __name__ == "__main__":
    FinalGeometry = 平焊法兰()
    place(FinalGeometry)
