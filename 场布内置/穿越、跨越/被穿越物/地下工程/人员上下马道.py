from pyp3d import *
class 人员上下马道(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['应用场景'] = Attr("隧道穿越", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("地下工程", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("人员马道", obvious=True, group="构件分类")
        self['垂直高度'] = Attr(1200, obvious=True, readonly=True, group="马道尺寸")
        self['水平长度'] = Attr(6000, obvious=True, group="马道尺寸")
        self['马道宽度'] = Attr(800, obvious=True, group="马道尺寸")
        self['扶手高度'] = Attr(1200, obvious=True, group="扶手尺寸")
        self['平台高'] = Attr(1200, obvious=True,group="平台尺寸")
        self['平台宽'] = Attr(800, obvious=True,readonly=True, group="平台尺寸")
        self['平台长'] = Attr(1500, obvious=True, group="平台尺寸")
        self['平台厚'] = Attr(200, readonly=True, group="平台尺寸")
        self['平台出口'] = Attr("左", obvious=True, group="平台尺寸")
        self['人员上下马道'] = Attr(None, show=True)

        self.replace()

    @export
    def replace(self):

        # active parameters
        L_access=self['水平长度']
        D_access=self['马道宽度']
        H_handrail=self['扶手高度']
        h_platform=self['平台高']
        l_platform=self['平台长']      
        t_platform=self['平台厚']
        平台出口=self['平台出口']#选择左时，站在地面面对坡道时平台左边无栏杆，右侧同理。
        # passsive parameters        
        d_platform=D_access
        self['平台宽']=d_platform
        H_access=h_platform
        self['垂直高度']=H_access
        # create access and platform
        section_access= to_section(Vec3(0,0,0),Vec3(0,D_access,0), Vec3(0,D_access,t_platform), Vec3(0,0,t_platform))
        section1_access= to_section(Vec3(-L_access+l_platform,0,h_platform),Vec3(-L_access+l_platform,D_access,h_platform), 
        Vec3(-L_access+l_platform,D_access,t_platform+h_platform), Vec3(-L_access+l_platform,0,t_platform+h_platform))
        section_platform= to_section(Vec3(-L_access,0,h_platform),Vec3(-L_access,d_platform,h_platform), 
        Vec3(-L_access,d_platform,t_platform+h_platform), Vec3(-L_access,0,t_platform+h_platform))
        loft_ap= Loft(section_platform, section1_access, section_access).color(255/255,255/255,0/255,1)

        # create handrail
        
        sec= rotate(Vec3(0,1,0), 0.5*pi)*Section(scale(7.5) * Arc(pi*2))
        #扶手截面
        sec1_hd= translate(0, 0, t_platform+H_handrail)*sec
        sec2_hd= translate(-L_access+l_platform, 0, h_platform+t_platform+H_handrail)*sec
        sec3_hd= translate(-L_access, 0, h_platform+t_platform+H_handrail)*rotate(Vec3(0,0,1), -0.25*pi)*scale(1.414)*sec
        sec4_hd= translate(-L_access, d_platform, h_platform+t_platform+H_handrail)*rotate(Vec3(0,0,1), 0.25*pi)*scale(1.414)*sec
        sec6_hd= translate(0, d_platform, t_platform+H_handrail)*sec
        sec5_hd= translate(-L_access+l_platform, d_platform, h_platform+t_platform+H_handrail)*sec
        #竖杆
        sec7_hd= translate(0, 0, t_platform)*rotate(Vec3(0,1,0), -0.5*pi)*sec
        sec8_hd= translate(0, 0, t_platform+H_handrail)*rotate(Vec3(0,1,0), -0.5*pi)*sec
        loft_hdg= Loft(sec7_hd, sec8_hd)
        fence1_array=Array(loft_hdg)
        #斜坡竖杆
        for i in linspace(Vec3(0, 0, 0), Vec3(-L_access+l_platform,0,h_platform), int(((L_access)/500))):
            fence1_array.append(translate(i))
        fence5=translate(0, D_access, 0)*fence1_array
        fence3_array=Array(loft_hdg)
        #平台竖杆
        for j in linspace(Vec3(-L_access,0,h_platform), Vec3(-L_access,d_platform,h_platform), int((h_platform/500))):
            fence3_array.append(translate(j))                
        if 平台出口 == "左":
            loft1_hd= Loft(sec1_hd, sec2_hd)
            loft2_hd= Loft(sec3_hd, sec4_hd, sec5_hd, sec6_hd)
            fence2_array=Array(loft_hdg)
            for k in linspace(Vec3(-L_access+l_platform, D_access, h_platform), Vec3(-L_access,d_platform, h_platform), int((l_platform/500))):        
                fence2_array.append(translate(k))
        if 平台出口 == "右":
            loft1_hd= Loft(sec5_hd, sec6_hd)
            loft2_hd= Loft(sec1_hd, sec2_hd, sec3_hd, sec4_hd)
            for k in linspace(Vec3(-L_access+l_platform, 0, h_platform), Vec3(-L_access, 0, h_platform), int((l_platform/500))):        
                fence2_array.append(translate(k))
        fence=combine(fence1_array, fence5, fence3_array, fence2_array)
        loft_hd= combine(loft1_hd, loft2_hd)
        handrail=combine(fence, loft_hd, translate(0,0,-H_handrail/2)*loft_hd).color(255/255, 0/255, 0/255, 1)
        self['人员上下马道'] = combine(loft_ap, handrail)

if __name__ == "__main__":
    Final_Geometry = 人员上下马道 ()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)            

