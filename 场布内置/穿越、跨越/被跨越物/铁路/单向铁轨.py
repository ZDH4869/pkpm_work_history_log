from pyp3d import *
# 放样体
class 单向铁轨(Component):
    def __init__(self):
        Component.__init__(self)
        self['铁轨长'] = Attr(14000.0,obvious=True)
        self['应用场景'] = Attr('被跨越物', obvious=True,group='构建分类')
        self['构建类型'] = Attr('铁路', obvious = True,group='构建分类')
        self['构建名称'] = Attr('单向铁轨', obvious = True,group='构建分类')
        self['铁轨宽度'] = Attr(5000.0, obvious=True,group='铁轨尺寸')
        self['枕木间距'] = Attr(700, obvious = True,group='铁轨尺寸')
        self['铁轨'] = Attr(None, show=True)
        self.replace()
    @export
    def replace(self):
        L = self['铁轨长']
        b = self['铁轨宽度']
        h = self['枕木间距']
# 铁轨
    # 截面
        section1 = Section(Vec3(0,0,0),Vec3(64,0,0),translate(64,2,0)*scale(2) * Arc(-0.5*pi),Vec3(66,2,0),translate(62,6.5)*scale(4) * Arc(0.4*pi),\
                        Vec3(24,21,0),Vec3(9,36.7,0),Vec3(9.7,102.5,0),Vec3(15.4,113.8,0),Vec3(32.5,115.2,0),Vec3(35,117.7,0),Vec3(35,138.7,0),translate(23,138.7)*scale(12,13.3) * Arc(0.5*pi),\
                        Vec3(0,152,0),translate(-23,138.7)*rotation(Vec3(0,0,1),pi*0.5)*scale(13.3,12) * Arc(0.5*pi),Vec3(-35,138.7,0),Vec3(-35,118.7,0),Vec3(-15.4,113.8,0),\
                        Vec3(-9.7,102.5,0),Vec3(-9,36.7,0),Vec3(-24,21,0),translate(-62,6.5)*rotation(Vec3(0,0,1),pi*0.6)*scale(4) * Arc(0.4*pi),Vec3(-66,6.5,0),Vec3(-66,2,0),\
                        translate(-64,2,0)*rotation(Vec3(0,0,1),pi)*scale(2) * Arc(0.5*pi)).color(1,0,0,1)
     
    # 放样
        loft1 = Loft(rotation(Vec3(1,0,0),pi*0.5)*section1, translate(0,L,0) * rotation(Vec3(1,0,0),pi*0.5)*section1) 
    # 生成左右铁轨
        lofta = translate(0.5*b-66,0,584) * loft1.color(0,0,0,1)
        loftb = translate(-0.5*b+66,0,584) * loft1.color(0,0,0,1)
# 枕木
    # 截面
        section2 = to_section(Vec3(0,0,0),Vec3(0,600,0),Vec3(0,570,584),Vec3(0,30,584)).color(1,0,0,1) 
    # 放样
        loft2 = Loft(translate(-0.5*b-500,0,0) * section2,translate(0.5*b+500,0,0) * section2).color(0.41,0.41,0.41,1)
    # 线性排布
        Test_Array = Array(loft2)   
        for i in linspace(Vec3(0,0,0),Vec3(0,int(L/(h + 600))*(h + 600),0),int(L/(h + 600))):
            Test_Array.append(translate(i))
            
# 组合
        combine = Combine(lofta,loftb,Test_Array)
        self['铁轨'] = rotation(Vec3(0,0,1),1.5*pi) * combine
if __name__ == "__main__":
    FinalGeometry = 单向铁轨()
# 实现两点布置
    TwoPointPlace.linearize(FinalGeometry,'铁轨长')
    place(FinalGeometry)