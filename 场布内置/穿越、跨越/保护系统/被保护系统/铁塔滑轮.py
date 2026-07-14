from pyp3d import *
class 铁塔滑轮(Component):
    def __init__(self):
        Component.__init__(self)
        self['导线分类数'] = Attr(2.0, obvious=True, readonly = False)
        self['底径'] = Attr(280.0, obvious=True, readonly = False)
        self['架高'] = Attr(470.0, obvious=True, readonly = False)
        self['底径参数限制说明'] = Attr('底径只能为280、400、560、710、800、900', obvious=True, readonly = True)
        self['导线分类数限制说明'] = Attr('导线分类数只能为1/2/4', obvious=True, readonly = True)
        self['铁塔滑轮'] = Attr(None, show=True)
        self.replace()
    @export
    def replace(self):
        if self['底径'] == 280 or self['底径'] == 400 or self['底径'] == 560 or self['底径'] == 710 or self['底径'] == 800 or self['底径'] == 900:
            IR = self['底径']
        else:
            IR = 280
            self['底径'] = IR
        if self['导线分类数'] == 1:
            AW = 60
            AN = 1
        elif self['导线分类数'] == 2:
            AW = 180
            AN = 3
        elif self['导线分类数'] == 4:
            AW = 300
            AN = 5
        else:
            AW = 60
            AN = 1
            self['导线分类数'] = 1

        # 描述截面

        AH = self['架高']
        headsection1 = Section(Line(Vec3(20+AW/2,0,0), Vec3(-20-AW/2,0,0), Vec3(0,70,0),Vec3(20+AW/2,0,0)))
        headsection2 = Section(translate(0,40)*scale(10) * Arc(2*pi))
        standsection = Section(Vec3(0,0,0), Vec3(0,15,0), Vec3(20,15,0), Vec3(20,13,0), Vec3(2,13,0), Vec3(2,-13,0), Vec3(20,-13,0), Vec3(20,-15,0), Vec3(0,-15,0))
        basesection = Section(Vec3(0,0,0),Vec3(0,20,0), Vec3(25,20,0), Vec3(25,-20,0), Vec3(0,-20,0))
        pulleysection1 = Section(Vec3(0,25,0),Vec3(-60,25,0),Vec3(-60,0,0),Vec3(0,0,0))
        pulleysection2a = translate(0,IR/2-20)*Section(Vec3(0,65,0),Vec3(-60,65,0),Vec3(-60,0,0),Vec3(0,0,0))
        pulleysection2b = translate(-30,IR/2+45)*Section(scale(45)*Arc(2*pi))
        pulleysection3 = Section(Vec3(-25,10,0),Vec3(-35,10,0),Vec3(-35,-10,0),Vec3(-25,-10,0))
        # 描述轨迹
        line1 = Line(Vec3(0,0,0), Vec3(0,0,20))
        line2 = Line(Vec3(0,0,0), Vec3(0,0,AH-100))
        line3 = Line(Vec3(0,0,0), Vec3(0,0,3))
        pulleyline1 = Line(rotate(Vec3(0,0,1),pi/2)*rotate(Vec3(1,0,0),pi/2)*scale(25)* Arc(2*pi))
        pulleyline2 = Line(Vec3(0,0,0), Vec3(0,0,IR/2-5))
        
        # 扫略
        head1 =Loft(headsection1, translate(Vec3(0,0,20))*headsection1).color(0.75,0.75,0.75,1)
        head2 =Loft(headsection2, translate(Vec3(0,0,20))*headsection2).color(0.75,0.75,0.75,1)
        head = translate(0,10,AH-100)*rotate(Vec3(1,0,0),pi/2) * (head1 - head2)
        stand =translate(AW/2,0,0)*Loft(standsection, translate(Vec3(0,0,AH-100))*standsection).color(0.75,0.75,0.75,1)
        stand2 = translate(-AW/2,0,0)*rotate(pi)*Loft(standsection,  translate(Vec3(0,0,AH-100))*standsection).color(0.75,0.75,0.75,1)
        base = translate(AW/2,0,0)*Loft(basesection,  translate(Vec3(0,0,3)) * basesection).color(0.75,0.75,0.75,1)
        base2 = translate(-AW/2,0,0)*rotate(pi)*Loft(basesection,  translate(Vec3(0,0,3)) * basesection).color(0.75,0.75,0.75,1)
        pulley1 = translate(AW/2,0,AH*0.4)*Sweep(pulleysection1, pulleyline1).color(0.6,0.6,0.6,1)
        pulley2 = translate(AW/2,0,AH*0.4)*(Sweep(pulleysection2a, pulleyline1)-Sweep(pulleysection2b, pulleyline1))
        pulley2.color(237/255,233/255,206/255,1)
        pulley3 = Loft(pulleysection3, translate(Vec3(0,0,IR/2-5)) *pulleysection3).color(237/255,233/255,206/255,1)
        pulleyArraya = Array(pulley3)
        for i in range(6):
            pulleyArraya.append(rotate(Vec3(1,0,0),pi/3*i))
        pulley3a=translate(AW/2,0,AH*0.4)*pulleyArraya
        pulley=combine(pulley1,pulley2,pulley3a)
        pulleyArrayb = Array(pulley)
        for i in range(AN):
            pulleyArrayb.append(translate(-60*i,0,0))
        self['铁塔滑轮']=combine(head,stand,stand2,base,base2,pulleyArrayb)
if __name__ == "__main__":
    place(铁塔滑轮())