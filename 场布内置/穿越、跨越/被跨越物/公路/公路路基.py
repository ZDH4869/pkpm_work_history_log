from pyp3d import *
class 公路地基(Component):
    def __init__(self):
        Component.__init__(self)
        self['公路地基'] = Attr(None, show=True)
        self['场布类型'] = Attr("施工线路三跨", obvious=True, readonly=True, group="构件分类")
        self['构件类型'] = Attr("被跨越物—公路", obvious=True, readonly=True, group="构件分类")
        self['构件名称'] = Attr("公路地基", obvious=True, readonly=False, group="构件分类")
        self['旋转角度'] = Attr(0,obvious = False)
        self['顶面宽度'] = Attr(26500, obvious=True,group='公路地基')
        self['填土高度'] = Attr(2000, obvious=True,group='公路地基')
        self['设计坡比'] = Attr(1.5, obvious=True,group='公路地基')
        self['底面宽度'] = Attr(500,obvious=True, readonly = True,group='公路地基')
        self['总长度'] = Attr(0, obvious=True)
        self.replace()

    @export
    def replace(self):

        w_top = self['顶面宽度']
        n = self['设计坡比']
        pb = 1/n

        tt_h = self['填土高度']
        w_bottom = w_top + tt_h*pb*2
        self['底面宽度'] = w_bottom
        L = self['总长度']

        ljjm = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(w_bottom,0), Vec2(w_bottom-(w_bottom-w_top)/2,tt_h), Vec2(w_bottom-(w_bottom-w_top)/2-w_top,tt_h),Vec2(0,0), Vec2(w_bottom,0))
        ljjm_final = translate(0, L, 0) * ljjm
        gllj = Loft(ljjm , ljjm_final).color(237/255,189/255,101/255,1)
        gllj_final = rotate(Vec3(0,0,1), -0.5*pi) * translate(Vec3(-w_bottom/2,0,0)) * gllj

        self['公路地基'] = gllj_final

if __name__ == "__main__":
    Final_Geometry = 公路地基()
    TwoPointPlace.linearize(Final_Geometry,'总长度')
    place(Final_Geometry)