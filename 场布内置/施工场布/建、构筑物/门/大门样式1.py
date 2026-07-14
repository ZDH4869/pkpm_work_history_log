import pyp3d as p3d
import math

def door1(data: p3d.P3DData) -> None:
    ps = data['柱子边长']   # 柱子边长side
    ph = data['柱子高度']   # 柱子高度
    dl = data['门总长']     # 门总长
    dh = data['门高']       # 门高度
    da_w = data['侧门宽']                 # 侧门宽
    da_h = data['侧门高']                 # 侧门高
    dg_d =data['门下边缘距离地面']         # 门下边缘距离地面
    da_d =data['侧门底部距门下边缘']         # 侧门底部距离门下边缘
    dt = data['门厚']          # 门厚度
    bolt_h = data['门栓高度']                   # 门栓高度
    rot = data['旋转角度']      # 旋转角度

    rot_d = data['大门开合角度']
    if rot_d <0 :
        rot_d = 0
        data['大门开合角度'] = rot_d
    if rot_d > 90:
        rot_d = 90
        data['大门开合角度'] = rot_d

    rot_da = data['侧门开合角度']
    if rot_da <0 :
        rot_da = 0
        data['侧门开合角度'] = rot_da
    if rot_da > 90:
        rot_da = 90
        data['侧门开合角度'] = rot_da
    rot_da = -rot_da

    dt_r = 50                   # 门下轮子半径
    dt_t = 20                   # 门下轮子厚度
    dh_t = 20                   # 门把手厚度
    dh_r = 20                   # 门把手半径
    dr_d = 200             # 侧门右边缘与右柱边缘距离
    hinge_h  = 50           # 合叶接柱部分圆柱体高度
    hinge_r = 20            # 合叶半径
    door_gap = 20       # 两门之间预留空隙
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
    
    red = (1, 0, 0, 1)
    white = (0.9, 0.9, 0.9, 1)
    green = (0, 1, 0, 1)
    blue = (0.2,0.2,1,1)

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
    # 大门宽限制
    if dl < da_w*2+dr_d+door_gap+4*hinge_r:
        dl = da_w*2+dr_d+door_gap+4*hinge_r
    
    # 判断侧门高
    if da_h >(dh-2*da_d):
        da_h = dh-2*da_d
        data['侧门高'] = da_h
    elif da_h < 2000:
        da_h = 2000
        data['侧门高'] = da_h
    # 判断侧门宽
    if da_w < 0.1*dl:
        da_w = 0.1*dl
        data['侧门宽'] = da_w

    # 门栓高度限制
    if bolt_h<1000 :
        bolt_h = 1000
        data['门栓高度'] = bolt_h
    elif bolt_h>1600 :
        bolt_h = 1600
        data['门栓高度'] = bolt_h
    
    
    # 门下距离地面限制
    if dg_d > 300:
        dg_d = 300
        data['门下边缘距离地面'] = dg_d

    # 侧门底部距门下边缘限制
    if da_d> 300:
        da_d =300
        data['侧门底部距门下边缘'] = da_d

    # 1. 建立柱子
    pillar1_b = p3d.Box(p3d.Vec3(0, 0, 0), p3d.Vec3(0, 0, 0.5*ph), 
                p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), ps, ps, ps, ps).color(blue)
    pillar1_t = p3d.Box(p3d.Vec3(0, 0, 0.5*ph), p3d.Vec3(0, 0, ph), 
                p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), ps, ps, ps, ps).color(white)
    pillar1 = p3d.combine(pillar1_b,pillar1_t)
    pillar2 = p3d.translation(p3d.Vec3(dl+ps, 0, 0)) * pillar1
    pillar = p3d.combine(pillar1, pillar2)

    # 2.1 建立单门
    # 建立单门横栏与柱连接处门合叶
    hinge1 = p3d.Cone(p3d.Vec3(ps+hinge_r, ps*0.5, dg_d),p3d.Vec3(ps+hinge_r, ps*0.5, dg_d+hinge_h),hinge_r,hinge_r).color(white) 
    hinge2 = p3d.Cone(p3d.Vec3(ps+hinge_r, ps*0.5, dg_d+hinge_h),p3d.Vec3(ps+hinge_r, ps*0.5, dg_d+2*hinge_h),hinge_r,hinge_r).color(white)       # 合叶为圆柱体半径为20mm
    hinge_base = p3d.combine(hinge1,hinge2)
    hinge_top = p3d.translation(p3d.Vec3(0,0,dh-2*hinge_h))* hinge_base

    door1 = p3d.Box(p3d.Vec3(ps+2*hinge_r, (ps - dt)*0.5, dg_d), p3d.Vec3(ps+2*hinge_r, (ps - dt)*0.5,dg_d+dh),
                     p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), dl/2-2*hinge_r-door_gap, dt, dl/2-2*hinge_r-door_gap, dt).color(blue)
    # 建立门下滑轮
    tyre_left = p3d.Cone(p3d.Vec3(ps+0.2*dl/2, ps*0.5, dt_r),
                         p3d.Vec3(ps+0.2*dl/2+dt_t, ps*0.5, dt_r), dt_r, dt_r).color(white)
    tyre_right = p3d.translation(p3d.Vec3(dt_r, 0, 0)) * tyre_left
    tyre_link1 = p3d.Cone(p3d.Vec3(ps+0.2*dl/2+dt_t, ps*0.5, dt_r), p3d.Vec3(
                        ps+0.2*dl/2+dt_t+2*dt_t, ps*0.5, dt_r), dt_r*0.2, dt_r*0.2).color(white)
    tyre_link2 = p3d.Cone(p3d.Vec3(ps+0.2*dl/2+1.5*dt_t, ps*0.5, dt_r), p3d.Vec3(
                        ps+0.2*dl/2+1.5*dt_t, ps*0.5, dg_d), dt_r*0.2, dt_r*0.2).color(white)
    tyre_1 = p3d.combine(tyre_left, tyre_right, tyre_link1, tyre_link2)
    tyre_2 = p3d.translation(0.6*dl/2, 0, 0)*tyre_1
    hinge_left = p3d.combine(hinge_top,hinge_base)
    tyre = p3d.combine(tyre_1, tyre_2)
    door_1 = p3d.combine(door1, tyre,hinge_left)
    

    # 平移多门
    door_2base = p3d.translation(p3d.Vec3(2*ps+dl, ps,0))*p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*door1
    hinge_right = p3d.translation(p3d.Vec3(2*ps+dl, ps,0))*p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*hinge_left
    door_sub = p3d.Box(p3d.Vec3(dl+ps-dr_d, ps*0.5-0.5*dt, dg_d+da_d), p3d.Vec3(dl+ps-dr_d, ps*0.5-0.5*dt, dg_d+da_d+da_h),
                            p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), -da_w, dt, -da_w, dt).color(blue)    
    door_addition = p3d.Box(p3d.Vec3(dl+ps-dr_d-hinge_r, ps*0.5-0.25*dt, dg_d+da_d), p3d.Vec3(dl+ps-dr_d-hinge_r, ps*0.5-0.25*dt, dg_d+da_d+da_h),
                             p3d.Vec3(1, 0, 0), p3d.Vec3(0, 1, 0), -da_w+hinge_r, 0.5*dt, -da_w+hinge_r, 0.5*dt).color(blue)    # 建立侧门
    ad_hinge1 = p3d.Cone(p3d.Vec3(dl+ps-dr_d-0.5*hinge_r,0.5*ps,dg_d+da_d+0.2*da_h),p3d.Vec3(dl+ps-dr_d-0.5*hinge_r,0.5*ps,dg_d+da_d+0.2*da_h+hinge_h),0.5*hinge_r,0.5*hinge_r)
    ad_hinge2 = p3d.Cone(p3d.Vec3(dl+ps-dr_d-0.5*hinge_r,0.5*ps,dg_d+da_d+0.7*da_h),p3d.Vec3(dl+ps-dr_d-0.5*hinge_r,0.5*ps,dg_d+da_d+0.7*da_h+hinge_h),0.5*hinge_r,0.5*hinge_r)
    handle = p3d.Cone(p3d.Vec3(dl+ps-dr_d-0.8*da_w, ps*0.5, 0.5*da_h+dg_d+da_d), 
                    p3d.Vec3(dl+ps-dr_d-0.8*da_w, ps*0.5-0.5*dt-dh_t,0.5*da_h+dg_d+da_d), dh_r, dh_r).color(white)
    door_2board = p3d.substract(door_2base, door_sub).color(blue)
    tyre_door2 = p3d.translation(dl/2, 0, 0)*tyre
    door_ad = p3d.combine(door_addition,handle)
    door_2= p3d.combine(door_2board,tyre_door2,hinge_right,ad_hinge1,ad_hinge2)

    # 门下距离低于110轮子消失
    if dg_d < 100+10:
        door_1 = p3d.combine(door1,hinge_left)
        door_2 = door_2= p3d.combine(handle,hinge_right)

    # =====建立门栓======
    # 建立门栓底座
    bolt_bottom1 = p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,bolt_t,0),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),bolt_l,bolt_w,bolt_l,bolt_w)
    # 建立栓环一和二
    bolt_loop = p3d.translation(0.2*bolt_l,-bolt_r+bolt_rg,0.5*bolt_w)*p3d.rotation(p3d.Vec3(0,1,0),0.5*p3d.pi)*p3d.TorusPipe(p3d.Vec3(0,0,0),
                            p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),bolt_r,bolt_rg,p3d.pi*2).color(white)
    bolt_loop2 = p3d.translation(0.4*bolt_l,0,0)*bolt_loop
    bolt_bottom2 = p3d.Box(p3d.Vec3(0.2*bolt_l+bolt_rg,0,0),p3d.Vec3(0.2*bolt_l+bolt_rg,bolt_t,0),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),bolt_hw,-bolt_hl,bolt_hw,-bolt_hl)

    # 建立栓环三
    box1 = p3d.Box(p3d.Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw-0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw),
                    p3d.Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw+0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),-3*bolt_t,-0.5*bolt_kl,-3*bolt_t,-0.5*bolt_kl)
    box2 = p3d.Box(p3d.Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw-0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw-0.1*bolt_kl),
                    p3d.Vec3(0.2*bolt_l+bolt_rg+0.5*bolt_hw+0.5*bolt_rg,0,-0.5*bolt_hl+0.5*bolt_kw-0.1*bolt_kl),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),
                    -3*bolt_t+0.2*bolt_kl,-0.5*bolt_kl+0.2*bolt_kl,-3*bolt_t+0.2*bolt_kl,-0.5*bolt_kl+0.2*bolt_kl)
    bolt_loop3 = p3d.substract(box1,box2)
    bolt_part1 = p3d.combine(bolt_bottom1,bolt_loop,bolt_loop2,bolt_loop3)

    bolt_part2 = p3d.combine(bolt_bottom2)
    # 建立栓子
    bolt_cone = p3d.Cone(p3d.Vec3(0,-bolt_cr,0.5*bolt_w),p3d.Vec3(bolt_cl,-bolt_cr,0.5*bolt_w),bolt_cr,bolt_cr).color(white)

    # 建立门栓把手
    bolt_handle1 = p3d.Box(p3d.Vec3(0.5*bolt_l-0.5*bolt_hw,0.5*bolt_ht-bolt_cr,bolt_w*0.5),
                    p3d.Vec3(0.5*bolt_l-0.5*bolt_hw,0.5*bolt_ht-bolt_cr-bolt_cr,bolt_w*0.5),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),bolt_hw ,-bolt_hl,bolt_hw ,-bolt_hl)
    bolt_handle2 = p3d.Cone(p3d.Vec3(0.5*bolt_l,0.5*bolt_ht-bolt_cr,bolt_w*0.5-bolt_hl),
                            p3d.Vec3(0.5*bolt_l,0.5*bolt_ht-bolt_cr-bolt_cr,bolt_w*0.5-bolt_hl),0.5*bolt_hw,0.5*bolt_hw).color(white)
    bolt_move = p3d.unite(bolt_handle1,bolt_handle2,bolt_cone )
    bolt_sub = p3d.Box(p3d.Vec3(0.5*bolt_l-0.5*bolt_kw,0.5*bolt_ht-bolt_cr-bolt_ht,bolt_w*0.5-0.5*bolt_hl),
                        p3d.Vec3(0.5*bolt_l-0.5*bolt_kw,0.5*bolt_ht-bolt_cr,bolt_w*0.5-0.5*bolt_hl),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),bolt_kw,-bolt_kl,bolt_kw,-bolt_kl)
    bolt_handle = p3d.substract(bolt_move,bolt_sub)
    bolt_base = p3d.combine(bolt_part1,bolt_part2,bolt_handle)
    bolt = p3d.translation(p3d.Vec3(ps+0.5*dl,0.5*(ps+dt)+bolt_t,bolt_h))*p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*bolt_base

    # 另一门上的栓孔
    bolt_b = p3d.Box(p3d.Vec3(-bolt_w,0,0),p3d.Vec3(-bolt_w,bolt_t,0),p3d.Vec3(1,0,0),p3d.Vec3(0,0,1),bolt_w,bolt_w,bolt_w,bolt_w)
    bolt_loop4 = p3d.translation(-0.5*bolt_w,-bolt_r+bolt_rg,0.5*bolt_w)*p3d.rotation(p3d.Vec3(0,1,0),0.5*p3d.pi)*p3d.TorusPipe(p3d.Vec3(0,0,0),
                            p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),bolt_r,bolt_rg,p3d.pi*2).color(white)
    bolt_another = p3d.combine(bolt_loop4,bolt_b)
    bolt2 = p3d.translation(p3d.Vec3(ps+0.5*dl+door_gap,0.5*(ps+dt)+bolt_t,bolt_h))*p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*bolt_another 
   
    D1 = p3d.translation(p3d.Vec3(ps+hinge_r,0.5*ps,0))*p3d.rotation(p3d.Vec3(0,0,1),rot_d*p3d.pi/180)*p3d.translation(p3d.Vec3(-ps-hinge_r,-0.5*ps,0))*p3d.combine(door_1,bolt)
    D2 = p3d.translation(p3d.Vec3(ps+dl-hinge_r,0.5*ps,0))*p3d.rotation(p3d.Vec3(0,0,1),-rot_d*p3d.pi/180)*p3d.translation(p3d.Vec3(-ps-dl+hinge_r,-0.5*ps,0))*p3d.combine(door_2,bolt2)
    Da = p3d.translation(p3d.Vec3(ps+dl-hinge_r,0.5*ps,0))*p3d.rotation(p3d.Vec3(0,0,1),-rot_d*p3d.pi/180)*p3d.translation(p3d.Vec3(-ps-dl+hinge_r,-0.5*ps,0))*door_ad
    Da = p3d.translation(p3d.Vec3(ps+dl-hinge_r-(dr_d-0.5*hinge_r)*math.cos(-rot_d*p3d.pi/180),0.5*ps-(dr_d-0.5*hinge_r)*math.sin(-rot_d*p3d.pi/180),0))*p3d.rotation(p3d.Vec3(0,0,1),-rot_da*p3d.pi/180)*p3d.translation(p3d.Vec3(-ps-dl+hinge_r+(dr_d-0.5*hinge_r)*math.cos(-rot_d*p3d.pi/180),-0.5*ps+(dr_d-0.5*hinge_r)*math.sin(-rot_d*p3d.pi/180),0))*Da
    FD1 = p3d.translation(p3d.Vec3(0,-0.5*ps,0))*p3d.combine(pillar,D1,D2,Da)
    FD1 = p3d.rotation(p3d.Vec3(0,0,1),rot*p3d.pi/180)* FD1
    data['大门1'] = FD1

    data['场布分类']='建/构筑物'
    data['构件类型']='其他临建'


if __name__ == "__main__":
    data = p3d.P3DData({
        '柱子边长': 400,
        '柱子高度': 3300,
        '门总长': 6000,
        '门高': 3000,
        '侧门宽': 800,
        '侧门高': 2100,
        '构件名称':'大门样式1',
        '门下边缘距离地面':150,
        '门厚':50,
        '侧门底部距门下边缘':150,
        '侧门开合角度':0,
        '门栓高度':1200,
        '大门开合角度':0,
        '旋转角度':0,
    })

    # data.set_view(1,1)
    # 输出构件
    data.setup('大门1', show=True)
    # 设置可调整属性
    data.setup('柱子边长', obvious=True, group='柱子', description='——————')
    data.setup('柱子高度', obvious=True, group='柱子', description='—————')
    data.setup('门总长', obvious=True, group='大门', description='—————')
    data.setup('门高', obvious=True, group='大门', description='—————')
    data.setup('门下边缘距离地面', obvious=True, group='大门', description='—————')
    data.setup('门厚', obvious=True, group='大门', description='—————')
    data.setup('大门开合角度', obvious=True, group='大门', description='—————')
    data.setup('侧门宽', obvious=True, group='侧门', description='—————')
    data.setup('侧门高', obvious=True, group='侧门', description='—————')
    data.setup('侧门底部距门下边缘', obvious=True, group='侧门', description='—————')
    data.setup('侧门开合角度', obvious=True, group='侧门', description='—————')
    data.setup('门栓高度', obvious=True, group='插栓', description='—————')
    data.setup('旋转角度', obvious=True, group='转角', description='—————')
    data.setup('场布分类', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件类型', obvious=True,readonly=True,group = '类型参数')
    data.setup('构件名称', obvious=True)   

    # 设置replace算子
    data['replace'] = door1
    door1(data)
    p3d.launchData(data)
    # 发射数据到实例模板库
