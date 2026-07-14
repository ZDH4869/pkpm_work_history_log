import pyp3d as p3d
from pyp3d import *
def yumaoqiuchangdi(data:p3d.P3DData)->None:

    #建立羽毛球场
    l=15000  #data['场地长度']
    w=7500   #data['场地宽度']
    rota=data['旋转角度']
    data['场布分类']='辅助设施'
    data['构件类型']='简易体育设施'
    #场地建立
    cf=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,3), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l, w, l, w).color(41/255,164/255,123/255,1) 
    # createGeometry(cf)

    #建立线
    line1=p3d.Box(p3d.Vec3(0,0,3), p3d.Vec3(0,0,4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 40, 6100, 40, 6100).color(1,1,1,1)
    line1=p3d.translation(800,700,0)*line1
    line2=p3d.translation(720+40,0,0)*line1
    line3=p3d.translation(40+3880,0,0)*line2

    line4=p3d.Box(p3d.Vec3(0,0,3), p3d.Vec3(0,0,4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 6700, 40, 6700, 40).color(1,1,1,1)
    line4=p3d.translation(800,700,0)*line4
    line5=p3d.translation(0,420+40,0)*line4
    line7=p3d.translation(0,5140,0)*line5
    line8=p3d.translation(0,420+40,0)*line7

    line6=p3d.Box(p3d.Vec3(0,0,3), p3d.Vec3(0,0,4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 4720, 40, 4720, 40).color(1,1,1,1)
    line6=p3d.translation(800,700,0)*line6
    line6=p3d.translation(0,3030,0)*line6
    x=combine(line1,line2,line3,line4,line5,line6,line7,line8)
    # createGeometry(x)
    x2=rotation(p3d.Vec3(0,1,0),pi)*x
    x2=translation(15000,0,7)*x2
    # createGeometry(x2)
    xian=p3d.unite(x,x2)
    # createGeometry(xian)

    #建立柱子
    box1=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(100,0,0), p3d.Vec3(0,1,0), p3d.Vec3(0,0,1), 300, 100, 300, 100).color(1,1,0,1) 
    cone1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,1750),20,20)
    cone1=translation(50,250,0)*cone1
    zhuzi=unite(box1,cone1).color(1,1,0,1)
    zhuzi1=translation(0,200,0)*zhuzi
    # createGeometry(zhuzi1)
    zhuzi2=rotation(p3d.Vec3(0,0,1),pi)*zhuzi1
    zhuzi2=translation(100,7500,0)*zhuzi2
    # createGeometry(zhuzi2)
    zhuzi=combine(zhuzi1,zhuzi2)
    zhuzi=translation(7500-50,0,0)*zhuzi
    # createGeometry(zhuzi)

    #建立网
    mian=Box(p3d.Vec3(0,0,0), p3d.Vec3(10,0,0), p3d.Vec3(0,1,0), p3d.Vec3(0,0,1), 6560, 770, 6560, 770).color(1,1,1,0.4) 
    mian=translation(7500-5,470,780)*mian
    # createGeometry(mian)

    #组合构件
    badminton=combine(cf,xian,zhuzi,mian)
    badminton=translation(-l/2,-w/2,0)*badminton
    badminton=rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*badminton
    # createGeometry(badminton)
    data['羽毛球场地']=badminton
    data['场地长度']=l
    data['场地宽度']=w

if __name__ == "__main__":
    data = p3d.P3DData({
        '场地长度': 15000,  
        '场地宽度': 7500,
        '旋转角度':0,     
        '构件名称':'羽毛球场地'  
        })

    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('羽毛球场地', show=True)
    # 设置可调整属性
    data.setup('场地长度', obvious=True,readonly=True,group = '场地参数')
    data.setup('场地宽度', obvious=True,readonly=True,group = '场地参数')
    data.setup('旋转角度', obvious=True,group = '场地参数')
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = yumaoqiuchangdi
    yumaoqiuchangdi(data)
    # 发射数据到实例模板库
    p3d.launchData(data)