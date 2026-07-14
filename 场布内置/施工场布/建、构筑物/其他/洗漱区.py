import pyp3d as p3d
import math
def test_box(data:p3d.P3DData)->None:
    if data['池子高'] >data['棚顶高']-1000:
        data['池子高'] = data['棚顶高']-1000
    boxCz1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,(data['池子高']-400)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),40,40,40,40)
    boxCz2=p3d.translation(0,(data['池子长']-40),0)*boxCz1
    boxCz3=p3d.translation((data['池子宽']-40),0,0)*boxCz1
    boxCz4=p3d.translation((data['池子宽']-40),(data['池子长']-40),0)*boxCz1
    boxCl1=p3d.Box(p3d.Vec3(40,0,((data['池子高']-400)/2)-40),p3d.Vec3(40,0,((data['池子高']-400)/2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),(data['池子宽']-((40)*2)),40,(data['池子宽']-(40)*2),40)
    boxCl2=p3d.Box(p3d.Vec3(0,40,((data['池子高']-400)/2)-40),p3d.Vec3(0,40,((data['池子高']-400)/2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),40,(data['池子长']-((40)*2)),40,(data['池子长']-((40)*2)))
    boxCl3=p3d.translation((data['池子宽']-40),0,0)*boxCl2
    boxCl4=p3d.translation(0,(data['池子长']-40),0)*boxCl1
    boxCb1=p3d.Box(p3d.Vec3(0,0,(data['池子高']-400)),p3d.Vec3(0,0,data['池子高']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['池子宽'],data['池子长'],data['池子宽'],data['池子长'])
    boxCb2=p3d.Box(p3d.Vec3(40,40,(data['池子高']-400)+50),p3d.Vec3(40,40,data['池子高']+50),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),(data['池子宽']-((40)*2)),(data['池子长']-((40)*2)),(data['池子宽']-((40)*2)),(data['池子长']-((40)*2)))
    boxCb12=p3d.substract(boxCb1,boxCb2)
    boxSt=p3d.Box(p3d.Vec3(data['池子宽'],0,data['池子高']-40),p3d.Vec3(data['池子宽'],0,data['池子高']+460),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),320,data['池子长'],320,data['池子长'])
    boxC=p3d.combine(boxCz1,boxCz2,boxCz3,boxCz4,boxCl1,boxCl2,boxCl3,boxCl4,boxCb12).color(192/255,192/255,192/255,1)
    boxCz11=p3d.Box(p3d.Vec3(data['池子宽']+320,0,0),p3d.Vec3(data['池子宽']+320,0,(data['池子高']-400)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),40,40,40,40)
    boxCz22=p3d.translation(0,(data['池子长']-40),0)*boxCz11
    boxCz33=p3d.translation((data['池子宽']-40),0,0)*boxCz11
    boxCz44=p3d.translation((data['池子宽']-40),(data['池子长']-40),0)*boxCz11
    boxCl11=p3d.Box(p3d.Vec3(data['池子宽']+320,40,((data['池子高']-400)/2)-40),p3d.Vec3(data['池子宽']+320,40,((data['池子高']-400)/2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),40,(data['池子长']-((40)*2)),40,(data['池子长']-(40)*2))
    boxCl22=p3d.Box(p3d.Vec3(40+data['池子宽']+320,0,((data['池子高']-400)/2)-40),p3d.Vec3(40+data['池子宽']+320,0,((data['池子高']-400)/2)),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),(data['池子宽']-((40)*2)),40,(data['池子宽']-((40)*2)),40)
    boxCl33=p3d.translation(0,(data['池子长']-40),0)*boxCl22
    boxCl44=p3d.translation((data['池子宽']-40),0,0)*boxCl11
    boxCb11=p3d.Box(p3d.Vec3(data['池子宽']+320,0,(data['池子高']-400)),p3d.Vec3(data['池子宽']+320,0,data['池子高']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['池子宽'],data['池子长'],data['池子宽'],data['池子长'])
    boxCb22=p3d.Box(p3d.Vec3(data['池子宽']+320+40,40,(data['池子高']-400)+50),p3d.Vec3(40+data['池子宽']+320,40,data['池子高']+50),p3d.Vec3(0,1,0),p3d.Vec3(1,0,0),(data['池子长']-((40)*2)),(data['池子宽']-((40)*2)),(data['池子长']-((40)*2)),(data['池子宽']-((40)*2)))
    boxCb1122=p3d.substract(boxCb11,boxCb22)
    boxCC=p3d.combine(boxCz11,boxCz22,boxCz33,boxCz44,boxCl11,boxCl22,boxCl33,boxCl44,boxCb1122).color(192/255,192/255,192/255,1)
    

    #水龙头
    F1 = p3d.FilletPipe([p3d.Vec3(data['池子宽'],data['池子长']/2,data['池子高']+200),p3d.Vec3((2*data['池子宽']/3),data['池子长']/2,data['池子高']+200),p3d.Vec3((2*data['池子宽']/3),data['池子长']/2,data['池子高']+150)],[0,30,0],10).color(192/255,192/255,192/255,1)  
    Cone1 = p3d.Cone(p3d.Vec3(data['池子宽']-40-10,data['池子长']/2,data['池子高']+200),p3d.Vec3(data['池子宽']-40-10,data['池子长']/2,data['池子高']+235),5,5).color(192/255,192/255,192/255,1)    
    Box111=p3d.Box(p3d.Vec3((data['池子宽'])-40-5,data['池子长']/2+5,data['池子高']+230),p3d.Vec3((data['池子宽'])-40-5,data['池子长']/2+5,data['池子高']+235),p3d.Vec3(-1,0,0),p3d.Vec3(0,-1,0),80,10,80,10).color(192/255,192/255,192/255,1)  
    F2= p3d.FilletPipe([p3d.Vec3(data['池子宽']+320,data['池子长']/2,data['池子高']+200),p3d.Vec3((4*data['池子宽']/3)+320,data['池子长']/2,data['池子高']+200),p3d.Vec3((4*data['池子宽']/3)+320,data['池子长']/2,data['池子高']+150)],[0,30,0],10).color(192/255,192/255,192/255,1)
    Cone2= p3d.Cone(p3d.Vec3(data['池子宽']+320+40+10,data['池子长']/2,data['池子高']+200),p3d.Vec3((data['池子宽'])+320+40+10,data['池子长']/2,data['池子高']+235),5,5).color(192/255,192/255,192/255,1)
    Box222=p3d.Box(p3d.Vec3((data['池子宽'])+320+40+5,data['池子长']/2+5,data['池子高']+230),p3d.Vec3((data['池子宽'])+320+40+5,data['池子长']/2+5,data['池子高']+235),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),80,10,80,10).color(192/255,192/255,192/255,1)    
    GGG=p3d.combine(F1,boxC,boxCC,boxSt,Cone1,Box111,F2,Cone2,Box222)
    GGG=p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi* 0.5)*GGG 
    cz = p3d.combine()
    for i in range(data['池子个数']):
        cz.append(p3d.translation(p3d.Vec3(data['池子长']*i,0,0))*GGG)  
 
    # 圈梁参数
    data['圈梁支撑立柱粗']=100
    data['圈梁粗']=80
    # 支撑梁参数
    z=data['支撑梁粗']=80
    data['竖直支撑梁长']=420
    xz=data['斜支撑梁长']=336 
    # 棚顶参数
    data['棚顶厚']=80
    data['棚顶梁半径']=25
    data['棚顶斜梁数']=7
    data['棚子宽度']=2*data['池子宽']+320+2680
    data['棚子长度']=((data['池子长']*data['池子个数'])+3000)
    # 固定参数
    a1=40  
    a2=-15
    b1=data['圈梁粗']+data['竖直支撑梁长']
    k=data['旋转角度']
    # 立柱
    lz11=p3d.Box(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340),0),p3d.Vec3(-data['池子长']-1500,(2*data['池子宽'])+320+1340,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['圈梁支撑立柱粗'],data['圈梁支撑立柱粗'],data['圈梁支撑立柱粗'],data['圈梁支撑立柱粗']).color(0.5,0.5,0.5,1)
    lz = p3d.combine()
    n=4
    for i in range(n):
        lz.append(p3d.translation(p3d.Vec3((((data['池子长']*data['池子个数'])+3000)/3)*i,0,0))*lz11)
    rebars8 = p3d.translation(p3d.Vec3(0,-((2*data['池子宽'])+320+2680+(data['圈梁支撑立柱粗'])),0))* lz    
    lz=p3d.combine(rebars8,lz)
    #  圈梁
    ql1=p3d.Box(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗']),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3(-data['池子长']-1500,(2*data['池子宽'])+320+1340+(data['圈梁支撑立柱粗']),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])
    +data['圈梁粗']),p3d.Vec3(1,0,0),p3d.Vec3(0,-1,0),((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],(2*data['池子宽'])+320+2680+(data['圈梁支撑立柱粗']*2),((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],(2*data['池子宽'])+320+2680+(data['圈梁支撑立柱粗']*2)).color(30/255,166/255,1,1)
    ql2=p3d.Box(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-data['圈梁粗'],data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-data['圈梁粗'],data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['圈梁粗']),p3d.Vec3(1,0,0),p3d.Vec3(0,-1,0),((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],(2*data['池子宽'])+320+2680-(data['圈梁粗']*2)+(data['圈梁支撑立柱粗']*2),((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],(2*data['池子宽'])+320+2680-(data['圈梁粗']*2)+(data['圈梁支撑立柱粗']*2)).color(30/255,166/255,1,1)
    ql=p3d.substract(ql1,ql2).color(30/255,166/255,1,1)


    # #棚顶

    pd1=p3d.Box(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗']),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3(-data['池子长']-1500,((data['池子宽'])+160),data['棚顶高']-(data['圈梁粗'])),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],data['棚顶厚'],((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],data['棚顶厚']).color(30/255,166/255,1,1)
    pd2=p3d.Box(p3d.Vec3(-data['池子长']-1500,-1340-(data['圈梁支撑立柱粗']),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3(-data['池子长']-1500,((data['池子宽'])+160),data['棚顶高']-(data['圈梁粗'])),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],data['棚顶厚'],((data['池子长']*data['池子个数'])+3000)+data['圈梁支撑立柱粗'],data['棚顶厚']).color(30/255,166/255,1,1)
    pd=p3d.combine(pd1,pd2).color(30/255,166/255,1,1)
    qlandpd=p3d.unite(ql,pd).color(30/255,166/255,1,1)
    

    #棚顶梁
    apdl=p3d.Cone(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/4-50),p3d.Vec3(((data['池子长']*(data['池子个数']-1))+1500),((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/4-50),data['棚顶梁半径'],data['棚顶梁半径']).color(1,0,0,1)
    bpdl=p3d.Cone(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/4,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/2-75),p3d.Vec3(((data['池子长']*(data['池子个数']-1))+1500),((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/4,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/2-75),data['棚顶梁半径'],data['棚顶梁半径']).color(1,0,0,1)
    cpdl=p3d.Cone(p3d.Vec3(-data['池子长']-1500,((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)*3/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1*3/4-100),p3d.Vec3(((data['池子长']*(data['池子个数']-1))+1500),((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗'])-((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)*3/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1*3/4-100),data['棚顶梁半径'],data['棚顶梁半径']).color(1,0,0,1)
    aapdl=p3d.Cone(p3d.Vec3(-data['池子长']-1500,-data['圈梁支撑立柱粗']-1340+((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)*3/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1*3/4-100),p3d.Vec3(((data['池子长']*(data['池子个数']-1))+1500),-data['圈梁支撑立柱粗']-1340+((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)*3/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1*3/4-100),data['棚顶梁半径'],data['棚顶梁半径']).color(1,0,0,1)
    bbpdl=p3d.Cone(p3d.Vec3(-data['池子长']-1500,-data['圈梁支撑立柱粗']-1340+((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/4,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/2-75),p3d.Vec3(((data['池子长']*(data['池子个数']-1))+1500),-data['圈梁支撑立柱粗']-1340+((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/4,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/2-75),data['棚顶梁半径'],data['棚顶梁半径']).color(1,0,0,1)
    ccpdl=p3d.Cone(p3d.Vec3(-data['池子长']-1500,-data['圈梁支撑立柱粗']-1340+((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/4-50),p3d.Vec3(((data['池子长']*(data['池子个数']-1))+1500),-data['圈梁支撑立柱粗']-1340+((2*data['池子宽'])+320+2680+data['圈梁支撑立柱粗']*2)/8,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+b1/4-50),data['棚顶梁半径'],data['棚顶梁半径']).color(1,0,0,1)
    pdl=p3d.combine(apdl,bpdl,cpdl,aapdl,bbpdl,ccpdl)
  

    #横梁
    hl1=p3d.Box(p3d.Vec3((-data['池子长']-1500),((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗']),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3((-data['池子长']-1500),((2*data['池子宽'])+320+1340)+(data['圈梁支撑立柱粗']),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['圈梁粗']),p3d.Vec3(1,0,0),p3d.Vec3(0,-1,0),data['圈梁粗'],((2*data['池子宽'])+320+2680)+2*(data['圈梁支撑立柱粗']),data['圈梁粗'],((2*data['池子宽'])+320+2680)+2*(data['圈梁支撑立柱粗'])).color(0.5,0.5,0.5,1)
    hl = p3d.combine() 
    n=4
    for i in range(n):
        hl.append(p3d.translation(p3d.Vec3((((data['池子长']*data['池子个数'])+3000)/3)*i,0,0))*hl1)  
    #支撑梁
    szcl1=p3d.Box(p3d.Vec3((-data['池子长']-1500),data['池子宽']-z+data['圈梁支撑立柱粗']*2,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3((-data['池子长']-1500),data['池子宽']-z+data['圈梁支撑立柱粗']*2,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['竖直支撑梁长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),z,z,z,z).color(0.5,0.5,0.5,1)    
    zcl = p3d.combine() 
    n=4
    for i in range(n):
        zcl.append(p3d.translation(p3d.Vec3((((data['池子长']*data['池子个数'])+3000)/3)*i,0,0))*szcl1)
    #斜支撑梁
    xl1=p3d.Box(p3d.Vec3((-data['池子长']-1500),data['池子宽']-z+data['圈梁支撑立柱粗']*2-(820),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['圈梁粗']),p3d.Vec3((-data['池子长']-1500),data['池子宽']-z+data['圈梁支撑立柱粗']*2-(820),data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['圈梁粗']+b1/2-a1/2-data['圈梁粗']/2),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),z,z,z,z).color(0.5,0.5,0.5,1)
    xzcl = p3d.combine() 
    n=4
    for i in range(n):
        zcl.append(p3d.translation(p3d.Vec3((((data['池子长']*data['池子个数'])+3000)/3)*i,0,0))*xl1)
    
    xl2=p3d.Box(p3d.Vec3((-data['池子长']-1500),data['池子宽']-z+data['圈梁支撑立柱粗']*2+(820)+data['圈梁支撑立柱粗'],data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['圈梁粗']),p3d.Vec3((-data['池子长']-1500),data['池子宽']-z+data['圈梁支撑立柱粗']*2+(820)+data['圈梁支撑立柱粗'],data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+data['圈梁粗']+b1/2-a1/2-data['圈梁粗']/2),p3d.Vec3(1,0,0),p3d.Vec3(0,-1,0),z,z,z,z).color(0.5,0.5,0.5,1)
    xzcl = p3d.combine() 
    n=4
    for i in range(n):
        zcl.append(p3d.translation(p3d.Vec3((((data['池子长']*data['池子个数'])+3000)/3)*i,0,0))*xl2)
    
    xl=p3d.combine(xl1,xl2) 
  
    # 牌子
    Box0=p3d.Box(p3d.Vec3((-data['池子长']-1530),data['池子宽']-40,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])),p3d.Vec3((-data['池子长']-1530),data['池子宽']-40,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+150),p3d.Vec3(0,1,0),p3d.Vec3(1,0,0),400,30,400,30).color(225/255,225/255,225/255,1)
    text= p3d.Text("洗漱区",90,90).color(30/255,166/255,1, 1)
    text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi* 0.5)*text
    text= p3d.rotation(p3d.Vec3(0, 0, -1),p3d.pi* 0.5)*text
    text= p3d.translation(p3d.Vec3((-data['池子长']-1500)-40,data['池子宽']+160+200,data['棚顶高']-(data['圈梁粗']+data['竖直支撑梁长'])+30))*text
    B1=p3d.combine(cz,lz,ql,qlandpd,pdl,hl,zcl,text,Box0)
    B1=p3d.translation(p3d.Vec3(-data['池子长']/2,-data['池子宽']-160,0))*B1
    B1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*B1
    
    data['洗漱区']=B1

if __name__ == "__main__":
    data=p3d.P3DData({
    
        '场布分类':'辅助设施',
        '构件类型':'洗漱区',
        '构件名称':'洗漱区',
        '棚子宽度':4000,
        '棚顶高':4000,
        '旋转角度':0,
        '圈梁支撑立柱高':3500,
        '池子宽':500,
        '池子高':800,
        '池子长':1000,
        '池子个数':3,
        '棚子长度':6000
        })

#data
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('洗漱区',show=True)
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    data.setup('棚子长度' , obvious = True ,readonly=True,group='棚子参数' , description ='棚子长度')
    data.setup('棚子宽度' , obvious = True ,readonly=True,group='棚子参数' , description ='棚子宽度')
    data.setup('棚顶高' , obvious = True ,group='棚子参数' , description ='棚顶高')
    data.setup('旋转角度',obvious=True,group='旋转',description='旋转角度')
    data.setup('池子宽' , obvious = True ,group='池子参数' , description ='池子宽')
    data.setup('池子高' , obvious = True ,group='池子参数' , description ='池子高')
    data.setup('池子长' , obvious = True ,group='池子参数' , description ='池子长')
    data.setup('池子个数' , obvious = True ,group='池子参数' , description ='池子个数')
    data.setup('旋转角度',obvious=True,group='旋转',description='旋转角度')
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)