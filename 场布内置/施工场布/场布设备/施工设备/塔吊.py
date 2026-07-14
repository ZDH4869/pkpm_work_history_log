import pyp3d as p3d
import math
def tadiao(data:p3d.P3DData)->None:
    n=data['塔身单元节个数']#单元节个数
    data['高度']=n*2000
    x=data['吊臂单元节个数']
    k=data['吊臂旋转角度']
    if data['延伸距离'] >3550+n*2000+30-3000: 
       data['延伸距离'] = 3550+n*2000+30-3000
    if data['平移距离'] >(x-1)*1500: 
       data['平移距离'] =(x-1)*1500
    if data['平移距离'] <1000: 
       data['平移距离'] = 1000
#文档 李可涵
#精神支柱 王科
#底座 崔迅
    Box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,500), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),4000,4000,4000,4000).color(210/255,180/255,140/255,1)
    #地面柱子
    Cone1 = p3d.Cone(p3d.Vec3(1000,1000,530),p3d.Vec3(3000,1000,530),30,30).color(139/255,69/255,19/255,1)
    Cone2 = p3d.Cone(p3d.Vec3(1000,3000,530),p3d.Vec3(3000,3000,530),30,30).color(139/255,69/255,19/255,1)
    Cone3 = p3d.Cone(p3d.Vec3(1000,1000,530),p3d.Vec3(1000,3000,530),30,30).color(139/255,69/255,19/255,1)
    Cone4 = p3d.Cone(p3d.Vec3(3000,1000,530),p3d.Vec3(3000,3000,530),30,30).color(139/255,69/255,19/255,1)

    Cone5 = p3d.Cone(p3d.Vec3(1000,1000,560),p3d.Vec3(1000,1000,2560),30,30).color(139/255,69/255,19/255,1)
    Cone6 = p3d.Cone(p3d.Vec3(3000,1000,560),p3d.Vec3(3000,1000,2560),30,30).color(139/255,69/255,19/255,1)
    Cone7 = p3d.Cone(p3d.Vec3(3000,3000,560),p3d.Vec3(3000,3000,2560),30,30).color(139/255,69/255,19/255,1)
    Cone8 = p3d.Cone(p3d.Vec3(1000,3000,560),p3d.Vec3(1000,3000,2560),30,30).color(139/255,69/255,19/255,1)

    Cone9 = p3d.Cone(p3d.Vec3(1000,1000,2530),p3d.Vec3(3000,1000,2530),30,30).color(139/255,69/255,19/255,1)
    Cone10 = p3d.Cone(p3d.Vec3(1000,3000,2530),p3d.Vec3(3000,3000,2530),30,30).color(139/255,69/255,19/255,1)
    Cone11 = p3d.Cone(p3d.Vec3(1000,1000,2530),p3d.Vec3(1000,3000,2530),30,30).color(139/255,69/255,19/255,1)
    Cone12= p3d.Cone(p3d.Vec3(3000,1000,2530),p3d.Vec3(3000,3000,2530),30,30).color(139/255,69/255,19/255,1)

    Cone13 = p3d.Cone(p3d.Vec3(1000,1000,530),p3d.Vec3(3000,1000,2530),30,30).color(139/255,69/255,19/255,1)
    Cone14 = p3d.Cone(p3d.Vec3(1000,3000,530),p3d.Vec3(1000,1000,2530),30,30).color(139/255,69/255,19/255,1)
    Cone15 = p3d.Cone(p3d.Vec3(3000,3000,530),p3d.Vec3(1000,3000,2530),30,30).color(139/255,69/255,19/255,1)
    Cone16 = p3d.Cone(p3d.Vec3(3000,1000,530),p3d.Vec3(3000,3000,2530),30,30).color(139/255,69/255,19/255,1)
    AA=p3d.combine(Cone5,Cone6,Cone7,Cone8,Cone9,Cone10,Cone11,Cone12,Cone13,Cone14,Cone15,Cone16)
    td = p3d.combine()
    for i in range(n):
        td.append(p3d.translation(p3d.Vec3(0,0,2000*i))*AA)
    Box2=p3d.Box(p3d.Vec3(0,0,(n-3)*2000),p3d.Vec3(0,0,((n-3)*2000)+50), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),4000,4000,4000,4000).color(1,1,1,1)
    Box3=p3d.Box(p3d.Vec3(1000,1000,(n-3)*2000),p3d.Vec3(1000,1000,((n-3)*2000)+50), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),2000,2000,2000,2000).color(1,1,1,1)
    BB = p3d.substract(Box2,Box3).color(1,1,1,1)
    #围栏
    Cone17 = p3d.Cone(p3d.Vec3(30,30,(n-3)*2000),p3d.Vec3(30,30,((n-3)*2000)+1000),30,30).color(1,1,1,1)
    langan1 = p3d.combine()
    Number = 4
    for i in range(Number):
       langan1.append(p3d.translation(p3d.Vec3(1000*i,0,0))*Cone17)
    langan4 = p3d.combine()
    Number = 4
    for i in range(Number):
       langan4.append(p3d.translation(p3d.Vec3(0,1000*i,0))*Cone17)
    Cone18 = p3d.Cone(p3d.Vec3(3970,30,(n-3)*2000),p3d.Vec3(3970,30,((n-3)*2000)+1000),30,30).color(1,1,1,1)
    langan2 = p3d.combine()
    Number = 4
    for i in range(Number):
       langan2.append(p3d.translation(p3d.Vec3(0,1000*i,0))*Cone18)
    Cone19 = p3d.Cone(p3d.Vec3(30,3970,(n-3)*2000),p3d.Vec3(30,3970,((n-3)*2000)+1000),30,30).color(1,1,1,1)
    langan3 = p3d.combine()
    Number = 5
    for i in range(Number):
       langan3.append(p3d.translation(p3d.Vec3(1000*i,0,0))*Cone19)
    Cone20 = p3d.Cone(p3d.Vec3(30,30,((n-3)*2000)+800),p3d.Vec3(30,3970,((n-3)*2000)+800),30,30).color(1,1,1,1)
    Cone21 = p3d.Cone(p3d.Vec3(3970,30,((n-3)*2000)+800),p3d.Vec3(3970,3970,((n-3)*2000)+800),30,30).color(1,1,1,1)
    Cone22 = p3d.Cone(p3d.Vec3(3972,3970,((n-3)*2000)+800),p3d.Vec3(30,3970,((n-3)*2000)+800),30,30).color(1,1,1,1)
    Cone23 = p3d.Cone(p3d.Vec3(30,30,((n-3)*2000)+800),p3d.Vec3(3970,30,((n-3)*2000)+800),30,30).color(1,1,1,1)

    B2=p3d.combine(Cone20,Cone21,Cone22,Cone23,langan1,langan2,langan3,langan4,BB)
    B3= p3d.translation(p3d.Vec3(0,0,2000))*B2
    likehancuixun=p3d.combine(Cone1,Cone2,Cone3,Cone4,Box1,td,B3,B2)
#吊臂 陈梦菲
    db1=p3d.Cone(p3d.Vec3(0,1500,0),p3d.Vec3(750,0,0),30,30).color(139/255,69/255,19/255,1)
    db2=p3d.Cone(p3d.Vec3(1500,1500,0),p3d.Vec3(750,0,0),30,30).color(139/255,69/255,19/255,1)
    db3=p3d.Cone(p3d.Vec3(0,1500,0),p3d.Vec3(750,750,1500),30,30).color(139/255,69/255,19/255,1)
    db4=p3d.Cone(p3d.Vec3(1500,1500,0),p3d.Vec3(750,750,1500),30,30).color(139/255,69/255,19/255,1)
    db5=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(750,750,1500),30,30).color(139/255,69/255,19/255,1)
    db6=p3d.Cone(p3d.Vec3(1500,0,0),p3d.Vec3(750,750,1500),30,30).color(139/255,69/255,19/255,1)
    
    
    db=p3d.combine(db1,db2,db3,db4,db5,db6)
    p1 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((x-1)*1500,0,0),x)
    rebars2 = p3d.combine()
    for point in p1:
        rebars2.append(p3d.translation(point) * db)
    db11=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(x*1500,0,0),30,30).color(139/255,69/255,19/255,1)
    db12=p3d.Cone(p3d.Vec3(0,1500,0),p3d.Vec3(x*1500,1500,0),30,30).color(139/255,69/255,19/255,1)
    db13=p3d.Cone(p3d.Vec3(750,750,1500),p3d.Vec3((x*1500)-750,750,1500),30,30).color(139/255,69/255,19/255,1)
    db14=p3d.Cone(p3d.Vec3(x*1500,0,0),p3d.Vec3(x*1500,1500,0),30,30).color(139/255,69/255,19/255,1)
#塔尖 陈梦菲
    tj1=p3d.Cone(p3d.Vec3(0,750,0),p3d.Vec3(0,750,4500),30,30).color(139/255,69/255,19/255,1)
    tj2=p3d.Cone(p3d.Vec3(-1500,1500,0),p3d.Vec3(0,750,4500),30,30).color(139/255,69/255,19/255,1)
    tj3=p3d.Cone(p3d.Vec3(-1500,0,0),p3d.Vec3(0,750,4500),30,30).color(139/255,69/255,19/255,1)
    tj4=p3d.Cone(p3d.Vec3(-1500,0,0),p3d.Vec3(0,750,1000),30,30).color(139/255,69/255,19/255,1)
    tj5=p3d.Cone(p3d.Vec3(-1500,1500,0),p3d.Vec3(0,750,1000),30,30).color(139/255,69/255,19/255,1)
    tj6=p3d.Cone(p3d.Vec3(-900,300,1800),p3d.Vec3(0,750,1000),30,30).color(139/255,69/255,19/255,1)
    tj7=p3d.Cone(p3d.Vec3(-900,1200,1800),p3d.Vec3(0,750,1000),30,30).color(139/255,69/255,19/255,1)
    tj8=p3d.Cone(p3d.Vec3(-900,300,1800),p3d.Vec3(0,750,2700),30,30).color(139/255,69/255,19/255,1)
    tj9=p3d.Cone(p3d.Vec3(-900,1200,1800),p3d.Vec3(0,750,2700),30,30).color(139/255,69/255,19/255,1)
    tj10=p3d.Cone(p3d.Vec3(-(1300/3),535,3200),p3d.Vec3(0,750,2700),30,30).color(139/255,69/255,19/255,1)
    tj11=p3d.Cone(p3d.Vec3(-(1300/3),966,3200),p3d.Vec3(0,750,2700),30,30).color(139/255,69/255,19/255,1)
    tj12=p3d.Cone(p3d.Vec3(-(1300/3),535,3200),p3d.Vec3(0,750,3700),30,30).color(139/255,69/255,19/255,1)
    tj13=p3d.Cone(p3d.Vec3(-(1300/3),966,3200),p3d.Vec3(0,750,3700),30,30).color(139/255,69/255,19/255,1)
    tj14=p3d.Cone(p3d.Vec3(-1500,0,0),p3d.Vec3(-900,1200,1800),30,30).color(139/255,69/255,19/255,1)
    tj15=p3d.Cone(p3d.Vec3(-(1300/3),535,3200),p3d.Vec3(-900,1200,1800),30,30).color(139/255,69/255,19/255,1)
    tj16=p3d.Cone(p3d.Vec3(-900,300,1800),p3d.Vec3(-900,1200,1800),30,30).color(139/255,69/255,19/255,1)
    tj17=p3d.Cone(p3d.Vec3(-(1300/3),535,3200),p3d.Vec3(-(1300/3),966,3200),30,30).color(139/255,69/255,19/255,1)
    tj18=p3d.Cone(p3d.Vec3(0,750,4500),p3d.Vec3((x*1500/3),750,1500),30,30).color(1,1,1,1)
    tj19=p3d.Cone(p3d.Vec3(0,750,4500),p3d.Vec3((x*1500*3/4),750,1500),30,30).color(1,1,1,1)
    tj20=p3d.Cone(p3d.Vec3(0,750,4500),p3d.Vec3(-6000,1200,0),30,30).color(1,1,1,1)
    tj21=p3d.Cone(p3d.Vec3(0,750,4500),p3d.Vec3(-6000,300,0),30,30).color(1,1,1,1)
   
    

    AA22=p3d.combine(rebars2,db11,db12,db13,db14,tj1,tj2,tj3,tj4,tj5,tj6,tj7,tj8,tj9,tj10,tj11,tj12,tj13,tj14,tj15,tj16,tj17,tj18,tj19,tj20,tj21)
    
    chenmengfei= p3d.translation(p3d.Vec3(2750,1250,3550+n*2000+30))*AA22
# 吊钩 王科
    Boxjyj=p3d.Box(p3d.Vec3(0,0,-200),p3d.Vec3(0,0,-400),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),1500,1500,1500,1500).color(139/255,69/255,19/255,1)
    jyjlz1=p3d.Cone(p3d.Vec3(200,0,-200),p3d.Vec3(200,100,-200),200,200).color(139/255,69/255,19/255,1)
    jyjlz2=p3d.Cone(p3d.Vec3(1300,0,-200),p3d.Vec3(1300,100,-200),200,200).color(139/255,69/255,19/255,1)
    jyjlz3=p3d.Cone(p3d.Vec3(200,1400,-200),p3d.Vec3(200,1500,-200),200,200).color(139/255,69/255,19/255,1)
    jyjlz4=p3d.Cone(p3d.Vec3(1300,1400,-200),p3d.Vec3(1300,1500,-200),200,200).color(139/255,69/255,19/255,1)
    Boxjyjmd=p3d.Box(p3d.Vec3(400,400,-100),p3d.Vec3(400,400,-500),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),700,700,700,700).color(139/255,69/255,19/255,1)
    gsz=p3d.Cone(p3d.Vec3(500,750,-500),p3d.Vec3(500,750,-500-data['延伸距离']),10,10).color(139/255,69/255,19/255,1)
    gsy=p3d.Cone(p3d.Vec3(1000,750,-500),p3d.Vec3(1000,750,-500-data['延伸距离']),10,10).color(139/255,69/255,19/255,1)
    gzgz=p3d.Box(p3d.Vec3(400,650,-500-data['延伸距离']-100),p3d.Vec3(750,650,-500-data['延伸距离']-400),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),700,200,0,200).color(139/255,69/255,19/255,1)
    gzlzz=p3d.Cone(p3d.Vec3(500,700,-500-data['延伸距离']-100),p3d.Vec3(500,800,-500-data['延伸距离']-100),100,100).color(139/255,69/255,19/255,1)
    gzlzy=p3d.Cone(p3d.Vec3(1000,700,-500-data['延伸距离']-100),p3d.Vec3(1000,800,-500-data['延伸距离']-100),100,100).color(139/255,69/255,19/255,1)
    gz111=p3d.Cone(p3d.Vec3(750,750,-500-data['延伸距离']-400+100),p3d.Vec3(750,750,-500-data['延伸距离']-400-80),30,30).color(139/255,69/255,19/255,1)
    gz=p3d.RotationalSweep([p3d.Vec3(750,790,-500-data['延伸距离']-400-80+50),p3d.Vec3(750,710,-500-data['延伸距离']-400-80+50),p3d.Vec3(750,725,-500-data['延伸距离']-400-80+50-50),p3d.Vec3(750,775,-500-data['延伸距离']-400-80+50-50)],p3d.Vec3(750,750,-500-data['延伸距离']-400-80-150),p3d.Vec3(0,1,0),1.5*p3d.pi).color(139/255,69/255,19/255,1)
    dlss1=p3d.Cone(p3d.Vec3(750,750,-500-data['延伸距离']-400-80-100),p3d.Vec3(250,250,-500-data['延伸距离']-400-80-1000),5,5).color(139/255,69/255,19/255,1)
    dlss2=p3d.Cone(p3d.Vec3(750,750,-500-data['延伸距离']-400-80-100),p3d.Vec3(1250,250,-500-data['延伸距离']-400-80-1000),5,5).color(139/255,69/255,19/255,1)
    dlss3=p3d.Cone(p3d.Vec3(750,750,-500-data['延伸距离']-400-80-100),p3d.Vec3(250,1250,-500-data['延伸距离']-400-80-1000),5,5).color(139/255,69/255,19/255,1)
    dlss4=p3d.Cone(p3d.Vec3(750,750,-500-data['延伸距离']-400-80-100),p3d.Vec3(1250,1250,-500-data['延伸距离']-400-80-1000),5,5).color(139/255,69/255,19/255,1)
    dl1=p3d.Box(p3d.Vec3(250,250,-500-data['延伸距离']-400-80-1000),p3d.Vec3(250,250,-500-data['延伸距离']-400-80-1000-800),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),1000,1000,1000,1000).color(139/255,69/255,19/255,1)
    dl2=p3d.Box(p3d.Vec3(300,300,-500-data['延伸距离']-400-80-1000),p3d.Vec3(300,300,-500-data['延伸距离']-400-80-1000-750),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),900,900,900,900).color(139/255,69/255,19/255,1)
    dl=p3d.substract(dl1,dl2).color(139/255,69/255,19/255,1)
    JYJ=p3d.combine(Boxjyj,jyjlz3,jyjlz4,jyjlz1,jyjlz2, Boxjyjmd,gsz,gsy,gzgz,gzlzz,gzlzy,gz111,gz,dl,dlss1,dlss2,dlss3,dlss4)
    JYJ=p3d.translation(p3d.Vec3(data['平移距离'],0,0))*JYJ
    
    wangke=p3d.translation(p3d.Vec3(2750,1250,3550+n*2000+30))*JYJ
     



#驾驶室平台 何雨洋
    boxa=p3d.Box(p3d.Vec3(500,500,n*2000+30+500),p3d.Vec3(500,500,n*2000+30+500+50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),3000,3000,3000,3000).color(231/255,101/255,26/255,1)
#驾驶室 何雨洋
    boxb=p3d.Box(p3d.Vec3(2900,2900,n*2000+30+500+50),p3d.Vec3(2900,2900,n*2000+30+500+50+2000),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),1000,1000,1000,1000).color(231/255,101/255,26/255,1)
    #驾驶室栏杆    
    conea=p3d.Cone(p3d.Vec3(3500,500,n*2000+30+500+50),p3d.Vec3(3500,500,n*2000+30+500+50+600),20,20).color(139/255,69/255,19/255,1)
    coneb=p3d.Cone(p3d.Vec3(3500,500,n*2000+30+500+50+600),p3d.Vec3(3500,3400,n*2000+30+500+50+600),20,20).color(139/255,69/255,19/255,1)
    conec=p3d.Cone(p3d.Vec3(500,500,n*2000+30+500+50),p3d.Vec3(500,500,n*2000+30+500+50+600),20,20).color(139/255,69/255,19/255,1)
    coned=p3d.Cone(p3d.Vec3(500,500,n*2000+30+500+50+600),p3d.Vec3(3500,500,n*2000+30+500+50+600),20,20).color(139/255,69/255,19/255,1)
    conee=p3d.Cone(p3d.Vec3(3500,500,n*2000+30+500+50+300),p3d.Vec3(3500,3400,n*2000+30+500+50+300),20,20).color(139/255,69/255,19/255,1)
    conef=p3d.Cone(p3d.Vec3(500,500,n*2000+30+500+50+300),p3d.Vec3(3500,500,n*2000+30+500+50+300),20,20).color(139/255,69/255,19/255,1)
    coneg=p3d.Cone(p3d.Vec3(500,500,n*2000+30+500+50+600),p3d.Vec3(500,3500,n*2000+30+500+50+600),20,20).color(139/255,69/255,19/255,1)
    coneh=p3d.Cone(p3d.Vec3(500,3500,n*2000+30+500+50+600),p3d.Vec3(3400,3500,n*2000+30+500+50+600),20,20).color(139/255,69/255,19/255,1)
    conei=p3d.translation(p3d.Vec3(0,3000,0))*conec
    conej=p3d.translation(p3d.Vec3(0,0,-300))*coneg
    conek=p3d.Cone(p3d.Vec3(500,3500,n*2000+30+500+50+300),p3d.Vec3(3500,3500,n*2000+30+500+50+300),20,20).color(139/255,69/255,19/255,1)
    conel=p3d.translation(p3d.Vec3(0,800,0))*conea
    conem=p3d.translation(p3d.Vec3(0,1600,0))*conea
    conen=p3d.translation(p3d.Vec3(750,0,0))*conec
    coneo=p3d.translation(p3d.Vec3(1500,0,0))*conec
    conep=p3d.translation(p3d.Vec3(2250,0,0))*conec
    coneq=p3d.translation(p3d.Vec3(0,750,0))*conec
    coner=p3d.translation(p3d.Vec3(0,1500,0))*conec
    cones=p3d.translation(p3d.Vec3(0,2250,0))*conec
    conet=p3d.translation(p3d.Vec3(800,0,0))*conei
    coneu=p3d.translation(p3d.Vec3(1600,0,0))*conei
    #中间柱
    coneaa=p3d.Cone(p3d.Vec3(2750,1250,n*2000+30+500+50),p3d.Vec3(2750,1250,n*2000+30+500+50+3000),20,20).color(139/255,69/255,19/255,1)
    conebb=p3d.translation(p3d.Vec3(0,1500,0))*coneaa
    conecc=p3d.translation(p3d.Vec3(-1500,0,0))*conebb
    conedd=p3d.translation(p3d.Vec3(-1500,0,0))*coneaa
    coneee=p3d.Cone(p3d.Vec3(1250,2750,n*2000+30+500+50+1500),p3d.Vec3(2750,2750,n*2000+30+500+50+1500),20,20).color(139/255,69/255,19/255,1)
    coneff=p3d.translation(p3d.Vec3(0,-1500,0))*coneee
    conegg=p3d.Cone(p3d.Vec3(1250,2750,n*2000+30+500+50+1500),p3d.Vec3(1250,1250,n*2000+30+500+50+1500),20,20).color(139/255,69/255,19/255,1)
    conehh=p3d.translation(p3d.Vec3(1500,0,0))*conegg
    conemm=p3d.translation(p3d.Vec3(0,0,1500))*coneff
    conenn=p3d.translation(p3d.Vec3(0,0,1500))*conehh
    coneoo=p3d.translation(p3d.Vec3(0,0,1500))*coneee
    conepp=p3d.translation(p3d.Vec3(0,0,1500))*conegg
    #斜杆
    coneaa1=p3d.Cone(p3d.Vec3(1250,1250,n*2000+30+500+50),p3d.Vec3(2750,1250,n*2000+30+500+50+1500),20,20).color(139/255,69/255,19/255,1)
    coneaa2=p3d.Cone(p3d.Vec3(2750,1250,n*2000+30+500+50+1500),p3d.Vec3(1250,1250,n*2000+30+500+50+3000),20,20).color(139/255,69/255,19/255,1)
    coneaa3=p3d.Cone(p3d.Vec3(1250,2750,n*2000+30+500+50),p3d.Vec3(1250,1250,n*2000+30+500+50+1500),20,20).color(139/255,69/255,19/255,1)
    coneaa4=p3d.Cone(p3d.Vec3(1250,1250,n*2000+30+500+50+1500),p3d.Vec3(1250,2750,n*2000+30+500+50+3000),20,20).color(139/255,69/255,19/255,1)
    coneaa5=p3d.Cone(p3d.Vec3(1250,2750,n*2000+30+500+50+1500),p3d.Vec3(2750,2750,n*2000+30+500+50),20,20).color(139/255,69/255,19/255,1)
    coneaa6=p3d.Cone(p3d.Vec3(1250,2750,n*2000+30+500+50+1500),p3d.Vec3(2750,2750,n*2000+30+500+50+3000),20,20).color(139/255,69/255,19/255,1)
    coneaa7=p3d.Cone(p3d.Vec3(2750,2750,n*2000+30+500+50+3000),p3d.Vec3(2750,1250,n*2000+30+500+50+1500),20,20).color(139/255,69/255,19/255,1)
    coneaa8=p3d.Cone(p3d.Vec3(2750,1250,n*2000+30+500+50+1500),p3d.Vec3(2750,2750,n*2000+30+500+50),20,20).color(139/255,69/255,19/255,1)
    heyuyang=p3d.combine(boxa,boxb,conea,coneb,conec,coned,conee,conef,coneg,coneh,conei,conej,conek,conel,conem,conen,coneo,conep,coneq,coner,cones,conet,coneu,coneaa,conebb,conecc,conedd,coneee,coneff,conegg,conehh,conemm,conenn,coneoo,conepp,coneaa1,coneaa2,coneaa3,coneaa4,coneaa5,coneaa6,coneaa7,coneaa8)
#配重 王嵩霖
    PHBD1 = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,10),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),6000,1500,6000,1500).color(1,1,1,1)
    PHBD2 = p3d.Box(p3d.Vec3(-6000,-500,0),p3d.Vec3(-6000,-500,10),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),4000,2500,4000,2500).color(1,1,1,1)
    PHBD = p3d.unite(PHBD1,PHBD2).color(139/255,69/255,19/255,1)
    PHBFS1 = p3d.Box(p3d.Vec3(0,0,10),p3d.Vec3(0,0,1480),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),30,30,30,30).color(139/255,69/255,19/255,1)
    PHBFS2 = p3d.translation(p3d.Vec3(0,1470,0))*PHBFS1
    PHBFS3 = p3d.translation(p3d.Vec3(-6000,-500,0))*PHBFS1
    PHBFS4 = p3d.translation(p3d.Vec3(-6000,1970,0))*PHBFS1
    PHBFS5 = p3d.translation(p3d.Vec3(-9970,-500,0))*PHBFS1
    PHBFS6 = p3d.translation(p3d.Vec3(-9970,1970,0))*PHBFS1
    PHBFS7 = p3d.translation(p3d.Vec3(-9970,-253,0))*PHBFS1
    PHBFSS1 = p3d.combine()
    Number = 21
    for i in range(Number):
        PHBFSS1.append(p3d.translation(p3d.Vec3(-597/2*i,0,0))*PHBFS1)
    PHBFSS2 = p3d.combine()
    Number = 21
    for i in range(Number):
        PHBFSS2.append(p3d.translation(p3d.Vec3(-597/2*i,0,0))*PHBFS2)
    PHBFSS3 = p3d.combine()
    Number = 2
    for i in range(Number):
        PHBFSS3.append(p3d.translation(p3d.Vec3(0,235*i,0))*PHBFS3)
    PHBFSS4 = p3d.combine()
    Number = 2
    for i in range(Number):
        PHBFSS4.append(p3d.translation(p3d.Vec3(0,-235*i,0))*PHBFS4)
    PHBFSS5 = p3d.combine()
    Number = 20
    for i in range(Number):
        PHBFSS5.append(p3d.translation(p3d.Vec3(198.5*i,0,0))*PHBFS5)
    PHBFSS6 = p3d.combine()
    Number = 20
    for i in range(Number):
        PHBFSS6.append(p3d.translation(p3d.Vec3(198.5*i,0,0))*PHBFS6)
    PHBFSS7 = p3d.combine()
    Number = 9
    for i in range(Number):
        PHBFSS7.append(p3d.translation(p3d.Vec3(0,247*i,0))*PHBFS7)
    PHBFSS= p3d.combine(PHBFSS1,PHBFSS2,PHBFSS3,PHBFSS4,PHBFSS5,PHBFSS6,PHBFSS7)
    #扶手
    PHBFSFS1 = p3d.Box(p3d.Vec3(0,0,1480),p3d.Vec3(0,0,1510),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),6030,30,6030,30).color(1,1,1,1)
    PHBFSFS2 = p3d.translation(p3d.Vec3(0,1470,0))*PHBFSFS1
    PHBFSFS3 = p3d.Box(p3d.Vec3(-6000,-500,1480),p3d.Vec3(-6000,-500,1510),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),30,500,30,500).color(1,1,1,1)
    PHBFSFS4 = p3d.translation(p3d.Vec3(0,2000,0))*PHBFSFS3
    PHBFSFS5 = p3d.Box(p3d.Vec3(-6030,-500,1480),p3d.Vec3(-6030,-500,1510),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),3970,30,3970,30).color(1,1,1,1)
    PHBFSFS6 = p3d.translation(p3d.Vec3(0,2470,0))*PHBFSFS5
    PHBFSFS7 = p3d.Box(p3d.Vec3(-9970,-470,1480),p3d.Vec3(-9970,-500,1510),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),30,2440,30,2440).color(1,1,1,1)
    PHBFSFS = p3d.unite(PHBFSFS1,PHBFSFS2,PHBFSFS3,PHBFSFS4,PHBFSFS5,PHBFSFS6,PHBFSFS7).color(139/255,69/255,19/255,1)
    #配重
    PHBPZ = p3d.Box(p3d.Vec3(-6500,0,-1000),p3d.Vec3(-6500,0,1000),p3d.Vec3(-1,0,0), p3d.Vec3(0,1,0),3000,1500,3000,1500).color(1,1,1,1)


    WSL = p3d.combine(PHBD,PHBFSS,PHBFSFS,PHBPZ)
    WSL1=p3d.translation(p3d.Vec3(2750,1250,3550+n*2000+30))*WSL
#上半部
    
    Z=p3d.combine(chenmengfei,heyuyang,WSL1,wangke)
    Z1=p3d.translation(p3d.Vec3(-2000,-2000,0))*Z
    Z11=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*Z1
    Z111=p3d.translation(p3d.Vec3(2000,2000,0))*Z11
#构件名 

    data['塔吊'] = p3d.combine(likehancuixun,Z111)

if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'施工机械',
        '构件类型':'塔吊',
        '构件名称':'塔吊',
        '塔身单元节个数': 20,
        '吊臂单元节个数':35,
        '吊臂旋转角度':0,
        '延伸距离':1000,
        '平移距离':1000
         })
#data
    data.setup('塔吊',show = True)
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('塔身单元节个数' , obvious = True ,group='单元节个数' , description ='单元节个数')
    data.setup('吊臂单元节个数' , obvious = True ,group='单元节个数' , description ='吊臂单元节个数')
    data.setup('吊臂旋转角度',obvious = True ,group='旋转' , description ='吊臂旋转角度')
    data.setup('高度',obvious = True ,readonly=True,group='高度' , description ='高度')
    data.setup('延伸距离' , obvious = True ,group='塔吊吊钩' , description ='延申距离')
    data.setup('平移距离' , obvious = True ,group='塔吊吊钩' , description ='平移距离')
    data.setup('构件名称',obvious=True)
    data['replace'] = tadiao
    tadiao(data)
    p3d.launchData(data)