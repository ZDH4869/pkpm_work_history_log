import pyp3d as p3d
def zhangpeng(data:p3d.P3DData)->None:

    l= data['长度']
    h= data['总高度']
    a= data['宽度']
    z= data['门高度']
    x= data['门宽度']
    c_h=data['窗台高度']
    r_h=300  #坡屋顶高度
    rota=data['旋转角度']
    data['场布分类']='建/构筑物'
    data['构件类型']='其他临建'
    #创建帐篷
    x1=p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3((a-x)/2,0,0),p3d.Vec3((a-x)/2,0,z),\
        p3d.Vec3((a-x)/2+x,0,z),p3d.Vec3((a-x)/2+x,0,0),p3d.Vec3(a,0,0),\
            p3d.Vec3(a,0,h-r_h),p3d.Vec3(a/2,0,h),p3d.Vec3(0,0,h-r_h)),p3d.Vec3(0,l,0)).color(1,1,0,1)
    x2=p3d.Extrusion((p3d.Vec3(0+1,1,0),p3d.Vec3((a-x)/2,1,0),p3d.Vec3((a-x)/2,1,z),\
        p3d.Vec3((a-x)/2+x,1,z),p3d.Vec3((a-x)/2+x,1,0),p3d.Vec3(a-1,1,0),\
            p3d.Vec3(a-1,1,h-r_h),p3d.Vec3(a/2,1,h-1),p3d.Vec3(0+1,1,h-r_h)),p3d.Vec3(0,l-2,0)).color(1,1,0,1)
    bb=p3d.substract(x1,x2) .color(76/255,94/255,34/255,1)

    #建立后门
    x3=p3d.Extrusion((p3d.Vec3((a-x)/2-100,l-1,0),p3d.Vec3((a-x)/2+x+100,l-1,0),p3d.Vec3((a-x)/2+x,l-1,z),\
        p3d.Vec3((a-x)/2,l-1,z)),p3d.Vec3(0,1,0)).color(76/255,94/255,34/255,1)
    bb=p3d.unite(bb,x3) .color(76/255,94/255,34/255,1)


    #创建窗户洞，进行布尔减法，创建带洞的帐篷bb1
    cd = p3d.Box(p3d.Vec3(-50,0,0), p3d.Vec3(50+a,0,0), p3d.Vec3(0,0,1), p3d.Vec3(0,1,0), 700, 800, 700, 800).color(1,1,0,1) #窗户长800，高700
    cd1=p3d.translation(0,1700,c_h)*cd   #扣减体           
    bb1=p3d.substract(bb,cd1).color(76/255,94/255,34/255,1)

    #创建窗户
    ch = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), p3d.Vec3(0,1,0), 700, 800, 700, 800).color(1,1,1,0.5) 
    ch1=p3d.translation(0,1700,c_h)*ch
    ch2=p3d.translation(a-1,1700,c_h)*ch

    #组合
    zh=p3d.combine(bb1,ch1,ch2)

    data['帐篷高度']=h-r_h
    data['坡屋顶高度']=r_h
    zh=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*zh
    data ['帐篷'] = zh
if __name__ == "__main__":
    data = p3d.P3DData({
            '长度': 3900,  
            '总高度': 2500,
            '宽度': 3000,  
            '门宽度': 1200,
            '门高度': 1800,
            '窗台高度':800,
            '坡屋顶高度':300,
            '帐篷高度':2200,
            '旋转角度':0,    
            '构件名称':'临时工棚帐篷'
        })
    
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('帐篷', show=True)

    # 设置可调整属性
    data.setup('旋转角度', obvious=True,group='帐篷参数')
    data.setup('长度', obvious=True   ,group='帐篷参数')
    data.setup('总高度', obvious=True ,group='帐篷参数')
    data.setup('宽度', obvious=True ,group='帐篷参数')
    data.setup('帐篷高度',obvious=True,readonly=True, group='帐篷参数') 
    data.setup('坡屋顶高度', obvious=True,readonly=True, group='帐篷参数') 
    data.setup('门高度', obvious=True, group='门参数')
    data.setup('门宽度', obvious=True, group='门参数')
    data.setup('窗台高度', obvious=True, group='窗户参数') 
    data.setup('场布分类', obvious=True,readonly=True, group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True, group = '类型参数')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = zhangpeng
    zhangpeng(data)
    # 发射数据到实例模板库
    p3d.launchData(data)
