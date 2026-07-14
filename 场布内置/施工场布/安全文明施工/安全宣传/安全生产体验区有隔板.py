import pyp3d as p3d
def cui(data:p3d.P3DData)->None:
    #安全区域无隔板
    a1=data['底座长']#底座班长度
    a2=data['底座宽']#底座的宽度
    a3=data['底座高']#底座的高度
    b1=data['侧板高']#侧板的高度
    b2=data['侧板厚度']#侧板的厚度
    c1=data['顶牌厚度']#顶牌的厚度
    c2=data['顶牌高度']#顶牌的高度
    d1=data['后板厚度']#后板的厚度
    e1=data['顶板厚度']#顶板的厚度
    f1=data['旋转角度']#旋转角度
    Box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,a3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a2,a1,a2).color(67/255,142/255,219/255,1)
    Box2=p3d.Box(p3d.Vec3(0,0,a3),p3d.Vec3(0,0,b1+a3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(67/255,142/255,219/255,1)
    Box3=p3d.Box(p3d.Vec3(a1-b2,0,a3),p3d.Vec3(a1-b2,0,b1+a3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(67/255,142/255,219/255,1)
    Box4=p3d.Box(p3d.Vec3(0,a2-d1,a3),p3d.Vec3(0,a2-d1,b1+a3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,d1,a1,d1).color(67/255,142/255,219/255,1)
    Box5=p3d.Box(p3d.Vec3(0,0,b1+a3),p3d.Vec3(0,0,b1+a3+c2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,c1,a1,c1).color(67/255,142/255,219/255,1)
    Box6=p3d.Box(p3d.Vec3(0,0,b1+a3),p3d.Vec3(0,0,b1+a3+e1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a1,a2,a1,a2).color(67/255,142/255,219/255,1)
    Box7=p3d.Box(p3d.Vec3(a1/3,0,a3),p3d.Vec3(a1/3,0,a3+b1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(67/255,142/255,219/255,1)
    Box8=p3d.Box(p3d.Vec3(a1*2/3,0,a3),p3d.Vec3(a1*2/3,0,a3+b1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),b2,a2,b2,a2).color(67/255,142/255,219/255,1)
    text= p3d.Text("安全帽撞击体验",a1*0.09,c2*0.4).color(225/255,225/255,225/255, 1)
    text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text
    text= p3d.translation(p3d.Vec3(a1*0.06, -20, a3+b1+c2*0.15))*text
    text2= p3d.Text("怀化利霖建筑工程有限公司",a1*0.035,c2*0.1).color(225/255,225/255,225/255, 1)
    text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text2
    text2= p3d.translation(p3d.Vec3(a1*0.2, -20, a3+b1+c2*0.8))*text2
    data['侧板间距']=a1/3
    A1=p3d.combine(Box1,Box2,Box3,Box4,Box5,Box6,text,Box7,Box8,text2)
    A1=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f1)*A1
    data['安全区域有隔板']= p3d.combine(A1)

    
if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'安全区域有隔板',
        '构件类型':'安全区域有隔板',
        '构件名称':'安全生产体验区有隔板',
        '底座长': 2400,
        '底座宽': 1000,
        '底座高': 70,
        '侧板高': 2000,
        '侧板厚度': 40,
        '顶牌厚度': 40,
        '顶牌高度': 500,
        '后板厚度': 40,
        '顶板厚度':40,
        '旋转角度':0,
        })
    data.setup('安全区域有隔板',show = True)
    data.setup('底座长' , obvious = True ,group='底座参数' , description ='长')
    data.setup('底座宽',obvious = True,group='底座参数' , description ='宽')
    data.setup('底座高',obvious = True,group='底座参数' , description ='高')
    data.setup('侧板高',obvious = True,group='侧板参数' , description ='高')
    data.setup('侧板厚度',obvious = True,group='侧板参数', description='板厚')
    data.setup('顶牌厚度',obvious = True,group='顶牌参数', description='板厚')
    data.setup('顶牌高度',obvious = True,group='顶牌参数', description='高度')
    data.setup('后板厚度',obvious = True,group='后板参数', description='厚度')
    data.setup('顶板厚度',obvious = True,group='顶板参数', description='厚度')
    data.setup('侧板间距',obvious=True,readonly=True,group='侧板间距',description='间距')
    data.setup('旋转角度',obvious = True,group='旋转', description='旋转角度')
    data.setup('场布分类',obvious=True,readonly=True,group='公共属性',description='场布分类')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)
    data['replace'] = cui
    cui(data)
    p3d.launchData(data)