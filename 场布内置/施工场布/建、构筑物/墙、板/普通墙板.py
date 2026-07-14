from pyp3d import *
class 普通墙板(Component):
    def __init__(self):
        Component.__init__(self)
        self['普通墙板'] = Attr(None, show=True)
        self['场布类型'] = Attr("装配式钢结构", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("外墙板", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("普通外墙板", obvious=True, readonly=True, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['墙板长'] = Attr(3000.0, obvious=True,group='墙板')
        self['墙板高'] = Attr(1000.0, obvious=True,group='墙板')
        self['墙板厚'] = Attr(200.0, obvious=True,group='墙板')
        self['墙板X'] = Attr(0, obvious=False)
        self['墙板Y'] = Attr(0, obvious=False)
        self['墙板Z'] = Attr(0, obvious=False)
        self.replace()

    @export
    def replace(self):

        qb_c = self['墙板长']
        qb_g = self['墙板高']
        qb_h = self['墙板厚']
        qb_x = self['墙板X']
        qb_y = self['墙板Y']
        qb_z = self['墙板Z']
        Angle = self['旋转角度']

        墙板 = translate(qb_x,qb_y,qb_z) * rotation(math.pi/180 * Angle) * scale(qb_c,-qb_h,qb_g) * Cube()
        self['普通墙板'] = 墙板

if __name__ == "__main__":
    place(普通墙板())     
