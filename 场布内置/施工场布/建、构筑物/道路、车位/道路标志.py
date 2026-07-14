import pyp3d as p3d
def biaozhi(data:p3d.P3DData)->None:
    WHBJ = data['外环半径h']
    NHBJ = data['内环半径r']
    DYZ = data['底座高度']
    DYZBJ = data['底座半径']
    XYZG = data['杆高']
    WHBJ = data['外环半径h']
    XYZBJ = data['杆半径']
    HZBYDX = data['盒坐标原点x']
    HZBYDY = data['盒坐标原点y']
    HG = data['盒高']
    HC = data['盒长']
    HK = data['盒宽']
    SZGK = data['数字高宽']

# 增加联动参数
    data['盒坐标原点x'] = -HC/2
    data['盒坐标原点y'] = -HK/2

    MyEllipse = p3d.Ellipse(p3d.Vec3(0,0,0), p3d.Vec3(0, 450, 0), p3d.Vec3(450, 0, 0), 0, 2*p3d.pi)
    OuterContour = p3d.ContourLine([MyEllipse])
    Ellipse1 = p3d.Ellipse(p3d.Vec3(0,0,0), p3d.Vec3(0, 375, 0), p3d.Vec3(375, 0, 0), 0, 2*p3d.pi)
    InnerContour = p3d.ContourLine([Ellipse1])
    extrusionPlus1 = p3d.ExtrusionPlus([OuterContour, -InnerContour],p3d.Vec3(0, 0 ,5)).color(1,0,0,1)
    extrusionPlus2 = p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) * extrusionPlus1
    extrusionPlus3 = p3d.translation(p3d.Vec3(0,0,HG+XYZG+DYZ+450)) * extrusionPlus2
    Cone31 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,5),375,375).color(1,1,1,1)
    Cone32 = p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.5) * Cone31
    Cone3 = p3d.translation(p3d.Vec3(0,0,HG+XYZG+DYZ+450)) * Cone32    
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,DYZ),data['底座半径'],data['底座半径']).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,DYZ),p3d.Vec3(0,0,XYZG+DYZ),data['杆半径'],data['杆半径']).color(1,1,1,1)
    box1 = p3d.Box(p3d.Vec3(data['盒坐标原点x'],data['盒坐标原点y'],XYZG+DYZ), p3d.Vec3(data['盒坐标原点x'],data['盒坐标原点y'],HG+XYZG+DYZ), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), data['盒长'], data['盒宽'], data['盒长'],data['盒宽']).color(0,0,0,1)
    text1 = p3d.Text("5", 500,500).color(1, 1, 1, 1)
    text2 = p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text1
    text3 = p3d.translation(p3d.Vec3(-185, -6, HG+XYZG+DYZ+210))*text2
    data['一个圆锥台'] = p3d.combine(Cone1,Cone2,Cone3,box1,text3, extrusionPlus3)
if __name__ == "__main__":
    data = p3d.P3DData({
        '外环半径h':400,
        '内环半径r':325,
        '底座高度':500,
        '底座半径':200,
        '杆高':2500,
        '杆半径':40,
        '盒高':25,
        '盒长':400,
        '盒宽':125,
        '盒坐标原点x':-200,
        '盒坐标原点y':-62.5,
        '数字高宽':400,
        '场布分类':'构筑物',
        '构件类型':'道路标志',
        '构件名称':'道路标志',
    })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('一个圆锥台', show=True)
    data.setup('外环半径h', obvious=True, readonly=True,group='半径',description='外环半径h')
    data.setup('内环半径r', obvious=True, readonly=True,group='半径',description='内环半径r')
    data.setup('底座半径', obvious=True, group='半径',description='底座半径')
    data.setup('杆半径', obvious=True, group='半径',description='杆半径')
    data.setup('盒长', obvious=True, group='半径',description='盒长')
    data.setup('盒宽', obvious=True, group='半径',description='盒宽')
    data.setup('底座高度', obvious=True, group='高',description='底座高度')
    data.setup('杆高', obvious=True, group='高',description='杆高')
    data.setup( '盒高', obvious=True, group='高',description= '盒坐标高')
    data.setup( '盒坐标原点x', obvious=True, readonly=True,group='轴',description= '盒坐标原点x')
    data.setup( '盒坐标原点y', obvious=True, readonly=True,group='轴',description= '盒坐标原点y')
    data.setup( '数字高宽', obvious=True, readonly=True, group='高',description= '数字高宽')
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = biaozhi
    biaozhi(data)
    p3d.launchData(data)




#p3d.createGeometry(extrusionPlus1)
