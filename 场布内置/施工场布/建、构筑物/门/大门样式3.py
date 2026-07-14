import pyp3d as p3d
from pyp3d import *


def door3(data: p3d.P3DData) -> None:
    ps = data['柱子边长']      # 柱子边长side
    ph = data['柱子高度']     # 柱子高度
    dl = data['门总长']       # 门总长
    dh = data['门高']         # 门高度
    v_hd  = data['竖向门栏间距']             # 竖向门栏间距
    h_dd = data['上下横向杆间距']            # 上下横向杆间距
    m_t = data['栏杆厚度']               # 单门围栏厚度
    m_w = data['栏杆宽度']               # 单门围栏宽度
    rot = data['旋转角度']      # 旋转角度
    dg_d =data['门下边缘距离地面']         #data['门下边缘距离地面'] 

    rot_d = data['大门开合角度']
    if rot_d <-90 :
        rot_d = -90
        data['大门开合角度'] = rot_d
    if rot_d > 90:
        rot_d = 90
        data['大门开合角度'] = rot_d


    spine_th = 80            # 刺头高
    spine_bh = 50            # 刺头下底座高
    spine_w = 50            # 刺头三角底边宽度
    hinge_h  = 50           # 合叶接柱部分圆柱体高度
    hinge_r = 20            # 合叶半径
    door_gap = 20           # 两门之间预留空隙

    bolt_t = 4          # 底座厚度4mm
    bolt_l = 150        # 底座长度150mm
    bolt_w = 20         # 底座宽度20mm
    bolt_r = 6          # 底座环半径6mm
    bolt_rg = 2         # 圆环管半径2mm
    bolt_cr = 4         # 插栓半径4mm
    bolt_cl = 150        # 插栓长150mm
    bolt_hl = 50        # 插栓把手长50mm
    bolt_hw = 10        # 插栓把手宽10mm
    bolt_ht = 4         # 插栓把手厚度4mm
    bolt_kw = 4         # 插栓把手孔宽4mm
    bolt_kl = 20         # 插栓把手孔长20mm
    bolt_h = 1200                  # 插栓高
    hw_l  = 100             # 单个花纹长度
    hw_gap = 200            
    red = (1,0,0,1)  
    white = (0.9,0.9,0.9,1) 
    green = (0,1,0,1)  
    black = (0.5,0.5,0.5,1)
    blue = (0,0,0.9,1)
    orange = (1, 0.5, 0, 1)
    white = (0.9,0.9,0.9,1) 

        # 柱高限制
    if ph < 2300:
        ph =2300
        data['柱子高度'] = ph
    

    # 大门高需要小于柱高
    if dh+dg_d>ph:
        dh = ph - dg_d
        data['门高'] = dh
    elif dh+dg_d<2300:
        dh = 2300 - dg_d
        data['门高'] = dh
    # 大门总长限制
    if dl < 2000:
        dl = 2000
        data['门总长'] = dl

    # 门栓高度限制
    if bolt_h<1000 :
        bolt_h = 1000
        data['门栓高度'] = bolt_h
    elif bolt_h>1600 :
        bolt_h = 1600
        data['门栓高度'] = bolt_h

    

    # 建立门栓底座
    bolt_bottom1 = p3d.Box(Vec3(0,0,0),Vec3(0,bolt_t,0),Vec3(1,0,0),Vec3(0,0,1),bolt_l,bolt_w,bolt_l,bolt_w)
    # 建立栓环一和二
    bolt_loop = p3d.translation(0.2*bolt_l,-bolt_r+bolt_rg,0.5*bolt_w)*p3d.rotation(Vec3(0,1,0),0.5*p3d.pi)*p3d.TorusPipe(Vec3(0,0,0),
                            Vec3(1,0,0),Vec3(0,1,0),bolt_r,bolt_rg,p3d.pi*2).color(white)
    bolt_loop2 = p3d.translation(0.4*bolt_l,0,0)*bolt_loop
    bolt_bottom2 = p3d.Box(Vec3(0.2*bolt_l+bolt_rg,0,0),Vec3(0.2*bolt_l+bolt_rg,bolt_t,0),Vec3(1,0,0),Vec3(0,0,1),bolt_hw,-bolt_hl,bolt_hw,-bolt_hl)

    # 建立栓环三
    box1 = p3d.Box(Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw-0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw),
                    Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw+0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw),Vec3(0,1,0),Vec3(0,0,1),-3*bolt_t,-0.5*bolt_kl,-3*bolt_t,-0.5*bolt_kl)
    box2 = p3d.Box(Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw-0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw-0.1*bolt_kl),
                    Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw+0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw-0.1*bolt_kl),Vec3(0,1,0),Vec3(0,0,1),
                    -3*bolt_t+0.2*bolt_kl,-0.5*bolt_kl+0.2*bolt_kl,-3*bolt_t+0.2*bolt_kl,-0.5*bolt_kl+0.2*bolt_kl)
    bolt_loop3 = p3d.substract(box1,box2)
    bolt_part1 = p3d.combine(bolt_bottom1,bolt_loop,bolt_loop2,bolt_loop3)
    bolt_part2 = p3d.combine(bolt_bottom2)
    # 建立栓子
    bolt_cone = p3d.Cone(Vec3(0,-bolt_cr,0.5*bolt_w),Vec3(bolt_cl,-bolt_cr,0.5*bolt_w),bolt_cr,bolt_cr).color(white)

    # 建立门栓把手
    bolt_handle1 = p3d.Box(Vec3(0.5*bolt_l-0.5*bolt_hw,0.5*bolt_ht-bolt_cr,bolt_w*0.5),
                    Vec3(0.5*bolt_l-0.5*bolt_hw,0.5*bolt_ht-bolt_cr-bolt_cr,bolt_w*0.5),Vec3(1,0,0),Vec3(0,0,1),bolt_hw ,-bolt_hl,bolt_hw ,-bolt_hl)
    bolt_handle2 = p3d.Cone(Vec3(0.5*bolt_l,0.5*bolt_ht-bolt_cr,bolt_w*0.5-bolt_hl),
                            Vec3(0.5*bolt_l,0.5*bolt_ht-bolt_cr-bolt_cr,bolt_w*0.5-bolt_hl),0.5*bolt_hw,0.5*bolt_hw).color(white)
    bolt_move = p3d.unite(bolt_handle1,bolt_handle2,bolt_cone )
    bolt_sub = p3d.Box(Vec3(0.5*bolt_l-0.5*bolt_kw,0.5*bolt_ht-bolt_cr-bolt_ht,bolt_w*0.5-0.5*bolt_hl),
                        Vec3(0.5*bolt_l-0.5*bolt_kw,0.5*bolt_ht-bolt_cr,bolt_w*0.5-0.5*bolt_hl),Vec3(1,0,0),Vec3(0,0,1),bolt_kw,-bolt_kl,bolt_kw,-bolt_kl)
    bolt_handle = p3d.substract(bolt_move,bolt_sub)
    bolt_base = p3d.combine(bolt_part1,bolt_part2,bolt_handle)
    bolt = p3d.translation(Vec3(ps+0.5*dl,0.5*(ps+m_t)+bolt_t,bolt_h))*p3d.rotation(Vec3(0,0,1),p3d.pi)*bolt_base

    # 另一门上的栓孔
    bolt_b = p3d.Box(Vec3(-bolt_w,0,0),Vec3(-bolt_w,bolt_t,0),Vec3(1,0,0),Vec3(0,0,1),bolt_w,bolt_w,bolt_w,bolt_w)
    bolt_loop4 = p3d.translation(-0.5*bolt_w,-bolt_r+bolt_rg,0.5*bolt_w)*p3d.rotation(Vec3(0,1,0),0.5*p3d.pi)*p3d.TorusPipe(Vec3(0,0,0),
                            Vec3(1,0,0),Vec3(0,1,0),bolt_r,bolt_rg,p3d.pi*2).color(white)
    bolt_another = p3d.combine(bolt_loop4,bolt_b)
    bolt2 = p3d.translation(Vec3(ps+0.5*dl+door_gap,0.5*(ps+m_t)+bolt_t,bolt_h))*p3d.rotation(Vec3(0,0,1),p3d.pi)*bolt_another 
  
    # 1. 建立柱子
    pillar_head =  p3d.Box(p3d.Vec3(-ps/4,-ps/4, ph), p3d.Vec3(-ps/4,-ps/4, ph+ps/2), p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), 1.5*ps, 1.5*ps, 1.5*ps, 1.5*ps).color(blue) 
    pillar_l1 = p3d.Box(p3d.Vec3(0, 0, 0), p3d.Vec3(0, 0, ph*0.5), p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), ps, ps, ps, ps).color(blue)   # 单柱子上部分
    pillar_l2 = p3d.Box(p3d.Vec3(0, 0, ph*0.5), p3d.Vec3(0, 0, ph), p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), ps, ps, ps, ps).color(white) # 单柱子下部分
    pillar1 = p3d.combine(pillar_head,pillar_l1,pillar_l2)
    pillar2 = p3d.translation(p3d.Vec3(dl+ps, 0, 0)) * pillar1
    pillar = p3d.combine(pillar1, pillar2)
    

    # 2. 建立单门4
    # 建立单门横栏与柱连接处门合叶
    hinge1 = p3d.Cone(p3d.Vec3(ps+hinge_r, ps*0.5, dg_d),p3d.Vec3(ps+hinge_r, ps*0.5, dg_d+hinge_h),hinge_r,hinge_r).color(white) 
    hinge2 = p3d.Cone(p3d.Vec3(ps+hinge_r, ps*0.5, dg_d+hinge_h),p3d.Vec3(ps+hinge_r, ps*0.5, dg_d+2*hinge_h),hinge_r,hinge_r).color(white)       # 合叶为圆柱体半径为20mm
    hinge_base = p3d.combine(hinge1,hinge2)
    hinge_top = p3d.translation(p3d.Vec3(0,0,dh-2*hinge_h))* hinge_base

    # 2.2 建立单门栏横栏与纵栏
    mem_h1 = p3d.Box(p3d.Vec3(ps+2*hinge_r,ps*0.5-m_t*0.5, dg_d),p3d.Vec3(ps+2*hinge_r,ps*0.5+m_t*0.5, dg_d), p3d.Vec3(1, 0, 0), p3d.Vec3(0, 0, 1),dl/2-door_gap/2-2*hinge_r,m_w,dl/2-door_gap/2-2*hinge_r,m_w)      # 外框横向
    mem_v1 = p3d.Box(p3d.Vec3(ps+2*hinge_r,ps*0.5-m_t*0.5, dg_d),p3d.Vec3(ps+2*hinge_r,ps*0.5+m_t*0.5, dg_d), p3d.Vec3(1, 0, 0), p3d.Vec3(0, 0, 1),m_w ,dh,m_w ,dh)              # 外框纵向
    mem_v2 = p3d.translation(p3d.Vec3(dl/2-door_gap/2-2*hinge_r-m_w, 0, 0))*mem_v1
    mem_h2 =  p3d.translation(p3d.Vec3(0, 0,dh-m_w ))*mem_h1
    mem_h3 = p3d.translation(p3d.Vec3(0, 0,-h_dd  ))*mem_h2
    mem_h4 = p3d.translation(p3d.Vec3(0, 0,h_dd  ))*mem_h1
    mem_part1 = p3d.unite(mem_h1,mem_v1,mem_v2,mem_h2,mem_h3,mem_h4)        # 外框建立          

    bar_base = p3d.Box(p3d.Vec3(ps+2*hinge_r,ps*0.5-m_t*0.5,dg_d+h_dd +m_w),p3d.Vec3(ps+2*hinge_r,ps*0.5+m_t*0.5,dg_d+h_dd+m_w),     
                    p3d.Vec3(1, 0, 0), p3d.Vec3(0, 0, 1),m_w ,dh-2*h_dd -2*m_w,m_w ,dh-2*h_dd-2*m_w)       # 内部门栏单个
    n = int((dl/2 - 1.2*v_hd )/v_hd )
    bar_left = p3d.combine()
    list_bar = [0 for i in range(n) ]
    for i in range(n):                                                                      
        list_bar[i] = p3d.translation(p3d.Vec3(v_hd *(i+1),0,0))*bar_base                                   # 内部门栏复制
        bar_left.append(list_bar[i])
    # bar_left = p3d.combine(list_bar)                                                                       # 内部门栏合并

    # 3.门栏上尖刺
    spine_base1 = p3d.Cone(Vec3(ps+2*hinge_r+v_hd+0.5*m_w ,ps*0.5,dh+dg_d),Vec3(ps+2*hinge_r+v_hd+0.5*m_w,ps*0.5,dh+dg_d+spine_bh), 
                    m_t/2,m_t/2)  
    spine_base2 = p3d.Box(Vec3(ps+2*hinge_r+v_hd ,ps*0.5-m_t*0.5,dh+dg_d+spine_bh),Vec3(ps+2*hinge_r+v_hd+0.5*spine_w,ps*0.5+0.01,dh+dg_d+spine_bh+spine_th), 
                        p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0),spine_w,m_t,0.1,0.1)    
    spine_base = p3d.combine(spine_base1,spine_base2) 
    spine_left = p3d.combine()
    list_spine = [0 for i in range(n) ]
    for i in range(n):                                                                      
        list_spine[i] = p3d.translation(p3d.Vec3(v_hd *i,0,0))*spine_base
        spine_left.append(list_spine[i])  
    door_left = p3d.combine(hinge_base,hinge_top,bar_left,mem_part1,spine_left)   
    door_right = p3d.translation(p3d.Vec3(2*ps+dl, ps,0))*p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*door_left

    # 4. 门上花纹
    n = int ((dl-door_gap-4*hinge_r)/2/hw_gap)
    HW1 = p3d.Box(Vec3(0.5*m_w,0,0),Vec3(0.5*m_w+0.8*hw_gap,0,h_dd),Vec3(1,0,0),Vec3(0,1,0),m_t,0.5*m_t,m_t,0.5*m_t)
    HW2 = p3d.Box(Vec3(0.5*m_w+0.8*hw_gap,0,0),Vec3(0.5*m_w,0,h_dd),Vec3(1,0,0),Vec3(0,1,0),m_t,0.5*m_t,m_t,0.5*m_t)
    HW_base = p3d.unite(HW1,HW2)
    HW_1 = p3d.translation(Vec3(ps+1.25*m_w,0.5*ps-0.25*m_t,dg_d+0.5*m_w))*HW_base
    hw_left1 = p3d.combine()
    list_hw = [0 for i in range(n) ]
    for i in range (n):
        list_hw[i] = p3d.translation(Vec3(i*hw_gap,0,0))*HW_1
        hw_left1.append(list_hw[i])
    hw_left2 = p3d.translation(Vec3(0,0,dh-2*m_w-(h_dd-m_w)))*hw_left1
    hw_right1 = p3d.translation(Vec3(dl/2-0.5*door_gap-2*hinge_r,0,0))*hw_left1
    hw_right2 = p3d.translation(Vec3(dl/2-0.5*door_gap-2*hinge_r,0,0))*hw_left2

    DL = p3d.translation(Vec3(ps+hinge_r,0.5*ps,0))*p3d.rotation(Vec3(0,0,1),rot_d*p3d.pi/180)*p3d.translation(Vec3(-ps-hinge_r,-0.5*ps,0))*p3d.combine(door_left,hw_left1,hw_left2,bolt)
    DR = p3d.translation(Vec3(ps+dl-hinge_r,0.5*ps,0))*p3d.rotation(Vec3(0,0,1),-rot_d*p3d.pi/180)*p3d.translation(Vec3(-ps-dl+hinge_r,-0.5*ps,0))*p3d.combine(door_right,hw_right1,hw_right2,bolt2)

    FD3 = p3d.translation(Vec3(0,-0.5*ps,0))*p3d.combine(DL,DR,pillar)
    FD3= p3d.rotation(Vec3(0,0,1),rot*p3d.pi/180)*FD3
    data['大门3'] = FD3

    data['场布分类']='建/构筑物'
    data['构件类型']='其他临建'
    



if __name__ == "__main__":
    data = p3d.P3DData({
        '柱子边长': 400,
        '柱子高度': 2700,
        '门总长': 5000,
        '门高': 2300,
        '门下边缘距离地面':150,
        '竖向门栏间距':150,
        '上下横向杆间距':200,
        '栏杆厚度':20,
        '栏杆宽度':50,
        '门栓高度':1200,
        '大门开合角度':0,
        '旋转角度':0,
        '构件名称':'大门样式3',
    })
    # data.set_view(1,1)
    # 输出构件
    data.setup('大门3', show=True)
    # 设置可调整属性
    data.setup('柱子边长', obvious=True, group='柱子', description='——————')
    data.setup('柱子高度', obvious=True, group='柱子', description='—————')
    data.setup('门总长', obvious=True, group='大门', description='—————')
    data.setup('门高', obvious=True, group='大门', description='—————')
    data.setup('门下边缘距离地面', obvious=True, group='大门', description='—————')
    data.setup('大门开合角度', obvious=True, group='大门', description='—————')
    data.setup('竖向门栏间距', obvious=True, group='门栏', description='—————')
    data.setup('上下横向杆间距', obvious=True, group='门栏', description='—————')
    data.setup('栏杆厚度', obvious=True, group='门栏', description='—————')
    data.setup('栏杆宽度', obvious=True, group='门栏', description='—————')
    data.setup('门栓高度', obvious=True, group='门栓', description='—————')
    data.setup('旋转角度', obvious=True, group='转角', description='—————')

    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称', obvious=True)   

    # 设置replace算子
    data['replace'] = door3
    door3(data)
    p3d.launchData(data)
    # 发射数据到实例模板库
