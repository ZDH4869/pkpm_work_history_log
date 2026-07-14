import pyp3d as p3d # 导入pyp3d，可以直接使用pyp3d中的函数而无需前缀

def desk(data:p3d.P3DData)->None:
    H=data['桌子高度']
    L=data['桌子长度']
    W=data['桌子宽度']
    m=data['桌面不透明度']
    a=80 #桌腿宽度
    hc=40 #圆柱体高度
    hup=10 #上垫片高度
    hdown=30 #下垫片高度
    hglass=10 #桌面玻璃高度
    #桌腿=垫片+木桌腿+圆柱体+上垫片 以木桌腿左下角为原点
    aa=10 #下方垫片边长为a+aa
    ztbox1=p3d.Box(p3d.Vec3(-aa/2,-aa/2,0),p3d.Vec3(-aa/2,-aa/2,hdown),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a+aa,a+aa,a+aa,a+aa).color(1,1,1,1)
    ztbox2=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,H),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a,a,a,a)
    ztcone1=p3d.Cone(p3d.Vec3(a/2,a/2,H),p3d.Vec3(a/2,a/2,H+hc),a/2,a/2)
    ztbox3=p3d.Box(p3d.Vec3(0,0,H+hc),p3d.Vec3(0,0,H+hc+hup),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),a,a,a,a)
    zt1=p3d.combine(ztbox1,ztbox2,ztcone1,ztbox3)
    zt2=p3d.translation(p3d.Vec3(L-a,0,0))*zt1
    zt3=p3d.translation(p3d.Vec3(0,W-a,0))*zt1
    zt4=p3d.translation(p3d.Vec3(L-a,W-a,0))*zt1
    zt=p3d.combine(zt1,zt2,zt3,zt4)

    ##桌面
    #顶面玻璃 先做一个厚30的玻璃，再布尔减掉中间一部分
    zmbox1=p3d.Box(p3d.Vec3(a/2,a/2,H+0.5*hc-30),p3d.Vec3(a/2,a/2,H+0.5*hc),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),L-a,W-a,L-a,W-a)
    #侧面玻璃 
    zmbox2=p3d.Box(p3d.Vec3(a/2+hglass,a/2+hglass,H+0.5*hc-30),p3d.Vec3(a/2+hglass,a/2+hglass,H+0.5*hc-hglass),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),L-a-2*hglass,W-a-2*hglass,L-a-2*hglass,W-a-2*hglass)
    zmbox=p3d.substract(zmbox1,zmbox2).color(0.5,0.5,0.5,m)
    #插座 给定插座边长cc 四角曲率半径cr 高度hcz
    cc=100
    cr=15
    hcz=45
    czbox1=p3d.Box(p3d.Vec3(cr,0,0),p3d.Vec3(cr,0,hcz),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),cc-2*cr,cc,cc-2*cr,cc)
    czbox2=p3d.Box(p3d.Vec3(0,cr,0),p3d.Vec3(0,cr,hcz),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),cc,cc-2*cr,cc,cc-2*cr)
    czcone1=p3d.Cone(p3d.Vec3(cr,cr,0),p3d.Vec3(cr,cr,hcz),cr,cr)
    czcone2=p3d.translation(p3d.Vec3(0,cc-2*cr,0))*czcone1
    czcone3=p3d.translation(p3d.Vec3(cc-2*cr,cc-2*cr,0))*czcone1
    czcone4=p3d.translation(p3d.Vec3(cc-2*cr,0,0))*czcone1
    czboxn=p3d.unite(czbox1,czbox2,czcone1,czcone2,czcone3,czcone4)
    #插孔
    czboxk1=p3d.Box(p3d.Vec3(37.5,16.5,hcz-10),p3d.Vec3(37.5,16.5,hcz),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),3,10,3,10)
    czboxk2=p3d.translation(p3d.Vec3(19,0,0))*czboxk1
    czboxk3=p3d.translation(p3d.Vec3(9.5,12,0))*czboxk1
    czboxk4=p3d.translation(p3d.Vec3(0,57,0))*czboxk1
    czboxk5=p3d.translation(p3d.Vec3(0,57,0))*czboxk2
    czk=p3d.combine(czboxk1,czboxk2,czboxk3,czboxk4,czboxk5)
    cz=p3d.translation(p3d.Vec3(100,W-a-100,H-50))*p3d.substract(czboxn,czk)

    #装饰品
    zscone1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(250,0,0),45,45)
    zskcone1=p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(250,0,0),42,42)
    zstem=p3d.substract(zscone1,zskcone1)
    zsbox=p3d.Box(p3d.Vec3(-60,60,-60),p3d.Vec3(-60,60,0),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),500,-500,500,-500)
    zs1=p3d.substract(zstem,zsbox)
    zscone2=p3d.Cone(p3d.Vec3(0,-60,24),p3d.Vec3(250,-60,25),25,25)
    zskcone2=p3d.Cone(p3d.Vec3(0,-60,24),p3d.Vec3(250,-60,25),22,22)
    zstem2=p3d.substract(zscone2,zskcone2)
    zsbox2=p3d.Box(p3d.Vec3(-30,30,24),p3d.Vec3(-30,30,60),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),300,-300,300,-300)
    zs2=p3d.substract(zstem2,zsbox2)
    
    zs=p3d.translation(p3d.Vec3(400,W-100,H+hglass))*p3d.unite(zs1,zs2)
    data['桌子'] =p3d.combine(zt,zmbox,cz,zs)
    # data['桌子'] =p3d.combine(zs)
   
if __name__ == "__main__":
    data = p3d.P3DData({
        '桌子高度':800,
        '桌子长度':1400,
        '桌子宽度': 600,
        '桌面不透明度':0.1,
        '构件名称':'办公桌'
        })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('桌子', show=True)
    data.setup('桌子高度',obvious=True, group='办公桌', description='桌子高度')
    data.setup('桌子长度',obvious=True, group='办公桌', description='桌子长度')
    data.setup('桌子宽度',obvious=True, group='办公桌', description='桌子宽度')
    data.setup('桌面不透明度',obvious=True, group='办公桌', description='桌面不透明度')
    data.setup('构件名称',obvious=True)
    data['replace'] = desk
    desk(data)
    p3d.launchData(data)
