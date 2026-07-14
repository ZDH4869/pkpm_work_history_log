import pyp3d as p3d
def test_GWHZTCQ(data:p3d.P3DData)->None:
    tmd = data['透明度']
    # ctrl+?添加注释可以跳过
    ConeDz1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-8),51.5,51.5)
    ConeDz2 = p3d.Cone(p3d.Vec3(0,0,-8),p3d.Vec3(0,0,-24),51.5,51.5)
    ConeDz3 = p3d.Cone(p3d.Vec3(0,0,-24),p3d.Vec3(0,0,-32),51.5,50)
    Dz = p3d.combine(ConeDz1,ConeDz2,ConeDz3)
    # p3d.createGeometry(Dz)
    ConeWg1 = p3d.Cone(p3d.Vec3(0,0,-32),p3d.Vec3(0,0,-55),31.279,18)
    ConeWg2 = p3d.Cone(p3d.Vec3(0,0,-32),p3d.Vec3(0,0,-55),29.279,16)
    Sg1 = p3d.substract(ConeWg1,ConeWg2)
    # p3d.createGeometry(Sg1)
    XZsmtn = p3d.RotationalSweep([p3d.Vec3(0,-15,-52),p3d.Vec3(0,-29,-32),p3d.Vec3(0,-32,-32),p3d.Vec3(0,-20,-52)],p3d.Vec3(0,0,0),p3d.Vec3(0,0,1),16.5/180*p3d.pi)
    XZsmt1 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*3/180) * XZsmtn
    XZsmt2 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*25.5/180) * XZsmtn
    XZsmt3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*48/180) * XZsmtn
    XZsmt4 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*70.5/180) * XZsmtn
    XZsmt5 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*93/180) * XZsmtn
    XZsmt6 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*115.5/180) * XZsmtn
    XZsmt7 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*138/180) * XZsmtn
    XZsmt8 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*160.5/180) * XZsmtn
    XZsmt9 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*183/180) * XZsmtn
    XZsmt10 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*205.5/180) * XZsmtn
    XZsmt11 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*228/180) * XZsmtn
    XZsmt12 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*250.5/180) * XZsmtn
    XZsmt13 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*273/180) * XZsmtn
    XZsmt14 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*295.5/180) * XZsmtn
    XZsmt15 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*318/180) * XZsmtn
    XZsmt16 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*340.5/180) * XZsmtn
    Sg0 = p3d.combine(XZsmt1,XZsmt2,XZsmt3,XZsmt4,XZsmt5,XZsmt6,XZsmt7,XZsmt8,XZsmt9,XZsmt10,XZsmt11,XZsmt12,XZsmt13,XZsmt14,XZsmt15,XZsmt16)
    # p3d.createGeometry(Sg0)
    Sg2 = p3d.substract(Sg1,Sg0)
    # p3d.createGeometry(Sg2)
    Lst1 = p3d.Extrusion([p3d.Vec3(-2,-9,-55),p3d.Vec3(-2,-17.8,-55),p3d.Vec3(2,-17.8,-55),p3d.Vec3(2,-9,-55)],p3d.Vec3(0,0,3))
    Lst2 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*0.5) * Lst1
    Lst3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*1) * Lst1
    Lst4 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*1.5) * Lst1
    Lst = p3d.combine(Lst1,Lst2,Lst3,Lst4)
    Sg3 = p3d.unite(Lst, Sg2)
    Cone1 = p3d.Cone(p3d.Vec3(0,0,-52),p3d.Vec3(0,0,-55),10,10)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,-54.5),p3d.Vec3(0,0,-55),8,8)
    Sg4 = p3d.substract(Cone1,Cone2)
    Sg = p3d.unite(Sg3, Sg4)
    # p3d.createGeometry(Sg)
    Gwhztcq = p3d.combine(Dz,Sg).color(1,1,1,tmd)
    data['感温火灾探测器'] = Gwhztcq
    # p3d.createGeometry(Gwhztcq)
if __name__ == "__main__":
    data = p3d.P3DData({
        '透明度': 1,
        '构件名称':'烟感'
        })

    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('感温火灾探测器', show=True)
    data.setup('透明度', obvious=True, group='探测器')
    data.setup('构件名称',obvious=True)
    data['replace'] = test_GWHZTCQ
    test_GWHZTCQ(data)
    p3d.launchData(data)