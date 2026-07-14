#消防器材架
import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:

  ConeS1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(2000,0,0),20,20).color(1,0,0,1)
  ConeS2 = p3d.Cone(p3d.Vec3(20,0,0),p3d.Vec3(0,0,1750),20,20).color(1,0,0,1)
  ConeS3=p3d.Cone(p3d.Vec3(1980,0,0),p3d.Vec3(1980,0,1750),20,20).color(1,0,0,1)
  BoxS1=p3d.Box(p3d.Vec3(0,-300,-20),p3d.Vec3(0,300,-20),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),40,40,40,40).color(1,0,0,1)
  BoxS2=p3d.Box(p3d.Vec3(1960,-300,-20),p3d.Vec3(1960,300,-20),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),40,40,40,40).color(1,0,0,1)
  BoxS3=p3d.Box(p3d.Vec3(1040,-300,-20),p3d.Vec3(1040,300,-20),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),40,40,40,40).color(1,0,0,1)
  BoxS4=p3d.Box(p3d.Vec3(0,-300,350),p3d.Vec3(0,100,350),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),2000,40,2000,40).color(1,0,0,1)
  ConeS4 = p3d.Cone(p3d.Vec3(20,0,600),p3d.Vec3(1980,0,600),20,20).color(1,0,0,1)
  ConeS5 = p3d.Cone(p3d.Vec3(20,0,1300),p3d.Vec3(1980,0,1300),20,20).color(1,0,0,1)
  BoxS5=p3d.Extrusion((p3d.Vec3(-20,350,1450),p3d.Vec3(-20,310,1450),p3d.Vec3(-20,0,1750),p3d.Vec3(-20,-310,1450),p3d.Vec3(-20,-350,1450),p3d.Vec3(-20,0,1800)),p3d.Vec3(2020,0,0)).color(1,0,0,1)
  W=p3d.combine(ConeS1,ConeS2,ConeS3,BoxS1,BoxS2,BoxS3,BoxS4,ConeS4,ConeS5,BoxS5)
  text= p3d.Text("消防器材 禁止挪用",160,220).color(225/255,225/255,225/255, 1)
  text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.25)*text
  text= p3d.translation(p3d.Vec3(10,-350,1500))*text
  H=p3d.combine(text,W)

  Cone6 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,205),95,140).color(1,0,0,1)
  Cone7=p3d.TorusPipe(p3d.Vec3(0,0,205),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),140,2.5,p3d.pi*1).color(1,0,0,1)
  F=p3d.combine(Cone6,Cone7)#消防水桶
  F1=p3d.translation(p3d.Vec3(200,0,945))*F
  F2=p3d.translation(p3d.Vec3(600,0,945))*F
  F3=p3d.translation(p3d.Vec3(1000,0,945))*F
  F4=p3d.translation(p3d.Vec3(1400,0,945))*F
  F5=p3d.translation(p3d.Vec3(1800,0,945))*F
  J=p3d.combine(H,F1,F2,F3,F4,F5)


  Cone8 = p3d.Cone(p3d.Vec3(-30,0,0),p3d.Vec3(30,0,0),10,10).color(1,0,0,1)
  Cone9 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,-535),10,10).color(1,0,0,1)
  Box3=p3d.Box(p3d.Vec3(-52.5,-5,-535),p3d.Vec3(-52.5,5,-535),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),105,-110,105,-110).color(1,0,0,1)
  Box4=p3d.Extrusion((p3d.Vec3(-52.5,-5,-645),p3d.Vec3(52.5,-5,-645),p3d.Vec3(0,-5,-685)),p3d.Vec3(0,10,0)).color(1,0,0,1)

  Q=p3d.combine(Cone8,Cone9,Box3,Box4)#消防铁锹
  Q1=p3d.translation(p3d.Vec3(400,0,1350))*Q
  Q2=p3d.translation(p3d.Vec3(800,0,1350))*Q
  Q3=p3d.translation(p3d.Vec3(1200,0,1350))*Q
  Q4=p3d.translation(p3d.Vec3(1600,0,1350))*Q
  P=p3d.combine(J,Q1,Q2,Q3,Q4)

  Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,355),65,65).color(1,0,0,1)
  Sphere1 = p3d.Sphere(p3d.Vec3(0,0,355),65).color(1,0,0,1)
  BB= p3d.unite(Cone1,Sphere1).color(1,0,0,1)
  Cone2= p3d.Cone(p3d.Vec3(0,0,380),p3d.Vec3(0,0,465),17,17).color(192/255,192/255,192/255,1)
  # BB= p3d.unite(Cone2,BB).color(1,0,0,1)
  Cone3= p3d.Cone(p3d.Vec3(0,0,435),p3d.Vec3(-37,0,435),10,10).color(192/255,192/255,192/255,1)
  CC= p3d.unite(Cone3,Cone2).color(192/255,192/255,192/255,1)
  A=p3d.combine(BB,CC)
  Cone4= p3d.Cone(p3d.Vec3(-37,0,435),p3d.Vec3(-63,0,435),9,15).color(192/255,192/255,192/255,1)
  G1=p3d.Box(p3d.Vec3(-17,-17,455),p3d.Vec3(17,-17,455),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),34,15,34,30).color(192/255,192/255,192/255,1)
  G2=p3d.Box(p3d.Vec3(17,-10,470),p3d.Vec3(97,-10,486),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),20,10,20,10).color(192/255,192/255,192/255,1)
  G3=p3d.Box(p3d.Vec3(17,-10,458),p3d.Vec3(97,-10,458),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),20,10,20,10).color(192/255,192/255,192/255,1)
  D=p3d.combine(A,Cone4)#灭火器
  D1=p3d.translation(p3d.Vec3(200,-100,350))*D
  D2=p3d.translation(p3d.Vec3(600,-100,350))*D
  D3=p3d.translation(p3d.Vec3(1000,-100,350))*D
  D4=p3d.translation(p3d.Vec3(1400,-100,350))*D
  D5=p3d.translation(p3d.Vec3(1800,-100,350))*D
  v=p3d.combine(P,D1,D2,D3,D4,D5)
  M=data['旋转角度']
  M1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*M)*v
  data['消防器材架']=M1
if __name__ == "__main__":
    data = p3d.P3DData({
        '场布分类':'消防水电',
        '构件类型':'消防设备',
        '旋转角度':0,
        '构件名称':'消防器材架'
         })
    
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('消防器材架', show=True)
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('构件名称',obvious=True)
    
    data.setup('旋转角度',obvious=True,group='旋转位置',description='旋转角度')
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)



