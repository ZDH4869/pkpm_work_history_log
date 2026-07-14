from pyp3d import *
import math

class 百叶窗矩形面(Component):
    def __init__(self):
        Component.__init__(self)
        self['风管宽度'] = Attr(180, obvious = True)
        self['风管高度'] = Attr(150, obvious = True)
        self['面板厚度'] = Attr(4.5, obvious = True)
        self['叶片深度'] = Attr(31, obvious = True)
        self['叶片厚度'] = Attr(2.1, obvious = True)
        self['百叶窗长度'] = Attr(214, obvious = True)
        self['窗高'] = Attr(100, obvious = True)  # 添加缺失的属性
        self['窗宽'] = Attr(100, obvious = True)  # 添加缺失的属性
        self['百叶窗矩形面'] = Attr(None, show=True)
        self.replace()
    
    @export
    def replace(self):
        # 宽y
        FGH_Box = self['风管高度']
        #长x
        FGW_Box = self['风管宽度']
        BYH_Box = self['窗高']
        BYW_Box = self['窗宽']
        BYL_Box = self['百叶窗长度']
        BYW_Box = FGH_Box + 54.0
        BYL_Box = FGW_Box + 54.0
        planeThick = self['面板厚度']
        
        # 风管
        mainCube = translate(-0.5 * FGW_Box, -0.5 * FGH_Box, 0) * scale(FGW_Box, FGH_Box, BYH_Box - planeThick) * Cube()
        
        # 百叶窗面
        planeCube = translate(-0.5 * BYL_Box, -0.5 * BYW_Box, BYH_Box - planeThick) * scale(BYL_Box, BYW_Box, planeThick) * Cube()
        mainCube = mainCube + planeCube
        
        BYW_BoxEmpty = FGH_Box - 3
        BYL_BoxEmpty = FGW_Box - 3
        emptyCube = translate(-0.5 * BYL_BoxEmpty, -0.5 * BYW_BoxEmpty, 0) * scale(BYL_BoxEmpty, BYW_BoxEmpty, BYH_Box) * Cube()
        mainCube = mainCube - emptyCube
        
        liefThick = self['叶片厚度']
        liefHeight = self['叶片深度']
        
        # 逆时针以原点为中心的叶片
        liefx = 0.5 * FGW_Box
        liefy = 0.5 * liefThick
        
        # 去除一个厚度的偏移
        liefOffset = liefHeight - liefThick
        liefHLoction = BYH_Box - planeThick
        
        # 修复translation为translate，修复参数
        sectionlief = translate(0.5 * BYL_BoxEmpty - 30, -0.5 * BYW_BoxEmpty, liefHLoction) * rotate(Vec3(1, 0, 0), 0.5 * math.pi) * Section(
            Vec3(0, 0),
            Vec3(-10, 0),
            Vec3(-10 - liefOffset, -liefOffset),
            Vec3(-10 - liefOffset - 3.6, -liefOffset),
            Vec3(-10 - liefOffset - 3.6, -liefOffset + 5.5),
            Vec3(-10 - liefOffset - 3.6 - liefThick, -liefOffset + 5.5),
            Vec3(-10 - liefOffset - 3.6 - liefThick, -liefOffset - liefThick),
            Vec3(-liefOffset - 8.3, -liefThick - liefOffset),
            Vec3(-8.3, -liefThick),
            Vec3(0, -liefThick)
        )
        
        line = Line(Vec3(0, 0, 0), Vec3(0, BYW_BoxEmpty, 0))
        lief = Sweep(sectionlief, line)
        
        # 风管内侧减去第一个起点距离
        canOffsetLength = BYL_BoxEmpty - 30
        
        # 每一个叶片的厚度 +40的间距
        liefoffset = liefHeight + liefThick + 3.6 + 10 + 23
        
        num = int(canOffsetLength / liefoffset)
        
        for i in range(num):
            mainCube = mainCube + translate(-i * liefoffset, 0, 0) * lief
        
        self['百叶窗矩形面'] = mainCube

if __name__ == "__main__":
    Final_Geometry = 百叶窗矩形面()
    place(Final_Geometry)
