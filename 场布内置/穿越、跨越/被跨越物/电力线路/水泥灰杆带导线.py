from pyp3d import *
class 水泥灰杆带导线(Component):
    def __init__(self):
        Component.__init__(self)
        self['水泥灰杆-带导线'] = Attr(None, show=True)
        self['场布类型'] = Attr("施工线路三跨", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("被跨越物—电力线路", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("水泥灰杆-带导线", obvious=True, readonly=False, group="构件分类")
        self['电杆高度'] = Attr(15000, obvious=True,group='电杆')
        self['电杆间距'] = Attr(50000, obvious=True,group='电杆')
        self['电杆上口直径'] = Attr(200, obvious=True,group='电杆')
        self['电杆下口直径'] = Attr(350, obvious=True,group='电杆')
        self['电杆数量'] = Attr(2,obvious=True,group='电杆')

        self['横担位置高度'] = Attr(14000, obvious=True,group='横担')
        self['横担长度'] = Attr(1400, obvious=True,readonly=False,group='横担')

        self['导线直径'] = Attr(6, obvious=False, readonly=True, group='导线')
        self['导线数量'] = Attr(4, obvious=False, readonly=True, group='导线')
        
        self['导线弧垂'] = Attr(100, obvious=True, readonly=True,group='导线')
        self.replace()

    @export
    def replace(self):
        r_bottom = self['电杆下口直径']/2
        r_top = self['电杆上口直径']/2
        dx_r = self['导线直径']/2
        dg_l = self['电杆间距']
        n = self['电杆数量']

        H = self['电杆高度']
        h = self['横担位置高度']
        x = self['横担长度']

        sag = self['导线弧垂']
        h_max = H

        if h > H :
            h = H

        
    #电杆
        hg = rotate(Vec3(0,0,1), 0.5*pi) * to_section(Vec3(0,0,0),Vec3(r_bottom,0,0),Vec3(r_top,0,H),Vec3(0,0,H))
        hg_way = Line(scale(1) * Arc(pi*2))
        hg_final = Sweep(hg,hg_way).color(169/255,169/255,169/255,1)

    #短导线
        hd = Section(scale(6,6) * Arc(math.pi*2))
        hd_top = translate(Vec3(0,0,((r_top+r_bottom)*(H-h)/H+r_top*2)+100)) * hd
        dx_1 = Loft(hd, hd_top).color(1,1,1,1)
        hd_2 = translate(0,0,-r_top/2-50) * dx_1
        hd_3 = rotate(Vec3(1,0,0),0.5*pi) * hd_2
        dx_s1 = translate(Vec3(-x/2/3+10,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_s2 = translate(Vec3(-x/3+10,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_s3 = translate(Vec3(x/3+10,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_s4 = translate(Vec3(x/2/3+10,(r_top+r_bottom)*(H-h)/H/2+r_top/2,0)) * hd_3
        dx_short_1 = combine(dx_s1,dx_s2,dx_s3,dx_s4)
        dx_short = translate(Vec3(0,0,h+60)) * dx_short_1.color(169/255,169/255,169/255,1)
        
    #横担
        hd_1 = translate(Vec3(-x/2,-50,-25)) * scale(x,100,50) * Cube()
        xz_1 = translate(Vec3(-x/2/3,-10,0)) * scale(20,20,60) * Cube()
        xz_2 = translate(Vec3(-x/3,-10,0)) * scale(20,20,60) * Cube()
        xz_3 = translate(Vec3(x/2/3,-10,0)) * scale(20,20,60) * Cube()
        xz_4 = translate(Vec3(x/3,-10,0)) * scale(20,20,60) * Cube()
        xz = combine(xz_1,xz_2,xz_3,xz_4)
        xz_front = translate(Vec3(0,(r_top+r_bottom)*(H-h)/H+r_top+50,h)) * xz
        xz_behind = translate(Vec3(0,-((r_top+r_bottom)*(H-h)/H+r_top)-50,h)) * xz
        hd_front = translate(Vec3(0,(r_top+r_bottom)*(H-h)/H+r_top+50,h)) * hd_1
        hd_behind = translate(Vec3(0,-((r_top+r_bottom)*(H-h)/H+r_top)-50,h)) * hd_1
        #((r_top+r_bottom)*(H-h)/H+r_top)
        
        '''xz_1 = translate(Vec3(-x/2/3,-10,0)) * scale(20,20,60) * Cube()
        xz_2 = translate(Vec3(-x/3,-10,0)) * scale(20,20,60) * Cube()
        xz_3 = translate(Vec3(x/2/3,-10,0)) * scale(20,20,60) * Cube()
        xz_4 = translate(Vec3(x/3,-10,0)) * scale(20,20,60) * Cube()
        xz = combine(xz_1,xz_2,xz_3,xz_4)
        xz_front = translate(Vec3(0,r_top,h)) * xz
        xz_behind = translate(Vec3(0,-r_top,h)) * xz
        hd_front = translate(Vec3(0,r_top,h)) * hd_1
        hd_behind = translate(Vec3(0,-r_top,h)) * hd_1
        hd_final = combine(hd_front,hd_behind).color(169/255,169/255,169/255,1)
        hd_final = (hd_final - hg_final).color(169/255,169/255,169/255,1)'''
        hd_final = combine(xz_front,xz_behind,hd_front,hd_behind)
        
        

        
        #导线
        R = dx_r
        #angle = 2*atan(0.5*dg_l/(R-sag))
        dx_sec1=translate(-dg_l/2+200,(r_top+r_bottom)*(H-h)/H/2+r_top/2,h)*rotate(Vec3(0,1,0),pi/2)*scale(R)*Section(Arc(2*pi))
        dx_sec2=translate(dg_l/2-200,(r_top+r_bottom)*(H-h)/H/2+r_top/2,h)*rotate(Vec3(0,1,0),pi/2)*scale(R)*Section(Arc(2*pi))
        
        dx = Loft(dx_sec1, dx_sec2)



        dx_final = dx

        dx_a = translate(Vec3(0,-x/2/3+10,0)) * dx_final
        dx_b = translate(Vec3(0,-x/3+10,0)) * dx_final
        dx_c = translate(Vec3(0,x/3+10,0)) * dx_final
        dx_d = translate(Vec3(0,x/2/3+10,0)) * dx_final
        dx_final = translate(Vec3(0,0,0))*combine(dx_a,dx_b,dx_c,dx_d)
        

        dx_Array = Array(dx_final)
        
        snhg = combine(hg_final,hd_final,hd_3,dx_short)
        snhg_1 = rotate(Vec3(0,0,1),0.5*pi) * snhg
        
        snhg_Array = Array(snhg_1)
        

        for i in linspace(Vec3(0,0,0),Vec3((n-1)*dg_l,0,0),n):
            snhg_Array.append(translate(i))
        snhg_final = combine(snhg_Array)

        for i in linspace(Vec3(dg_l/2,0,0),Vec3((n-2)*dg_l+dg_l/2,0,0),n-1):
            dx_Array.append(translate(i))
        dx_final = combine(dx_Array)

        pole = combine(snhg_final,dx_final)


        #减掉方块会发生变形，导线向上移。       
        self['水泥灰杆-带导线'] = pole


if __name__ == "__main__":
    Final_Geometry = 水泥灰杆带导线()
    #TwoPointPlace.linearize(Final_Geometry,'总长度')
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)