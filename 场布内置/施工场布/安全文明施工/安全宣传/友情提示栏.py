import pyp3d as p3d

def cui(data:p3d.P3DData)->None:
    data['场布分类']='挂牌资料'
    data['构件类型']='其它标识牌'
    # ==文字限制
    f=data['旋转角度']#旋转角度
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,20),60,60).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,1560),30,30).color(1,1,1,1)
    Cone3 = p3d.Cone(p3d.Vec3(860,0,0),p3d.Vec3(860,0,20),60,60).color(1,1,1,1)
    Cone4 = p3d.Cone(p3d.Vec3(860,0,20),p3d.Vec3(860,0,1560),30,30).color(1,1,1,1)
    Box1=p3d.Box(p3d.Vec3(30,0,1020),p3d.Vec3(30,0,1080), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),800,30,800,30).color(1,1,1,1)
    Box2=p3d.Box(p3d.Vec3(30,0,1080),p3d.Vec3(30,0,1410), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),800,30,800,30).color(61/255,145/255,64/255,1)
    Box3=p3d.Box(p3d.Vec3(30,0,1410),p3d.Vec3(30,0,1520), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),800,30,800,30).color(1,1,1,1)
    A1=p3d.combine(Box1,Box2,Box3,Cone1,Cone2,Cone3,Cone4)
    Text= p3d.Text("友情提示",60,60).color(1,1,0,1)
    Text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text
    Text= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text
    Text= p3d.translation(p3d.Vec3(600,35,1300))*Text
    Text1= p3d.Text("为了您的安全与健康",30,30).color(1,1,0,1)
    Text1= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text1
    Text1= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text1
    Text1= p3d.translation(p3d.Vec3(800,35,1210))*Text1
    Text2= p3d.Text("请不要进入施工区域",30,30).color(1,1,0,1)
    Text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text2
    Text2= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text2
    Text2= p3d.translation(p3d.Vec3(500,35,1110))*Text2
    Text3= p3d.Text("送变电公司",40,40).color(1,1,0,1)
    Text3= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text3
    Text3= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text3
    Text3= p3d.translation(p3d.Vec3(800,35,1450))*Text3
    Text4= p3d.Text("铁路工程项目部",25,25).color(1,1,0,1)
    Text4= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text4
    Text4= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text4
    Text4= p3d.translation(p3d.Vec3(450,35,1040))*Text4
    A2=p3d.combine(A1,Text,Text1,Text2,Text3,Text4)
    A2 =p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*A2
    A2 = p3d.translation(p3d.Vec3(860,0,0)) * A2
    AA2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f)*A2
    
    data['友情提示栏'] = AA2
if __name__ == "__main__":
    data=p3d.P3DData({
        '旋转角度':0,
        '构件名称':'友情提示栏'
        })
    data.set_view(1,1)
    data.setup('友情提示栏',show = True)
    data.setup('旋转角度' , obvious = True ,group='旋转角度' , description ='旋转角度')
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称',obvious=True)
    data['replace'] = cui
    cui(data)
    p3d.launchData(data)