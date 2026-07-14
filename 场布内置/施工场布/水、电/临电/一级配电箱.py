from pyp3d import *
from math import *
class 一级配电箱(Component):
    def __init__(self):
        Component.__init__(self)
        self['配电箱长'] = Attr(2000, obvious=True,group="配电箱")
        self['配电箱宽'] = Attr(600.0, obvious=True,group="配电箱")
        self['配电箱高'] = Attr(2000, obvious = True,group="配电箱")
        self['防护棚长'] = Attr(4000, obvious = True,group="防护棚")
        self['防护棚宽'] = Attr(3000, obvious = True,group="防护棚")
        self['防护棚高'] = Attr(2500, obvious = True,group="防护棚")
        self['顶棚高'] = Attr(500, obvious = True,group="顶棚")
        self['承台高'] = Attr(300, obvious = True,group="承台")
        self['一级配电箱'] = Attr(None, show=True)
        self['旋转角度'] = Attr(0,obvious = True,group="旋转")
        self['开关门'] = Attr("关门",obvious = True,group="开关门")
        self['场布类型'] = Attr('临电', obvious=True,readonly = True,group="构件分类")
        self['构件类型'] =  Attr('配电箱', obvious=True,readonly = True,group="构件分类")
        self['构件名称'] =  Attr('一级配电箱', obvious=True,group="构件分类")
        self.replace()
    @export
    def replace(self):
        cd_h = self['承台高']
        fh_l = self['防护棚长']
        fh_w = self['防护棚宽']
        fh_h = self['防护棚高']
        pd_l = self['配电箱长']
        pd_w = self['配电箱宽']
        pd_h = self['配电箱高']
        tp_h = self['顶棚高']
        men = self['开关门']
        场布类型 = self['场布类型']
        构件类型 = self['构件类型']
        Angle = self['旋转角度']
        pdd_h=200
        k_i=0
        if self['防护棚宽']<2000:
            fh_w=2000
            self['防护棚宽']=2000
        if self['防护棚长']<2500:
            fh_l=2500
            self['防护棚长']=2500
        if self['防护棚高']<2000:
            fh_h=2000
            self['防护棚高']=2000
        # if self['顶棚高']>(self['防护棚长']+200)*2/9:
        #     tp_h=(self['防护棚长']+200)*2/9
        #     self['顶棚高']=(self['防护棚长']+200)*2/9
        if  self['顶棚高']>800:
            tp_h =800
            self['顶棚高']=800
        if  self['顶棚高']<300:
            tp_h =300
            self['顶棚高']=300
        # if self['防护棚长']<-200+tp_h*5/2+tp_h/2*4:
        #     fh_l=-200+tp_h*5/2+tp_h/2*4
        #     self['防护棚长']=-200+tp_h*5/2+tp_h/2*4
        if self['配电箱长']>self['防护棚长']-300:
            pd_l=self['防护棚长']-300
            self['配电箱长']=self['防护棚长']-300
        if self['配电箱宽']>self['防护棚宽']-300:
            pd_w=self['防护棚宽']-300
            self['配电箱宽']=self['防护棚宽']-300
        # if self['配电箱高']<self['配电箱长']:
        #     pd_h=self['配电箱长']
        #     self['配电箱高']=self['配电箱长']
        if self['配电箱高']>self['防护棚高']-100-pdd_h:
            pd_h=self['防护棚高']-100-pdd_h
            self['配电箱高']=self['防护棚高']-100-pdd_h
        if self['配电箱宽']<300:
            pd_w=300
            self['配电箱宽']=300
        if self['配电箱长']<400:
            pd_l=400
            self['配电箱长']=400
        if men=="开门" or men=="开" :
            k_i=1
        if men=="关门" or men=="关" :
            k_i=0
        if pd_h>pd_l :
            kk=pd_l
        else:
            kk=pd_h
        san_ll=tp_h/2
        san_lz=kk/2
        #承台
        section = Section(Vec2(-fh_l/2-100,-fh_w/2-100),Vec2(fh_l/2+100,-fh_w/2-100), Vec2(fh_l/2+100,fh_w/2+100), Vec2(-fh_l/2-100,fh_w/2+100))
        loftx = Loft(section, translate(0,0,cd_h) * section).color(1,1,1,1)
        # create_geometry(loft)
        #配电箱
        section_w = Section(Vec2(-pd_l/2-50,-pd_w/2-50),Vec2(pd_l/2+50,-pd_w/2-50), Vec2(pd_l/2+50,pd_w/2+50), Vec2(-pd_l/2-50,pd_w/2+50))
        loft_wsection_w = translate(0,0,cd_h) *Loft(section_w, translate(0,0,pdd_h) * section_w).color(1,1,1,1)
        # create_geometry(loft_wsection_w)
        section_e = Section(Vec2(-pd_l/2,-pd_w/2),Vec2(pd_l/2,-pd_w/2), Vec2(pd_l/2,pd_w/2), Vec2(-pd_l/2,pd_w/2))
        loft_esection_e = translate(0,0,cd_h+pdd_h) *Loft(section_e, translate(0,0,pd_h) * section_e).color(147/255,60/255,44/255,1)
        # create_geometry(loft_esection_e)
        #防护棚 
        section_r = Section(Vec2(-fh_l/2,-fh_w/2+10),Vec2(-fh_l/2,-fh_w/2),Vec2(fh_l/2,-fh_w/2), Vec2(fh_l/2,fh_w/2), Vec2(-fh_l/2,fh_w/2),Vec2(-fh_l/2,-fh_w/2+1010),Vec2(-fh_l/2+10,-fh_w/2+1010), Vec2(-fh_l/2+10,fh_w/2-10), Vec2(fh_l/2-10,fh_w/2-10),Vec2(fh_l/2-10,-fh_w/2+10))
        loft_rsection_r = translate(0,0,cd_h) *Loft(section_r, translate(0,0,fh_h) * section_r).color(0.812,0.912,0.969,0.5)
        # create_geometry(loft_rsection_r)
        #顶棚
        section_u = Section(Vec2(-fh_l/2-100,-fh_w/2-100),Vec2(fh_l/2+100,-fh_w/2-100), Vec2(fh_l/2+100,fh_w/2+100), Vec2(-fh_l/2-100,fh_w/2+100))
        ding_w_x=translate(-500*5/4,-fh_w/2-100-1,cd_h+fh_h+tp_h/3) *rotation(Vec3(1,0,0),pi/2) *Text("一级配电箱",500/300,500/300).color(1,1,1,1)
        loft_m = translate(0,0,cd_h+fh_h) *Loft(section_u, translate(0,0,tp_h) * section_u).color(38/255,64/255,200/255,1)
        # create_geometry(loft_usection_u)

        #门
        section_i = Section(Vec2(0,10),Vec2(10,10), Vec2(10,1000), Vec2(0,1000))
        loft_i = translate(0,0,cd_h) *Loft(section_i, translate(0,0,fh_h) * section_i).color(0.812,0.912,0.969,0.5)
        section_a = Section(scale(5) * Arc(2*pi))
        loft_a =translate(5,5,0) *Loft(section_a, translate(0,0,20) * section_a,translate(0,0,40) * section_a).color(0.812,0.912,0.969,0.5)
        hua_wsection_w=translate(0,0,cd_h+fh_h/4) *loft_a
        hua_esection_e=translate(0,0,cd_h+fh_h*3/4) *loft_a
        m_wsection_w=rotation(Vec3(0,0,1),0.5*pi*k_i) *combine(hua_esection_e,hua_wsection_w,loft_i)
        m_esection_e=translate(-fh_l/2,-fh_w/2+10,0) *m_wsection_w
        # create_geometry(m_esection_e)
        #顶部文字
        #感叹号
        section = Section(Vec2(-san_ll/2,-san_ll/2*1.5),Vec2(san_ll/2,-san_ll/2*1.5), Vec2(san_ll/2,san_ll/2*1.5), Vec2(-san_ll/2,san_ll/2*1.5))
        loft = Loft(section, translate(0,0,0.01) * section).color(1,1,1,1)
        section_y = Section(Vec2(-san_ll/2,-san_ll*(sqrt(3)/2-3/4)),Vec2(san_ll/2,-san_ll*(sqrt(3)/2-3/4)), Vec2(0,san_ll/2*1.5))
        loft_ysection_y = translate(0,0,0.01) *Loft(section_y, translate(0,0,0.01) * section_y).color(0,0,0,1)
        section_z = Section(Vec2(-san_ll/2+20*sqrt(3)/2,10-san_ll*(sqrt(3)/2-3/4)),Vec2(san_ll/2-20*sqrt(3)/2,10-san_ll*(sqrt(3)/2-3/4)), Vec2(0,san_ll/2*1.5-20))
        loft_zsection_z = translate(0,0,0.01) *Loft(section_z, translate(0,0,0.01) * section_z).color(191/255,175/255,105/255,1)
        loft_usection_u=(loft_ysection_y-loft_zsection_z).color(0,0,0,1)
        section_c = Section(translate(0,san_ll/4,0) *scale(san_ll/15,san_ll/15) * Arc(math.pi),Vec2(-san_ll/20,0), Vec2(san_ll/20,0))
        loft_csection_c =Loft(section_c, translate(0,0,0.03) * section_c).color(0,0,0,1)
        section_v = Section(translate(0,-san_ll/8,0) *scale(san_ll/16,san_ll/16) * Arc(math.pi*2))
        loft_csection_v =Loft(section_v, translate(0,0,0.03) * section_v).color(0,0,0,1)
        loft_cv=translate(0,san_ll*3/16,0) *combine(loft_csection_c,loft_csection_v)
        wen_x= translate(-san_ll*7/20,-san_ll/2,1) *Text("注意安全",san_ll/800,san_ll/800).color(0,0,0,1)
        dxcd_x=translate(fh_l/2+100-san_ll,-fh_w/2-100-0.01,cd_h+fh_h+tp_h/2) *rotation(Vec3(1,0,0),pi/2) *combine(loft,loft_usection_u,loft_cv,wen_x,loft_zsection_z)
        #闪电
        section = Section(Vec2(-san_ll/2,-san_ll/2*1.5),Vec2(san_ll/2,-san_ll/2*1.5), Vec2(san_ll/2,san_ll/2*1.5), Vec2(-san_ll/2,san_ll/2*1.5))
        loft = Loft(section, translate(0,0,0.01) * section).color(1,1,1,1)
        section_y = Section(Vec2(-san_ll/2,-san_ll*(sqrt(3)/2-3/4)),Vec2(san_ll/2,-san_ll*(sqrt(3)/2-3/4)), Vec2(0,san_ll/2*1.5))
        loft_ysection_y = translate(0,0,0.01) *Loft(section_y, translate(0,0,0.01) * section_y).color(0,0,0,1)
        section_z = Section(Vec2(-san_ll/2+20*sqrt(3)/2,10-san_ll*(sqrt(3)/2-3/4)),Vec2(san_ll/2-20*sqrt(3)/2,10-san_ll*(sqrt(3)/2-3/4)), Vec2(0,san_ll/2*1.5-20))
        loft_zsection_z = translate(0,0,0.01) *Loft(section_z, translate(0,0,0.01) * section_z).color(191/255,175/255,105/255,1)
        loft_usection_u=(loft_ysection_y-loft_zsection_z).color(0,0,0,1)
        section_c = Section(Vec2(0,san_ll/4),Vec2(-san_ll/10,-san_ll/24), Vec2(san_ll/50,-san_ll/24),Vec2(0,-san_ll/4),Vec2(san_ll/10,san_ll/24),Vec2(-san_ll/50,san_ll/24))
        loft_csection_c = translate(0,san_ll*(-sqrt(3)/4+3/4-1/10),0.02) *Loft(section_c, translate(0,0,0.01) * section_c).color(0,0,0,1)
        wen_x= translate(-san_ll*7/20,-san_ll/2,1) *Text("当心触电",san_ll/800,san_ll/800).color(0,0,0,1)
        dxcd_xx=translate(-fh_l/2-100+san_ll,-fh_w/2-100-0.01,cd_h+fh_h+tp_h/2) *rotation(Vec3(1,0,0),pi/2) *combine(loft,loft_usection_u,loft_csection_c,wen_x,loft_zsection_z)
        dw_q=combine(dxcd_xx,dxcd_x,ding_w_x)
        dw_h=rotation(Vec3(0,0,1),pi) *dw_q
        dw=combine(dw_h,dw_q)
        # create_geometry(dw)
        #
        section = Section(Vec2(-san_lz/2,-san_lz/2*1.5),Vec2(san_lz/2,-san_lz/2*1.5), Vec2(san_lz/2,san_lz/2*1.5), Vec2(-san_lz/2,san_lz/2*1.5))
        loft = Loft(section, translate(0,0,0.01) * section).color(1,1,1,1)
        section_y = Section(Vec2(-san_lz/2,-san_lz*(sqrt(3)/2-3/4)),Vec2(san_lz/2,-san_lz*(sqrt(3)/2-3/4)), Vec2(0,san_lz/2*1.5))
        loft_ysection_y = translate(0,0,0.01) *Loft(section_y, translate(0,0,0.01) * section_y).color(0,0,0,1)
        section_z = Section(Vec2(-san_lz/2+20*sqrt(3)/2,10-san_lz*(sqrt(3)/2-3/4)),Vec2(san_lz/2-20*sqrt(3)/2,10-san_lz*(sqrt(3)/2-3/4)), Vec2(0,san_lz/2*1.5-20))
        loft_zsection_z = translate(0,0,0.01) *Loft(section_z, translate(0,0,0.01) * section_z).color(191/255,175/255,105/255,1)
        loft_b=(loft_ysection_y-loft_zsection_z).color(0,0,0,1)
        section_c = Section(Vec2(0,san_lz/4),Vec2(-san_lz/10,-san_lz/24), Vec2(san_lz/50,-san_lz/24),Vec2(0,-san_lz/4),Vec2(san_lz/10,san_lz/24),Vec2(-san_lz/50,san_lz/24))
        loft_csection_c = translate(0,san_lz*(-sqrt(3)/4+3/4-1/10),0.02) *Loft(section_c, translate(0,0,0.01) * section_c).color(0,0,0,1)
        wen_x= translate(-san_lz*7/20,-san_lz/2,1) *Text("当心触电",san_lz/800,san_lz/800).color(0,0,0,1)
        dxcd_xx=translate(0,-pd_w/2,cd_h+pdd_h+pd_h/2) *rotation(Vec3(1,0,0),pi/2) *combine(loft,loft_b,loft_csection_c,wen_x,loft_zsection_z)
        dxcd_xy=rotation(Vec3(0,0,1),pi) *dxcd_xx
        dxcd_xz=combine(dxcd_xy,dxcd_xx)
        # create_geometry(dxcd_xz)
        yi_f=rotation(math.pi/180 * Angle) *translate(fh_l/2+100,fh_w/2+100,0) *combine(loftx,loft_wsection_w,loft_esection_e,loft_rsection_r,loft_m,m_esection_e,dw,dxcd_xz)
        self['一级配电箱']=yi_f

if __name__ == "__main__":
    place(一级配电箱())