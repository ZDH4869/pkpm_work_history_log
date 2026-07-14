import pyp3d as p3d
from pyp3d import *
def railing(data:p3d.P3DData)->None:
    H1 = data['立柱高度']
    R = data['立柱半径']
    H2 = data['短肢护栏高度']
    H3 = data['长肢护栏高度']
    B1 = data['基础宽度']
    H4 = data['基础高度']
    data['短肢护栏半径'] = 30
    data['长肢护栏半径'] = 30
    data['长短肢护栏间隔'] = 120
    data['护栏红色值'] = 0
    data['护栏绿色值'] = 0
    data['护栏蓝色值'] = 0
    data['护栏颜色透明度'] = 1
    data['基础红色值'] = 255
    data['基础绿色值'] = 255
    data['基础蓝色值'] = 255
    data['基础颜色透明度'] = 1
    data['场布分类'] = '建/构筑物'
    data['构件类型'] = '建筑墙'
    
# L1 = data['护栏长度']
    if H1 < 1800:
        H1 =1800
    else:
        H1 = H1
#立柱
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,H1-400),R,R).color(0,0,0,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,H1-400),p3d.Vec3(0,0,H1),R,1).color(0,0,0,1)
    a1 = p3d.TorusPipe(p3d.Vec3(0,0,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),R,10,p3d.pi*2).color(0,0,0,1)
    a2 = p3d.translation(p3d.Vec3(0,0,H1-420)) * a1
    a3 = p3d.translation(p3d.Vec3(0,0,H1-400)) * a1

    A1 = p3d.Extrusion(
        (p3d.Vec3(0,0,0),p3d.Vec3(150,0,100),p3d.Vec3(190,0,20),p3d.Vec3(165,0,10),p3d.Vec3(145,0,50),p3d.Vec3(0,0,0)),p3d.Vec3(0,20,0)
        ).color(0,0,0,1)
    A2 = p3d.translation(p3d.Vec3(0,0,H1-380)) * A1  
    A3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * A2
    a4 = p3d.translation(p3d.Vec3(0,0,H1-250)) * a1
    LineString2 = p3d.LineString([p3d.Vec3(0,0,0),p3d.Vec3(-41,0,85)])
    LineString3 = p3d.LineString([p3d.Vec3(-41,0,85),p3d.Vec3(-31,0,107),p3d.Vec3(-37,0,111),p3d.Vec3(-60,0,81),p3d.Vec3(-20,0,0),p3d.Vec3(0,0,0)])
    b1 = p3d.ContourLine([LineString2,LineString3])
    b2 = p3d.ExtrusionPlus([b1],p3d.Vec3(0,20,0)).color(0,0,0,1)
    b3 = p3d.translation(p3d.Vec3(-13*R/20,0,H1-290)) * b2
    b4 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * b3
    b5 = p3d.combine(a4,b3,b4).color(0,0,0,1)
    a5 = p3d.translation(p3d.Vec3(0,0,H1-200)) * a1
    data['立柱'] = p3d.combine(Cone1,Cone2,a3,a2,b5,A2,A3,a5)

#中间连接处
    Ellipse3 = p3d.Ellipse(p3d.Vec3(0,0,0), p3d.Vec3(100,0,0), p3d.Vec3(0,0,120),0, p3d.pi)
    LineString4 = p3d.LineString([p3d.Vec3(-100,0,0),p3d.Vec3(-80,0,0)])
    Ellipse4 = p3d.Ellipse(p3d.Vec3(0,0,0), p3d.Vec3(-80,0,0), p3d.Vec3(0,0,100),0, p3d.pi)
    LineString5 = p3d.LineString([p3d.Vec3(80,0,0),p3d.Vec3(100,0,0)])
    c1 = p3d.ContourLine([Ellipse3,LineString5,Ellipse4,LineString4])
    c2 = p3d.ExtrusionPlus([c1],p3d.Vec3(0,20,0)).color(0,0,0,1)
    c3 = p3d.translation(p3d.Vec3(115,0,150)) * c2
    c4 = p3d.rotation(p3d.Vec3(1,0,0),p3d.pi) * c2
    c5 = p3d.translation(p3d.Vec3(115,20,550)) * c4
    c6 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,40), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),250,20,250,20).color(0,0,0,1)
    c7 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,180), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 30, 20, 30, 20).color(0,0,0,1)  
    c8 = p3d.translation(p3d.Vec3(115,0,-60)) * c7
    c9 = p3d.combine(c6,c8)
    c10 = p3d.translation(p3d.Vec3(-10,0,325)) * c9
    lj0 = p3d.combine(c10,c3,c5)
    lj1 = p3d.translation(p3d.Vec3(0,0,700)) * lj0
    lj = p3d.combine(lj0,lj1)
    if H2 < 1410:
        H2 = 1410
    else:
        H2 = H2
#z中间短柱
    d1 = p3d.Cone(p3d.Vec3(220,0,0),p3d.Vec3(220,0,H2-120),30,30).color(0,0,0,1)

    d2 = p3d.FilletPipe((p3d.Vec3(0,0,0),p3d.Vec3(-30,0,-40),p3d.Vec3(0,0,-60)), (0,10,0), 22).color(0,0,0,1)
    d3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * d2
    d31 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/2) * d2
    d32 = p3d.rotation(p3d.Vec3(0,0,1),-p3d.pi/2) * d2
    d4 = p3d.combine(d2,d3,d31,d32)
    d5 = p3d.translation(p3d.Vec3(220,0,H2-70)) * d4#胞
    d6 = p3d.TorusPipe(p3d.Vec3(0,0,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),29,10,p3d.pi*2).color(0,0,0,1)
    d7 = p3d.translation(p3d.Vec3(220,0,H2-140)) * d6#环
    d8 = p3d.Cone(p3d.Vec3(220,0,H2-70),p3d.Vec3(220,0,H2),22,6).color(0,0,0,1)#尖
    dlz = p3d.combine(d1,d5,d7,d8)
    if H3 < 1600:
        H3 = 1600
    else:
        H3 = H3 
#长立柱
    e1 = p3d.Cone(p3d.Vec3(220*2,0,0),p3d.Vec3(220*2,0,H3-120),30,30).color(0,0,0,1)
    e2 = p3d.translation(p3d.Vec3(220*2,0,H3-140)) * d6
    e3 = p3d.translation(p3d.Vec3(220*2,0,H3-70)) * d4
    e4 = p3d.Cone(p3d.Vec3(220*2,0,H3-70),p3d.Vec3(220*2,0,H3),20,6).color(0,0,0,1)
    clz = p3d.combine(e1,e2,e3,e4)
    lj3 = p3d.translation(p3d.Vec3(215,0,0)) * lj
# #护栏下面台
    data['基础1']= p3d.Box(p3d.Vec3(-R,-B1/2,-H4), p3d.Vec3(-R,-B1/2,0), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), R*2, B1, R*2, B1).color(1,1,1,1) 

#一组组件
    whole_length = data['输入长度']
    
    n_dg = data['护栏个数']
    min_dis = 420
    no1 = int(whole_length//min_dis)
    n_xg = int(no1//n_dg)
    zj = p3d.combine(lj,lj3,dlz,clz)
    lizhu_2 = p3d.translation(Vec3(min_dis+R/2,0,0))*data['立柱']
    zj2 = p3d.translation(p3d.Vec3(min_dis*(n_xg-1),0,0)) * p3d.combine(lj,lj3,dlz,lizhu_2)
    
    data['基础2']= p3d.Box(p3d.Vec3(R,-B1/2,-H4), p3d.Vec3( R,-B1/2,0), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),  min_dis*n_xg, B1, min_dis*n_xg, B1).color(1,1,1,1) 

    data['显示长度'] = (whole_length//min_dis)//n_dg*min_dis*n_dg
    data['基础长度'] =  data['显示长度']

    ZJ0 = p3d.Array(zj)
    
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(min_dis*(n_xg-2),0,0),n_xg-1):
        ZJ0.append(translation(i))
    ZJ1 = p3d.combine(ZJ0,data['基础2'],zj2)

    ZJ2 = p3d.Array(ZJ1)
    for i in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(min_dis*(n_dg)*n_xg,0,0),n_dg+1):
        ZJ2.append(translation(i))

    data ['铁艺护栏'] =p3d.combine(data['立柱'],data['基础1'],ZJ2)

  

if __name__ == "__main__":
    data = p3d.P3DData({
         '立柱高度':1800,
         '立柱半径':40,
         '短肢护栏高度':1410,
         '长肢护栏高度':1600,
         '基础宽度':200,
         '基础高度':200,
         '护栏个数':3,
         '输入长度': 5000,
         '构件名称':'铁艺护栏两点布置'
        })
    
    # data.set_view(1,1)
    # data.setup('立柱', show=True)
    # data.setup('', show=True) 
    # data.setup('铁艺护栏0', show=True)
    data.setup('铁艺护栏', show=True)


    data.setup('场布分类',obvious=True,readonly = True, group='类型参数')
    data.setup('构件类型',obvious=True,readonly = True, group='类型参数')
    data.setup('立柱半径',obvious=True, group='立柱参数')
    data.setup('立柱高度',obvious=True, group='立柱参数')

    data.setup('短肢护栏高度',obvious=True, group='护栏参数')
    data.setup('长肢护栏高度',obvious=True, group='护栏参数')
    data.setup('护栏个数',obvious=True, group='护栏参数')
    data.setup('短肢护栏半径',obvious=True,readonly = True, group='护栏参数')
    data.setup('长肢护栏半径',obvious=True,readonly = True, group='护栏参数')
    data.setup('长短肢护栏间隔',obvious=True,readonly = True, group='护栏参数')

    data.setup('基础宽度',obvious=True, group='基础参数')
    data.setup('基础高度',obvious=True, group='基础参数')
    data.setup('基础长度',obvious=True,readonly = True, group='基础参数')   
    data.setup('输入长度',obvious=True,group='几何尺寸')
    data.setup('显示长度',readonly = True,obvious=True, group='几何尺寸')

    data.setup('护栏红色值',obvious=True,readonly = True, group='护栏颜色')
    data.setup('护栏绿色值',obvious=True,readonly = True, group='护栏颜色')
    data.setup('护栏蓝色值',obvious=True,readonly = True, group='护栏颜色')
    data.setup('护栏颜色透明度',obvious=True,readonly = True, group='护栏颜色')
    data.setup('基础红色值',obvious=True,readonly = True, group='基础颜色')
    data.setup('基础绿色值',obvious=True,readonly = True, group='基础颜色')
    data.setup('基础蓝色值',obvious=True,readonly = True, group='基础颜色')
    data.setup('基础颜色透明度',obvious=True,readonly = True, group='基础颜色')
    data.setup('构件名称',obvious=True)
    data['replace'] = railing
    railing(data)
    p3d.TwoPointPlace.linearize(data, '输入长度')
    p3d.launchData(data)