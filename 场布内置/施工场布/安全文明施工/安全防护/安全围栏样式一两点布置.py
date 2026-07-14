import pyp3d as p3d
#import math
# import TwoPointPlace
def test_box(data:p3d.P3DData)->None:
    
    a=data['围栏长度']
    b=data['围栏高度']
    R=data['外圈管径']
    r=data['内部管径']
    x=data['竖杆间距']
    c=data['竖杆个数']  #随长度和间距变化
    d=data['短杆距外杆距离']
    z=data['围栏个数']
    m=data['底座高']
    x=(a-R*3-c*2*r)/(c+1)+R+r
    data['竖杆间距']=x
    #k=data['旋转角度']
    #l=a*(z-1)+20*(z-1)*2+R*z
    #l=a*z
    l=data['总长度']
    
    #z=l/a
    #z=data['围栏个数']

    if R+d+r>a/2:
        d=a/2-R-r

#底座
    a1=p3d.FilletPipe((p3d.Vec3(0,225,-m),p3d.Vec3(0,225,-R),p3d.Vec3(0,-225,-R),p3d.Vec3(0,-225,-m)),(0,20,20,0),R).color(1,1,1,1)
    a2=p3d.translation(p3d.Vec3(a,0,0))*a1

#左侧柱
    Cone1=p3d.Cone(p3d.Vec3(0,0,-R),p3d.Vec3(0,0,20),R,R).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,(b-r*2-220)/6+20),R,R).color(1,0,0,1)
    Cone3 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6+20),p3d.Vec3(0,0,(b-r*2-220)/6*2+20),R,R).color(1,1,1,1)
    Cone4 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*2+20),p3d.Vec3(0,0,(b-r*2-220)/6*3+20),R,R).color(1,0,0,1)
    Cone5 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*3+20),p3d.Vec3(0,0,(b-r*2-220)/6*4+60),R,R).color(1,1,1,1)
    Cone6 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*4+60),p3d.Vec3(0,0,(b-r*2-220)/6*5+60),R,R).color(1,0,0,1)
    Cone7 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*5+60),p3d.Vec3(0,0,(b-r*2-220)/6*6+100),R,R).color(1,1,1,1)
    # Cone8 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*6+100),p3d.Vec3(0,0,b-r*8),R,R).color(1,0,0,1)
    AAA = p3d.combine(Cone1,Cone2,Cone3,Cone4,Cone5,Cone6,Cone7)
    
#右侧柱
    BBB=p3d.translation(p3d.Vec3(a,0,0))*AAA
    
#下横柱
    Cone11=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,20),r,r).color(1,1,1,1)
    Cone12 = p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,(a-220)/6+20),r,r).color(1,0,0,1)
    Cone13 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6+20),p3d.Vec3(0,0,(a-220)/6*2+20),r,r).color(1,1,1,1)
    Cone14 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*2+20),p3d.Vec3(0,0,(a-220)/6*3+20),r,r).color(1,0,0,1)
    Cone15 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*3+20),p3d.Vec3(0,0,(a-220)/6*4+60),r,r).color(1,1,1,1)
    Cone16 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*4+60),p3d.Vec3(0,0,(a-220)/6*5+60),r,r).color(1,0,0,1)
    Cone17 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*5+60),p3d.Vec3(0,0,(a-220)/6*6+100),r,r).color(1,1,1,1)
    Cone18 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*6+100),p3d.Vec3(0,0,a),r,r).color(1,0,0,1)
    CCC=p3d.combine(Cone11,Cone12,Cone13,Cone14,Cone15,Cone16,Cone17,Cone18)
    DDD=p3d.rotation(p3d.Vec3(0,1,0),p3d.pi*0.5)*CCC
    
#中横柱
    EEE=p3d.translation(p3d.Vec3(0,0,(b*3/4-r*3-R*3/2)))*DDD
    
#上横柱
    #Cone21=p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,20),R,R).color(1,1,1,1)
    #Cone22=p3d.Cone(p3d.Vec3(0,0,20),p3d.Vec3(0,0,(a-220)/6+20),R,R).color(1,0,0,1)
    Cone23 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6+20),p3d.Vec3(0,0,(a-220)/6*2+20),R,R).color(1,1,1,1)
    Cone24 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*2+20),p3d.Vec3(0,0,(a-220)/6*3+20),R,R).color(1,0,0,1)
    Cone25 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*3+20),p3d.Vec3(0,0,(a-220)/6*4+60),R,R).color(1,1,1,1)
    Cone26 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*4+60),p3d.Vec3(0,0,(a-220)/6*5+60),R,R).color(1,0,0,1)
    Cone27 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*5+60),p3d.Vec3(0,0,(a-220)/6*6+100-30),R,R).color(1,1,1,1)
    #Cone28 = p3d.Cone(p3d.Vec3(0,0,(a-220)/6*6+100),p3d.Vec3(0,0,a-10),R,R).color(1,0,0,1)
    FFF=p3d.combine(Cone23,Cone24,Cone25,Cone26,Cone27)
    GGG=p3d.rotation(p3d.Vec3(0,1,0),p3d.pi*0.5)*FFF
    HHH=p3d.translation(p3d.Vec3(0,0,b-R*2))*GGG
    
#圆角管
    aaa=p3d.FilletPipe((p3d.Vec3(0,0,b-r*8),p3d.Vec3(0,0,b-R*2),p3d.Vec3((a-200)/6+20,0,b-R*2)),(0,40,0),R).color(1,0,0,1)
    bbb=p3d.FilletPipe((p3d.Vec3(a,0,b-r*8),p3d.Vec3(a,0,b-R*2),p3d.Vec3(a-150,0,b-R*2)),(0,40,0),R).color(1,0,0,1)
    
#上部竖杆
    ccc=p3d.Cone(p3d.Vec3(R+d+r,0,(b*3/4-r*3-R*3/2)),p3d.Vec3(R+d+r,0,b-R*2),r,r).color(1,0,0,1)
    ddd=p3d.Cone(p3d.Vec3(a-R*3-d,0,(b*3/4-r*3-R*3/2)),p3d.Vec3(a-R*3-d,0,b-R*2),r,r).color(1,0,0,1)

#竖杆
    
    Cone32 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,(b-r*2-220)/6+20),r,r).color(1,0,0,1)
    Cone33 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6+20),p3d.Vec3(0,0,(b-r*2-220)/6*2+20),r,r).color(1,1,1,1)
    Cone34 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*2+20),p3d.Vec3(0,0,(b-r*2-220)/6*3+20),r,r).color(1,0,0,1)
    Cone35 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*3+20),p3d.Vec3(0,0,(b-r*2-220)/6*4+60),r,r).color(1,1,1,1)
    Cone36 = p3d.Cone(p3d.Vec3(0,0,(b-r*2-220)/6*4+60),p3d.Vec3(0,0,(b*3/4-R*3/2-r*3)),r,r).color(1,0,0,1)

    aa=p3d.combine(Cone32,Cone33,Cone34,Cone35,Cone36)
    aa2=p3d.translation(p3d.Vec3(r+x,0,0))*aa

    ##################
    VerticalCone = p3d.Array(aa2)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(a-R*3-x*2+R*2,0,0),c):
        VerticalCone.append(p3d.translation(i))
    #线性排布
    
    # points1=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(a-R*3-x*2+R*2,0,0),c)
    # VerticalCone=p3d.combine()
    # for point in points1:
    #     VerticalCone.append(p3d.translation(point)*aa2)

#插栓
    b1=p3d.Box(p3d.Vec3(-20-R+5,0,b/10),p3d.Vec3(-20-R+5,0,b/10+50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,20,20,20).color(128/255,138/255,135/255,1)
    b2=p3d.Box(p3d.Vec3(-20-R+5,0,b*3/5-50),p3d.Vec3(-20-R+5,0,b*3/5),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,20,20,20).color(128/255,138/255,135/255,1)
    b3=p3d.Box(p3d.Vec3(a+R-5,0,b/10+50),p3d.Vec3(a+R-5,0,b/10+50+50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,20,20,20).color(128/255,138/255,135/255,1)
    b4=p3d.Box(p3d.Vec3(a+R-5,0,b*3/5-50+50),p3d.Vec3(a+R-5,0,b*3/5+50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),20,20,20,20).color(128/255,138/255,135/255,1)
    b5=p3d.Cone(p3d.Vec3(a+R+7,10,b/10-20+50),p3d.Vec3(a+R+7,10,b/10+50),5,5).color(128/255,138/255,135/255,1)
    b6=p3d.Cone(p3d.Vec3(a+R+7,10,b*3/5-50-20+50),p3d.Vec3(a+R+7,10,b*3/5-50+50),5,5).color(128/255,138/255,135/255,1)
    chashuan=p3d.combine(b1,b2,b3,b4,b5,b6)
#两点布置，线性排布

    weilan=p3d.combine(AAA,BBB,a1,a2,DDD,EEE,HHH,aaa,bbb,ccc,ddd,VerticalCone,chashuan)
    anquanweilan = p3d.Array(weilan)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((a+40+R)*(l//(a+40+R)),0,0),p3d.math.floor(l//(a+40+R)+1)):
        anquanweilan.append(p3d.translation(i))
    # for point in points2:
    #     anquanweilan.append(p3d.translation(point)*weilan)

    data['安全围栏-线性排布']=p3d.translation(p3d.Vec3(0,0,m)) * anquanweilan
    data['竖杆间距']=(a-R*3-c*r*2)/(c+1)+R+r
    data['底座半径']=R
    data['围栏个数']=int(l//(a+20))+1
    data['总长度'] = data['围栏个数']*data['围栏长度']

if __name__ == "__main__":
    data = p3d.P3DData({
        '围栏长度':1500,
        '围栏高度':1000,
        '外圈管径':30,
        '内部管径':20,
        '竖杆间距':180,
        '竖杆个数':5,
        '短杆距外杆距离':180,
        '围栏个数':1,
        '底座高':200,
        '底座宽':450,
        '底座半径':50,
        #'旋转角度':0,
        '总长度':1520,
        '场布分类':'辅助设施',
        '构件类型':'区域维护类',
        '构件名称':'安全围栏样式一两点布置',
        })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('安全围栏-线性排布', show=True)
    data.setup('围栏长度', obvious=True, group='围栏', description='围栏长度')
    data.setup('围栏高度', obvious=True, group='围栏', description='围栏高度')
    data.setup('外圈管径', obvious=True, group='管径', description='外圈管径')
    data.setup('内部管径', obvious=True, group='管径', description='内部管径') 
    data.setup('竖杆间距', obvious=True,readonly=True,group='围栏', description='竖杆间距') 
    data.setup('竖杆个数', obvious=True,group='围栏', description='竖杆个数') 
    data.setup('短杆距外杆距离', obvious=True,group='围栏', description='短杆距外杆距离') 
    data.setup('围栏个数', obvious=True,readonly=True,group='围栏', description='围栏个数') 
    data.setup('底座高', obvious=True,group='底座', description='底座高') 
    data.setup('底座宽', obvious=True,readonly=True,group='底座', description='底座宽') 
    data.setup('底座半径', obvious=True,readonly=True,group='底座', description='底座半径') 
    #data.setup('旋转角度', obvious=True, group='旋转角度', description='内部管径旋转角度')
    data.setup('总长度', obvious=True, group='总长度', description='总长度')
    data.setup('场布分类', obvious=True,readonly=True,group='公共属性', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='公共属性', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.TwoPointPlace.linearize(data, '总长度')
    p3d.launchData(data)