from pyp3d import *

#建立参数化模型
class 信号灯(Component):
    def __init__(self):
        Component.__init__(self)

        #参数化模型初始参数
        #模型信息
        self['构件类型'] = Attr('被跨越物-铁路', obvious=True, readonly=True, group='模型信息')
        self['构件名称'] = Attr('信号灯', obvious=True, readonly=True, group='模型信息')

        #1.底座参数
        self['底座长度'] = Attr(800, obvious=True, group='底座')
        self['底座宽度'] = Attr(300, obvious=True, group='底座')
        self['底座高度'] = Attr(250, obvious=True, group='底座')
        self['底座'] = Attr(None, show=True)

        #2.转动轴参数
        self['转动轴底面边长'] = Attr(250, obvious=False, readonly=True, group='转动轴')
        self['转动轴顶面边长'] = Attr(150, obvious=False, readonly=True, group='转动轴')
        self['转动轴'] = Attr(None, show=True)

        #3.路灯背板参数
        self['后背板宽度'] = Attr(600, obvious=False, readonly=True, group='路灯背板')
        self['后背板高度'] = Attr(1300, obvious=False, readonly=True, group='路灯背板')
        self['后背板厚度'] = Attr(38, obvious=False, readonly=True, group='路灯背板')
        self['前背板宽度'] = Attr(560, obvious=False, readonly=True, group='路灯背板')
        self['前背板高度'] = Attr(1260, obvious=False, readonly=True, group='路灯背板')
        self['前背板厚度'] = Attr(100, obvious=False, readonly=True, group='路灯背板')
        self['背板'] = Attr(None, show=False)
        
        #4.信号灯参数
        self['信号灯宽度'] = Attr(400, obvious=False, readonly=True, group='信号灯')
        self['信号灯高度'] = Attr(400, obvious=False, readonly=True, group='信号灯')
        self['信号灯厚度'] = Attr(100, obvious=False, readonly=True, group='信号灯')
        self['灯泡半径'] = Attr(175, obvious=False, readonly=True, group='信号灯')
        self['灯泡厚度'] = Attr(50, obvious=False, readonly=True, group='信号灯')
        self['遮阳板悬挑长度'] = Attr(260, obvious=False, readonly=True, group='信号灯')
        self['信号灯'] = Attr(None, show=False)

        #5.边孔参数
        self['边孔宽度'] = Attr(75, obvious=False, readonly=True, group='边孔')
        self['边孔高度'] = Attr(75, obvious=False, readonly=True, group='边孔')
        self['边孔厚度'] = Attr(25, obvious=False, readonly=True, group='边孔')
        self['通孔半径'] = Attr(14, obvious=False, readonly=True, group='边孔')
        self['单边孔半径'] = Attr(25, obvious=False, readonly=True, group='边孔')
        self['通孔'] = Attr(None, show=False)
        self['单边孔'] = Attr(None, show=False)
        
        self['信号灯'] = Attr(None, show=True)

        self.replace()

    @export

    def replace(self):

        #1.底座模型建立
        L_base = self['底座长度']
        W_base = self['底座宽度']
        H_base = self['底座高度']
        base = translate(-L_base/2, 0) * scale(L_base, W_base, H_base) * Cube()
        self['底座'] = base

        #2.转动轴模型建立
        L_section1 = self['转动轴底面边长']
        L_section2 = self['转动轴顶面边长']
        section1 = Section(Vec3(-L_section1/2,0,0),Vec3(L_section1/2,0,0),Vec3(L_section1/2,L_section1,0),Vec3(-L_section1/2,L_section1,0))
        section2 = translate(0,100,25) * Section(Vec3(-L_section2/2,0,0),Vec3(L_section2/2,0,0),Vec3(L_section2/2,L_section2,0),Vec3(-L_section2/2,L_section2,0))
        axle_section = translate(0,0,H_base) * Loft(section1, section2)
        self['转动轴'] = axle_section

        #3.路灯背板模型建立
        W_panel1 = self['后背板宽度']
        H_panel1 = self['后背板高度']
        T_panel1 = self['后背板厚度']
        W_panel2 = self['前背板宽度']
        H_panel2 = self['前背板高度']
        T_panel2 = self['前背板厚度']
        panel1_section = rotate(Vec3(1,0,0),pi/2) * Section(
            Vec3(-W_panel1/2-20,0,0),
            Vec3(W_panel1/2-20,0,0),
            translate(W_panel1/2-20,20,0) * rotate(-pi/2) * scale(20,20,1) * Arc(pi/2),
            Vec3(W_panel1/2,H_panel1-20,0),
            translate(W_panel1/2-20,H_panel1-20,0) * scale(20,20,1) * Arc(pi/2),
            Vec3(-W_panel1/2-20,H_panel1,0),
            translate(-W_panel1/2+20,H_panel1-20,0) * rotate(pi/2) * scale(20,20,1) * Arc(pi/2),Vec3(-W_panel1/2,20,0),
            translate(-W_panel1/2+20,20,0) * rotate(pi) * scale(20,20,1) * Arc(pi/2))
        panel1_section = translate(0,200-T_panel1,H_base+25) * Loft(panel1_section, translate(0,T_panel1) * panel1_section)
        panel2_section = rotate(Vec3(1,0,0),pi/2) * Section(Vec3(-W_panel2/2-20,0,0),Vec3(W_panel2/2-20,0,0),translate(W_panel2/2-20,20,0) * rotate(-pi/2) * scale(20,20,1) * Arc(pi/2),Vec3(W_panel2/2,H_panel2-20,0),translate(W_panel2/2-20,H_panel2-20,0) * scale(20,20,1) * Arc(pi/2),Vec3(-W_panel2/2-20,H_panel2,0),translate(-W_panel2/2+20,H_panel2-20,0) * rotate(pi/2) * scale(20,20,1) * Arc(pi/2),Vec3(-W_panel2/2,20,0),translate(-W_panel2/2+20,20,0) * rotate(pi) * scale(20,20,1) * Arc(pi/2))
        panel2_section = translate(0,200-T_panel2,H_base+25+20) * Loft(panel2_section, translate(0,T_panel2) * panel2_section)
        self['背板'] = Combine(panel1_section, panel2_section)

        #4.信号灯模型建立
        W_bulb_panel = self['信号灯宽度']
        H_bulb_panel = self['信号灯高度']
        T_bulb_panel = self['信号灯厚度']
        r_bulb = self['灯泡半径']
        T_bulb = self['灯泡厚度']
        L_shelf = self['遮阳板悬挑长度']

        bulb_panel1 = translate(-W_bulb_panel/2,0,0) * scale(W_bulb_panel,T_bulb_panel,H_bulb_panel) * Cube()
        bulb_panel2 = translate(-W_bulb_panel/2,0,H_bulb_panel) * scale(W_bulb_panel,T_bulb_panel,H_bulb_panel) * Cube()
        bulb_panel3 = translate(-W_bulb_panel/2,0,H_bulb_panel + H_bulb_panel) * scale(W_bulb_panel,T_bulb_panel,H_bulb_panel) * Cube()
        bulb_panel = translate(0,50,H_base+25+50) * Combine(bulb_panel1, bulb_panel2, bulb_panel3)

        bulb_section = rotate(Vec3(1,0,0),pi/2) * Section(scale(r_bulb-10,r_bulb-10,r_bulb-10) * Arc(2*pi))
        bulb1 = translate(0, 0, r_bulb) * Loft(bulb_section, translate(0,T_bulb) * bulb_section).color(28/255,28/255,28/255,0.5)
        bulb2 = translate(0, 0, r_bulb*3) * Loft(bulb_section, translate(0,T_bulb) * bulb_section).color(238/255,0,0,0.5)
        bulb3 = translate(0, 0, r_bulb*5) * Loft(bulb_section, translate(0,T_bulb) * bulb_section).color(28/255,28/255,28/255,0.5)
        bulb = translate(0,0,H_base+25+50+75) * Combine(bulb1, bulb2, bulb3)

        shelf_seciton1 = rotate(Vec3(1,0,0),pi/2) * Section(scale(r_bulb,r_bulb,r_bulb) * Arc(2*pi))
        shelf1 = Loft(shelf_seciton1, translate(0,L_shelf, 0) * shelf_seciton1)
        shelf_seciton2 = rotate(Vec3(1,0,0),pi/2) * Section(scale(r_bulb+5,r_bulb+5,r_bulb+5) * Arc(2*pi))
        shelf2 = Loft(shelf_seciton2, translate(0,L_shelf, 0) * shelf_seciton2)
        shelf = shelf2 - shelf1
        shelf_seciton3 = translate(-500,-525,-900) * rotate(Vec3(1,0,0),pi/6) * scale(1000,1000,1000) * Cube()
        shelf = Combine(translate(0,-r_bulb,r_bulb+H_base+25+50+75) * (shelf - shelf_seciton3),translate(0,-r_bulb,r_bulb*3+H_base+25+50+75) * (shelf - shelf_seciton3),translate(0,-r_bulb,r_bulb*5+H_base+25+50+75) * (shelf - shelf_seciton3))


        self['信号灯'] = Combine(bulb_panel, bulb, shelf)

        #5.边孔模型建立
        W_hole = self['边孔宽度']
        H_hole = self['边孔高度']
        T_hole = self['边孔厚度']
        r1_hole = self['通孔半径']
        r2_hole = self['单边孔半径']

        hole_panel1 = translate(-W_hole/2, 0, -H_hole/2) * scale(W_hole, T_hole, H_hole) * Cube()
        hole1 = rotate(Vec3(1,0,0),pi/2) * Section(scale(r1_hole, r1_hole, r1_hole) * Arc(2*pi))
        hole1 = Loft(hole1, translate(0,T_hole)*hole1)
        hole1 = Combine(translate(325,170,1400+H_base-250) * (hole_panel1 - hole1),translate(325,170,1470+H_base-250) * (hole_panel1 - hole1),translate(325,170,490+H_base-250) * (hole_panel1 - hole1),translate(325,170,420+H_base-250) * (hole_panel1 - hole1),translate(-325,170,1400+H_base-250) * (hole_panel1 - hole1),translate(-325,170,1470+H_base-250) * (hole_panel1 - hole1),translate(-325,170,490+H_base-250) * (hole_panel1 - hole1),translate(-325,170,420+H_base-250) * (hole_panel1 - hole1))

        hole_panel2 = translate(-W_hole/2, 0, -H_hole/2) * scale(W_hole, T_hole, H_hole) * Cube()
        hole2 = rotate(Vec3(1,0,0),pi/2) * Section(scale(r2_hole, r2_hole, r2_hole) * Arc(2*pi))
        hole2 = Loft(hole2, translate(0,T_hole)*hole2)
        hole2 = Combine(translate(325,170,1195+H_base-250) * (hole_panel2 - hole2),translate(-325,170,1195+H_base-250) * (hole_panel2 - hole2))

        self['通孔'] = Combine(hole1, hole2)

        self['信号灯'] = translate(0,-100,50) * rotate(Vec3(1,0,0),-pi/12) * Combine(self['背板'], self['信号灯'], self['通孔'])
    
if __name__ == "__main__":
    place(信号灯())

