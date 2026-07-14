from pyp3d import *

class 电气化接触网(Component):
    def __init__(self):
        Component.__init__(self)

        #设置模型初始参数
        #设置模型信息
        self['构件类型'] = Attr('被跨越物—铁路', obvious=True, readonly=True, group='构件信息')
        self['构件名称'] = Attr('电气化接触网', obvious=True, readonly=True, group='构件信息')
        self['支柱颜色'] = Attr('白色', obvious=True, readonly=True, group='构件信息')
        self['腕臂颜色'] = Attr('银白色', obvious=True, readonly=True, group='构件信息')

        #1.基础参数
        self['基础长度'] = Attr(400, obvious=True, group='基础')
        self['基础宽度'] = Attr(400, obvious=True, group='基础')
        self['基础厚度'] = Attr(0, obvious=True, group='基础')
        self['基础'] = Attr(None, show=True)

        #2.柱子参数
        self['支柱长'] = Attr(280, obvious=True, group='支柱')
        self['支柱宽'] = Attr(280, obvious=True, group='支柱')
        self['支柱高'] = Attr(6300, obvious=True, readonly=True, group='支柱')
        self['翼缘宽度'] = Attr(18, obvious=False, group='支柱')
        self['腹板宽度'] = Attr(10.5, obvious=False, group='支柱')
        self['半径'] = Attr(24, obvious=False, group='支柱')
        self['柱子'] = Attr(None, show=True)

        #3.腕臂参数
        self['腕臂臂长'] = Attr(4100, obvious=True, group='腕臂')
        self['腕臂直径'] = Attr(100, obvious=True, group='腕臂')
        self['腕臂高'] = Attr(6000, obvious=True, group='腕臂')
        self['圆片直径'] = Attr(200, obvious=False, readonly=True, group='腕臂')
        self['腕臂'] = Attr(None, show=True)

        #4.拉杆参数
        self['拉杆与腕臂间距'] = Attr(2000, obvious=True, group='拉杆')
        self['拉杆长'] = Attr(4100, obvious=True, readonly=True, group='拉杆')
        self['拉杆直径'] = Attr(100, obvious=True, readonly=True, group='拉杆')
        self['旋转角度'] = Attr(60, obvious=True, group='拉杆')
        self['拉杆'] = Attr(None, show=True)

        self.replace()
    @export
    def replace(self):

        #1.基础模型建立
        L_base = self['基础长度']
        W_base = self['基础宽度']
        H_base = self['基础厚度']
        #2.柱子模型建立
        L_pillar = self['支柱长']
        W_pillar = self['支柱宽']
        H_pillar = self['支柱高']
        T_pillar1 = self['翼缘宽度']
        T_pillar2 = self['腹板宽度']
        r_pillar = self['半径']
        #3.腕臂模型建立
        L_pipe = self['腕臂臂长']
        H_pipe = self['腕臂高']
        d_pipe = self['腕臂直径']
        #4.拉杆模型建立
        L_support = self['拉杆长']
        d_support = self['拉杆直径']
        dist_support = self['拉杆与腕臂间距']
        Angle = self['旋转角度']

        #1.基础模型建立
        base = translate(-L_base/2, -W_base/2) * scale(L_base, W_base, -H_base) * Cube()
        self['基础'] = base

        #2.柱子模型建立
        pillar = Section(Vec3(0, 0, 0), Vec3(L_pillar, 0, 0), Vec3(L_pillar, T_pillar1, 0), Vec3(L_pillar/2+T_pillar2/2+r_pillar, T_pillar1, 0),
         translate(L_pillar/2+T_pillar2/2+r_pillar, T_pillar1+r_pillar) * rotate(-pi/2) * scale(r_pillar, r_pillar) * Arc(-pi/2), 
         Vec3(L_pillar/2+T_pillar2/2, W_pillar-T_pillar1-r_pillar,0), 
         translate(L_pillar/2+T_pillar2/2+r_pillar, W_pillar-T_pillar1-r_pillar,0) * rotate(pi) * scale(r_pillar, r_pillar) * Arc(-pi/2), 
         Vec3(L_pillar, W_pillar-T_pillar1,0),Vec3(L_pillar, W_pillar, 0),Vec3(0,W_pillar,0),Vec3(0,W_pillar-T_pillar1,0),Vec3(L_pillar/2-T_pillar2/2-r_pillar,W_pillar-T_pillar1,0), 
         translate(L_pillar/2-T_pillar1/2-r_pillar,W_pillar-T_pillar1-r_pillar,0) * rotate(pi/2) * scale(r_pillar, r_pillar) * Arc(-pi/2), 
         Vec3(L_pillar/2-T_pillar2/2,T_pillar1+r_pillar,0), 
         translate(L_pillar/2-T_pillar2/2-r_pillar,T_pillar1+r_pillar,0) * scale(r_pillar, r_pillar) * Arc(-pi/2), 
         Vec3(0,T_pillar1,0))
        H_pillar = H_pipe + 300
        pillar = rotate(pi/2) * translate(-L_pillar/2,-W_pillar/2) * Loft(pillar, translate(0,0,H_pillar)*pillar)

        self['柱子'] = pillar.color(1,1,1,1)

        #3.腕臂模型建立
        pipe_section = rotate(pi/2) * rotate(Vec3(1,0,0),pi/2) * Section(scale(d_pipe/2,d_pipe/2) * Arc(2*pi))
        pipe = Loft(pipe_section, translate(L_pipe,0,0)*pipe_section)
        pipe = translate(L_pillar/2,0,H_pipe) * pipe
        circle_section = rotate(pi/2) * rotate(Vec3(1,0,0),pi/2) * Section(scale(d_pipe,d_pipe) * Arc(2*pi))
        circle = Loft(circle_section, translate(10,0,0)*circle_section)
        circle = Array(circle)
        for i in linspace(Vec3(0,0,0),Vec3(500,0,0),9):
            circle.append(translate(i))

        self['腕臂'] = combine(pipe, translate(300,0,H_pipe) * circle).color(245/255,245/255,245/255,1)

        #4.拉杆模型建立
        Angle = 90-Angle
        d_support = d_pipe
        support_section = rotate(pi/2) * rotate(Vec3(1,0,0),pi/2) * Section(scale(d_support/2,d_support/2) * Arc(2*pi))
        L_support = dist_support/math.sin(pi/180 * Angle)
        support = Loft(support_section, translate(L_support,0,0)*support_section)
        support = combine(support , translate(300,0,0) * circle)
        support = rotate(Vec3(0,-1,0), math.pi/180 * Angle) * support
        support = translate(L_pillar/2,0,H_pipe-dist_support) * support

        self['拉杆'] = support.color(245/255,245/255,245/255,1)
        
        
if __name__ == "__main__":
    place(电气化接触网())
