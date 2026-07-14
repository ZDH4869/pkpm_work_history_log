import pyp3d as p3d

def room(data:p3d.P3DData)->None:
    # 场地布置参数
    data1 = {       
        '场地区域总长':44000,
        '场地区域总宽':31000,
        '1号板房总长':42000,
        '1号板房统一深度':6000,
        '1号板房墙面高度':3000,
        '1号板房屋顶高度':1000,
        '1号板房统一厚度':100,          # 墙板、楼板统一
        '楼层':2,
        '走廊宽':1000,
        '楼梯踏面数':17,
        '屋顶厚度':100,
        '屋顶前沿伸出水平距离':800,
        '屋顶后沿伸出水平距离':100,
        '1号板房基点x':0,
        '1号板房基点y':0,
        '1号板房基点z':0,
    }
    # 墙面单元参数
    data2 = {
        '墙面颜色R':0.9,
        '墙面颜色G':0.9,
        '墙面颜色B':0.9,
        '门高':2100,
        '门宽':800,
        '门框宽':30,
        '门距基点x距离':500,
        '窗高':900,
        '窗宽':600,
        '窗距地':1000,
        '窗间隔':1700
        }
    # 原点参数赋值
    x_w = 0
    y_w = 0
    z_w = 0
    # 场地布置参数赋值
    x1 = data1['1号板房基点x']
    y1 = data1['1号板房基点y']
    z1 = data1['1号板房基点z']
    l1 = data['隔间进深']
    h1 = data['隔间层高']
    b1 = data['墙面、楼板厚度']
    b_roof = data['屋顶厚度']
    h_roof = data['屋顶高度']
    tg1 = h_roof/(l1/2)
    roof_inf = data['屋顶前沿伸出水平距离']
    roof_beh = data['屋顶后、两侧伸出水平距离']
    color_r = data2['墙面颜色R']
    color_g = data2['墙面颜色G']
    color_b = data2['墙面颜色B']
    n_floor = data['楼层数(1或2)']
    d_corri = data['走廊宽']
    n_stair = data['楼梯踏面数']
    l_stair = data['楼梯宽']
    h_stair = h1/n_stair
    d_stair = h_stair*1.2


    wall = [0]*5
    n = [0]*5
    wall[1] = data['左侧单间开间长度']
    n[1] = data['左侧单间数目']
    wall[2] = data['左侧大通间开间长度']
    n[2] = data['左侧大通间数目']
    wall[3] = data['右侧大通间开间长度']
    n[3] = data['右侧大通间数目']
    wall[4] = data['右侧单间开间长度']
    n[4] = data['右侧单间数目']
    xi = 0

    h_door = data['门高']
    d_door = data['门宽']
    t_door = data['门厚']
    x_door = data['门窗距离']
    b_door = data2['门框宽']
    h_win = data['窗高']
    d_win = data['窗宽']
    z_win = data['窗距地距离']
    x_win = 2*x_door+d_door
    if n_floor>2:
        n_floor = 1
    if n_floor<0:
        n_floor = 1
    #################################################################################################################
    #初始侧墙体(沿y轴方向)
    wall0_bottom = p3d.Extrusion((
        p3d.Vec3(x_w,y_w,z_w),
        p3d.Vec3(x_w+l1,y_w,z_w),
        p3d.Vec3(x_w+l1,y_w,z_w+h1),
        p3d.Vec3(x_w,y_w,z_w+h1),
        p3d.Vec3(x_w,y_w,z_w),
    ),p3d.Vec3(0,b1,0)
    ).color(color_r,color_g,color_b,1)
    wall0_top = p3d.Extrusion((
        p3d.Vec3(x_w,y_w,z_w+h1*n_floor),
        p3d.Vec3(x_w+l1,y_w,z_w+h1*n_floor),
        p3d.Vec3(x_w+l1/2,y_w,z_w+tg1*l1/2+h1*n_floor),
        p3d.Vec3(x_w,y_w,z_w+h1*n_floor),
    ),p3d.Vec3(0,b1,0)
    ).color(color_r,color_g,color_b,1)
    wall0_origin = p3d.combine(wall0_bottom)
    wall_y = p3d.translation(p3d.Vec3(x1+b1,y1,z1))*p3d.rotation(p3d.Vec3(0,0,1),0.5*p3d.pi)*wall0_origin
    wall0_top = p3d.translation(p3d.Vec3(x1+b1,y1,z1))*p3d.rotation(p3d.Vec3(0,0,1),0.5*p3d.pi)*wall0_top
    wall1 = wall_y
    # 不同隔间循环开始################################################################################################################
    # 不同隔间的循环，一共4个隔间，4次循环
    for i in range(1,5):
        # print('%d号隔间*************************************************'%i)
        # 隔间墙体组合，以个数和x轴长为参数
        # 隔间x方向的墙体
        wall_i_x = p3d.Extrusion((
            p3d.Vec3(xi,y_w,z_w),
            p3d.Vec3(xi+wall[i],y_w,z_w),
            p3d.Vec3(xi+wall[i],y_w,z_w+h1),
            p3d.Vec3(xi,y_w,z_w+h1),
            p3d.Vec3(xi,y_w,z_w),
        ),p3d.Vec3(0,b1,0)
        ).color(color_r,color_g,color_b,1)
        # 隔间三面墙组合，为一个复制单元
        wall_i_ori = p3d.combine(
        wall_i_x,
        p3d.translation(0,l1-b1,0)*wall_i_x,
        p3d.translation(xi+wall[i]-b1,0,0)*wall_y    
        )
        # 在三墙复制单元内，减门洞，加门框，生成门板
        # 外门洞
        door_out = p3d.Extrusion((
            p3d.Vec3(xi+x_door,y_w-20,z_w),
            p3d.Vec3(xi+x_door+d_door,y_w-20,z_w),
            p3d.Vec3(xi+x_door+d_door,y_w-20,z_w+h_door),
            p3d.Vec3(xi+x_door,y_w-20,z_w+h_door),
            p3d.Vec3(xi+x_door,y_w-20,z_w)
            ),p3d.Vec3(0,t_door+40,0)
        )
        # 内门洞
        door_in = p3d.Extrusion((
            p3d.Vec3(xi+x_door+b_door,y_w-30,z_w+b_door),
            p3d.Vec3(xi+x_door+d_door-b_door,y_w-30,z_w+b_door),
            p3d.Vec3(xi+x_door-b_door+d_door,y_w-30,z_w+h_door-b_door),
            p3d.Vec3(xi+x_door+b_door,y_w-30,z_w+h_door-b_door),
            p3d.Vec3(xi+x_door+b_door,y_w-30,z_w+b_door)
            ),p3d.Vec3(0,t_door+2*30,0)
        )
        # 门板
        door_plank = p3d.substract(
            p3d.Extrusion((
                p3d.Vec3(xi+x_door+b_door,y_w,z_w+b_door),
                p3d.Vec3(xi+x_door+d_door-b_door,y_w,z_w+b_door),
                p3d.Vec3(xi+x_door-b_door+d_door,y_w,z_w+h_door-b_door),
                p3d.Vec3(xi+x_door+b_door,y_w,z_w+h_door-b_door),
                p3d.Vec3(xi+x_door+b_door,y_w,z_w+b_door)
                ),p3d.Vec3(0,t_door,0)
            ),
            p3d.Cone(
                p3d.Vec3(xi+x_door+d_door-b_door-100,y_w-30,z_w+b_door+1000),
                p3d.Vec3(xi+x_door+d_door-b_door-100,y_w+t_door+60,z_w+b_door+1000),
                30,30
            )
        ).color(139/255,69/255,19/255,1)
        # 门框
        door_frame = p3d.substract(door_out,door_in)
        # 在三墙复制单元内减去外门框，不含门板与门框
        wall_i_doorhole = p3d.substract(wall_i_ori,door_out)

        # 在含门洞的三墙复制元内布置窗户
        n_win = (wall[i]-b1)//(x_win+d_win)                # 根据墙尺寸调节窗户个数
        # print('窗户个数：',n_win)
        xi_win = xi+x_win                               # 每个窗户布置的x轴基点
        wall_i_door_win_hole = wall_i_doorhole
        wall_i_door_glass = door_plank

        #窗循环开始---------------------------------------------------------------------------#
        # 每个窗户的布置循环，一共n_win次循环
        for i_win in range(n_win):              
            # 外窗洞
            win_out = p3d.Extrusion((
                p3d.Vec3(xi_win,y_w-20,z_w+z_win),
                p3d.Vec3(xi_win+d_win,y_w-20,z_w+z_win),
                p3d.Vec3(xi_win+d_win,y_w-20,z_w+z_win+h_win),
                p3d.Vec3(xi_win,y_w-20,z_w+z_win+h_win),
                p3d.Vec3(xi_win,y_w-20,z_w+z_win)
                ),p3d.Vec3(0,b1+2*20,0)
            ).color(color_r,color_g,color_b,1)
            # 内窗洞
            win_in = p3d.Extrusion((
                p3d.Vec3(xi_win+b_door,y_w-40,z_w+z_win+b_door),
                p3d.Vec3(xi_win+d_win-b_door,y_w-40,z_w+z_win+b_door),
                p3d.Vec3(xi_win+d_win-b_door,y_w-40,z_w+z_win+h_win-b_door),
                p3d.Vec3(xi_win+b_door,y_w-40,z_w+z_win+h_win-b_door),
                p3d.Vec3(xi_win+b_door,y_w-40,z_w+z_win+b_door)
                ),p3d.Vec3(0,b1+2*40,0)
            ).color(0,0,0,1)
            # 窗框
            win_frame = p3d.substract(win_out,win_in)
            # 玻璃
            win_i_glass = p3d.Extrusion((
                p3d.Vec3(xi_win+b_door,y_w,z_w+z_win+b_door),
                p3d.Vec3(xi_win+d_win-b_door,y_w,z_w+z_win+b_door),
                p3d.Vec3(xi_win+d_win-b_door,y_w,z_w+z_win+h_win-b_door),
                p3d.Vec3(xi_win+b_door,y_w,z_w+z_win+h_win-b_door),
                p3d.Vec3(xi_win+b_door,y_w,z_w+z_win+b_door)
                ),p3d.Vec3(0,b1/2,0)
            ).color(100/255,149/255,237/255,0.5)
            # 含门洞、窗洞的三墙复制元
            wall_i_door_win_hole = p3d.substract(wall_i_door_win_hole,win_out).color(color_r,color_g,color_b,1)
            # 窗户和门存储在一起
            wall_i_door_glass = p3d.combine(win_i_glass,wall_i_door_glass,win_frame)
            # glass.append(win_i_glass)         
            # 调整下一循环窗户布置X轴基点 
            xi_win = xi_win+x_win+d_win
        #---------------------------------------------------------------------------窗循环结束#
        # 组装墙、门、窗
        wall_i_door_win = p3d.combine(wall_i_door_win_hole,wall_i_door_glass,door_frame)
        # 隔间线性分布
        points_i = p3d.linspace(
        p3d.Vec3(0,y_w,z_w),
        p3d.Vec3((n[i]-1)*wall[i],y_w,z_w),
        n[i]
        )
        wall_i = p3d.combine() 
        for point in points_i:
            wall_i.append(p3d.translation(point) * wall_i_door_win)
        wall1 = p3d.combine(wall1,wall_i)
        # print(':隔间个数=%d,单元墙长度=%d,起始点=%d'%(n[i],wall[i],xi))
        #调整下一循环隔间基点
        xi = xi+n[i]*wall[i]   
    ################################################################################################################不同隔间循环结束#
    # 屋顶
    roof1 =  p3d.Extrusion((
        p3d.Vec3(-roof_beh,l1+roof_beh,n_floor*h1-tg1*roof_beh),
        p3d.Vec3(-roof_beh,l1/2,tg1*l1/2+n_floor*h1),
        p3d.Vec3(-roof_beh,-roof_inf,n_floor*h1-tg1*roof_inf),
        p3d.Vec3(-roof_beh,-roof_inf,n_floor*h1-tg1*roof_inf+b_roof),    
        p3d.Vec3(-roof_beh,l1/2,tg1*l1/2+n_floor*h1+b_roof),
        p3d.Vec3(-roof_beh,l1+roof_beh,n_floor*h1-tg1*roof_beh+b_roof),
        p3d.Vec3(-roof_beh,l1+roof_beh,n_floor*h1-tg1*roof_beh)
    ),p3d.Vec3(xi+2*roof_beh,0,0)
    ).color(0.2,0.2,0.8,1)
    # 屋顶和墙面之间的三角形区域循环
    xi = 0
    #————————————————————————————————————————————————————————————————————————
    for i in range(1,5):
        points_i_top = p3d.linspace(
        p3d.Vec3(xi+wall[i],y_w,z_w),
        p3d.Vec3(xi+(n[i])*wall[i],y_w,z_w),
        n[i]
        )
        wall_i = p3d.combine() 
        for point in points_i_top:
            wall_i.append(p3d.translation(point) * p3d.translation(-b1,0,0)*wall0_top)
        roof1 = p3d.combine(roof1,wall_i,wall0_top)
        xi = xi+n[i]*wall[i]   
    #——————————————————————————————————————————————————————————————————————
    # 楼面
    floor1 = p3d.Box(
        p3d.Vec3(x_w,y_w,z_w),
        p3d.Vec3(x_w,y_w,z_w-b1),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        xi,l1,
        xi,l1,
    )
    room = p3d.combine(wall1,roof1,floor1)
    # 二层以上布置
    if n_floor == 2:
        # 墙面复制
        wall2 = p3d.translation(
            p3d.Vec3(0,0,h1)
        )*wall1
        # 楼面复制
        floor2 = p3d.translation(
            p3d.Vec3(0,0,h1)
        )*floor1
        # 二层走廊
        corri2 = p3d.Box(
            p3d.Vec3(x_w-l_stair,y_w,z_w+h1*(n_floor-1)),
            p3d.Vec3(x_w-l_stair,y_w,z_w+h1*(n_floor-1)-b1),
            p3d.Vec3(1,0,0),
            p3d.Vec3(0,1,0),
            xi+l_stair*2,-d_corri,
            xi+l_stair*2,-d_corri,
        )
        # 扶手
        b_handrail = 30
        h_handrail = data['扶手高度']
        handrail_z = p3d.Box(
            p3d.Vec3(x_w-l_stair,y_w-d_corri,z_w+h1*(n_floor-1)),
            p3d.Vec3(x_w-l_stair,y_w-d_corri,z_w+h1*(n_floor-1)+h_handrail),
            p3d.Vec3(1,0,0),
            p3d.Vec3(0,1,0),
            b_handrail,b_handrail,
            b_handrail,b_handrail
        )
        # 走廊扶手立柱
        points_handrail_x = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(xi+2*l_stair-b_handrail,0,0),xi//300)
        handrail_x = p3d.combine()
        for p_hr_x in points_handrail_x:
            handrail_x.append(p3d.translation(p_hr_x) * handrail_z)
        points_handrail_y = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(0,d_corri-b_handrail,0),d_corri//300+1)
        handrail_y = p3d.combine()
        for p_hr_y in points_handrail_y:
            handrail_y.append(p3d.translation(p_hr_y) * handrail_z)
        handrail_y = p3d.combine(p3d.translation(p3d.Vec3(xi+2*l_stair-b_handrail,0,0))*handrail_y,handrail_y)

        # 楼梯立杆
        handrail_stair_z_ori = p3d.Box(
            p3d.Vec3(x_w-l_stair,y_w+d_stair+b1,z_w+h1*(n_floor-1)-h_stair),
            p3d.Vec3(x_w-l_stair,y_w+d_stair+b1,z_w+h1*(n_floor-1)-h_stair+h_handrail),
            p3d.Vec3(1,0,0),
            p3d.Vec3(0,1,0),
            b_handrail,b_handrail,
            b_handrail,b_handrail        
        )
        # 扶手横杆
        handrail_hori_x = p3d.Box(
            p3d.Vec3(x_w-l_stair,y_w-d_corri,z_w+h1*(n_floor-1)+h_handrail-b_handrail),
            p3d.Vec3(xi+l_stair,y_w-d_corri,z_w+h1*(n_floor-1)+h_handrail-b_handrail),
            p3d.Vec3(0,1,0),
            p3d.Vec3(0,0,1),
            b_handrail,b_handrail,
            b_handrail,b_handrail  
        )
        handrail_hori_y = p3d.Box(
            p3d.Vec3(x_w-l_stair,y_w-d_corri,z_w+h1*(n_floor-1)+h_handrail-b_handrail),
            p3d.Vec3(x_w-l_stair,y_w+b1+b_handrail,z_w+h1*(n_floor-1)+h_handrail-b_handrail),
            p3d.Vec3(1,0,0),
            p3d.Vec3(0,0,1),
            b_handrail,b_handrail,
            b_handrail,b_handrail  
        )
        handrail_hori_stair = p3d.Extrusion((
            p3d.Vec3(x_w-l_stair,y_w+b1+b_handrail,z_w+h1*(n_floor-1)+h_handrail-b_handrail),
            p3d.Vec3(x_w-l_stair+b_handrail,y_w+b1+b_handrail,z_w+h1*(n_floor-1)+h_handrail-b_handrail),
            p3d.Vec3(x_w-l_stair+b_handrail,y_w+b1+b_handrail,z_w+h1*(n_floor-1)+h_handrail+b_handrail-b_handrail),
            p3d.Vec3(x_w-l_stair,y_w+b1+b_handrail,z_w+h1*(n_floor-1)+h_handrail+b_handrail-b_handrail),
            p3d.Vec3(x_w-l_stair,y_w+b1+b_handrail,z_w+h1*(n_floor-1)+h_handrail-b_handrail)),
            p3d.Vec3(0,d_stair*n_stair,-h_stair*n_stair)
        )
        # 楼梯
        stair_y = p3d.Box(
            p3d.Vec3(x_w,y_w,z_w+h1*(n_floor-1)),
            p3d.Vec3(x_w,y_w,z_w+h1*(n_floor-1)-b1),
            p3d.Vec3(1,0,0),
            p3d.Vec3(0,1,0),
            -l_stair,d_stair,
            -l_stair,d_stair,
        )
        stair_x = p3d.Box(
            p3d.Vec3(x_w,y_w+d_stair,z_w+h1*(n_floor-1)),
            p3d.Vec3(x_w,y_w+d_stair,z_w+h1*(n_floor-1)-h_stair),
            p3d.Vec3(1,0,0),
            p3d.Vec3(0,1,0),
            -l_stair,b1,
            -l_stair,b1,
        )
        stair_ori = p3d.combine(stair_x,stair_y)
        stair1 = stair_ori
        handrail_stair_z = handrail_stair_z_ori
        for i_stair in range(n_stair):# 楼梯循环布置,联代楼梯扶手
            stair1 = p3d.combine(
            p3d.translation(0,d_stair*i_stair,0)*p3d.translation(0,0,-h_stair*i_stair)*stair_ori,
            stair1
            )
            handrail_stair_z= p3d.combine(
            p3d.translation(0,d_stair*i_stair,0)*p3d.translation(0,0,-h_stair*i_stair)*handrail_stair_z_ori,
            handrail_stair_z
            )
        # 扶手横杆组装
        handstair = p3d.unite(handrail_x,handrail_y,handrail_stair_z,handrail_hori_x,handrail_hori_y,handrail_hori_stair,
        p3d.translation(p3d.Vec3(xi+l_stair*2-b_handrail,0,0))*handrail_stair_z,
        p3d.translation(p3d.Vec3(xi+l_stair*2-b_handrail,0,0))*handrail_hori_y,
        p3d.translation(p3d.Vec3(xi+l_stair*2-b_handrail,0,0))*handrail_hori_stair)
        # 房屋组装
        room = p3d.combine(room,wall2,floor2,corri2,stair1,
        p3d.translation(p3d.Vec3(xi+l_stair,0,0))*stair1,
        handstair
        )
    data['总长度'] = xi    
    data['总深度'] = l1
    # if n_floor<3:    
    data['总高度'] = h1*n_floor+h_roof+b_roof    
    data['屋顶坡角'] = tg1    
    data['踢步高'] = h_stair
    data['踏面宽'] = d_stair    
    data['楼层数(1或2)'] = n_floor

    data['活动板房A1'] = room    
# 

if __name__ == "__main__":
    data = p3d.P3DData({
        '楼层数(1或2)':1,
        '左侧单间数目':4,
        '左侧大通间数目':1,
        '右侧大通间数目':1,
        '右侧单间数目':4,
        '左侧单间开间长度':3000,
        '左侧大通间开间长度':12000,
        '右侧大通间开间长度':15000,
        '右侧单间开间长度':3000,
        '隔间层高':3000,
        '隔间进深':6000,
        '墙面、楼板厚度':100,

        '屋顶高度':800,
        '屋顶坡角':0,
        '屋顶厚度':100,
        '屋顶前沿伸出水平距离':800,
        '屋顶后、两侧伸出水平距离':100,

        '门高':2100,
        '门宽':800,
        '门厚':100,

        '窗高':900,
        '窗宽':600,
        '窗距地距离':1000,
        '门窗距离':500,

        '楼梯踏面数':17,
        '楼梯宽':1000,
        '走廊宽':1000,
        '扶手高度':1200,
                
        '场布分类': '建/构筑物' ,
        '构件类型': '活动板房' ,
        '构件名称': '活动板房双楼梯' ,
    })
    # data.set_view(1,1)
    data.setup('活动板房A1',show = True)
    data.setup('总长度',obvious = True,readonly = True,group = '板房参数')
    data.setup('总深度',obvious = True,readonly = True,group = '板房参数')
    data.setup('总高度',obvious = True,readonly = True,group = '板房参数')
    data.setup('楼层数(1或2)',obvious = True,group = '板房参数')

    data.setup('左侧单间数目',obvious = True,group = '房间类型布置参数')
    data.setup('左侧大通间数目',obvious = True,group = '房间类型布置参数')
    data.setup('右侧大通间数目',obvious = True,group = '房间类型布置参数')
    data.setup('右侧单间数目',obvious = True,group = '房间类型布置参数')
    data.setup('左侧单间开间长度',obvious = True,group = '房间类型布置参数')
    data.setup('左侧大通间开间长度',obvious = True,group = '房间类型布置参数')
    data.setup('右侧大通间开间长度',obvious = True,group = '房间类型布置参数')
    data.setup('右侧单间开间长度',obvious = True,group = '房间类型布置参数')
    data.setup('隔间层高',obvious = True,group = '隔间布置参数')
    data.setup('隔间进深',obvious = True,group = '隔间布置参数')
    data.setup('墙面、楼板厚度',obvious = True,readonly = True,group = '隔间布置参数')

    data.setup('屋顶高度',obvious = True,group = '屋顶参数')
    data.setup('屋顶坡角',obvious = True,readonly = True,group = '屋顶参数')
    data.setup('屋顶厚度',obvious = True,readonly = True,group = '屋顶参数')
    data.setup('屋顶前沿伸出水平距离',obvious = True,group = '屋顶参数')
    data.setup('屋顶后、两侧伸出水平距离',obvious = True,group = '屋顶参数')

    data.setup('门高',obvious = True,group = '门参数')
    data.setup('门宽',obvious = True,group = '门参数')
    data.setup('门厚',obvious = True,group = '门参数')

    data.setup('窗高',obvious = True,group = '窗参数')
    data.setup('窗宽',obvious = True,group = '窗参数')
    data.setup('窗距地距离',obvious = True,group = '窗参数')
    data.setup('门窗距离',obvious = True,group = '窗参数')

    data.setup('楼梯踏面数',obvious = True,group = '楼梯、走廊参数')
    data.setup('踢步高',obvious = True,readonly = True,group = '楼梯、走廊参数')
    data.setup('踏面宽',obvious = True,readonly = True,group = '楼梯、走廊参数')
    data.setup('楼梯宽',obvious = True,group = '楼梯、走廊参数')
    data.setup('走廊宽',obvious = True,group = '楼梯、走廊参数')
    data.setup('扶手高度',obvious = True,group = '楼梯、走廊参数')
    data.setup('场布分类', obvious=True, readonly = True, group='类型参数')
    data.setup('构件类型', obvious=True, readonly = True, group='类型参数')
    data.setup('构件名称',obvious=True)

    data['replace'] = room
    room(data)
    p3d.launchData(data)    
