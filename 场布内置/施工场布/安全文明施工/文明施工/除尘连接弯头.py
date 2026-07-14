from pyp3d import *
class 连接弯头(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['场布类型'] = Attr("临水", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("防尘", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("除尘连接弯头", obvious=True, group="构件分类")
        self['壁厚'] = Attr(3, obvious=True, group="连接弯头")
        self['转角度数'] = Attr(90, obvious=True, group="连接弯头")
        self['直径'] = Attr(20, obvious=True, group="连接弯头")
        self['连接弯头'] = Attr(None, show=True)

        
        self.replace()

    @export
    def replace(self):    
        wg_D = self['直径']
        wg_W = self['壁厚']
        wg_R = wg_D * 1.5
        self['弯曲半径'] = wg_R 

        if wg_D < 25:
            wg_R=38

        if wg_W>=wg_D/2:
            wg_W=wg_D/2-1
        
        sectionOut3 = translation(wg_R,0,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(wg_D,wg_D) * Arc(math.pi*2))
        line3 = Line(scale(500) * Arc(math.pi/180 * self['转角度数']))
        sweep3 = Sweep(sectionOut3,line3)
        sweep3=rotate(Vec3(1,0,0),0.5*pi) * sweep3
        sweep3=rotate(Vec3(0,0,1),0.5*pi) * sweep3

        sectionOut4 = translation(wg_R,0,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(wg_D - wg_W*2,wg_D - wg_W*2) * Arc(math.pi*2))
        line4 = Line(scale(500) * Arc(math.pi/180 * self['转角度数']))
        sweep4 = Sweep(sectionOut4,line4)
        sweep4=rotate(Vec3(1,0,0),0.5*pi) * sweep4
        sweep4=rotate(Vec3(0,0,1),0.5*pi) * sweep4

        wg = (sweep3 - sweep4)
        wg = translate(Vec3(0,-wg_R,0))*wg
        self['连接弯头'] = (wg)  

            
if __name__ == "__main__":
    Final_Geometry = 连接弯头()
    #RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)