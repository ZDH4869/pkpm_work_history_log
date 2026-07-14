from os import waitpid
from pyp3d import *
class 接地扁铁直角转弯段(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['场布类型'] = Attr("设备接地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("扁铁", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("接地扁铁直角转弯段", obvious=True, group="构件分类")
        self['起始段长'] = Attr(150, obvious=True, group="两端尺寸")
        self['末尾段长'] = Attr(150, obvious=True, group="两端尺寸")
        self['宽'] = Attr(50, obvious=True, group="扁铁尺寸")
        self['厚'] = Attr(5, obvious=True, group="扁铁尺寸")
        self['弯段角度'] = Attr(90, obvious=True, readonly=True, group="弯段尺寸")
        self['弯段半径'] = Attr(20, obvious=True, group="弯段尺寸")
        self['弯段方向'] = Attr("右", obvious=True, group="弯段尺寸")
        self['接地扁铁直角转弯段'] = Attr(None, show=True)

        
        self.replace()

    @export
    def replace(self):
       
        y_l = self['起始段长']
        
        h_l = self['末尾段长']
        d = self['宽']
        h = self['厚']


        r = self['弯段角度']
        rd = self['弯段半径']

        sczd = translate(0,0,0)*  rotate(Vec3(0,0,1), 2*pi)* rotate(Vec3(0,0,1), pi/180*r)* translate(d+rd,rd,0)* scale(h_l,d,h) *Cube().color(0,0,0,1) 
        wd = translation(rd,0,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), Vec2(d,0), Vec2(d,h), Vec2(0,h))
        line = Line(scale(500) * Arc(pi/180*r))
        wd_f = Sweep(wd , line)
        wd_f = rotate(Vec3(0,0,1),pi) * translate(Vec3(0,-d-rd,0)) * rotate(Vec3(0,1,0),pi)* rotate(Vec3(0,0,1),pi*0.5)* translate(Vec3(0,0,-h))* wd_f.color(1,1,0,1)
        yczd = translate(0,0,0)* rotate(Vec3(0,0,1), 0.5*pi)* rotate(Vec3(0,0,1), pi+pi/180*r) *scale(y_l,d,h) * Cube().color(0,0,0,1)
        bg = combine(sczd,wd_f,yczd)
        bg = translate(Vec3(-y_l,-(d/2),0)) * bg
        bg = rotate(pi) * bg
        if self['弯段方向'] == "左":
            bg = translate(0,0,h) * rotate(Vec3(1,0,0),pi) * bg
        else:
            self['弯段方向'] == "右"

        self['接地扁铁直角转弯段'] = bg
if __name__ == "__main__":
    Final_Geometry = 接地扁铁直角转弯段()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)
