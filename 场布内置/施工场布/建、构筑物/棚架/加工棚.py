import pyp3d as p3d
import math
from pyp3d import *
def kcpj(data:p3d.P3DData)->None:

# 立柱参数
    
    l2=data['立柱粗']
    lzx=data['立柱数']
    
# 圈梁参数8
    cl1=data['圈梁支撑立柱高']
    cl2=data['圈梁支撑立柱粗']
    qld=data['圈梁粗']
    l1=cl1+1000
    data['立柱高']=cl1+1000
    
# 支撑梁参数
    z=data['支撑梁粗']
    sz=data['竖直支撑梁长']
    xz=data['斜支撑梁长']

# 楼板参数
    lbc=data['楼板长']
    lbk=data['楼板宽']
    lbh=data['楼板厚']

# 棚顶参数
    pdw=data['棚顶厚']
    pdlr=data['棚顶梁半径']
    pdlx=data['棚顶斜梁数']
    pdh=data['棚顶高']

#固定参数
    a1=100   
    b1=cl1+qld+sz-l1
    k=data['旋转角度']
    l=data['场布分类']
    m=data['构件类型']

#立柱
    lz01=p3d.Box(p3d.Vec3(0,-l2/2,0),p3d.Vec3(0,-l2/2,cl1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),l2,l2,l2,l2).color(192/255,192/255,192/255,1)
    lz02=p3d.Box(p3d.Vec3(lbc,-l2/2,0),p3d.Vec3(lbc,-l2/2,cl1),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),l2,l2,l2,l2).color(192/255,192/255,192/255,1)
    
    lz11=p3d.Box(p3d.Vec3(0,lbk/2+l2,0),p3d.Vec3(0,lbk/2+l2,cl1+1000),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),l2,l2,l2,l2).color(192/255,192/255,192/255,1)
    lz111=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*1) * lz11
    points7=p3d.linspace(p3d.Vec3(l2,l2,0),p3d.Vec3(lbc+l2,l2,0),lzx)
    rebars7 = p3d.combine()
    for point in points7:
        rebars7.append(p3d.translation(point) * lz111)

    rebars8 = p3d.translation(p3d.Vec3(0,lbk+l2,0)) * rebars7   
    lz=p3d.combine(lz01,lz02,rebars8,rebars7)

#圈梁
    ql1=p3d.Box(p3d.Vec3(0,-lbk/2-l2,cl1),p3d.Vec3(0,-lbk/2-l2,cl1+qld),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),lbc+l2,lbk+l2*2,lbc+l2,lbk+l2*2)
    ql2=p3d.Box(p3d.Vec3(0,-lbk/2+qld-l2,cl1),p3d.Vec3(0,-lbk/2+qld-l2,cl1+qld),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),lbc+l2,lbk-qld*2+l2*2,lbc+l2,lbk-qld*2+l2*2)
    ql=p3d.substract(ql1,ql2).color(210/255,180/255,140/255,1)

#支撑梁
    szcl1=p3d.Box(p3d.Vec3(0,-z/2,cl1+qld),p3d.Vec3(0,-z/2,cl1+qld+sz),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),z,z,z,z).color(210/255,180/255,140/255,1)
    points6=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(lbc,0,0),lzx)
    rebars6 = p3d.combine()
    for point in points6:
        rebars6.append(p3d.translation(point) * szcl1)
    zcl=p3d.combine(rebars6)

#横梁
    hl1=p3d.Box(p3d.Vec3(lbc/3,-lbk/2,cl1),p3d.Vec3(lbc/3,-lbk/2,cl1+qld),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),qld,lbk,qld,lbk).color(210/255,180/255,140/255,1)
    points3=p3d.linspace(p3d.Vec3(-lbc/3,0,0),p3d.Vec3(lbc*2/3,0,0),lzx)
    rebars3 = p3d.combine()
    for point in points3:
        rebars3.append(p3d.translation(point) * hl1)

#斜支撑梁
    xl1=p3d.Box(p3d.Vec3(0,lbk/4,cl1+qld),p3d.Vec3(0,lbk/4,cl1+qld+b1/2+l1-cl1-a1/2-qld/2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),z,z,z,z).color(210/255,180/255,140/255,1)
    points4=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(lbc,0,0),lzx)
    rebars4 = p3d.combine()
    for point in points4:
        rebars4.append(p3d.translation(point) * xl1)
    
    xl2=p3d.Box(p3d.Vec3(0,-lbk/4+a1,cl1+qld),p3d.Vec3(0,-lbk/4+a1,cl1+qld+b1/2+l1-cl1-a1/2-qld/2),p3d.Vec3(1,0,0),p3d.Vec3(0,-1,0),z,z,z,z).color(210/255,180/255,140/255,1)
    points5=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(lbc,0,0),lzx)
    rebars5 = p3d.combine()
    for point in points5:
        rebars5.append(p3d.translation(point) * xl2)
    
    xl=p3d.combine(rebars5,rebars4)

#棚顶
    pdy=p3d.Extrusion((p3d.Vec3(0,0,cl1+qld+sz),p3d.Vec3(0,0,cl1+qld+sz+pdw),p3d.Vec3(0,l2+lbk/2,cl1+1000+pdw),p3d.Vec3(0,l2+lbk/2,cl1+1000)),p3d.Vec3(lbc+l2,0,0)).color(65/255,105/255,1,1)
    pdy2=p3d.Extrusion((p3d.Vec3(0,0,cl1+qld+sz),p3d.Vec3(0,0,cl1+qld+sz+pdw),p3d.Vec3(0,-l2-lbk/2,cl1+1000+pdw),p3d.Vec3(0,-l2-lbk/2,cl1+1000)),p3d.Vec3(lbc+l2,0,0)).color(65/255,105/255,1,1)
    pd=p3d.combine(pdy,pdy2)

#楼板
    lb=p3d.Box(p3d.Vec3(0,-lbk/2-l2,-lbh),p3d.Vec3(0,-lbk/2-l2,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),lbc+l2,lbk+l2*2,lbc+l2,lbk+l2*2).color(0.5,0.5,0.5,1)

#棚顶斜梁
    pdl1=p3d.Cone(p3d.Vec3(300+pdlr,0,cl1+qld+sz),p3d.Vec3(300+pdlr,lbk/2+l2,cl1+1000),pdlr,pdlr).color(210/255,180/255,140/255,1)
    pdl2=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*1) * pdl1
    points1 = p3d.linspace(p3d.Vec3(300+pdlr,0,0),p3d.Vec3(lbc-300-pdlr,0,0),pdlx)
    rebars1 = p3d.combine()
    for point in points1:
        rebars1.append(p3d.translation(point) * pdl2)
    
    pdl3=p3d.Cone(p3d.Vec3(300+pdlr,0,cl1+qld+sz),p3d.Vec3(300+pdlr,-lbk/2-l2,cl1+1000),pdlr,pdlr).color(210/255,180/255,140/255,1)
    pdl4=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*1) * pdl3
    points2 = p3d.linspace(p3d.Vec3(300+pdlr,0,0),p3d.Vec3(lbc-300-pdlr,0,0),pdlx)
    rebars2 = p3d.combine()
    for point in points2:
        rebars2.append(p3d.translation(point) * pdl4)

    pdxl=p3d.combine(rebars1,rebars2)

#棚顶梁
    apdl=p3d.Cone(p3d.Vec3(0,lbk*3/8+l2/4,l1+b1/4),p3d.Vec3(lbc,lbk*3/8+l2/4,l1+b1/4),pdlr,pdlr).color(210/255,180/255,140/255,1)
    bpdl=p3d.Cone(p3d.Vec3(0,lbk/4+l2/4,l1+b1/2),p3d.Vec3(lbc,lbk/4+l2/4,l1+b1/2),pdlr,pdlr).color(210/255,180/255,140/255,1)
    cpdl=p3d.Cone(p3d.Vec3(0,lbk/8-l2/4,l1+b1*3/4),p3d.Vec3(lbc,lbk/8-l2/4,l1+b1*3/4),pdlr,pdlr).color(210/255,180/255,140/255,1)
    aapdl=p3d.Cone(p3d.Vec3(0,-lbk*3/8,l1+b1/4),p3d.Vec3(lbc,-lbk*3/8,l1+b1/4),pdlr,pdlr).color(210/255,180/255,140/255,1)
    bbpdl=p3d.Cone(p3d.Vec3(0,-lbk/4,l1+b1/2),p3d.Vec3(lbc,-lbk/4,l1+b1/2),pdlr,pdlr).color(210/255,180/255,140/255,1)
    ccpdl=p3d.Cone(p3d.Vec3(0,-lbk/8,l1+b1*3/4),p3d.Vec3(lbc,-lbk/8,l1+b1*3/4),pdlr,pdlr).color(210/255,180/255,140/255,1)
    pdl=p3d.combine(apdl,bpdl,cpdl,aapdl,bbpdl,ccpdl)

#斜柱
    xz1=p3d.Box(p3d.Vec3(0,lbk/6,0),p3d.Vec3(0,lbk/2,cl1+800),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),50,50,50,50).color(192/255,192/255,192/255,1)
    xz11=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(lbc,0,0),2)
    r1=p3d.combine()
    for point in xz11:
        r1.append(p3d.translation(point) * xz1)
    xz2=p3d.Box(p3d.Vec3(0,-lbk/6-50,0),p3d.Vec3(0,-lbk/2-50,cl1+800),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),50,50,50,50).color(192/255,192/255,192/255,1)
    xz21=p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(lbc,0,0),2)
    r2=p3d.combine()
    for point in xz21:
        r2.append(p3d.translation(point) * xz2)
    xz=p3d.combine(r1,r2)

#构件名
    if lbh == 0:
       A1= p3d.combine(lz,ql,zcl,pd,pdl,pdxl,rebars3,xl,xz) 
    else:
        A1= p3d.combine(lz,ql,zcl,pd,lb,pdl,pdxl,rebars3,xl,xz)
    A1=p3d.translation(p3d.Vec3(-(lbc+l2)/2,0,0))*A1
    A1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*A1
    data['加工棚']=p3d.combine(A1)

if __name__ == "__main__":
    data=p3d.P3DData({
        '立柱粗':100,
        '立柱数':4,
        '圈梁支撑立柱高':3000,
        '圈梁支撑立柱粗':100,
        '圈梁粗':80,
        '支撑梁粗':80,
        '竖直支撑梁长':2000,
        '斜支撑梁长':1600,
        '楼板长':16000,
        '楼板宽':9000,
        '楼板厚':0,
        '棚顶厚':60,
        '棚顶梁半径':25,
        '棚顶斜梁数':7,
        '棚顶高':1000,
        '旋转角度':0,
        '斜柱边长':50,
        '场布分类':'材料堆场',
        '构件类型':'土建',
        '构件名称':'加工棚',
        })
    
#data
    data.setup('加工棚',show=True)
    data.setup('立柱高' , obvious = True ,readonly=True,group='顶棚参数' , description ='棚高')
    data.setup('立柱粗' , obvious = True ,group='立柱参数' , description ='立柱边长')
    data.setup('圈梁支撑立柱高' , obvious = True ,group='棚顶参数' , description ='棚高')
    data.setup('圈梁支撑立柱粗' , obvious = False ,group='立柱参数' , description ='圈梁支撑立柱粗')
    data.setup('立柱数' , obvious = True ,group='立柱参数' , description ='立柱数')
    data.setup('圈梁粗' , obvious = True ,group='梁参数' , description ='圈梁边长')
    data.setup('支撑梁粗' , obvious = True ,group='梁参数' , description ='支撑梁边长')
    data.setup('竖直支撑梁长' , obvious = True ,group='顶棚参数' , description ='棚顶高')
    data.setup('斜支撑梁长' , obvious = False ,readonly=True,group='梁参数' , description ='斜支撑梁长')
    data.setup('楼板长' , obvious = True ,group='楼板参数' , description ='楼板长')
    data.setup('楼板宽' , obvious = True ,group='楼板参数' , description ='楼板宽')
    data.setup('楼板厚' , obvious = True ,group='楼板参数' , description ='楼板厚')
    data.setup('棚顶厚' , obvious = True ,group='棚顶参数' , description ='棚顶厚')
    data.setup('棚顶梁半径' , obvious = True ,group='棚顶参数' , description ='棚顶梁半径')
    data.setup('棚顶斜梁数' , obvious = True ,group='棚顶参数' , description ='棚顶斜梁数')
    data.setup('棚顶高' , obvious = False ,group='棚顶参数' , description ='棚顶高')
    data.setup('旋转角度',obvious=True,group='旋转',description='旋转角度')
    data.setup('斜柱边长',obvious=True,readonly=True,group='立柱参数',description='斜柱边长')
    data.setup('场布分类', obvious=True,readonly=True,group='公共属性', description='场部分类') 
    data.setup('构件类型', obvious=True,readonly=True,group='公共属性', description='构件类型') 
    data.setup('构件名称',obvious=True)
    data['replace'] = kcpj
    kcpj(data)
    p3d.launchData(data)