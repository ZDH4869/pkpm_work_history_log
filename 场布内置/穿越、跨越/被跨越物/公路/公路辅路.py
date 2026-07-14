from pyp3d import *
class 高速公路辅路(Component):
    def __init__(self):
        Component.__init__(self)
        self['高速公路辅路'] = Attr(None, show=True)
        self['场布类型'] = Attr("施工线路三跨", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("被跨越物—公路", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("高速公路辅路", obvious=True, readonly=False, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['宽度'] = Attr(7500, obvious=True,group='高速公路辅路')
        self['高度'] = Attr(220, obvious=True,group='高速公路辅路')
        self['长度'] = Attr(0, obvious=True,group='高速公路辅路')
        self['分道线宽度'] = Attr(150, obvious=True, readonly=True,group='高速公路辅路')
        self['高速公路辅路X'] = Attr(0, obvious=False)
        self['高速公路辅路Y'] = Attr(0, obvious=False)
        self['高速公路辅路Z'] = Attr(0, obvious=False)
        self.replace()

    @export
    def replace(self):

        w = self['宽度']
        h = self['高度']
        L = self['长度']
        x = self['高速公路辅路X']
        y = self['高速公路辅路Y']
        z = self['高速公路辅路Z']
        Angle = self['旋转角度']
        n = int(self['长度']/3000)
        print(type(n))

        fl = translate(x,y,z) * rotation(math.pi/180 * Angle) * scale(L,w,h) * Cube().color(128/255,138/255,135/255,1)
        fl_final = translate(Vec3(0,-w/2,0))*fl

        fdx = translate(x,y,z) * rotation(math.pi/180 * Angle) * scale(2000,150,1) * Cube().color(225/255,225/255,225/255,1)
        fdx_final = translate(Vec3(0,-75,h))*fdx

        fdx2 = Array(fdx_final)
        for i in linspace(Vec3(0,0,0),Vec3(L-2000,0,0),n):
            fdx2.append(translate(i))
        finalmodel = fdx2
        
        leftline = translate(x,y,z) * rotation(math.pi/180 * Angle) * scale(L,150,1) * Cube().color(225/255,225/255,225/255,1)
        leftline = translate(Vec3(0,-w/2,h))*leftline

        rightline = translate(Vec3(0,w-150,0))*leftline

        self['高速公路辅路'] = combine(fl_final,finalmodel,leftline,rightline)

if __name__ == "__main__":
    Final_Geometry = 高速公路辅路()
    TwoPointPlace.linearize(Final_Geometry,'长度')
    place(Final_Geometry)