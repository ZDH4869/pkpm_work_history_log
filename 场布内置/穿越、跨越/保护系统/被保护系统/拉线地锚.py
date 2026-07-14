from pyp3d import *
import math
class 拉线地锚(Component):
    def __init__(self):
        Component.__init__(self)
        self['地锚型号（SDM），可选SDM3/5/10/16'] = Attr(3, obvious=True, readonly = False)
        self['拉线与地面角度'] = Attr(45.0, obvious=True, readonly = False)
        self['伸出地面长度'] = Attr(250.0, obvious=True, readonly = False)
        self['拉线末端高度'] = Attr(4000.0, obvious=True, readonly = False)
        self['埋深'] = Attr(1800.0, obvious=True, readonly = False)
        self['钢丝绳套直径'] = Attr(30.0, obvious=True, readonly = False)
        self['拉线直径'] = Attr(20.0, obvious=True, readonly = False)
        self['拉线地锚'] = Attr(None, show=True)
        self.replace()
    @export
    def replace(self):
        if self['地锚型号（SDM），可选SDM3/5/10/16'] == 3:
            SA = 800
            SB = 250
            SC = 150
        elif self['地锚型号（SDM），可选SDM3/5/10/16'] == 5:
            SA = 900
            SB = 270
            SC = 180
        elif self['地锚型号（SDM），可选SDM3/5/10/16'] == 10:
            SA = 1200
            SB = 290
            SC = 220
        elif self['地锚型号（SDM），可选SDM3/5/10/16'] == 16:
            SA = 1500
            SB = 500
            SC = 258
        # 描述截面

        R1 = 50
        L1 = self['伸出地面长度']
        D1 = self['埋深']
        H2 = self['拉线末端高度']
        Angle = self['拉线与地面角度']*pi/180
        L2 = D1/math.sin(Angle)
        L3 = H2/math.sin(Angle)-L1
        R2 = self['拉线直径']/2
        R3 = self['钢丝绳套直径']/2
        section1 = Section(Vec3(SA/2,SB/2,0), Vec3(-SA/2,SB/2,0),Vec3(-SA/2,-SB/2,0),Vec3(SA/2,-SB/2,0))
        section2 = to_section(Vec3(SA/4,SB/4,-SC), Vec3(-SA/4,SB/4,-SC),Vec3(-SA/4,-SB/4,-SC),Vec3(SA/4,-SB/4,-SC))
        section3 = Section(translate(R1,0)*scale(10) * Arc(2*pi))
        section4 = Section(scale(10) * Arc(2*pi))
        section3a = Section(translate(30,0)*scale(5) * Arc(2*pi))
        section4a = Section(scale(5) * Arc(2*pi))
        section4b = rotate(Vec3(0,1,0),pi/2)*Section(scale(5) * Arc(2*pi))
        section5 = Section(scale(R3) * Arc(2*pi))
        section5b = Section(scale(R2) * Arc(2*pi))

        # 描述轨迹
        line1 = rotate(Vec3(1,0,0),pi/2)*Line(scale(R1) * Arc(pi))
        line1a = rotate(Vec3(1,0,0),pi/2)*Line(scale(30) * Arc(pi))
        
        # 扫略
        testloft = Loft(section1,section2)
        sweep1 = translate(0,0,50)*Sweep(section3 , line1)
        Loft2 = translate(R1,0)*Loft(section4 , translate(0,0,50)*section4)
        Loft3 = translate(-R1,0)*Loft(section4 , translate(0,0,50)*section4)
        sweep1a = translate(0,0,40)*Sweep(section3a , line1a)
        Loft2a = translate(30,0,-20)*Loft(section4a , translate(0,0,60)*section4a)
        Loft3a = translate(-30,0,-20)*Loft(section4a , translate(0,0,60)*section4a)
        Loft3b = translate(40,0,-10)*Loft(section4b , translate(-80,0,0)*section4b)
        Loft4a = translate(0,0,110)*Loft(section5 , translate(0,0,L2)*section5).color(0.66,0.66,0.66)
        Loft4b = translate(0,0,110+L2)*Loft(section5 , translate(0,0,L1)*section5).color(0.66,0.66,0.66)
        Loft4c = translate(0,0,110+L2+L1)*Loft(section5 , translate(0,0,L3)*section5b).color(0.66,0.66,0.66)
        
        dimao = combine(testloft,sweep1,Loft2,Loft3).color(1,0,0)
        xiekou = combine(sweep1a,Loft2a,Loft3a,Loft3b).color(85/255,107/255,47/255)
        xiekou1 = translate(0,0,140)*rotate(Vec3(1,0,0),pi)*rotate(Vec3(0,0,1),pi/2)*xiekou
        xiekou2 = translate(0,0,140+L2+L1)*rotate(Vec3(1,0,0),pi)*rotate(Vec3(0,0,1),pi/2)*xiekou
        self['拉线地锚']=rotate(Vec3(0,1,0),Angle-pi/2)*translate(0,0,-110-L2)*combine(dimao,xiekou1,xiekou2,Loft4a,Loft4b,Loft4c)
if __name__ == "__main__":
    place(拉线地锚())