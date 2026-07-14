from pyp3d import *

class 三维文字(Component):
    def __init__(self):
        Component.__init__(self)
        self['显示文字'] = Attr("参数化组件", obvious=True)
        self['三维文字'] = Attr(None, show=True)
        self['三维文字高度'] = Attr(20, obvious=True)
        self['文字高度'] = Attr(300, obvious=True)
        # self['文字宽度'] = Attr(300, obvious=True)
        self['R'] = Attr(0, obvious=True)
        self['G'] = Attr(0, obvious=True)
        self['B'] = Attr(0, obvious=True)
        self['A'] = Attr(1, obvious=True)

        self.replace()
    @export
    def replace(self):
        # TextSize_W = self['文字宽度']
        TextSize_H = self['文字高度']
        R = self['R']
        B = self['B']
        G = self['G']
        A = self['A']
        
        text1 = Text(self['显示文字'],TextSize_H,TextSize_H)
        TextHight = self['三维文字高度']

        text2 = translate(Vec3(0,0,TextHight)) * text1
        TextHightLine = Line(Vec3(0,0,0), Vec3(0,0,TextHight))
        ThreeDText = Sweep(text1,TextHightLine).color(R/255,G/255,B/255,A)
        # ThreeDText = Loft(text1,text2).color(R/255,G/255,B/255,A)
        self['三维文字'] = ThreeDText

if __name__ == "__main__":
    FinalGeometry = 三维文字()
    place(FinalGeometry)
