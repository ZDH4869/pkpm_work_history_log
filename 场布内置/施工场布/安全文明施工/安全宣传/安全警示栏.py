import pyp3d as p3d
def cui(data:p3d.P3DData)->None:
    f=data['旋转角度']#旋转角度
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,20),60,60).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,1560),30,30).color(1,1,1,1)
    Cone3 = p3d.Cone(p3d.Vec3(860,0,0),p3d.Vec3(860,0,20),60,60).color(1,1,1,1)
    Cone4 = p3d.Cone(p3d.Vec3(860,0,20),p3d.Vec3(860,0,1560),30,30).color(1,1,1,1)
    Box1=p3d.Box(p3d.Vec3(30,0,1020),p3d.Vec3(30,0,1080), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),800,30,800,30).color(1,1,1,1)
    Box2=p3d.Box(p3d.Vec3(30,0,1080),p3d.Vec3(30,0,1410), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),800,30,800,30).color(61/255,145/255,64/255,1)
    Box3=p3d.Box(p3d.Vec3(30,0,1410),p3d.Vec3(30,0,1520), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),800,30,800,30).color(1,1,1,1)
    A1=p3d.combine(Box1,Box2,Box3,Cone1,Cone2,Cone3,Cone4)
    Text4= p3d.Text("铁路工程项目部",25,25).color(61/255,145/255,64/255,1)
    Text4= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text4
    Text4= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text4
    Text4= p3d.translation(p3d.Vec3(450,35,1040))*Text4
    Text3= p3d.Text("送变电公司",40,40).color(61/255,145/255,64/255,1)
    Text3= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text3
    Text3= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text3
    Text3= p3d.translation(p3d.Vec3(800,35,1450))*Text3
    Text2= p3d.Text("自觉遵章守纪",50,50).color(225/255,225/255,225/255,1)
    Text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text2
    Text2= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text2
    Text2= p3d.translation(p3d.Vec3(500,35,1300))*Text2
    Text1= p3d.Text("预防事故发生",50,50).color(225/255,225/255,225/255,1)
    Text1= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text1
    Text1= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text1
    Text1= p3d.translation(p3d.Vec3(500,35,1200))*Text1
    AA2=p3d.combine(A1,Text4,Text3,Text2,Text1)
    AA2=p3d.rotation(p3d.Vec3(0,0,1),p3d.math.pi)*AA2
    AA2=p3d.translation(860,0,0)*AA2
    AA2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f)*AA2
    data['安全提示栏'] = AA2
if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'安全提示栏',
        '构件类型':'安全提示栏',
        '构件名称':'安全警示栏',
        '旋转角度':0,
        })
    data.setup('安全提示栏',show = True)
    data.setup('旋转角度' , obvious = True ,group='旋转角度' , description ='旋转角度')
    data.setup('场布分类',obvious=True,readonly=True,group='公共属性',description='场布分类')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = cui
    cui(data)
    p3d.launchData(data)