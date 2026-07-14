from pyp3d import *
class 路灯单灯(Component):
    def __init__(self):
        Component.__init__(self)
        self['路灯-单灯'] = Attr(None, show=True)
        self['场布类型'] = Attr("施工线路三跨", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("被跨越物—公路", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("路灯-单灯", obvious=True, readonly=False, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['总高度'] = Attr(11000, obvious=True,group='路灯')
        self['灯杆上口直径'] = Attr(70, obvious=True,readonly=True,group='路灯')
        self['灯杆下口直径'] = Attr(202, obvious=True,readonly=True,group='路灯')
        self.replace()

    @export
    def replace(self):
        r_bottom = self['灯杆下口直径']/2
        r_top = self['灯杆上口直径']/2
        H = self['总高度']-2166
        if H < 1200:
            H = 1200
    #灯杆
        ld_bottom = rotate(Vec3(0,0,1), 0.5*pi) * to_section(Vec3(0,0,1200),Vec3(r_bottom,0,1200),Vec3(r_top,0,H),Vec3(0,0,H))
        ld_way = Line(scale(1) * Arc(pi*2))
        ldg = Sweep(ld_bottom,ld_way).color(225/255,225/255,225/255,1)

    #底杆
        lddg = rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(r_bottom,r_bottom) * Arc(math.pi*2))
        lddg_line = translate(0,1200,0) * lddg
        lddg_1 = Loft(lddg,lddg_line).color(30/255,144/255,1,1)
        lddg_final = rotate(Vec3(1,0,0),0.5*pi) * lddg_1

    #弯杆
        zw = translation(1000,0,0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(r_top,r_top) * Arc(math.pi*2))
        zw_line = Line(scale(1000) * Arc(math.pi/3))
        zw_1 = Sweep(zw,zw_line).color(225/255,225/255,225/255,1)
        zw_2=rotate(Vec3(1,0,0),0.5*pi) * zw_1
        zw_final = rotate(Vec3(0,0,1),0.5*pi) * translate(Vec3(-1000,0,H)) * zw_2

    #斜杆
        xg_jm = rotate(Vec3(0,0,1), 0.5*pi) * to_section(Vec3(0,0,0),Vec3(r_top,0,0),Vec3(r_top,0,1600),Vec3(0,0,1600))
        xg_way = Line(scale(1) * Arc(pi*2))
        xg = Sweep(xg_jm,xg_way).color(225/255,225/255,225/255,1)
        #xg_2 = rotate(Vec3(1,0,0),pi/3) * xg_1
        #xg = translate(Vec3(0,-500,H+866)) * xg_2

    #灯罩
        ldz = translate(-200,-50,1600) * scale(400,100,1000) * Cube()
        ldz_in = translate(-175,-50,1650) * scale(350,70,600) * Cube()
        ldz_final = (ldz - ldz_in).color(20/255,50/255,100/255,1)

        dg = rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(25,25) * Arc(math.pi*2))
        dg_line = translate(0,600,0) * dg
        dg_1 = Loft(dg,dg_line).color(1,1,0,0.7)
        dg_2 = rotate(Vec3(1,0,0),0.5*pi) * dg_1 
        dg_left = translate(75,-25,1650) * dg_2
        dg_right = translate(-150,0,0) * dg_left
        dg_final = combine(dg_left,dg_right)
        #ldz_2 = rotate(Vec3(1,0,0),pi/3) * ldz_1
        #ldz = translate(Vec3(0,-500,H+866)) * ldz_2

    #方向调整
        dz_1 = combine(xg,ldz_final,dg_final)
        dz_2 = rotate(Vec3(1,0,0),pi/3) * dz_1
        dz = translate(Vec3(0,-500,H+866)) * dz_2


        #ldg_z = ldg + zw_final + xg
        ld_1 = combine(ldg,lddg_final,ldg,zw_final,dz)
        ld = rotate(Vec3(0,0,1),pi/2) * ld_1
        self['路灯-单灯'] = ld


if __name__ == "__main__":
    Final_Geometry = 路灯单灯()
    #TwoPointPlace.linearize(Final_Geometry,'总长度')
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)

