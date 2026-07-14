import pyp3d as p3d
from pyp3d import *
def lkh(data:p3d.P3DData)->None:
    #安全区域无隔板
    a1=data['底座垫块边长']#底座垫块边长度
    b1=data['底座平台长度']#底座平台长度度
    b2=data['底座平台宽度']#底座平台宽度
    c1=data['立柱边长']#立柱边长度
    c2=data['立柱高']#立柱高度
    d1=data['顶板厚']#顶板厚度
    e1=data['字牌厚度']#字牌厚度
    e2=data['字牌高度']#自拍高度
    f1=data['旋转角度']
    Box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box2=p3d.Box(p3d.Vec3(b1*0.5-a1,0,0),p3d.Vec3(b1*0.5-a1,0,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box3=p3d.Box(p3d.Vec3(b1-a1,0,0),p3d.Vec3(b1-a1,0,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box4=p3d.Box(p3d.Vec3(0,b2*0.5-a1,0),p3d.Vec3(0,b2*0.5-a1,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box5=p3d.Box(p3d.Vec3(0,b2-a1,0),p3d.Vec3(0,b2-a1,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box6=p3d.Box(p3d.Vec3(b1*0.5-a1,b2-a1,0),p3d.Vec3(b1*0.5-a1,b2-a1,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box7=p3d.Box(p3d.Vec3(b1-a1,b2-a1,0),p3d.Vec3(b1-a1,b2-a1,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box8=p3d.Box(p3d.Vec3(b1-a1,b2*0.5-a1,0),p3d.Vec3(b1-a1,b2*0.5-a1,a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a1,a1,a1).color(67/255,142/255,219/255,1)
    Box9=p3d.Box(p3d.Vec3(0,0,a1),p3d.Vec3(0,0,a1+a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b1,b2,b1,b2).color(67/255,142/255,219/255,1)
    Box10=p3d.Box(p3d.Vec3(0,0,a1+a1),p3d.Vec3(0,0,c2+a1+a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),c1,c1,c1,c1).color(67/255,142/255,219/255,1)
    Box11=p3d.Box(p3d.Vec3(b1-c1,0,a1+a1),p3d.Vec3(b1-c1,0,c2+a1+a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),c1,c1,c1,c1).color(67/255,142/255,219/255,1)
    Box12=p3d.Box(p3d.Vec3(0,b2-c1,a1+a1),p3d.Vec3(0,b2-c1,c2+a1+a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),c1,c1,c1,c1).color(67/255,142/255,219/255,1)
    Box13=p3d.Box(p3d.Vec3(b1-c1,b2-c1,a1+a1),p3d.Vec3(b1-c1,b2-c1,c2+a1+a1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),c1,c1,c1,c1).color(67/255,142/255,219/255,1)
    Box14=p3d.Box(p3d.Vec3(0,0,a1+c2+a1),p3d.Vec3(0,0,a1+c2+a1+d1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b1,b2,b1,b2).color(67/255,142/255,219/255,1)
    Box15=p3d.Box(p3d.Vec3(0,0,a1*2+c2+d1),p3d.Vec3(0,0,a1*2+c2+d1+e2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b1,e1,b1,e1).color(67/255,142/255,219/255,1)
    text= p3d.Text("厨房卫生间样板",b1*0.09,e2*0.6).color(225/255,225/255,225/255, 1)
    text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text
    text= p3d.translation(p3d.Vec3(b1*0.07, -20, c2+a1+a1+d1+e2*0.2))*text
    A1= p3d.combine(Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8,Box9,Box10,Box11,Box12,Box13,Box14,Box15,text)
    A2= p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f1) *A1
    data['样板间']=p3d.combine(A2)
if __name__ == "__main__":
    data=p3d.P3DData({
        '底座垫块边长': 100,
        '底座平台长度': 2400,
        '底座平台宽度': 2000,
        '立柱边长': 60,
        '立柱高': 2800,
        '顶板厚': 30,
        '字牌厚度': 60,
        '字牌高度':500,
        '旋转角度':0,
        '场布分类':'辅助设施',
        '构件类型':'施工管理、技术（标准工艺等）展示区域',
        '构件名称':'厨房卫生间展示台',
        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('样板间',show = True)
    data.setup('底座垫块边长' , obvious = True ,group='底座垫块参数' , description ='边长')
    data.setup('底座平台长度',obvious = True,group='底座平台参数' , description ='长')
    data.setup('底座平台宽度',obvious = True,group='底座平台参数' , description ='宽')
    data.setup('立柱边长',obvious = True,group='立柱参数', description='板厚')
    data.setup('立柱高',obvious = True,group='立柱参数', description='板厚')
    data.setup('顶板厚',obvious = True,group='顶板参数', description='高度')
    data.setup('字牌厚度',obvious = True,group='字牌参数', description='厚度')
    data.setup('字牌高度',obvious = True,group='字牌参数', description='高度')
    data.setup( '旋转角度', obvious=True, group='旋转',description= '旋转角度')
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = lkh
    lkh(data)
    p3d.launchData(data)