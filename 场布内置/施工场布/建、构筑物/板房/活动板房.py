import pyp3d as p3d
import math
def hbf(data:p3d.P3DData)->None:
#楼体参数
    a=data['开间']
    b=data['进深']
    h=data['层高']#柱高

#支撑柱参数
    jw=data['角支撑边长']
    zw=data['中部支撑边长']

#门参数
    mw=data['门宽']
    mh=data['门高']
    md=data['门厚']

#窗参数
    wdh=data['窗底高']
    wh=data['窗高']
    ww=data['窗宽'] 
    
    w=10

#屋顶参数
    rh=data['屋顶高']       #仅屋顶的高度
    x=data['山墙出挑距离']
    y=data['屋檐出挑距离']
    rd=data['屋顶厚度']

#底部参数
    dd=data['底部厚度']

#算式
    z=-((rh)/(b/2+zw/2))*(y+b/2+zw/2)+rh+h
    za=((rh)/(b/2+zw/2))*(-y-b/2-zw/2)+rh+h

#旋转参数
    k=data['旋转角度']

      # if h>rh:
    #     rh=h
    #     wd=p3d.Box(p3d.Vec3(-x,-y-b/2-zw/2,h),p3d.Vec3(-x,-y-b/2-zw/2,h+rd),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a+x+x,b+y+y+jw,a+x+x,b+y+y+jw).color(0,0,1,1)
    # # elif h<=rh:
    #     box3=p3d.Extrusion((p3d.Vec3(-x,0,rh+h),p3d.Vec3(-x,0,rh+h+rd),p3d.Vec3(-x,y+b/2+zw/2,za+rd),p3d.Vec3(-x,y+b/2+zw/2,za)),p3d.Vec3(a+x+x,0,0)).color(0,0,1,1)
    #     box4=p3d.Extrusion((p3d.Vec3(-x,0,rh+h),p3d.Vec3(-x,0,rh+h+rd),p3d.Vec3(-x,-y-b/2-zw/2,z+rd),p3d.Vec3(-x,-y-b/2-zw/2,z)),p3d.Vec3(a+x+x,0,0)).color(0,0,1,1)
    #     wd=p3d.combine(box3,box4)
    # if wh>h-wdh:
    #     wh=h-wdh
    # if mh>h:
    #     mh=h
    #if ww>a-jw/2-240:
    #    ww=a-jw/2-240

#楼
    box1=p3d.Box(p3d.Vec3(0,-b/2-zw/2,0),p3d.Vec3(0,0-b/2-zw/2,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a,b+zw,a,b+zw).color(0,0,0,1)
    box11=p3d.Box(p3d.Vec3(zw/2,-b/2,0),p3d.Vec3(zw/2,0-b/2,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a-zw,b,a-zw,b).color(0,0,0,1)
    box111=p3d.substract(box1,box11)
    # box2=p3d.Extrusion((p3d.Vec3(0,-b/2-zw/2,h),p3d.Vec3(0,0,rh+h),p3d.Vec3(0,b/2+zw/2,h)),p3d.Vec3(a,0,0)).color(0,0,0,1)
    box2=p3d.Extrusion((p3d.Vec3(0,-b/2-jw,h),p3d.Vec3(0,0,rh+h),p3d.Vec3(0,b/2+jw,h)),p3d.Vec3(a,0,0)).color(0,0,0,1)
    box22=p3d.Extrusion((p3d.Vec3(zw/2,-b/2,h),p3d.Vec3(0,0,rh+h-zw/2),p3d.Vec3(0,b/2,h)),p3d.Vec3(a-zw,0,0)).color(0,0,0,1)
    box222=p3d.substract(box2,box22)
    box=p3d.combine(box111,box222)

#支撑柱
    j1=p3d.Box(p3d.Vec3(-jw/2,b/2,0),p3d.Vec3(-jw/2,b/2,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),jw,jw,jw,jw).color(0,0,1,1)
    j2=p3d.Box(p3d.Vec3(a-jw/2,b/2,0),p3d.Vec3(a-jw/2,b/2,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),jw,jw,jw,jw).color(0,0,1,1)
    j3=p3d.Box(p3d.Vec3(-jw/2,-b/2-jw,0),p3d.Vec3(-jw/2,-b/2-jw,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),jw,jw,jw,jw).color(0,0,1,1)
    j4=p3d.Box(p3d.Vec3(a-jw/2,-b/2-jw,0),p3d.Vec3(a-jw/2,-b/2-jw,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),jw,jw,jw,jw).color(0,0,1,1)
    z1=p3d.Box(p3d.Vec3(a/3-zw/2,b/2,0),p3d.Vec3(a/3-zw/2,b/2,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zw,zw,zw,zw).color(0,0,1,1)
    z2=p3d.Box(p3d.Vec3(a*2/3-zw/2,b/2,0),p3d.Vec3(a*2/3-zw/2,b/2,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zw,zw,zw,zw).color(0,0,1,1)
    z3=p3d.Box(p3d.Vec3(a/3-zw/2,-b/2-zw,0),p3d.Vec3(a/3-zw/2,-b/2-zw,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zw,zw,zw,zw).color(0,0,1,1)
    z4=p3d.Box(p3d.Vec3(a*2/3-zw/2,-b/2-zw,0),p3d.Vec3(a*2/3-zw/2,-b/2-zw,h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zw,zw,zw,zw).color(0,0,1,1)
    l1=p3d.Box(p3d.Vec3(-zw/2,-zw/2,0),p3d.Vec3(-zw/2,-zw/2,rh+h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zw,zw,zw,zw).color(0,0,1,1)
    r1=p3d.Box(p3d.Vec3(-zw/2+a,-zw/2,0),p3d.Vec3(-zw/2+a,-zw/2,rh+h),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zw,zw,zw,zw).color(0,0,1,1)
    zz=p3d.combine(j1,j2,j3,j4,z1,z2,z3,z4,l1,r1)

#屋顶
    #box3=p3d.Extrusion((p3d.Vec3(-x,0,rh),p3d.Vec3(-x,0,rh+rd),p3d.Vec3(-x,y+b/2+zw/2,za+rd),p3d.Vec3(-x,y+b/2+zw/2,za)),p3d.Vec3(a+x+x,0,0)).color(0,0,0,1)
    # box4=p3d.Extrusion((p3d.Vec3(-x,0,rh+h),p3d.Vec3(-x,0,rh+h+rd),p3d.Vec3(-x,-y-b/2-zw/2,z+rd),p3d.Vec3(-x,-y-b/2-zw/2,z)),p3d.Vec3(a+x+x,0,0)).color(0,0,0,1)
    #wd=p3d.combine(box3,box4)
    box3=p3d.Extrusion((p3d.Vec3(-x,0,rh+h),p3d.Vec3(-x,0,rh+h+rd),p3d.Vec3(-x,y+b/2+zw/2,za+rd),p3d.Vec3(-x,y+b/2+zw/2,za)),p3d.Vec3(a+x+x,0,0)).color(0,0,1,1)
    box4=p3d.Extrusion((p3d.Vec3(-x,0,rh+h),p3d.Vec3(-x,0,rh+h+rd),p3d.Vec3(-x,-y-b/2-zw/2,z+rd),p3d.Vec3(-x,-y-b/2-zw/2,z)),p3d.Vec3(a+x+x,0,0)).color(0,0,1,1)
    wd=p3d.combine(box3,box4) 

#楼板
    box5=p3d.Box(p3d.Vec3(-jw/2,-jw-b/2,-dd),p3d.Vec3(-jw/2,-jw-b/2,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a+jw,b+jw*2,a+jw,b+jw*2).color(0.5,0.5,0.5,1)

#门
    #door=p3d.Box(p3d.Vec3(jw+120,-b/2-zw/2,0),p3d.Vec3(jw+120,-b/2-zw/2,mh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),mw,md,mw,md).color(0,0,0,1)
    if mw>a/3-zw/2-jw-240:
        mw=a/3-zw/2-jw-240
    door=p3d.Box(p3d.Vec3(jw+120,-b/2-zw/2,0),p3d.Vec3(jw+120,-b/2-zw/2,mh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),mw,md,mw,md).color(0,0,0,1)

#窗
    if ww>a-(200+a/3-zw/2):
        ww=a-(200+a/3-zw/2)
    window=p3d.Box(p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh),p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh+wh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),ww,w,ww,w).color(1,1,1,0.3)

#洞
    d9=p3d.Box(p3d.Vec3(jw+120,-b/2-zw/2,0),p3d.Vec3(jw+120,-b/2-zw/2,mh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),mw,md,mw,md).color(0,0,0,1)
    d10=p3d.Box(p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh),p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh+wh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),ww,jw,ww,jw).color(1,1,1,0.3)


#挖洞
    q1=p3d.substract(box,d9)
    q2=p3d.substract(q1,d10).color(1,1,1,1)

#构件名
    #A1=p3d.combine(q2,zz,box5,door,window,wd)
    #A1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*A1
    B1=p3d.combine(q1,zz,box5,door,wd)       
    B1=p3d.translation(p3d.Vec3(-(a+jw)/2,0,0))*B1
    B1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*B1
    #B1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*B1
    d10=p3d.Box(p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh),p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh+wh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),ww,jw,ww,jw).color(1,1,1,0.3)
    q1=p3d.substract(box,d9)
    q2=p3d.substract(q1,d10).color(1,1,1,1)
    window=p3d.Box(p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh),p3d.Vec3(200+a/3-zw/2,-b/2-zw/2,wdh+wh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),ww,w,ww,w).color(1,1,1,0.3)
    A1=p3d.combine(q2,zz,box5,door,window,wd)       
    A1=p3d.translation(p3d.Vec3(-(a+jw)/2,0,0))*A1
    A1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*A1
    if a<3500:
        data['活动样板房']=B1

    else:
        data['活动样板房']=A1

if __name__ == "__main__":
    data=p3d.P3DData({
        '开间':10000,
        '进深':7000,
        '层高':4000,
        '角支撑边长':100,
        '中部支撑边长':80,
        '门宽':1400,
        '门高':2000,
        '门厚':60,
        '窗底高':1200,
        '窗高':1000,
        '窗宽':2000,
        '屋顶高':1000,
        '山墙出挑距离':200,
        '屋檐出挑距离':300,
        '屋顶厚度':60,
        '底部厚度':120,
        '旋转角度':0,
        '场布类型':'建筑物',
        '构件类型':'活动样板房',
        '构件名称':'活动板房'

    })

#data
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)

    data.setup('活动样板房',show=True)
    data.setup('开间' , obvious = True ,group='楼体参数' , description ='开间')
    data.setup('进深' , obvious = True ,group='楼体参数' , description ='进深')
    data.setup('层高' , obvious = True ,group='楼体参数' , description ='层高')
    data.setup('角支撑边长' , obvious = True ,group='支撑柱' , description ='角支撑边长')
    data.setup('中部支撑边长' , obvious = True ,group='支撑柱' , description ='中部支撑边长')
    data.setup('门宽' , obvious = True ,group='门' , description ='门宽')
    data.setup('门高' , obvious = True ,group='门' , description ='门高')
    data.setup('门厚' , obvious = True ,group='门' , description ='门厚')
    data.setup('窗底高' , obvious = True ,group='窗' , description ='窗底高')
    data.setup('窗高' , obvious = True ,group='窗' , description ='窗高')
    data.setup('窗宽' , obvious = True ,group='窗' , description ='窗宽')
    data.setup('屋顶高' , obvious = True ,group='坡屋顶' , description ='屋顶高')
    data.setup('山墙出挑距离' , obvious = True ,group='坡屋顶' , description ='山墙出挑距离')
    data.setup('屋檐出挑距离' , obvious = True ,group='坡屋顶' , description ='屋檐出挑距离')
    data.setup('屋顶厚度' , obvious = True ,group='坡屋顶' , description ='屋顶厚度')
    data.setup('底部厚度' , obvious = True ,group='底部厚度' , description ='底部厚度')
    data.setup('旋转角度',obvious=True,group='旋转',description='旋转角度')
    data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
    data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
    data.setup('构件名称',obvious=True)

    data['replace'] = hbf
    hbf(data)
    p3d.launchData(data)
