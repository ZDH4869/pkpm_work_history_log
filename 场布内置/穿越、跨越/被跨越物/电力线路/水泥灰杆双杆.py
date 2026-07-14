from pyp3d import *
class 水泥灰杆双杆(Component):
    def __init__(self):
        Component.__init__(self)
        self['水泥灰杆-双杆'] = Attr(None, show=True)
        self['场布类型'] = Attr("施工线路三跨", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("被跨越物—电力线路", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("水泥灰杆-双杆", obvious=True, readonly=False, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['电杆高度'] = Attr(15000, obvious=True,group='电杆')
        self['电杆间距'] = Attr(3000, obvious=True,group='电杆')
        self['电杆上口直径'] = Attr(200, obvious=True,group='电杆')
        self['电杆下口直径'] = Attr(350, obvious=True,group='电杆')
        self['横担位置高度'] = Attr(14000, obvious=True,group='横担')
        #self['横担长度'] = Attr(14000, obvious=True,group='横担')
        self['水泥灰杆双杆X'] = Attr(0, obvious=False)
        self['水泥灰杆双杆Y'] = Attr(0, obvious=False)
        self['水泥灰杆双杆Z'] = Attr(0, obvious=False)
        self['横担长度'] = Attr(1400, obvious=False,group='水泥灰杆')
        self.replace()

    @export
    def replace(self):
        r_bottom = self['电杆下口直径']/2
        r_top = self['电杆上口直径']/2
        dg_l = self['电杆间距']
        hd_l = self['电杆间距']+600*2  #横担长度
        self['横担长度'] = Attr(hd_l, obvious=True,readonly=True,group='横担')

        H = self['电杆高度']
        h = self['横担位置高度']
        x = self['横担长度']
        
        if h > H :
            h = H

        hg = rotate(Vec3(0,0,1), 0.5*pi) * to_section(Vec3(0,0,0),Vec3(r_bottom,0,0),Vec3(r_top,0,H),Vec3(0,0,H))
        hg_way = Line(scale(1) * Arc(pi*2))
        hg_final = Sweep(hg,hg_way).color(169/255,169/255,169/255,1)
        lift = translate(Vec3(-dg_l/2,0,0)) * hg_final
        right = translate(Vec3(dg_l/2,0,0)) * hg_final

        
        hd_1 = translate(Vec3(-hd_l/2,-50,-25)) * scale(hd_l,100,50) * Cube()
        hd_front = translate(Vec3(0,(r_top+r_bottom)*(H-h)/H+r_top+50,h)) * hd_1
        hd_behind = translate(Vec3(0,-((r_top+r_bottom)*(H-h)/H+r_top)-50,h)) * hd_1
        hd_combine = combine(hd_front,hd_behind).color(169/255,169/255,169/255,1)
        hd_2 = (hd_combine - lift).color(169/255,169/255,169/255,1)
        hd_final = (hd_2 - right).color(169/255,169/255,169/255,1)

        xz_1 = translate(Vec3(-x/2/3,-10,0)) * scale(20,20,60) * Cube()
        xz_2 = translate(Vec3(-x/3-300,-10,0)) * scale(20,20,60) * Cube()
        xz_3 = translate(Vec3(x/2/3,-10,0)) * scale(20,20,60) * Cube()
        xz_4 = translate(Vec3(x/3+300,-10,0)) * scale(20,20,60) * Cube()
        xz = combine(xz_1,xz_2,xz_3,xz_4)
        xz_front = translate(Vec3(0,(r_top+r_bottom)*(H-h)/H+r_top+50,h)) * xz
        xz_behind = translate(Vec3(0,-((r_top+r_bottom)*(H-h)/H+r_top)-50,h)) * xz
        xz_final = combine(xz_behind,xz_front)

         #短导线
        hd = Section(scale(6,6) * Arc(math.pi*2))
        hd_top = translate(Vec3(0,0,((r_top+r_bottom)*(H-h)/H+r_top*2)+100)) * hd
        dx_1 = Loft(hd, hd_top).color(1,1,1,1)
        hd_2 = translate(0,0,-r_top/2-50) * dx_1
        hd_3 = rotate(Vec3(1,0,0),0.5*pi) * hd_2
        dx_s1 = translate(Vec3(-x/2/3+10,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_s2 = translate(Vec3(-x/3-300,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_s3 = translate(Vec3(x/3+300,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_s4 = translate(Vec3(x/2/3,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_short_1 = combine(dx_s1,dx_s2,dx_s3,dx_s4)
        dx_short = translate(Vec3(0,0,h+60)) * dx_short_1.color(169/255,169/255,169/255,1)

       
        
        self['水泥灰杆-双杆'] = combine(lift,right,hd_final,dx_short,xz_final)


if __name__ == "__main__":
    Final_Geometry = 水泥灰杆双杆()
    #TwoPointPlace.linearize(Final_Geometry,'总长度')
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)