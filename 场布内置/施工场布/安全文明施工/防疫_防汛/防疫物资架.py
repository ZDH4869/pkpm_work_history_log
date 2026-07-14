from pyp3d import *
class 防疫物资架(Component):
    def __init__(self):
        Component.__init__(self)
        self['总长'] = Attr(2000.0, obvious=True,group="架子尺寸")
        self['总宽'] = Attr(600.0, obvious=True,group="架子尺寸")
        self['总高'] = Attr(2000, obvious = True,group="架子尺寸")
        self['防疫物资架'] = Attr(None, show=True)
        self['旋转角度'] = Attr(0,obvious = True,group="旋转")
        self['场布类型'] = Attr('防疫', obvious=True,readonly = True,group="构件分类")
        self['构件类型'] =  Attr('器具', obvious=True,readonly = True,group="构件分类")
        self['构件名称'] =  Attr('防疫物资架', obvious=True,group="构件分类")
        self.replace()
    @export
    def replace(self):
        z_l = self['总长']
        z_w = self['总宽']
        z_h = self['总高']
        场布类型 = self['场布类型']
        构件类型 = self['构件类型']
        Angle = self['旋转角度']
        jz_l=100
        jz_w=10
        p_w=50 #平台板厚度
        b_ll=50 #板距离上下距离
        b_lz=200#板距离下距离
        hz_l=350
        hz_w=400
        hz_h=250
        if self['总长']<hz_l*4+50:
            z_l=hz_l*4+50
            self['总长']=hz_l*4+50
        if self['总宽']<hz_w+50:
            z_w=hz_w+50
            self['总宽']=hz_w+50
        if self['总高']<(hz_h+50)*3+b_ll+b_lz+p_w:
            z_h=(hz_h+50)*3+b_ll+b_lz+p_w
            self['总高']=(hz_h+50)*3+b_ll+b_lz+p_w
        p_l=(z_h-b_ll-b_lz-p_w)/3
        #角柱
        section = Section(Vec2(0,0),Vec2(jz_l,0), Vec2(jz_l,jz_w), Vec2(jz_w,jz_w), Vec2(jz_w,jz_l),Vec2(0,jz_l))
        loft = Loft(section, translate(0,0,z_h) * section).color(61/255,150/255,190/255,1)
        z_x=translation(z_l/2,-z_w/2,0) *rotation(Vec3(0,0,1),0.5*pi) *loft
        z_y=translation(z_l/2,z_w/2,0) *rotation(Vec3(0,0,1),pi) *loft
        z_z=translation(-z_l/2,z_w/2,0) *rotation(Vec3(0,0,1),-pi/2) *loft
        z_c=translation(-z_l/2,-z_w/2,0)  *loft
        z_f=combine(z_x,z_y,z_z,z_c).color(61/255,150/255,190/255,1)
        # create_geometry(z_f)
        #平台
        section = Section(Vec2(-z_l/2+jz_w,-z_w/2+jz_w),Vec2(z_l/2-jz_w,-z_w/2+jz_w), Vec2(z_l/2-jz_w,z_w/2-jz_w), Vec2(-z_l/2+jz_w,z_w/2-jz_w))
        loft = Loft(section, translate(0,0,p_w) * section).color(61/255,150/255,190/255,1)
        p_x=translation(0,0,b_lz)  *loft
        p_y=translation(0,0,p_l)  *p_x
        p_z=translation(0,0,p_l*2)  *p_x
        p_c=translation(0,0,p_l*3)  *p_x
        p_f=combine(p_x,p_y,p_z,p_c).color(61/255,150/255,190/255,1)
        # create_geometry(p_f)
        #盒子
        section = Section(Vec2(-hz_l/2,-hz_w/2),Vec2(hz_l/2,-hz_w/2), Vec2(hz_l/2,hz_w/2), Vec2(-hz_l/2,hz_w/2))
        loft = Loft(section, translate(0,0,hz_h) * section).color(1,1,1,1)

        #消毒液盒子
        wz_x=translate(-105,-hz_w/2-0.01,100) *rotation(Vec3(1,0,0),pi/2) *Text("消毒液",50, 50).color(1,1,1,1)
        wz_y=rotation(Vec3(0,0,1),pi) *wz_x
        xy_h=combine(loft,wz_x,wz_y)

        xy_hx=translate(-hz_l/2,0,b_lz+p_w) *xy_h
        xy_hy=translate(hz_l/2,0,b_lz+p_w) *xy_h
        xy_hf=combine(xy_hy,xy_hx)
        # create_geometry(xy_hf)
        #口罩盒子
        wz_x=translate(-70,-hz_w/2-0.01,100) *rotation(Vec3(1,0,0),pi/2) *Text("口罩",50, 50).color(1,1,1,1)
        wz_y=rotation(Vec3(0,0,1),pi) *wz_x
        kz_h=combine(loft,wz_x,wz_y)

        kz_hx=translate(-hz_l/2-hz_l,0,b_lz+p_w+p_l) *kz_h
        kz_hy=translate(-hz_l/2,0,b_lz+p_w+p_l) *kz_h
        kz_hz=translate(hz_l/2,0,b_lz+p_w+p_l) *kz_h
        kz_hc=translate(hz_l/2+hz_l,0,b_lz+p_w+p_l) *kz_h
        kz_hf=combine(kz_hx,kz_hy,kz_hz,kz_hc)
        # create_geometry(kz_hf)
        #体温计盒子
        wz_x=translate(-105,-hz_w/2-0.01,100) *rotation(Vec3(1,0,0),pi/2) *Text("体温计",50, 50).color(1,1,1,1)
        wz_y=rotation(Vec3(0,0,1),pi) *wz_x
        tw_h=combine(loft,wz_x,wz_y)

        tw_h1=translate(-hz_l/2,0,b_lz+p_w+p_l*2) *tw_h
        # create_geometry(tw_h1)
        #洗手液盒子
        wz_x=translate(-105,-hz_w/2-0.01,100) *rotation(Vec3(1,0,0),pi/2) *Text("洗手液",50, 50).color(1,1,1,1)
        wz_y=rotation(Vec3(0,0,1),pi) *wz_x
        xs_h=combine(loft,wz_x,wz_y)

        xs_h1=translate(hz_l/2,0,b_lz+p_w+p_l*2) *xs_h
        # create_geometry(xs_h1)
        wzj_f=rotation(math.pi/180 * Angle) *translate(z_l/2,z_w/2,0) *combine(xs_h1,tw_h1,kz_hf,xy_hf,p_f,z_f)
        self['防疫物资架']=wzj_f

if __name__ == "__main__":
    place(防疫物资架())