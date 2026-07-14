from pyp3d import *
class 墙角板(Component):
    def __init__(self):
        Component.__init__(self)

        self['墙角板'] = Attr(None, show=True)
        self['场布类型'] = Attr("装配式钢结构", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("外墙板", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("普通外墙角板", obvious=True, readonly=True, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['左角板长'] = Attr(600.0, obvious=True,group='左角板')
        self['左角板高'] = Attr(1000.0, obvious=True,group='左角板')
        self['左角板厚'] = Attr(200.0, obvious=True,group='左角板')
        self['左角板X'] = Attr(0, obvious=False)
        self['左角板Y'] = Attr(0, obvious=False)
        self['左角板Z'] = Attr(0, obvious=False)
        self['右角板长'] = Attr(600.0, obvious=True,group='右角板')
        self['右角板高'] = Attr(1000.0, obvious=True,group='右角板')
        self['右角板厚'] = Attr(200.0, obvious=True,readonly=True, group='右角板')
        self['右角板X'] = Attr(0, obvious=False)
        self['右角板Y'] = Attr(0, obvious=False)
        self['右角板Z'] = Attr(0, obvious=False)

        self['连接长'] = Attr(200, obvious=False)
        self['连接宽'] = Attr(200.0, obvious=False)
        self['连接高'] = Attr(1000.0, obvious=False)
        self['连接X'] = Attr(0, obvious=False)
        self['连接Y'] = Attr(0, obvious=False)
        self['连接Z'] = Attr(0, obvious=False)
        self.replace()
    @export
    def replace(self):

        H = self['左角板厚']
        self['右角板厚'] = self['左角板厚']
        h = self['连接高']

        zjb_c = self['左角板长']
        zjb_g = self['左角板高']
        zjb_x = self['左角板X']
        zjb_y = self['左角板Y']
        zjb_z = self['左角板Z']

        Angle = self['旋转角度']

        yjb_c = self['右角板长']
        yjb_g = self['右角板高']
        yjb_x = self['右角板X']
        yjb_y = self['右角板Y']
        yjb_z = self['右角板Z']

        lj_c = self['连接长']
        lj_k = self['连接宽']
        lj_x = self['连接X']
        lj_y = self['连接Y']
        lj_z = self['连接Z']

        if zjb_g > yjb_g:
            h = zjb_g
        if zjb_g <=yjb_g:
            h = yjb_g

        左角板 = translate(zjb_x,zjb_y,zjb_z) * rotation(math.pi/180 * Angle) * scale(-H,H-zjb_c,zjb_g) * Cube()
        右角板 = translate(yjb_x,yjb_y,yjb_z) * rotation(math.pi/180 * Angle) * scale(-H+yjb_c,H,yjb_g) * Cube()
        连接 = translate(lj_x,lj_y,lj_z) * rotation(math.pi/180 * Angle) * scale(-H,H,h) * Cube()

       
        self['墙角板'] = 左角板 + 连接 +右角板

if __name__ == "__main__":
    place(墙角板())  


























