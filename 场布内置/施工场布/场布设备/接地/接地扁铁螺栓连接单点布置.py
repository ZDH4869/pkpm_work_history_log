from pyp3d import *
class 接地扁铁螺栓连接单点布置(Component):
    def __init__(self):
        Component.__init__(self)
        self['接地扁铁螺栓连接单点布置'] = Attr(None, show=True)
        self['场布类型'] = Attr("设备接地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("扁铁", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("接地扁铁螺栓连接单点布置", obvious=True, readonly=True, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['扁铁长'] = Attr(150.0, obvious=True,group='扁铁')
        self['扁铁宽'] = Attr(50.0, obvious=True,group='扁铁')
        self['扁铁厚'] = Attr(5.0, obvious=True,group='扁铁')
        self['搭接长度'] = Attr(50,obvious=True,group='扁铁')
        self['扁铁个数'] = Attr(1,obvious=True,group='扁铁')
        #self['长度'] = Attr(200, obvious=True, group='扁铁')
        #self['总长度'] = Attr()
        self['扁铁X'] = Attr(0, obvious=False)
        self['扁铁Y'] = Attr(0, obvious=False)
        self['扁铁Z'] = Attr(0, obvious=False)
        self.replace()

    @export
    def replace(self):

        bt_c = self['扁铁长']
        bt_g = self['扁铁宽']
        bt_h = self['扁铁厚']
        bt_x = self['扁铁X']
        bt_y = self['扁铁Y']
        bt_z = self['扁铁Z']
        dj_c = self['搭接长度']
        n = self['扁铁个数']
        Angle = self['旋转角度']
        self['总长度'] = bt_c* n


        一段扁铁 = translate(bt_x,bt_y,bt_z) * rotation(math.pi/180 * Angle) * scale(bt_c,-bt_h,bt_g) * Cube().color(1,1,0,1)
        二段扁铁 = translate(bt_x,bt_y,bt_z) * rotation(math.pi/180 * Angle) * scale(bt_c,-bt_h,bt_g) * Cube().color(0,0,0,1)
        二段扁铁 = translate(Vec3(bt_c-dj_c,bt_h,0))*二段扁铁
        # bt = combine(一段扁铁,二段扁铁)
        # bt = rotate(Vec3(1,0,0),pi*1.5) *translate(0,0,-bt_g/2) *bt

        sxt_top = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), scale(3) * Arc(pi/2), Vec2(0,0))
        sxt_way = Line(scale(1) * Arc(pi*2))
        sxt_topp = Sweep(sxt_top,sxt_way).color(225/255,225/255,225/255,1)
        sectionOut =  Section(scale(2) * Arc(pi*2))
        sectionOut_final = translate(0, 0, -bt_h*2-2)*sectionOut
        
        BottomPipe =  Loft(sectionOut, sectionOut_final)

        top = (sxt_topp + BottomPipe).color(225/255,225/255,225/255,1)
        top = translate(Vec3(bt_c-35,0,bt_h)) * top

        top2 = translate(Vec3(20,0,0)) * top

        TOP = combine(top,top2)

        #BT1 = (一段扁铁 - TOP).color(1,1,0,1)
        BT1 = rotate(Vec3(1,0,0),pi*1.5) *translate(0,0,-bt_g/2) *一段扁铁
        A = (BT1-TOP).color(1,1,0,1)
        #BT2 = (二段扁铁 - TOP).color(0,0,0,1)
        BT2 = rotate(Vec3(1,0,0),pi*1.5) *translate(0,0,-bt_g/2) *二段扁铁
        B = (BT2-TOP).color(0,0,0,1)
        a = combine(TOP,A,B) 

        p1 = linspace(Vec3(0,0,0),Vec3(n*bt_c,0,0),n)
        r1 = []
        for point in p1:
            r1.append(translation(point)*a)
        New_r1 = combine(*r1)
        self['接地扁铁螺栓连接单点布置'] = New_r1

if __name__ == "__main__":
    Final_Geometry = 接地扁铁螺栓连接单点布置()
    place(Final_Geometry)