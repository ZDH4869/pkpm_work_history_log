from pyp3d import *
import math

class 格构构件(Component):
    def __init__(self):
        Component.__init__(self)

        self['名称'] = Attr('格构柱', obvious = True, readonly = True, group = '基本参数')
        self['柱高'] = Attr(4500, obvious = True, readonly = False, group = '基本参数')

        self['分支间距H3'] = Attr(1000, obvious = True, readonly = False, group = '分支')

        #分支截面1
        self['翼缘宽度 B1'] = Attr(400, obvious = True, readonly = False, group = '分支1截面')
        self['腹板厚度 T1'] = Attr(16, obvious = True, readonly = False, group = '分支1截面')
        self['翼缘厚度 T2'] = Attr(20, obvious = True, readonly = False, group = '分支1截面')
        self['截面高度 H1'] = Attr(500, obvious = True, readonly = False, group = '分支1截面')

        #分支截面2
        self['翼缘宽度 B2'] = Attr(400, obvious = True, readonly = False, group = '分支2截面')
        self['腹板厚度 T3'] = Attr(16, obvious = True, readonly = False, group = '分支2截面')
        self['翼缘厚度 T4'] = Attr(20, obvious = True, readonly = False, group = '分支2截面')
        self['截面高度 H2'] = Attr(500, obvious = True, readonly = False, group = '分支2截面')

        #缀条
        self['横缀条中心间距'] = Attr(1000, obvious = True, readonly = False, group = '缀条')
        self['横缀条距柱底距离'] = Attr(1000, obvious = True, readonly = False, group = '缀条')
        
        self['h'] = Attr(124, obvious = True, readonly = False, group = '横缀条截面')
        self['b'] = Attr(124, obvious = True, readonly = False, group = '横缀条截面')
        self['R'] = Attr(8, obvious = True, readonly = False, group = '横缀条截面')
        self['tw'] = Attr(5, obvious = True, readonly = False, group = '横缀条截面')
        self['t'] = Attr(8, obvious = True, readonly = False, group = '横缀条截面')

        self['h0'] = Attr(124, obvious = True, readonly = False, group = '斜缀条截面')
        self['b0'] = Attr(124, obvious = True, readonly = False, group = '斜缀条截面')
        self['R0'] = Attr(8, obvious = True, readonly = False, group = '斜缀条截面')
        self['tw0'] = Attr(5, obvious = True, readonly = False, group = '斜缀条截面')
        self['t0'] = Attr(8, obvious = True, readonly = False, group = '斜缀条截面')

        self['缀板b'] = Attr(20, obvious = True, readonly = False, group = '缀板')
        self['缀板t'] = Attr(6, obvious = True, readonly = False, group = '缀板')
        self['缀板R'] = Attr(3.5, obvious = True, readonly = False, group = '缀板')



        self['模型'] = Attr(None, show = True)
        self.setDrivenFeaturePoint('格构柱点位', SnapMode.EndPoint, '[定位点X]', '[定位点Y]' ,'[定位点Z]')

    @export
    def replace(self):
        #柱
        H = self['柱高']
        H3 = self['分支间距H3']
        
        #分支截面1
        B1 = self['翼缘宽度 B1']
        T1 = self['腹板厚度 T1']
        T2 = self['翼缘厚度 T2']
        H1 = self['截面高度 H1']

        #分支截面2
        B2 = self['翼缘宽度 B1']
        T3 = self['腹板厚度 T1']
        T4 = self['翼缘厚度 T2']
        H2 = self['截面高度 H1']

        #横截条
        h = self['h']
        b = self['b']
        R = self['R']
        tw = self['tw']
        t = self['t']

        #斜截条
        h0 = self['h0']
        b0 = self['b0']
        R0 = self['R0']
        tw0 = self['tw0']
        t0 = self['t0']

        #缀条
        h1 = self['横缀条中心间距']
        h2 = self['横缀条距柱底距离']

        #缀板
        b_1 = self['缀板b']
        t_1 = self['缀板t']
        R_1 = self['缀板R']

        #分支截面1
        line1 = Line(Vec2((H1-2*T2)/2,T1/2),Vec2((H1-2*T2)/2,B1/2),Vec2(H1/2,B1/2),Vec2(H1/2,-B1/2),Vec2((H1-2*T2)/2,-B1/2),Vec2((H1-2*T2)/2,-T1/2),Vec2(-(H1-2*T2)/2,-T1/2),Vec2(-(H1-2*T2)/2,-B1/2),Vec2(-H1/2,-B1/2),Vec2(-H1/2,B1/2),Vec2(-(H1-2*T2)/2,B1/2),Vec2(-(H1-2*T2)/2,T1/2),Vec2((H1-2*T2)/2,T1/2))
        section1 = Section(line1)
        sweepline1 = Line(Vec3(0,0,0),Vec3(0,0,H))
        sweep1 = trans(Vec3(0,H3/2,0)) * Sweep(section1,sweepline1)

        #分支截面2
        line2 = Line(Vec2((H2-2*T4)/2,T3/2),Vec2((H2-2*T4)/2,B2/2),Vec2(H2/2,B2/2),Vec2(H2/2,-B2/2),Vec2((H2-2*T4)/2,-B2/2),Vec2((H2-2*T4)/2,-T3/2),Vec2(-(H2-2*T4)/2,-T3/2),Vec2(-(H2-2*T4)/2,-B2/2),Vec2(-H2/2,-B2/2),Vec2(-H2/2,B2/2),Vec2(-(H2-2*T4)/2,B2/2),Vec2(-(H2-2*T4)/2,T3/2),Vec2((H2-2*T4)/2,T3/2))
        section2 = Section(line2)
        sweepline2 = Line(Vec3(0,0,0),Vec3(0,0,H))
        sweep2 = trans(Vec3(0,-H3/2,0)) * Sweep(section2,sweepline2)

        #横截条
        line3_1 = Line(Vec2(-b/2,0),Vec2(-b/2,-t),Vec2(-tw/2-R,-t),translate(-R-tw/2,-R-t) * rotz(pi/2) * scale(R) * Arc(-pi/2),Vec2(-tw/2,-h),Vec2(tw/2,-h),Vec2(tw/2,-R-t),translate(R+tw/2,-R-t) * rotz(pi) * scale(R) * Arc(-pi/2),Vec2(b/2,-t),Vec2(b/2,0),Vec2(-b/2,0))
        section3_1 = rotx(pi/2) * rotz(pi/2) * Section(line3_1)
        section4_1 = rotx(pi/2) * rotz(-pi/2) * Section(line3_1)

        #斜截条
        line3_2 = Line(Vec2(-b0/2,0),Vec2(-b0/2,-t0),Vec2(-tw0/2-R0,-t0),translate(-R0-tw0/2,-R0-t0) * rotz(pi/2) * scale(R0) * Arc(-pi/2),Vec2(-tw0/2,-h0),Vec2(tw0/2,-h0),Vec2(tw0/2,-R0-t0),translate(R0+tw0/2,-R0-t0) * rotz(pi) * scale(R0) * Arc(-pi/2),Vec2(b0/2,-t0),Vec2(b0/2,0),Vec2(-b0/2,0))
        section3_2 = rotx(pi/2) * rotz(pi/2) * Section(line3_2)
        section4_2 = rotx(pi/2) * rotz(-pi/2) * Section(line3_2)

        #缀板
        line4 = Line(Vec2(0,b_1),Vec2(t_1,b_1),trans(t_1+R_1,t_1+R_1) * rotate(pi) * scale(R_1) * Arc(pi/2),Vec2(b_1,t_1),Vec2(b_1,0),Vec2(0,0))
        #将上部角点(0,b_1)移到局部原点，使sweepline穿过上部角点
        section0 = trans(0,-b_1,0) * Section(line4)


        x1 = -H1/2
        x2 = -H2/2
        x3 = H1/2
        x4 = H2/2
        y1 = H3/2
        y2 = -H3/2
        z0 = 0        
        z = h2
        
        #
        tan_val1 = h2/H3
        angle_rad1 = math.atan(tan_val1)
        angle_deg1 = math.degrees(angle_rad1)

        sweepline_T1 = Line(Vec3(x1,y1,z),Vec3(x2,y2,z))
        sweepline_T2 = Line(Vec3(x3,y1,z),Vec3(x4,y2,z))
        sweep_T1 = Sweep(trans(x1,y1,z) * section3_1,sweepline_T1)
        sweep_T2 = Sweep(trans(x3,y1,z) * section4_1,sweepline_T2)

        section5 = rotx(-angle_deg1*pi/180) * section3_2
        section6 = rotx(-angle_deg1*pi/180) * section4_2
        sweepline_T3 = Line(Vec3(x1,y1,z0),Vec3(x2,y2,z))
        sweepline_T4 = Line(Vec3(x3,y1,z0),Vec3(x4,y2,z))
        sweep_T3 = Sweep(trans(x1,y1,z0) * section5,sweepline_T3)
        sweep_T4 = Sweep(trans(x3,y1,z0) * section6,sweepline_T4)

        section0_1 = trans((x1+x2)/2+h0-75,(y1+y2)/2) * rotx(-angle_deg1*pi/180) * rotz(-pi/2) * rotx(pi/2) * section0
        sweepline0_1 = Line(Vec3((x1+x2)/2+h0-75,(y1+y2)/2,0),Vec3((x3+x4)/2-h0+75,(y1+y2)/2,0))
        sweep0_1 = Sweep(section0_1,sweepline0_1)

        sweep_T0 = sweep_T1 + sweep_T2 + sweep_T3 +sweep_T4

        while True:
            z = z + h1
            if z < H:
                tan_val2 = h1/H3
                angle_rad2 = math.atan(tan_val2)
                angle_deg2 = math.degrees(angle_rad2)

                section7 = rotx(-angle_deg2*pi/180) * section3_2
                section8 = rotx(-angle_deg2*pi/180) * section4_2
                sweepline_T5 = Line(Vec3(x1,y1,z-h1),Vec3(x2,y2,z))
                sweepline_T6 = Line(Vec3(x3,y1,z-h1),Vec3(x4,y2,z))
                sweep_T5 = Sweep(trans(x1,y1,z-h1) * section7,sweepline_T5)
                sweep_T6 = Sweep(trans(x3,y1,z-h1) * section8,sweepline_T6)

                sweepline_T1 = Line(Vec3(x1,y1,z),Vec3(x2,y2,z))
                sweepline_T2 = Line(Vec3(x3,y1,z),Vec3(x4,y2,z))
                sweep_T1 = Sweep(trans(x1,y1,z) * section3_1,sweepline_T1)
                sweep_T2 = Sweep(trans(x3,y1,z) * section4_1,sweepline_T2)

                sweep_T0 = sweep_T0 + sweep_T1 + sweep_T2 + sweep_T5 + sweep_T6
            else:
                tan_val3 = (H-z+h1)/H3
                angle_rad3 = math.atan(tan_val3)
                angle_deg3 = math.degrees(angle_rad3)

                section9 = rotx(-angle_deg3*pi/180) * section3_2
                section10 = rotx(-angle_deg3*pi/180) * section4_2
                sweepline_T7 = Line(Vec3(x1,y1,z-h1),Vec3(x2,y2,H))
                sweepline_T8 = Line(Vec3(x3,y1,z-h1),Vec3(x4,y2,H))
                sweep_T7 = Sweep(trans(x1,y1,z-h1) * section9,sweepline_T7)
                sweep_T8 = Sweep(trans(x3,y1,z-h1) * section10,sweepline_T8)
                sweep_T0 = sweep_T0 + sweep_T7 + sweep_T8
                break



        #self['模型'] = trans(0,0,0) * (sweep1 + sweep2 + sweep_T0 + sweep0_1)
        self['模型'] = combine(trans(-100,0,0) *section0_1, trans(-100,0,0) *sweepline0_1, sweep0_1)
        

if __name__ == "__main__":
    FinalGeometry = 格构构件()
    FinalGeometry.replace()
    place(FinalGeometry)