import pyp3d as p3d
def ybj(data:p3d.P3DData)->None:

    
    # 宣传架参数设置
    A1= data['宣传架长']#宣传架长度及两立柱间距离
    A2= data['宣传架宽']#宣传架宽度
    C1= data['柱高']#立柱高柱
    C2= data['柱半径']#立柱半径
    E1= data['宣传架厚']#宣传架厚度
    k=data['旋转角度']

    #立柱
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,C1),C2,C2).color(0.5,0.5,0.5,1)
    Cone2 = p3d.Cone(p3d.Vec3(A1+C2+C2,0,0),p3d.Vec3(A1+C2+C2,0,C1),C2,C2).color(0.5,0.5,0.5,1)

    #宣传架
    Box1 = p3d.Box(p3d.Vec3(C2,-30,C1-50-A2),p3d.Vec3(C2,-30,C1-50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),A1,E1,A1,E1).color(1,1,1,1)
    #Box2 = p3d.RotationalSweep([p3d.Vec3(-200,240,C1-D2),p3d.Vec3(-200,250,C1-D2),p3d.Vec3(A1+D2+C2+C2,250,C1-D2),p3d.Vec3(A1+D2+C2+C2,240,C1-D2)],p3d.Vec3(2100,0,C1-D2),p3d.Vec3(1,0,0),1*p3d.pi).color(0.5,0.5,0.5,1)
    #蓝板
    Box2=p3d.Box(p3d.Vec3(C2,30,C1-50-A2),p3d.Vec3(C2,30,C1-50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),A1,1,A1,1).color(30/255,144/255,255/255,1)
    #四个板
    Box3=p3d.Box(p3d.Vec3(C2+50,31,C1-50-A2+100),p3d.Vec3(C2+50,31,C1-50-150),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),350,1,350,1).color(1,1,1,1)
    Box4=p3d.Box(p3d.Vec3(C2+50+350+100,31,C1-50-A2+100),p3d.Vec3(C2+50+350+100,31,C1-50-150),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),350,1,350,1).color(1,1,1,1)
    Box5=p3d.Box(p3d.Vec3(C2+50+350+100+350+100,31,C1-50-A2+100),p3d.Vec3(C2+50+350+100+350+100,31,C1-50-150),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),350,1,350,1).color(1,1,1,1)
    Box6=p3d.Box(p3d.Vec3(C2+50+350+100+350+100+350+100,31,C1-50-A2+100),p3d.Vec3(C2+50+350+100+350+100+350+100,31,C1-50-150),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),350,1,350,1).color(1,1,1,1)
    #text1 = p3d.Text("温馨提示", 50, 50).color(224/255,224/255,224/255,1)
    #text1 =p3d.translation(p3d.Vec3(C2+50+50,33, C1-50-50))*text1
    Sphere1=p3d.Sphere(p3d.Vec3(0,0,C1+55),55).color(1,1,1,1)
    Sphere2=p3d.Sphere(p3d.Vec3(C2+C2+A1,0,C1+55),55).color(1,1,1,1)

    data['宣传架']= p3d.combine(Cone1,Cone2,Box1,Box2,Box3,Box4,Box5,Box6,Sphere1,Sphere2)
    # p3d.createGeometry(data['A'])
    data['宣传架']=p3d.translation(p3d.Vec3(-(A1/2+C2),0,0))*data['宣传架']
    data['宣传架']= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*data['宣传架']
   
   
   
   
    text1= p3d.Text("温馨提示",30,30).color(1,1,0, 1)
    text1= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text1
    text1= p3d.translation(p3d.Vec3(-A1+85,-33, C1-50-50-50))*text1
   
    text2= p3d.Text("施工人员着装规范",30,30).color(1,1,0, 1)
    text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text2
    text2= p3d.translation(p3d.Vec3(-A1+450,-33, C1-50-50-50))*text2
 
    text3= p3d.Text("重大危险源公示",30,30).color(1,1,0, 1)
    text3= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text3
    text3= p3d.translation(p3d.Vec3(-A1+925,-33, C1-50-50-50))*text3
 
    text4= p3d.Text("班前教育",30,30).color(1,1,0, 1)
    text4= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text4
    text4= p3d.translation(p3d.Vec3(-A1+1440,-33, C1-50-50-50))*text4

    text=p3d.combine(text1,text2,text3,text4)
    text=p3d.translation(p3d.Vec3((A1/2+C2),0,0))*text
 
   
    Z1=p3d.combine(data['宣传架'],text)
    #Z1=p3d.translation(p3d.Vec3(A1/2+C2,0,0))*Z1
    Z1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*Z1
    Z1=p3d.translation(A1/2+C2,0,0)*Z1
    data['宣传架']=p3d.combine(Z1)
   

if __name__ == "__main__":
    data=p3d.P3DData({
        '宣传架长': 1800,
        '宣传架宽': 1200,
        '柱高': 2340,
        '柱半径': 50,
        '宣传架厚': 60,
        '旋转角度': 0,
        '场布类型':'挂牌资料',
        '构件类型':'标识牌基本类型',
        '构件名称':'宣传架无顶棚'
        })
    data.setup('宣传架',show = True)
    data.setup('宣传架长' , obvious = True ,readonly=True,group='宣传架' , description ='宣传架长')
    data.setup('宣传架宽',obvious = True,readonly=True,group='宣传架' , description ='宣传架宽')
    data.setup('柱高',obvious = True,readonly=True,group='立柱' , description ='柱高')
    data.setup('柱半径',obvious = True,readonly=True,group='立柱' , description ='柱半径')
    data.setup('宣传架厚',obvious = True,readonly=True,group='宣传架', description='宣传架厚')
    data.setup('旋转角度',obvious=True,group='旋转',description='旋转角度')
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    
    data['replace'] = ybj
    ybj(data)
    p3d.launchData(data)