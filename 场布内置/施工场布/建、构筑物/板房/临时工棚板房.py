import pyp3d as p3d
def banfang(data:p3d.P3DData)->None:
    rota=data['旋转角度']
    l= data['长度']
    m= data['宽度']
    h_w=data['墙高度']
    j=  data['单位墙板长度']

    r_h=data['坡屋顶高度'] 
    r_t=data[ '屋顶厚度']   
    r_c=data['屋檐前外伸长度']
    r_ch=data['屋檐后外伸长度']          
    r_lc=data['山墙左侧外伸长度']
    r_lcr=data['山墙右侧外伸长度']

    m_g= data['门高度']
    m_k= data['门宽度']
    m_q= data['门距离墙距离']
    
    c_g= data['窗户高度']
    c_k= data['窗户宽度']
    c_h= data['窗台高度']
    c_q= data['窗户距离墙距离']

    di=data['地板厚度']        
    di_c=data['地板前外延长度']
    di_ch=data['地板后外延长度']          
    di_lc=data['地板左侧外延长度']
    di_lcr=data['地板右侧外延长度']
    k_k = 30         # 窗框宽度
    k_h = k_k+30     # 窗框厚度
    d_k = 30         # 门框宽度
    d_h = d_k+30     # 门框厚度
    data['场布分类']='建/构筑物'
    data['构件类型']='其他临建'

    #创建工棚  
    x1=p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(l,0,0),p3d.Vec3(l,0,h_w),p3d.Vec3(0,0,h_w)),p3d.Vec3(0,m,0)).color(1,1,1,1)
    x2=p3d.Extrusion((p3d.Vec3(100,100,0),p3d.Vec3(l-100,100,0),p3d.Vec3(l-100,100,h_w),p3d.Vec3(100,100,h_w)),p3d.Vec3(0,m-200,0)).color(1,1,1,1)   #墙厚100
    bb=p3d.substract(x1,x2) .color(0.95,0.95,0.95,1)


    #创建窗户洞和门洞，进行布尔减法，创建带窗洞和门洞的临时工棚
    cd=p3d.Box(p3d.Vec3(0,-150,0), p3d.Vec3(0,150,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  c_g, c_k, c_g, c_k).color(1,1,0,1) 
    cd=p3d.translation(c_q-k_k,0,c_h)*cd         #扣减体 900窗台高度，500距离墙体距离
    bb=p3d.substract(bb,cd).color(1,1,1,1)

    md = p3d.Box(p3d.Vec3(0,-150,0), p3d.Vec3(0,150,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  m_g, m_k, m_g, m_k).color(1,1,0,1) 
    md=p3d.translation(l-m_q-m_k,0,0)*md   #300距离墙体距离
    bb =p3d.substract(bb,md).color(1,1,1,1)

    #创建窗户
    #创建窗户玻璃
    b = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  c_g, c_k/2, c_g, c_k/2).color(1,1,1,0)   #10 玻璃厚度
    b=p3d.translation(k_k,k_h,k_k)*b  
    b1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  c_g, c_k/2, c_g, c_k/2).color(1,1,1,0) 
    b1=p3d.translation(k_k+c_k/2,k_h-10,k_k)*b1

    #创建窗框
    c_k_w=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,k_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), c_g+2*k_k, c_k+2*k_k, c_g+2*k_k, c_k+2*k_k).color(1,1,0,1) 
    c_k_n=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,k_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), c_g, c_k, c_g, c_k).color(1,1,0,1) 
    c_k_n=p3d.translation(k_k,0,k_k)*c_k_n
    ck =p3d.substract(c_k_w,c_k_n).color(1,1,1,1)

    #窗户组合
    c=p3d.combine(b,b1,ck)
    c=p3d.translation(c_q-k_k,-k_h,c_h-k_k)*c


    #创建门
    #创建门框
    m_wk=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,d_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), m_g, m_k, m_g, m_k).color(1,1,0,1) 
    m_nk=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,d_h,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), m_g-2*d_k, m_k-2*d_k, m_g-2*d_k, m_k-2*d_k).color(1,1,0,1) 
    m_nk=p3d.translation(d_k,0,d_k)*m_nk
    mk =p3d.substract(m_wk,m_nk).color(1,1,1,1)
    #创建门板
    mb=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,20,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0), m_g-2*d_k, m_k-2*d_k, m_g-2*d_k, m_k-2*d_k).color(1,1,0,1)   #20 门厚度
    mb=p3d.translation(d_k,d_h/2-10,d_k)*mb
    #创建有门洞的门板
    m_d=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,300,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300, 500,  300, 500).color(1,1,0,1) 
    m_d=p3d.translation(m_k/2-250,0,m_g-600)*m_d
    mb=p3d.substract(mb,m_d).color(1,1,1,1)

    #继续创建门玻璃
    m_b=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300, 500,  300, 500).color(1,1,1,0)                       #10 门玻璃厚度
    m_b=p3d.translation(m_k/2-250,d_h/2-5,m_g-600)*m_b

    #创建门玻璃框
    m_b_wk=p3d.Box(p3d.Vec3(0-10,0,0-10), p3d.Vec3(0-10,10,0-10), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300+20, 500+20,  300+20, 500+20).color(1,1,1,1)                      
    m_b_nk=p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,10,0), p3d.Vec3(0,0,1), p3d.Vec3(1,0,0),  300, 500,  300, 500).color(1,1,1,1)              #10 门玻璃框厚度               
    m_b_k=p3d.substract(m_b_wk,m_b_nk).color(1,1,1,1)
    m_b_k=p3d.translation(m_k/2-250,d_h/2-5-10,m_g-600)*m_b_k
    #门组合
    m1=p3d.combine(mk,mb,m_b,m_b_k)
    m1=p3d.translation(l-m_q-m_k,-d_h,0)*m1 
    # p3d.createGeometry(m1)


    #建立线
    zhu1=p3d.Extrusion((p3d.Vec3(0,0,0), p3d.Vec3(21,0,0), p3d.Vec3(14,-10,0), p3d.Vec3(7,-10,0)),p3d.Vec3(0,0,h_w))
    points1 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((int(l/j))*j,0,0),int(l/j))
    xiaozhu1 = p3d.combine() 
    for point in points1:
        xiaozhu1.append(p3d.translation(point) * zhu1)
    xiaozhu1=p3d.substract(xiaozhu1,cd)
    xiaozhu1=p3d.substract(xiaozhu1,md)

    zhu2=p3d.rotation(p3d.Vec3(0,0,1),-p3d.pi/2)*zhu1
    zhu2=p3d.translation(0,21,0)*zhu2
    points2 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,(int(m/j))*j,0),int(m/j))
    xiaozhu2 = p3d.combine() 
    for point in points2:
        xiaozhu2.append(p3d.translation(point) * zhu2)

    zhu3=p3d.rotation(p3d.Vec3(0,0,-1),p3d.pi)*zhu1
    zhu3=p3d.translation(21,0,0)*zhu3
    points3 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3((int(l/j))*j,0,0),int(l/j))
    xiaozhu3 = p3d.combine() 
    for point in points3:
        xiaozhu3.append(p3d.translation(point) * zhu3)
    xiaozhu3=p3d.translation(0,m,0)*xiaozhu3

    zhu4=p3d.rotation(p3d.Vec3(0,0,-1),-p3d.pi/2)*zhu1
    zhu4=p3d.translation(l,0,0)*zhu4
    points4 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,(int(m/j))*j,0),int(m/j))
    xiaozhu4 = p3d.combine() 
    for point in points4:
        xiaozhu4.append(p3d.translation(point) * zhu4)

    #建立屋顶
    roof=p3d.Extrusion((
        p3d.Vec3(0,-r_c,h_w),
        p3d.Vec3(0,m/2,h_w+r_h),
        p3d.Vec3(0,m+r_ch,h_w),
        p3d.Vec3(0,m+r_ch,h_w+r_t),
        p3d.Vec3(0,m/2,h_w+r_h+r_t),
        p3d.Vec3(0,-r_c,h_w+r_t)
        ),p3d.Vec3(l+r_lc+r_lcr,0,0)
    ).color(0/255,133/255,232/255,1)
    roof =p3d.translation(-r_lc,0,0)*roof

    #建立侧面屋顶
    roof1= p3d.Extrusion((
        p3d.Vec3(0,-r_c,h_w),
        p3d.Vec3(0,m+r_ch,h_w),
        p3d.Vec3(0,m/2,h_w+r_h),
    ),p3d.Vec3(100,0,0)
    ).color(1,1,1,1)
    roof2=p3d.translation(l-140,0,0)*roof1
    roof1=p3d.translation(40,0,0)*roof1

    #创建屋顶框
    r_kj=p3d.Extrusion((p3d.Vec3(0,m/2-20,h_w),p3d.Vec3(0,m/2+20,h_w),p3d.Vec3(0,m/2+20,h_w+r_h), p3d.Vec3(0,m/2-20,h_w+r_h)),p3d.Vec3(40,0,0)).color(1,1,1,1)  
    r_kj1=p3d.translation(0,0,0)*r_kj
    r_kj2=p3d.translation(l-40,0,0)*r_kj

    #创建整体
    wz=p3d.combine(bb,c,m1,xiaozhu1,xiaozhu2,xiaozhu3,xiaozhu4,roof,roof1,roof2,r_kj1,r_kj2)
    wz=p3d.translation(0,0,di)* wz
    di=data['地板厚度']        
    di_c=data['地板前外延长度']
    di_ch=data['地板后外延长度']          
    di_lc=data['地板左侧外延长度']
    di_lcr=data['地板右侧外延长度']
    wzd=p3d.Extrusion((p3d.Vec3(0-di_lc,0-di_c,0),p3d.Vec3(l+di_lcr,0-di_c,0), p3d.Vec3(l+di_lcr,m+di_ch,0), p3d.Vec3(0-di_lc,m+di_ch,0)),p3d.Vec3(0,0,di)).color(0/255,133/255,232/255,1)
    wz=p3d.combine(wz,wzd)
    wz=p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*rota/180)*wz
    data['板房']=wz
    data['窗框宽度']=k_k         
    data['窗框厚度']=k_h
    data['门框宽度']=d_k
    data['门框厚度']=d_h
if __name__ == "__main__":
    data = p3d.P3DData({
            '长度': 4400,  
            '宽度': 3000,
            '墙高度': 2500,
            '单位墙板长度':300,

            '坡屋顶高度':500,
            '屋顶厚度':100,
            '屋檐前外伸长度':200,
            '屋檐后外伸长度':200,
            '山墙左侧外伸长度':100,
            '山墙右侧外伸长度':100,

            '门高度': 2000,
            '门宽度': 900,
            '门距离墙距离':400,

            '窗户宽度': 1400,
            '窗户高度': 1000,
            '窗台高度':900,
            '窗户距离墙距离':400,
            '地板厚度':100,
            '地板前外延长度':100,
            '地板后外延长度':100,
            '地板左侧外延长度':100,
            '地板右侧外延长度':100,
            '窗框宽度':30,
            '窗框厚度':60,
            '门框宽度':30,
            '门框厚度':60,
            '旋转角度':0,
            '构件名称':'临时工棚板房'
        })
    
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('板房', show=True)
    # 设置可调整属性
    data.setup('旋转角度', obvious=True,group='场地参数')
    data.setup('长度', obvious=True, group='场地参数' )
    data.setup('宽度', obvious=True, group='场地参数' )
    data.setup('墙高度', obvious=True, group='场地参数' )
    data.setup('单位墙板长度', obvious=True, group='场地参数' )
    data.setup('屋顶厚度', obvious=True, group='屋顶参数' )
    data.setup('坡屋顶高度', obvious=True, group='屋顶参数' )
    data.setup('屋檐前外伸长度', obvious=True, group='屋顶参数' )
    data.setup('屋檐后外伸长度', obvious=True, group='屋顶参数' )
    data.setup('山墙左侧外伸长度', obvious=True, group='屋顶参数' )
    data.setup('山墙右侧外伸长度', obvious=True, group='屋顶参数' )
    data.setup('门高度', obvious=True, group='门参数' )
    data.setup('门宽度', obvious=True, group='门参数' )
    data.setup('门距离墙距离', obvious=True, group='门参数' )  
    data.setup('门框宽度', obvious=True,readonly=True,group='门参数' )
    data.setup('门框厚度', obvious=True,readonly=True,group='门参数' )
    data.setup('窗户高度', obvious=True, group='窗户参数' )
    data.setup('窗户宽度', obvious=True, group='窗户参数' )
    data.setup('窗台高度', obvious=True, group='窗户参数' )
    data.setup('窗户距离墙距离', obvious=True, group='窗户参数' )  
    data.setup('窗框宽度', obvious=True,readonly=True,group='窗户参数' )
    data.setup('窗框厚度', obvious=True,readonly=True,group='窗户参数' )
    data.setup('地板厚度', obvious=True, group='地板参数' )   
    data.setup('地板前外延长度', obvious=True, group='地板参数' )
    data.setup('地板后外延长度', obvious=True, group='地板参数' )
    data.setup('地板左侧外延长度', obvious=True, group='地板参数' )
    data.setup('地板右侧外延长度', obvious=True, group='地板参数' )
    data.setup('场布分类', obvious=True,group = '类型参数')
    data.setup('构件类型', obvious=True,group = '类型参数')
    data.setup('构件名称',obvious=True)
    # 设置replace算子
    data['replace'] = banfang
    banfang(data)
    # 发射数据到实例模板库
    p3d.launchData(data)

