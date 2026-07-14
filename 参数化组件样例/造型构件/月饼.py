from pyp3d import *


class 月饼(Component):
    def __init__(self):
        Component.__init__(self)
        self['月饼直径'] = Attr(128.0, obvious=True)
        self['月饼厚'] = Attr(48.0, obvious=True)
        self['切开'] = Attr('否', obvious=True)
        self['月饼'] = Attr(None, show=True)

        self.replace()
    @export
    def replace(self):
        radis = self['月饼直径']
        thickness = self['月饼厚']
        # 截面
        mainsection = Section(scale(radis/2) * Arc(2*pi))
        # 主体放样
        mainloft = Loft(mainsection, translate(0,0,thickness) * mainsection).color(255/255,183/255,14/255,0.95)
        laceworkradis = radis/25
        # 馅儿
        mainsectioninner = Section(scale(radis/2-radis/20) * Arc(2*pi))
        mainloftinner = Loft(translate(0,0,radis/20) *mainsectioninner, translate(0,0,thickness-radis/20) * mainsectioninner).color(228/255,101/255,29/255,1)
        # 花边放样
        laceworksection = Section(scale(laceworkradis*2) * Arc(pi))
        laceworkloft = Loft(translate(0,0,thickness/24)*laceworksection, translate(0,0,thickness-(thickness/24)) * laceworksection)
        laceworkloft = translate(-radis/2+2,0,0)*rotate(pi/2)*laceworkloft.color(255/255,183/255,14/255,0.95)
        arraylaceworkloft = Array(laceworkloft)
        for i in range(0,360,18):
            arraylaceworkloft.append(rotate(i*(pi/180)))
        sphere = scale(radis) * Sphere()
        spheresub = translate(0,0,thickness-68)*scale(radis) * Sphere()
        sphere = sphere-spheresub
        sphere= translate(0,0,thickness-91)*sphere
        arraylaceworkloft = arraylaceworkloft-sphere
        arraylaceworkloft.color(255/255,183/255,14/255,0.95)
        #文字
        textline1 = translate(-radis/4,radis/12,thickness+1)*Text("中秋",radis/6,radis/9).color(228/255,101/255,29/255,1)
        textline2 = translate(-radis/4,-radis/5,thickness+1)*Text("快乐",radis/6,radis/9).color(228/255,101/255,29/255,1)
        #顶部圆环
        sectionOutloop = translate(-radis/3,0,thickness)*rotate(Vec3(1,0,0), 0.5*pi)*Section(scale(radis/100) *Arc(pi))
        lineloop = Line(Arc(2*pi))
        sweeploop = Sweep(sectionOutloop , lineloop).color(228/255,101/255,29/255,1)
        #顶部花纹
        sectionOutdecorativedesign = translate(-radis/8,0,thickness)*rotate(Vec3(1,0,0), 0.5*pi)*Section(scale(radis/100) *Arc(pi))
        linedecorativedesign = Line(Arc(pi))
        sweepdecorativedesign = translate(-radis/2.1,0,0)*rotate(pi/2)*Sweep(sectionOutdecorativedesign , linedecorativedesign).color(228/255,101/255,29/255,1)
        arraysweepdecorativedesign= Array(sweepdecorativedesign)
        for i in range(0,360,18):
            arraysweepdecorativedesign.append(rotate(i*(pi/180)))

        self['月饼'] = combine(mainloft,mainloftinner,arraylaceworkloft,textline1,textline2,sweeploop,arraysweepdecorativedesign)

        if self['切开'] == '是':
            cube =  translate(0,0,-10)*scale(radis,radis,radis) * Cube()
            mainloft = (mainloft-cube).color(255/255,183/255,14/255,0.95)
            arraylaceworkloft = (arraylaceworkloft-cube).color(255/255,183/255,14/255,0.95)
            textline1 = translate(-radis/4,radis/12,thickness+1)*Text("中",radis/6,radis/9).color(228/255,101/255,29/255,1)
            arraysweepdecorativedesign = (arraysweepdecorativedesign-cube).color(228/255,101/255,29/255,1)
            sweeploop = (sweeploop-cube).color(228/255,101/255,29/255,1)
            mainloftinner = (mainloftinner-translate(1,1,0)*cube).color(228/255,101/255,29/255,1)
            self['月饼'] = combine(mainloft,mainloftinner,arraylaceworkloft,textline1,textline2,sweeploop,arraysweepdecorativedesign)

if __name__ == "__main__":
    place(月饼())


