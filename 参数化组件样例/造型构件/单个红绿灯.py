import pyp3d as p3d # 导入pyp3d，可以直接使用pyp3d中的函数而无需前缀
import math
def trafficlight(data:p3d.P3DData)->None:
    H=data['灯杆高度']
    hn=data['红绿灯高度']
    w1=data['灯板宽度']
    h1=2.5*w1 #灯板高度是宽度的2.5倍
    d1=0.18*w1 #灯与板边距离
    dlight=w1-2*d1 #灯的直径
    d2=d1/2 #灯与灯之间纵向距离

    #基座 边长330，厚25 以杆的中心为原点
    aa1=330
    ah1=25
    abox1=p3d.Box(p3d.Vec3(-aa1/2,-aa1/2,0),p3d.Vec3(-aa1/2,-aa1/2,ah1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),aa1,aa1,aa1,aa1)
    #基座上四个钢片
    bline=p3d.Extrusion([p3d.Vec3(0,-6,0),p3d.Vec3(0,-6,aa1/2),p3d.Vec3(90,-6,aa1/2),p3d.Vec3(aa1/2,-6,aa1/4),\
        p3d.Vec3(aa1/2,-6,0),p3d.Vec3(0,-6,0)],p3d.Vec3(0,12,0))
    bline2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/2)*bline
    bline3=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*bline
    bline4=p3d.rotation(p3d.Vec3(0,0,1),1.5*p3d.pi)*bline
    bb=p3d.translation(p3d.Vec3(0,0,ah1))*p3d.unite(bline,bline2,bline3,bline4)

    #灯杆 半径取55
    cr=55
    c1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,H),cr,cr)
    #灯杆带个帽子
    c2=p3d.Sphere(p3d.Vec3(0,0,H),cr)
    cc=p3d.unite(c1,c2)

    #灯的部分以灯板左下角为原点 灯板厚度10
    dm=10
    dbox1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,h1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),w1,-dm,w1,-dm)
    dbox2=p3d.Box(p3d.Vec3(15,1,15),p3d.Vec3(15,1,h1-15),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),w1-30,2,w1-30,2)
    #第一个灯 灯罩长度240
    dz=240
    light11=p3d.Cone(p3d.Vec3(d1+dlight/2,0,d1+dlight/2),p3d.Vec3(d1+dlight/2,dz,d1+dlight/2),dlight/2,dlight/2)
    light12=p3d.Cone(p3d.Vec3(d1+dlight/2,0,d1+dlight/2),p3d.Vec3(d1+dlight/2,dz,d1+dlight/2),dlight/2-5,dlight/2-5)
    green=p3d.Cone(p3d.Vec3(d1+dlight/2,0,d1+dlight/2),p3d.Vec3(d1+dlight/2,5,d1+dlight/2),dlight/2-5,dlight/2-5).color(0,1,0,1)
    light13=p3d.substract(light11,light12)
    cone1=p3d.Cone(p3d.Vec3(0,dz+120,d1/2),p3d.Vec3(w1,dz+120,d1/2),dlight,dlight)
    light1=p3d.substract(light13,cone1)
    light3=p3d.translation(p3d.Vec3(0,0,2*dlight+2*d2))*light1
    red1=p3d.translation(p3d.Vec3(0,0,2*dlight+2*d2))*green
    red2=red1.color(1,0,0,1)
    #上下圆形灯完成，中间方形灯
    light21=p3d.Box(p3d.Vec3(d1,0,dlight+d1+d2),p3d.Vec3(d1,0,dlight+d1+d2+dlight),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),dlight,dlight,dlight,dlight)
    light22=p3d.Box(p3d.Vec3(d1+5,0,dlight+d1+d2),p3d.Vec3(d1,0,dlight+d1+d2+dlight-5),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),dlight-10,dlight,dlight-10,dlight)
    light23=p3d.substract(light21,light22)
    cone2=p3d.translation(0,0,dlight+d2)*cone1
    light2=p3d.substract(light23,cone2)
    #方形灯上面放数字88 灯宽dlight,数字距离灯罩左右方向1/10，两个数字间距及上下1/5，数字宽度0.3*dlight,高度0.6*dlight
    numbox1= p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,0.6*dlight),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),0.3*dlight,5,0.3*dlight,5)
    numboxsub1= p3d.Box(p3d.Vec3(2,0,2),p3d.Vec3(2,0,0.6*dlight-4),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),0.3*dlight-4,5,0.3*dlight-4,5)
    numbox2=p3d.substract(numbox1,numboxsub1)
    numbox3=p3d.Box(p3d.Vec3(0,0,0.3*dlight-1.5),p3d.Vec3(0,0,0.3*dlight+1.5),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),0.3*dlight,5,0.3*dlight,5)
    num1=p3d.unite(numbox2,numbox3)
    num2=p3d.translation(p3d.Vec3(0.5*dlight,0,0))*num1
    num=p3d.translation(p3d.Vec3(d1+0.1*dlight,0,1.2*dlight+d1+d2))*p3d.combine(num1,num2)

    #灯板后面创建一个与灯杆的连接件 长宽cr，高1/3h1
    lj=p3d.Box(p3d.Vec3((w1-cr)/2,-cr*2-dm,h1/3),p3d.Vec3((w1-cr)/2,-cr*2-dm,2*h1/3),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),cr*2,cr*2,cr*2,cr*2)
    lightn=p3d.translation(p3d.Vec3(-w1/2,3*cr,hn))*p3d.combine(dbox1,dbox2,light1,light3,light2,lj,green,red2,num)

    data['红绿灯'] =p3d.combine(abox1,bb,cc,lightn)
if __name__ == "__main__":
    data = p3d.P3DData({
        '灯杆高度':3500, 
        '红绿灯高度':2400, #R1
        '灯板宽度':400,
        '构件名称':'单个红绿灯'
        })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('红绿灯', show=True)
    data.setup('灯杆高度',obvious=True, group='红绿灯', description='灯杆高度')
    data.setup('红绿灯高度',obvious=True, group='红绿灯', description='内侧灯半径')
    data.setup('灯板宽度',obvious=True, group='红绿灯', description='灯板宽度')
    data.setup('构件名称',obvious=True)
    data['replace'] = trafficlight
    trafficlight(data)
    p3d.launchData(data)
