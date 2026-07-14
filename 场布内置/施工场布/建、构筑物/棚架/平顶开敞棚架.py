import pyp3d as p3d
from pyp3d import *
def kcpj(data:p3d.P3DData)->None:
#可变参数
    #支撑柱参数
        zd=data['立柱边长']
        i=data['立柱个数']
        #xzd=data['斜柱边长']
    #垫片参数
        dph=data['垫片厚']
    #棚参数
        pg=data['棚高']
        pdc=data['棚顶长']
        pdk=data['棚顶宽']
        pdh=data['棚顶厚']
    #桁架参数
        r=data['桁架半径']
    #旋转角度
        k=data['旋转角度']


#随动参数
        data['立柱高']=pg+500
        data['立柱间距']=(pdc-2*r)/(i-1)
        sd=pdc/(i-1)
        data['立柱垫片长']=zd+100
        data['斜柱高']=pg-1000
        data['斜柱宽']=pdk/4
        data['顶标高']=pg+500+pdh
        data['斜柱边长']=zd-50

#组件
    #棚
        p1=p3d.Box(p3d.Vec3(-50,-50-pdk/2,pg),p3d.Vec3(-50,-50-pdk/2,pg+500),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),pdc+100,pdk+100,pdc+100,pdk+100)
        p2=p3d.Box(p3d.Vec3(0,-pdk/2,pg),p3d.Vec3(0,-pdk/2,pg+500),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),pdc,pdk,pdc,pdk)
        p=p3d.substract(p1,p2).color(0.5,0.5,0.5,1)
    #棚顶
        pd=p3d.Box(p3d.Vec3(-50,-50-pdk/2,pg+500),p3d.Vec3(-50,-50-pdk/2,pg+500+pdh),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),pdc+100,pdk+100,pdc+100,pdk+100)
        ppd=p3d.unite(p,pd).color(30/255,144/255,1,1)
    #支撑柱
        z1=p3d.Box(p3d.Vec3(0,-zd/2,0),p3d.Vec3(0,-zd/2,pg+500),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zd,zd,zd,zd).color(0.5,0.5,0.5,1)
        dp=p3d.Box(p3d.Vec3(-50,-zd/2-50,0),p3d.Vec3(-50,-zd/2-50,-dph),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zd+100,zd+100,zd+100,zd+100).color(0.5,0.5,0.5,1)
        z=p3d.combine(z1,dp)
        zcz = p3d.Array(z)
        for point in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(pdc-zd,0,0),i):
            zcz.append(p3d.translation(point))
    #斜柱
        xz1=p3d.Box(p3d.Vec3(25,-(zd-50)/2,pg-1000),p3d.Vec3(25,-pdk/4,pg+500),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zd-50,zd-50,zd-50,zd-50).color(0.5,0.5,0.5,1)
        xz2=p3d.Box(p3d.Vec3(25,-(zd-50)/2,pg-1000),p3d.Vec3(25,pdk/4,pg+500),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),zd-50,zd-50,zd-50,zd-50).color(0.5,0.5,0.5,1)
        z2=p3d.combine(xz1,xz2)

        xz=p3d.Array(z2)
        for point in p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(pdc-zd-25,0,0),i):
            zcz.append(p3d.translation(point))
    #桁架
        hjz1=p3d.Cone(p3d.Vec3(r,-pdk/2,pg+r),p3d.Vec3(r,-pdk/2,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz2=p3d.Cone(p3d.Vec3(r,pdk/2,pg+r),p3d.Vec3(r,pdk/2,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz3=p3d.Cone(p3d.Vec3(r,-pdk/2,pg+r),p3d.Vec3(r,-pdk*5/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz4=p3d.Cone(p3d.Vec3(r,-pdk*4/12,pg+r),p3d.Vec3(r,-pdk*5/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz5=p3d.Cone(p3d.Vec3(r,-pdk*4/12,pg+r),p3d.Vec3(r,-pdk*3/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz6=p3d.Cone(p3d.Vec3(r,-pdk*2/12,pg+r),p3d.Vec3(r,-pdk*3/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz7=p3d.Cone(p3d.Vec3(r,-pdk*2/12,pg),p3d.Vec3(r,-pdk*1/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz8=p3d.Cone(p3d.Vec3(r,0,pg+r),p3d.Vec3(r,-pdk*1/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz9=p3d.Cone(p3d.Vec3(r,0,pg+r),p3d.Vec3(r,pdk*1/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz10=p3d.Cone(p3d.Vec3(r,pdk*2/12,pg+r),p3d.Vec3(r,pdk*1/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz11=p3d.Cone(p3d.Vec3(r,pdk*2/12,pg+r),p3d.Vec3(r,pdk*3/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz12=p3d.Cone(p3d.Vec3(r,pdk*4/12,pg+r),p3d.Vec3(r,pdk*3/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz13=p3d.Cone(p3d.Vec3(r,pdk*4/12,pg+r),p3d.Vec3(r,pdk*5/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz14=p3d.Cone(p3d.Vec3(r,pdk/2,pg+r),p3d.Vec3(r,pdk*5/12,pg+500),r,r).color(0.5,0.5,0.5,1)
        hjz=p3d.Cone(p3d.Vec3(r,-pdk/2,pg+r),p3d.Vec3(r,pdk/2,pg+r),r,r).color(0.5,0.5,0.5,1)
        hj=p3d.combine(hjz1,hjz2,hjz3,hjz4,hjz5,hjz6,hjz7,hjz8,hjz9,hjz10,hjz11,hjz12,hjz13,hjz14,hjz)

        r1 = p3d.Array(hj)
        for point in p3d.linspace(p3d.Vec3(r,0,0),p3d.Vec3(sd-r,0,0),4):
            r1.append(p3d.translation(point))
        
        r2 = p3d.Array(r1)
        for point in p3d.linspace(p3d.Vec3(sd+r,0,0),p3d.Vec3(pdc-r,0,0),i-1):
            r2.append(p3d.translation(point))
        r2=translation(-sd,0,0)*r2
        
#构件名
        A1= p3d.combine(ppd,zcz,xz,r2)
        A1=translation(100/2,(zd+100)/2,dph)*A1
        A1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*k)*A1
        # A1=p3d.translation(15000,0,0)*A1
        data['平顶开敞棚架']=A1
        
if __name__ == "__main__":
        data=p3d.P3DData({
            '立柱边长':150,
            '立柱个数':4,
            '斜柱边长':80,
            '垫片厚':20,
            '棚高':4000,
            '棚顶长':15600,
            '棚顶宽':7000,
            '棚顶厚':60,
            '桁架半径':25,
            '旋转角度':0,
            '场布类型':'材料堆场',
            '构件类型':'加工棚',
            '构件名称':'平顶开敞棚架'
        })

#data
        data.setup('平顶开敞棚架',show=True)
        data.setup('棚高' , obvious = True ,group='顶棚参数' , description ='棚高')
        data.setup('棚顶长' , obvious = True ,group='顶棚参数' , description ='棚顶长')
        data.setup('棚顶宽' , obvious = True ,group='顶棚参数' , description ='棚顶宽')
        data.setup('棚顶厚' , obvious = True ,group='顶棚参数' , description ='棚顶厚')
        data.setup('立柱边长' , obvious = True ,group='立柱参数' , description ='支撑柱边长')
        data.setup('立柱高' , obvious = True ,readonly=True,group='立柱参数' , description ='支撑柱高')
        data.setup('立柱间距' , obvious = True ,readonly=True,group='立柱参数' , description ='支撑柱间距')
        data.setup('立柱个数' , obvious = True ,readonly=True,group='立柱参数' , description ='支撑柱间距')
        data.setup('立柱垫片长' , obvious = True ,readonly=True ,group='立柱参数' , description ='支撑柱垫片长')
        data.setup('垫片厚' , obvious = True ,group='立柱参数' , description ='支撑柱垫片厚')
        data.setup('斜柱边长' , obvious = True ,readonly=True ,group='立柱参数' , description ='斜柱边长')
        data.setup('斜柱高' , obvious = True ,readonly=True,group='立柱参数' , description ='斜柱高')
        data.setup('斜柱宽' , obvious = True ,readonly=True,group='立柱参数' , description ='斜柱宽')
        data.setup('顶标高' , obvious = True ,readonly=True,group='顶棚参数' , description ='顶标高')
        data.setup('桁架半径' , obvious = True ,group='桁架参数' , description ='桁架半径')
        data.setup('旋转角度',obvious=True,group='旋转',description='旋转角度')
        data.setup('场布类型',obvious=True,readonly=True,group='公共属性',description='场布类型')
        data.setup('构件类型',obvious=True,readonly=True,group='公共属性',description='构件类型')
        data.setup('构件名称',obvious=True)

        data['replace'] = kcpj
        kcpj(data)
        p3d.launchData(data)