import pyp3d as p3d
from pyp3d import *
def cui(data:p3d.P3DData)->None:
    #组合罩棚
    a1=data['底板长度']#底板长度
    a2=data['底板宽度']#底板的宽度
    a3=data['底板厚度']#底板的厚度
    b1=data['立柱高度']#立柱高度
    b2=data['立柱边长']#立柱边长
    c1=data['立板高度']#立板高度
    d1=data['顶板厚度']#顶板厚度
    e1=data['字牌高度']#字牌高度
    NB=data['网密度']#网密度
    f=data['旋转角度']
    #立柱
    Box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,b1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,b2,b2,b2).color(1,1,1,1)
    Box2=p3d.Box(p3d.Vec3(b2+a1,0,0),p3d.Vec3(b2+a1,0,b1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,b2,b2,b2).color(1,1,1,1)
    Box3=p3d.Box(p3d.Vec3(b2+a1,b2+a2,0),p3d.Vec3(b2+a1,b2+a2,b1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,b2,b2,b2).color(1,1,1,1)
    Box4=p3d.Box(p3d.Vec3(0,b2+a2,0),p3d.Vec3(0,b2+a2,b1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,b2,b2,b2).color(1,1,1,1)
    #底板
    Box5=p3d.Box(p3d.Vec3(b2,b2,0),p3d.Vec3(b2,b2,a3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a2,a1,a2).color(0,0,1,0.5)
    #侧立板
    Box6=p3d.Box(p3d.Vec3(b2/4,b2,0),p3d.Vec3(b2/4,b2,c1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2/2,a2,b2/2,a2).color(0,0,1,1)
    Box7=p3d.Box(p3d.Vec3(b2*5/4+a1,b2,0),p3d.Vec3(b2*5/4+a1,b2,c1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2/2,a2,b2/2,a2).color(0,0,1,1)
    #后板
    Box8=p3d.Box(p3d.Vec3(b2,b2/4,0),p3d.Vec3(b2,b2/4,c1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,b2/2,a1,b2/2).color(0,0,1,1)
    #横杆
    Box9=p3d.Box(p3d.Vec3(b2,0,0),p3d.Vec3(b2,0,b2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,b2,a1,b2).color(1,1,1,1)
    Box10=p3d.Box(p3d.Vec3(0,b2,0),p3d.Vec3(0,b2,b2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(1,1,1,1)
    Box11=p3d.Box(p3d.Vec3(b2+a1,b2,0),p3d.Vec3(b2+a1,b2,b2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(1,1,1,1)
    Box12=p3d.Box(p3d.Vec3(b2,a2+b2,0),p3d.Vec3(b2,a2+b2,b2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,b2,a1,b2).color(1,1,1,1)
    #上横杆
    Box13=p3d.Box(p3d.Vec3(b2,0,b1*0.8),p3d.Vec3(b2,0,b2+b1*0.8),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,b2,a1,b2).color(1,1,1,1)
    Box14=p3d.Box(p3d.Vec3(0,b2,b1*0.8),p3d.Vec3(0,b2,b2+b1*0.8),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(1,1,1,1)
    Box15=p3d.Box(p3d.Vec3(b2+a1,b2,b1*0.8),p3d.Vec3(b2+a1,b2,b2+b1*0.8),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(1,1,1,1)
    Box16=p3d.Box(p3d.Vec3(b2,a2+b2,b1*0.8),p3d.Vec3(b2,a2+b2,b2+b1*0.8),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,b2,a1,b2).color(1,1,1,1)
    #顶板
    Box17=p3d.Box(p3d.Vec3(-0.2*a1,-0.2*a2,b1),p3d.Vec3(-0.2*a1,-0.2*a2,b1+d1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),(a1*1.4)+b2*2,(a2*1.4)+b2*2,(a1*1.4)+b2*2,(a2*1.4)+b2*2).color(0,0,1,1)
    #字牌
    Box18=p3d.Box(p3d.Vec3(b2+a1/3,a2+(b2*2)-5,b2+b1*0.8),p3d.Vec3(b2+a1/3,a2+(b2*2)-5,b2+b1*0.8+e1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1/3,5,a1/3,5).color(1,1,1,1)
    #字
    Text= p3d.Text("组合罩棚",a1/3*0.1,e1*0.5).color(1,0,0,1)
    Text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*Text
    Text= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 1)*Text
    Text= p3d.translation(p3d.Vec3((a1+b2*2)*7/11.8, a2+(2*b2)+5,(b2+30)+(b1*0.8)))*Text
    #网
    Cone1 = p3d.Cone(p3d.Vec3(0,b2+1,c1),p3d.Vec3(0,b2+1,b1*0.8),1,1).color(1,1,1,1)
    CQ = p3d.Array(Cone1)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,a2,0),NB):
          CQ.append(translation(i))
    
    Cone2 = p3d.Cone(p3d.Vec3(b2*5/4+a1,b2+1,c1),p3d.Vec3(b2*5/4+a1,b2+1,b1*0.8),1,1).color(1,1,1,1)
    CQ1 = p3d.Array(Cone2)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,a2,0),NB):
          CQ1.append(translation(i))

    Cone3 = p3d.Cone(p3d.Vec3(b2+1,0,c1),p3d.Vec3(b2+1,0,b1*0.8),1,1).color(1,1,1,1)
    CQ2 = p3d.Array(Cone3)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(a1,0,0),NB):
          CQ2.append(translation(i))

    Cone4 = p3d.Cone(p3d.Vec3(b2,0,c1),p3d.Vec3(b2+a1,0,c1),1,1).color(1,1,1,1)
    CQ3 = p3d.Array(Cone4)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,(b1*0.8)-c1+b2),NB):
          CQ3.append(translation(i))
    
    Cone5 = p3d.Cone(p3d.Vec3(0,b2,c1),p3d.Vec3(0,b2+a2,c1),1,1).color(1,1,1,1)
    CQ4 = p3d.Array(Cone5)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,(b1*0.8)-c1+b2),NB):
          CQ4.append(translation(i))
    
    Cone6 = p3d.Cone(p3d.Vec3(b2+a1,b2,c1),p3d.Vec3(b2+a1,b2+a2,c1),1,1).color(1,1,1,1)
    CQ5 = p3d.Array(Cone6)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,0,(b1*0.8)-c1+b2),NB):
          CQ5.append(translation(i))

    A1=p3d.combine(Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8,Box9,Box10,Box11,Box12,Box13,Box14,Box15,Box16,Box17,Cone1,CQ,CQ1,CQ2,Text,CQ3,CQ4,CQ5,Box18)
    A2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f)*A1
    A2=rotation(p3d.Vec3(0,0,1),p3d.pi)*A2
    A2=translation(a1+2*a3,a2+2*a3,0)*A2
    data['组合罩棚']= p3d.combine(A2)
if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'辅助设施',
        '构件类型':'区域维护类',
        '构件名称':'组合罩棚',
        '底板长度': 2400,
        '底板宽度': 2000,
        '底板厚度': 50,
        '立柱高度': 3200,
        '立柱边长': 50,
        '立板高度': 1600,
        '顶板厚度': 60,
        '字牌高度': 150,
        '网密度': 80,
        '旋转角度':0
        })
#     data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('组合罩棚',show = True)
    data.setup('底板长度' , obvious = True ,group='底板参数' , description ='长')
    data.setup('底板宽度' , obvious = True ,group='底板参数' , description ='宽')
    data.setup('底板厚度',obvious = True,group='底板参数' , description ='厚')
    data.setup('立柱高度',obvious = True,group='立柱参数' , description ='高')
    data.setup('立柱边长',obvious = True,group='立柱参数' , description ='边长')
    data.setup('立板高度',obvious = True,group='立柱参数', description='立柱高')
    data.setup('顶板厚度',obvious = True,group='顶牌参数', description='板厚')
    data.setup('字牌高度',obvious = True,group='顶牌参数', description='高度')
    data.setup('网密度',obvious = True,group='网密度', description='网密度')
    data.setup('旋转角度',obvious = True,group='旋转', description='旋转角度')
    data.setup('场布分类',obvious=True,readonly=True,group='公共属性',description='场布分类')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = cui
    cui(data)
    p3d.launchData(data)
   
   




