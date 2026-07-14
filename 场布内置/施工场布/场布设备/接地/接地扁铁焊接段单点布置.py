from pyp3d import *
class 接地扁铁焊接段单点布置(Component):
    def __init__(self):
        Component.__init__(self)
        self['接地扁铁焊接段单点布置'] = Attr(None, show=True)
        self['场布类型'] = Attr("设备接地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("扁铁", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("接地扁铁焊接段单点布置", obvious=True, readonly=True, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['扁铁长'] = Attr(150.0, obvious=True,group='扁铁')
        self['扁铁宽'] = Attr(50.0, obvious=True,group='扁铁')
        self['扁铁厚'] = Attr(5.0, obvious=True,group='扁铁')
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
        n = self['扁铁个数']
        Angle = self['旋转角度']
        self['总长度'] = bt_c* n


        一段扁铁 = translate(bt_x,bt_y,bt_z) * rotation(math.pi/180 * Angle) * scale(bt_c,-bt_h,bt_g) * Cube().color(1,1,0,1)
        二段扁铁 = translate(bt_x,bt_y,bt_z) * rotation(math.pi/180 * Angle) * scale(bt_c,-bt_h,bt_g) * Cube().color(0,0,0,1)
        二段扁铁 = translate(Vec3(bt_c-50,bt_h,0))*二段扁铁
        bt = combine(一段扁铁,二段扁铁)
        bt = rotate(Vec3(1,0,0),pi*1.5) *translate(0,0,-bt_g/2) *bt

        self['接地扁铁焊接段单点布置'] = bt

        p1 = linspace(Vec3(0,0,0),Vec3(n*bt_c,0,0),n)
        r1 = []
        for point in p1:
            r1.append(translation(point)*bt)
        New_r1 = combine(*r1)
        self['接地扁铁焊接段单点布置'] = New_r1

if __name__ == "__main__":
    Final_Geometry = 接地扁铁焊接段单点布置()
    place(Final_Geometry)