import pyp3d as p3d
import math
def LKH(data:p3d.P3DData)->None:
    z1=data['圆柱高度']#圆柱高度
    R =data['圆柱半径']#圆柱半径
    c =data['总围栏长']#总围栏长度
    s=data['柱子个数']#柱子个数
    f=data['旋转角度']#旋转角度
    l_loop=data['柱子间距']
    
    #竖
    Cone1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(0,0,z1/7),R,R).color(1,1,1,1)
    Cone2 = p3d.Cone(p3d.Vec3(0,0,z1/7),p3d.Vec3(0,0,z1*2/7),R,R).color(1,0,0,1)
    Cone3 = p3d.Cone(p3d.Vec3(0,0,z1*2/7),p3d.Vec3(0,0,z1*3/7),R,R).color(1,1,1,1)
    Cone4 = p3d.Cone(p3d.Vec3(0,0,z1*3/7),p3d.Vec3(0,0,z1*4/7),R,R).color(1,0,0,1)
    Cone5 = p3d.Cone(p3d.Vec3(0,0,z1*4/7),p3d.Vec3(0,0,z1*5/7),R,R).color(1,1,1,1)
    Cone6 = p3d.Cone(p3d.Vec3(0,0,z1*5/7),p3d.Vec3(0,0,z1*6/7),R,R).color(1,0,0,1)
    Cone7 = p3d.Cone(p3d.Vec3(0,0,z1*6/7),p3d.Vec3(0,0,z1),R,R).color(1,1,1,1)
    AA = p3d.combine(Cone1,Cone2,Cone3,Cone4,Cone5,Cone6,Cone7)
    SG = p3d.Array(AA)
    n_loop = int(c/l_loop)
    for i in range(n_loop+1):
        SG.append(p3d.translation(i*l_loop,0,0))
    # 补充剩余距离
    if c-l_loop*n_loop>0:
        SG = p3d.combine(SG,p3d.translate(c,0,0)*AA)  
        n_loop = n_loop+2  
    
#横杆
    # white
    ConeA = p3d.Cone(p3d.Vec3(R,0,z1*2.1/7),p3d.Vec3(R+150,0,z1*2.1/7),R,R).color(1,1,1,1)
    midsg1 = p3d.translation(p3d.Vec3(0,0,z1*3.8/7)) * ConeA
    whitecone= p3d.Array(p3d.combine(ConeA,midsg1))
    n = int((c+150)//300)
    for i in p3d.linspace(p3d.Vec3(-120,0,0),p3d.Vec3(c-220,0,0),n+1):
        whitecone.append(p3d.translation(i))

    # red
    ConeB = p3d.Cone(p3d.Vec3(R+150,0,z1*2.1/7),p3d.Vec3(R+300,0,z1*2.1/7),R,R).color(1,0,0,1)
    midsg2 = p3d.translation(p3d.Vec3(0,0,z1*3.8/7)) * ConeB
    redcone=p3d.Array(p3d.combine(ConeB,midsg2))
    k = int((c+150)//300)
    for i in p3d.linspace(p3d.Vec3(-120,0,0),p3d.Vec3(c-220,0,0),k+1):
        redcone.append(p3d.translation(i))


# 整体
    AA1=p3d.combine(SG,whitecone,redcone)
    AA2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi/180*f)*AA1
    data['提示遮拦'] = AA2
    data['柱子个数'] = n_loop
if __name__ == "__main__":
    data=p3d.P3DData({
        '圆柱高度': 1400,
        '圆柱半径': 40,
        '总围栏长': 2400,
        '柱子个数':5,
        '柱子间距':2100,
        '旗子个数':20,
        '旋转角度':0,
        '构件名称':'安全围栏样式二两点布置'
        })

    data.setup('提示遮拦',show = True)
    data.setup('圆柱高度' , obvious = True ,group='圆柱' , description ='高')
    data.setup('圆柱半径',obvious = True,group='圆柱' , description ='半径')
    data.setup('总围栏长',obvious = True,group='总围栏长' , description ='长')
    data.setup('柱子个数',obvious = True,readonly=True,group='圆柱' , description ='个数')
    data.setup('柱子间距',obvious=True,group='圆柱',description='侧板间距')
    data.setup('旋转角度',obvious = True,group='旋转', description='旋转角度')
    data.setup('构件名称',obvious=True)
    data['replace'] = LKH
    p3d.TwoPointPlace.linearize(data, '总围栏长')
    LKH(data)
    p3d.launchData(data)