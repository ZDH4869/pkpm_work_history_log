import pyp3d as p3d
def Prefabricated_fence(data:p3d.P3DData)->None:

    L1 = data['立柱长度']
    B1 = data['立柱宽度']
    H1 = data['立柱高度']
    H2 = data['柱帽高度']
    L2 = data['单个pvc围挡长度']
    B3 = data['单个pvc围挡宽度']
    H3 = data['单个pvc围挡高度']
    H4 = data['围挡下部高度']
    H6 = data['围挡上部高度']
    H5 = data['基础高度']
    l_loop = data['围挡柱间长度']
    R = data['防雨帽半径']
    # Elo = data['拉伸长度']
    l_p = data['段首柱子是否显示']
    r_p = data['段尾柱子是否显示']

    KeyPoint = data['关键点']
    data['预制式围挡0'] = p3d.combine()
    n_loop_ = 0
    for ix in range(len(KeyPoint)-1):   
        v12_norm = p3d.norm(KeyPoint[ix]-KeyPoint[ix+1])
        Elo =v12_norm     #长度

        #单个PVC蓝色构件
        if H3+H4+H6 < H1:
            H1 = H1
        else:
            H1 = H3+H4+H6+H2
        #PVC蓝色围栏尺寸个数确定（最小单元）（围栏由总长、栏-柱单元个数确定）    
        n_PVC = int((l_loop-L1)/L2)+1

        box_PVC = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H3), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L2, B3,L2, B3).color(0,0,1,1)
        rebars1 = p3d.Array(box_PVC) 
        for point in range(n_PVC):
            rebars1.append(p3d.translation(point*L2,0,0))
        rebars2 = p3d.translation(p3d.Vec3(L1/2,-B3/2,H4+H5)) * rebars1    # 中轴线对齐
        # 围栏白色下框 
        box9 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop, B1-50*2,l_loop, B1-50*2).color(1,1,1,1)
        box10 = p3d.translation(p3d.Vec3(L1/2,50-B1/2,H5)) * box9
        # 围栏白色上框 
        box13 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H6), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop, B1-50*2,l_loop, B1-50*2).color(1,1,1,1)
        box12 = p3d.translation(p3d.Vec3(L1/2,50-B1/2,H3+H4+H5)) * box13
        #立柱
        box1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H1-H2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1, B1, L1, B1).color(1,1,1,1) 
        box2 = p3d.Box(p3d.Vec3(-20,-20,0), p3d.Vec3(-20,-20,H2), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1+40, B1+40, L1+40, B1+40).color(1,1,1,1)
        box3 = p3d.translation(p3d.Vec3(0,0,H1-H2)) * box2 

        Sphere1 = p3d.Sphere(p3d.Vec3(0,0,0),R).color(1,1,1,1)
        box4 = p3d.Box(p3d.Vec3(-10000,-10000,0), p3d.Vec3(-10000,-10000,10000), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 20000, 20000, 20000, 20000).color(1,1,1,1)
        BB = p3d.substract(Sphere1,box4).color(1,1,1,1)
        F1 = p3d.rotation(p3d.Vec3(1,0,0),p3d.pi) * BB
        Sphere2 = p3d.translation(p3d.Vec3(L1/2,B1/2,H1)) * F1 
        # 红条
        box5 = p3d.Box(p3d.Vec3(0,0,500), p3d.Vec3(0,0,500+300), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 100, 10, 100, 10).color(1,0,0,1)
        box6 = p3d.Box(p3d.Vec3(0,0,H1-800), p3d.Vec3(0,0,H1-500), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 100, 10, 100, 10).color(1,0,0,1)
        box7 = p3d.combine(box5,box6)
        box8 = p3d.translation(p3d.Vec3(L1/2-100/2,-10,0)) * box7
        lz0 = p3d.combine(box1,box3,Sphere2,box8)
        lz = p3d.translation(p3d.Vec3(-L1/2,-B1/2,H5)) * lz0
        # 对面立柱
        LZ1 = p3d.translation(p3d.Vec3(l_loop,0,0)) * lz



        # 基础
        # 立柱基础
        DZ3 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), L1, B1,L1, B1).color(68/225,84/225,106/225,1) 
        l_base = p3d.translation(p3d.Vec3(-L1/2,-B1/2,0)) * DZ3
        # 围栏基础
        DZ1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1, B1,l_loop-L1, B1).color(68/225,84/225,106/225,1) 
        DZ2 = p3d.translation(p3d.Vec3(L1/2,-B1/2,0)) * DZ1

        # wall_base = p3d.combine(box10,box12,rebars2,DZ2)
        # Fence = p3d.combine(LZ1,wall_base)

        # 立柱组合
        pier_head = p3d.combine(lz,l_base)
        pier_tail = p3d.combine(LZ1,p3d.translate(l_loop,0,0)*l_base)
        # 围挡组合
        fence = p3d.combine(box10,box12,rebars2,DZ2)

        # 栏-柱单元组合（只含段尾立柱）
        loop = p3d.combine(pier_tail,fence)

        # 栏-柱单元循环(取单元长倍数)
        n_loop = int(Elo/l_loop)
        loop_int = p3d.Array(loop) 

        for point in range(1,n_loop):
            loop_int.append(p3d.translation(point*l_loop,0,0))
        # WD2.append(l_base)
        # WD = p3d.combine(lz,DZ,WD2,l_base)
        # p3d.place(loop_int)
    ####################################################################################
        # 段首补充
        n_PVC_head = int((l_loop-L1/2)/L2)+1
        # 段首PVC
        rebars_head = p3d.Array(box_PVC) 
        for point in range(n_PVC_head):
            rebars_head.append(p3d.translation(point*L2,0,0))
        rebars_head = p3d.translation(p3d.Vec3(0,-B3/2,H4+H5)) * rebars_head    # 中轴线对齐
        # rebars_supple = (rebars_supple - p3d.translate(Elo,-3*B1,-H1)*p3d.scale(l_loop,6*B1,4*H1)*p3d.Box()).color(0,0,1,1)   # 段首裁剪
        # 段首围栏白色下框 
        box9_head = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1/2, B1-50*2,l_loop-L1/2, B1-50*2).color(1,1,1,1)
        box10_head = p3d.translation(p3d.Vec3(0,50-B1/2,H5)) * box9_head
        # 段首围栏白色上框 
        box13_head = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H6), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1/2, B1-50*2,l_loop-L1/2, B1-50*2).color(1,1,1,1)
        box12_head = p3d.translation(p3d.Vec3(0,50-B1/2,H3+H4+H5)) * box13_head
        # 围栏基础
        DZ1_head = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_loop-L1/2, B1,l_loop-L1/2, B1).color(68/225,84/225,106/225,1) 
        DZ2_head = p3d.translation(p3d.Vec3(0,-B1/2,0)) * DZ1_head
        # 段首组合
        supple_head = p3d.combine(rebars_head,box10_head,box12_head,DZ2_head,pier_tail)
    #######################################################################################
        # 段尾补充
        l_supple = Elo-l_loop*n_loop
        n_PVC_supple = int((l_supple-L1/2)/L2)+1
        supple_tail = p3d.combine()
        if l_supple>0:
            # 段尾PVC
            rebars_supple = p3d.Array(box_PVC) 
            for point in range(n_PVC_supple):
                rebars_supple.append(p3d.translation(point*L2,0,0))
            rebars_supple = p3d.translation(p3d.Vec3(n_loop * l_loop + L1/2 - (n_PVC_supple*L2-l_supple+L1/2),-B3/2,H4+H5)) * rebars_supple    # 中轴线对齐
            # rebars_supple = (rebars_supple - p3d.translate(Elo,-3*B1,-H1)*p3d.scale(l_loop,6*B1,4*H1)*p3d.Box()).color(0,0,1,1)   # 段尾裁剪
            # 段尾围栏白色下框 
            box9_supple = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H4), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_supple-L1/2, B1-50*2,l_supple-L1/2, B1-50*2).color(1,1,1,1)
            box10_supple = p3d.translation(p3d.Vec3(n_loop * l_loop + L1/2,50-B1/2,H5)) * box9_supple
            # 段尾围栏白色上框 
            box13_supple = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H6), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_supple-L1/2, B1-50*2,l_supple-L1/2, B1-50*2).color(1,1,1,1)
            box12_supple = p3d.translation(p3d.Vec3(n_loop * l_loop + L1/2,50-B1/2,H3+H4+H5)) * box13_supple
            # 围栏基础
            DZ1_supple = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,H5), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), l_supple-L1/2, B1,l_supple-L1/2, B1).color(68/225,84/225,106/225,1) 
            DZ2_supple = p3d.translation(p3d.Vec3(n_loop * l_loop + L1/2,-B1/2,0)) * DZ1_supple
            # 段尾组合
            supple_tail = p3d.combine(rebars_supple,box10_supple,box12_supple,DZ2_supple,p3d.translate(Elo,0,0)*pier_head)
            n_loop=n_loop+1

    #######################################################################################
        #第一段特殊处理 
        if ix == 0:
        # 首立柱判断
            if l_p == '是':
                supple_head = p3d.combine(supple_head,pier_head)

        # 最后一段特殊处理
        if ix == len(KeyPoint)-2:
            supple_tail = p3d.combine(rebars_supple,box10_supple,box12_supple,DZ2_supple)
        # 尾立柱判断
            if r_p == '是':
                supple_tail = p3d.combine(supple_tail,p3d.translate(Elo,0,0)*pier_head)


        fence_final = p3d.combine(loop_int,supple_tail,supple_head)
        data['预制式围挡0'].append(p3d.translation(KeyPoint[ix]) * p3d.rotation_to(KeyPoint[ix+1]-KeyPoint[ix]) * fence_final)
        n_loop_ = n_loop_+n_loop

#######
    data['柱帽长度'] = L1+40
    data['柱帽宽度'] = B1+40
    data['贴面长度'] = 100
    data['贴面高度'] = 300
    # data['下围挡长度'] = Elo/n
    # data['下围挡宽度'] = B1-100
    # data['上围挡长度'] = Elo/n
    # data['上围挡宽度'] = B1-100
    data['基础长度'] = Elo
    data['基础宽度'] = B1
    data['围挡个数'] = n_loop_

    data['立柱红色值'] = 255
    data['立柱绿色值'] = 255
    data['立柱蓝色值'] = 255
    data['立柱颜色透明度']  = 1
    data['柱帽红色值'] = 255
    data['柱帽绿色值'] = 255
    data['柱帽蓝色值'] = 255
    data['柱帽颜色透明度'] = 1
    data['贴面红色值'] = 255
    data['贴面绿色值'] = 0
    data['贴面蓝色值'] = 0
    data['贴面颜色透明度'] = 1
    data['PVC围挡红色值'] = 0
    data['PVC围挡绿色值'] = 0
    data['PVC围挡蓝色值'] = 255
    data['PVC围挡颜色透明度'] = 1
    data['基础红色值'] = 68
    data['基础绿色值'] = 84
    data['基础蓝色值'] = 106
    data['基础颜色透明度'] = 1
    data['场布分类'] = '建/构筑物'
    data['构件类型'] = '建筑墙'
    l_p = data['段首柱子是否显示']
    r_p = data['段尾柱子是否显示']

if __name__ == "__main__":
    data = p3d.P3DData({
        '立柱长度':300,
        '立柱宽度':400,
        '立柱高度':1900,
        '柱帽高度':200,
        '单个pvc围挡长度':100,
        '单个pvc围挡宽度':50,
        '单个pvc围挡高度':1600,
        '围挡下部高度':100,
        '围挡上部高度':100,
        '基础高度':300,
        '围挡柱间长度':1950,
        '拉伸长度': 6000,
        '防雨帽半径':160,
        '段首柱子是否显示':'是',
        '段尾柱子是否显示':'是',
        '构件名称':'预制式围挡多点布置',
        '关键点':[p3d.Vec3(0,0,0),p3d.Vec3(10000,500,0),p3d.Vec3(15000,30000,0),p3d.Vec3(0,0,0)],

        })
    data.set_view(1,1)
    data.setup('预制式围挡0', show=True)

    data.setup('场布分类',obvious=True,readonly = True, group='类型参数')
    data.setup('构件类型',obvious=True,readonly = True, group='类型参数')

    data.setup('立柱长度',obvious=True, group='立柱几何属性')
    data.setup('立柱宽度',obvious=True, group='立柱几何属性')
    data.setup('立柱高度',obvious=True, group='立柱几何属性')
    data.setup('段首柱子是否显示', obvious=True, group='立柱几何属性', description='[是]或[否]')
    data.setup('段尾柱子是否显示', obvious=True, group='立柱几何属性', description='[是]或[否]')

    data.setup('柱帽高度',obvious=True, group='柱帽几何属性')
    data.setup('防雨帽半径',obvious=True, group='柱帽几何属性')
    data.setup('柱帽长度',obvious=True,readonly = True, group='柱帽几何属性')
    data.setup('柱帽宽度',obvious=True,readonly = True, group='柱帽几何属性')
    
    data.setup('单个pvc围挡长度',obvious=True, group='围挡几何属性')
    data.setup('单个pvc围挡宽度',obvious=True, group='围挡几何属性')
    data.setup('单个pvc围挡高度',obvious=True, group='围挡几何属性')
    data.setup('围挡柱间长度',obvious=True, group='围挡几何属性')
    data.setup('围挡下部高度',obvious=True, group='围挡几何属性')
    data.setup('围挡上部高度',obvious=True, group='围挡几何属性')
    # data.setup('下围挡长度',obvious=True,readonly = True, group='围挡几何属性')
    # data.setup('下围挡宽度',obvious=True,readonly = True, group='围挡几何属性')
    # data.setup('上围挡长度',obvious=True,readonly = True, group='围挡几何属性')
    # data.setup('上围挡宽度',obvious=True,readonly = True, group='围挡几何属性')
    data.setup('围挡个数',obvious=True,readonly = True, group='围挡几何属性')


    data.setup('基础高度',obvious=True, group='基础几何属性')
    data.setup('基础长度',obvious=True,readonly = True, group='基础几何属性')
    data.setup('基础宽度',obvious=True,readonly = True, group='基础几何属性')

    data.setup('贴面长度',obvious=True,readonly = True, group='贴面几何属性')
    data.setup('贴面高度',obvious=True,readonly = True, group='贴面几何属性')

    data.setup('拉伸长度', obvious=True,group='几何尺寸')

    data.setup('立柱红色值',obvious=True,readonly = True, group='立柱颜色')
    data.setup('立柱绿色值',obvious=True,readonly = True, group='立柱颜色')
    data.setup('立柱蓝色值',obvious=True,readonly = True, group='立柱颜色')
    data.setup('立柱颜色透明度',obvious=True,readonly = True, group='立柱颜色')
    data.setup('柱帽红色值',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('柱帽蓝色值',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('柱帽绿色值',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('柱帽颜色透明度',obvious=True,readonly = True, group='柱帽颜色')
    data.setup('贴面红色值',obvious=True,readonly = True, group='贴面颜色')
    data.setup('贴面绿色值',obvious=True,readonly = True, group='贴面颜色')
    data.setup('贴面蓝色值',obvious=True,readonly = True, group='贴面颜色')
    data.setup('贴面颜色透明度',obvious=True,readonly = True, group='贴面颜色')
    data.setup('PVC围挡红色值',obvious=True,readonly = True, group='围挡颜色')
    data.setup('PVC围挡绿色值',obvious=True,readonly = True, group='围挡颜色')
    data.setup('PVC围挡蓝色值',obvious=True,readonly = True, group='围挡颜色')
    data.setup('PVC围挡颜色透明度',obvious=True,readonly = True, group='围挡颜色')
    data.setup('基础红色值',obvious=True,readonly = True, group='基础颜色')
    data.setup('基础绿色值',obvious=True,readonly = True, group='基础颜色')
    data.setup('基础蓝色值',obvious=True,readonly = True, group='基础颜色')
    data.setup('基础颜色透明度',obvious=True,readonly = True, group='基础颜色')

    data.setup('构件名称',obvious=True)


    data['replace'] = Prefabricated_fence
    p3d.MultiPointPlace.MultiPointFunction(data, '关键点')
    Prefabricated_fence(data)

    p3d.launchData(data)
