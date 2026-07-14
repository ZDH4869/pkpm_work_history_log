from pyp3d import *


class River(Component):
    def __init__(self):
        Component.__init__(self)
        self['应用场景'] = Attr('隧道穿越', readonly=True, obvious=True, group='构件分类')
        self['构件类型'] = Attr('被穿越物', readonly=True, obvious=True, group='构件分类')
        self['构件名称'] = Attr('河', obvious=True, group='构件分类')
        self['顶面长'] = Attr(4000.0, obvious=True, group='截面尺寸')
        self['高'] = Attr(1700.0, obvious=True, group='截面尺寸')
        self['底面长'] = Attr(2100.0, obvious=True, group='截面尺寸')
        self['默认长度'] = Attr(5000.0, obvious=False, group='截面尺寸')
        self['RiverGeo'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):

        # Active Parameters
        TopLength = self['顶面长']
        Height = self['高']
        GroundLength = self['底面长']
        DefaultLength = self['默认长度']

        # Geometry
        RiverTopSec = Section(Vec3(0, TopLength/2, 0), Vec3(DefaultLength, TopLength/2, 0),
                              Vec3(DefaultLength, -TopLength/2, 0), Vec3(0, -TopLength/2, 0))
        RiverGroundSec = to_section(Vec3(0, GroundLength/2, -Height), Vec3(DefaultLength, GroundLength/2, -Height),
                                 Vec3(DefaultLength, -GroundLength/2, -Height), Vec3(0, -GroundLength/2, -Height))
        All_Geometry = Loft(RiverTopSec, RiverGroundSec).color(148/255, 195/255, 230/255, 0.5)
        self['RiverGeo'] = All_Geometry


if __name__ == "__main__":
    Final_Geometry = River()
    TwoPointPlace.linearize(Final_Geometry, '默认长度')
    place(Final_Geometry)
