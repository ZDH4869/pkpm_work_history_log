from pyp3d import *
class 龙门架(Component):
    def __init__(self):
        Component.__init__(self)
        
        self['应用场景'] = Attr("隧道穿越", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("地下工程", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("龙门架", obvious=True,readonly=False, group="构件分类")
        self['整体高'] = Attr(4000, obvious=True, group="架子尺寸")
        self['整体跨度'] = Attr(3500, obvious=True, group="架子尺寸")
        self['底梁长度'] = Attr(1500, obvious=True, group="架子尺寸")
        self['横梁高'] = Attr(180, obvious=True, group="细节尺寸")
        self['横梁宽'] = Attr(94, obvious=True,group="细节尺寸")
        self['腹板厚'] = Attr(10.7, obvious=True,readonly=True, group="细节尺寸")
        self['立柱截面边长'] = Attr(140, obvious=True, group="细节尺寸")
        self['斜杠截面边长'] = Attr(100, obvious=True, group="细节尺寸")
        self['底梁截面边长'] = Attr(120, obvious=True, group="细节尺寸")
        self['龙门架'] = Attr(None, show=True)

        self.replace()

    @export
    def replace(self):

        H1=self['整体高']
        W1=self['整体跨度']
        W3=self['底梁长度']
        #横梁尺寸
        H_beam=self['横梁高']
        d_beam=self['横梁宽']
        t_beam=self['腹板厚']
        #截面边长
        d_pillar=self['立柱截面边长']      
        d_slash=self['斜杠截面边长']
        d_mudsill=self['底梁截面边长']
        #底梁
        section = to_section(Vec3(-W3/2,0,0),Vec3(-W3/2,d_mudsill,0), Vec3(-W3/2,d_mudsill,d_mudsill), Vec3(-W3/2,0,d_mudsill))
        loft = Loft(section, translate(W3,0,0) * section)
        m_1=translation(0,0,0) *loft
        m_2=translation(0,W1-d_mudsill,0) *loft
        m_f=combine(m_1,m_2)
        # create_geometry(m_f)
        # 立柱
        section_pillar = Section(Vec3(0,0,0),Vec3(0,d_pillar,0), Vec3(d_pillar,d_pillar,0), Vec3(d_pillar,0,0))
        loft = Loft(section_pillar, translate(0,0,H1-d_mudsill-H_beam) * section_pillar)
        p_1=translation(-d_pillar/2,0,d_mudsill) *loft
        p_2=translation(-d_pillar/2,W1-d_pillar,d_mudsill) *loft
        p_f=combine(p_1,p_2)
        # create_geometry(p_f)
        # 横梁
        section_beam = to_section(Vec3(d_beam/2,0,0), Vec3(-d_beam/2,0,0), Vec3(-d_beam/2,0,10), Vec3(-t_beam/2,0,10),
         Vec3(-t_beam/2,0,H_beam-10),Vec3(-d_beam/2,0,H_beam-10), Vec3(-d_beam/2,0,H_beam), Vec3(d_beam/2,0,H_beam),
         Vec3(d_beam/2,0,H_beam-10),Vec3(t_beam/2,0,H_beam-10), Vec3(t_beam/2,0,10), Vec3(d_beam/2,0,10))
        loft = Loft(section_beam, translate(0,W1,0) * section_beam).color(255/255,0/255,0/255,1)
        b_f=translation(0,0,H1-H_beam) *loft
        # create_geometry(b_f)
        # 斜杠
        section_slash = Section(Vec3(-d_slash/2,0,0),Vec3(-d_slash/2,d_slash,0), Vec3(d_slash/2,d_slash,0), Vec3(d_slash/2,0,0))
        loft = Loft(section_slash, translate(0,0,W3-200) * section_slash)
        s_1=translation(W3/2-100,0,d_mudsill-d_slash/4) *rotation(Vec3(0,1,0),-pi/6) *loft
        s_2=translation(-W3/2+100,0,d_mudsill-d_slash/4) *rotation(Vec3(0,1,0),pi/6) *loft
        s_3=translation(W3/2-100,W1-d_slash,d_mudsill-d_slash/4) *rotation(Vec3(0,1,0),-pi/6) *loft
        s_4=translation(-W3/2+100,W1-d_slash,d_mudsill-d_slash/4) *rotation(Vec3(0,1,0),pi/6) *loft
        s_f=combine(s_1,s_2,s_3,s_4)
        # create_geometry(s_f)
        # create_frame
        low_geometry=m_f+p_f+s_f
        low_geometry=low_geometry.color(255/255,255/255,0/255,1)
        self['龙门架'] = combine(b_f,low_geometry)

       
if __name__ == "__main__":
    Final_Geometry = 龙门架   ()
    RotationPlace.RotationFunction(Final_Geometry)
    place(Final_Geometry)                            