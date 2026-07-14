from pyp3d import *
class 接地扁铁螺栓连接(Component):
    def __init__(self):
        Component.__init__(self)
        self['接地扁铁螺栓连接'] = Attr(None, show=True)
        self['场布类型'] = Attr("设备接地", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("扁铁", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("接地扁铁直段", obvious=True, readonly=False, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['扁铁长'] = Attr(150.0, obvious=True,group='扁铁')
        self['扁铁宽'] = Attr(50.0, obvious=True,group='扁铁')
        self['扁铁厚'] = Attr(20.0, obvious=True,group='扁铁')
        self['扁铁个数'] = Attr(1,obvious=True, readonly = True,group='扁铁')
        self['总长度'] = Attr(60, obvious=True)
        self['扁铁X'] = Attr(0, obvious=False)
        self['扁铁Y'] = Attr(0, obvious=False)
        self['扁铁Z'] = Attr(0, obvious=False)
        self.replace()

    @export
    def replace(self):

        bt_l = self['扁铁长']
        bt_d = self['扁铁宽']
        bt_h = self['扁铁厚']
        n = int(self['总长度']/self['扁铁长'])
        print(type(n))
        supple_l = self['总长度'] - (bt_l*n)
        self['扁铁个数'] = n

        # 扁铁单元
        bt_first = scale(bt_l,bt_d,bt_h) * Cube().color(1,1,0,1)
        bt_second = scale(bt_l,bt_d,bt_h) * Cube().color(0,0,0,1)

        # 扁铁补充段
        def supplebt(supple_i):
            if supple_i %2==1:
                supple_second = combine(
                    translate(bt_l*(supple_i),0,0) * scale(supple_l,bt_d,bt_h) * Cube().color(0,0,0,1),
                )
                return(supple_second)
            else:
                supple_first = combine(
                    translate(bt_l*(supple_i),0,0) * scale(supple_l,bt_d,bt_h) * Cube().color(1,1,0,1),
                )
                return(supple_first)


        # 循环组装

        bt1 = Array(bt_first)
        bt2 = Array(bt_second)
        bt_supple = combine()
        for i in range(n):
            if i%2==0:  # 奇数段
                bt1.append(translate(i*bt_l,0,0))
            else:       # 偶数段
                bt2.append(translate(i*bt_l,0,0))
            if i==n-1 and supple_l>0:
                bt_supple = supplebt(i+1)
                n = n+1
        self['扁铁个数'] = n
        # 定位
        bt = translate(0,-0.5*bt_d,0) * combine(bt1,bt2,bt_supple)
        finalmodel = bt
        self['接地扁铁螺栓连接'] = finalmodel 


if __name__ == "__main__":
    Final_Geometry = 接地扁铁螺栓连接()
    TwoPointPlace.linearize(Final_Geometry,'总长度')
    place(Final_Geometry)