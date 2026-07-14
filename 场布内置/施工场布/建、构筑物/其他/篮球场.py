import pyp3d as p3d

def courtA(data:p3d.P3DData)->None:

    # 参数赋值
    data1 = {
        '篮球半场长':28000/2,
        '篮球场宽':15000,
        '线条宽':50,
        '中圈半径':1800,
        '三分半径':6750,
        '罚球线距离':5800,
        '三秒区底线宽':4900,
        '三秒区长':5800,
        '三秒区圆半径':1800,
    }
    data2 = {
        '篮筐定位点x':data1['篮球半场长']-1570,
        '篮筐定位点y':0,
        '篮筐定位点z':3050,
        '篮筐内圈半径':250,  
        '篮筐圈粗':10,  
        '篮板下沿高':2850,
        '篮板上沿高':3900,
        '篮板宽':1800,
        '篮架半径':100,
        '篮架水平长度':2000,
    }
    alpha = data['球场旋转角度']/180*p3d.pi
    l_court = data1['篮球半场长']
    b_court = data1['篮球场宽']
    b_line= data1['线条宽']
    r_middleround = data1['中圈半径']
    r_3p = data1['三分半径']
    l_3s = data1['三秒区长']
    d_3s = data1['三秒区底线宽']
    x_3s = l_court-l_3s
    r_3s= data1['三秒区圆半径']

    x_bas = data2['篮筐定位点x']
    y_bas = data2['篮筐定位点y']
    z_bas = data2['篮筐定位点z']
    r_bas = data2['篮筐内圈半径']
    r_bas_deta = data2['篮筐圈粗']
    b_board = data2['篮板宽']
    H_board = data2['篮板上沿高']
    h_board = data2['篮板下沿高']
    l_frame = data2['篮架水平长度']
    r_frame = data2['篮架半径']
    d_bas_board = r_bas+r_bas_deta+40


    ground_ori = p3d.Box(
        p3d.Vec3(0,-b_court/2,0),
        p3d.Vec3(0,-b_court/2,-2*b_line),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        l_court,b_court,
        l_court,b_court,
    )
    ground_ori = p3d.combine(
        ground_ori,
        p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*ground_ori
    )
    # 中圈线绘制
    line_middleround_outer = p3d.Cone(
        p3d.Vec3(0,0,0),
        p3d.Vec3(0,0,-b_line),
        r_middleround,
        r_middleround,
    )
    line_middleround_inner = p3d.Cone(
        p3d.Vec3(0,0,0),
        p3d.Vec3(0,0,-b_line),
        r_middleround-b_line,
        r_middleround-b_line,
    )
    line_middleround_tailor = p3d.Box(
        p3d.Vec3(0,-r_middleround-b_line,0),
        p3d.Vec3(0,-r_middleround-b_line,-b_line),
        p3d.Vec3(0,1,0),
        p3d.Vec3(1,0,0),
        2*(b_line+r_middleround),r_middleround+b_line,
        2*(b_line+r_middleround),r_middleround+b_line,
    )
    line_middleround = p3d.intersection(p3d.substract(line_middleround_outer,line_middleround_inner),line_middleround_tailor)
    
    # 边线绘制
    line_edge_outer = p3d.Box(
        p3d.Vec3(0,-b_court/2,0),
        p3d.Vec3(0,-b_court/2,-b_line),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        l_court,b_court,
        l_court,b_court,
    )
    line_edge_inner = p3d.Box(
        p3d.Vec3(b_line/2,-b_court/2+b_line,0),
        p3d.Vec3(b_line/2,-b_court/2+b_line,-b_line),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        l_court-1.5*b_line,b_court-2*b_line,
        l_court-1.5*b_line,b_court-2*b_line,
    )
    line_edge = p3d.substract(line_edge_outer,line_edge_inner)

    # 三分线绘制
    line_3p_outer = p3d.Cone(
        p3d.Vec3(x_bas,y_bas,0),
        p3d.Vec3(x_bas,y_bas,-b_line),
        r_3p,r_3p
    )
    line_3p_inner = p3d.Cone(
        p3d.Vec3(x_bas,y_bas,1),
        p3d.Vec3(x_bas,y_bas,-b_line-1),
        r_3p-b_line,r_3p-b_line
    )
    line_3p = p3d.substract(line_3p_outer,line_3p_inner)
    line_3p = p3d.intersection(line_3p,ground_ori)
    # 三秒区绘制
    area_3s = p3d.Box(
        p3d.Vec3(x_3s,-d_3s/2,0.01),
        p3d.Vec3(x_3s,-d_3s/2,-b_line-0.01),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        l_3s-b_line,d_3s,
        l_3s-b_line,d_3s,
    ).color(165/255, 42/255, 42/255,1)
    area_3s = p3d.combine(
        area_3s,
        p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*area_3s
    )
    circle_3s_outer = p3d.Cone(
        p3d.Vec3(x_3s,0,0),
        p3d.Vec3(x_3s,0,-b_line),
        r_3s,r_3s
    )
    circle_3s_inner = p3d.Cone(
        p3d.Vec3(x_3s,0,1),
        p3d.Vec3(x_3s,0,-b_line-1),
        r_3s-b_line,r_3s-b_line
    )
    line_circle_3s = p3d.substract(p3d.substract(circle_3s_outer,circle_3s_inner),area_3s)
    
    # 线条合并
    line = p3d.combine(
        line_edge,line_middleround,line_3p,line_circle_3s
    )
    line = p3d.combine(
        line,
        p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*line
    )
    # 场地组合
    ground = p3d.combine(
        p3d.substract(p3d.substract(ground_ori,line),area_3s).color(46/255, 139/255, 87/255,1),
        line,
        area_3s
    )
    # 篮球架绘制
    frame = p3d.FilletPipe(
        [p3d.Vec3(x_bas+l_frame,0,-b_line),
        p3d.Vec3(x_bas+l_frame,0,z_bas),
        p3d.Vec3(x_bas+d_bas_board+b_line,0,z_bas),
        ],[0,2*r_frame,0],r_frame
    )
    # 篮板绘制
    board = p3d.Box(
        p3d.Vec3(x_bas+d_bas_board,-b_board/2,h_board),
        p3d.Vec3(x_bas+d_bas_board,-b_board/2,H_board),
        p3d.Vec3(0,1,0),
        p3d.Vec3(1,0,0),
        b_board,b_line,
        b_board,b_line,
    )
    # 篮筐绘制
    basket_ring = p3d.TorusPipe(
        p3d.Vec3(x_bas,y_bas,z_bas),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        r_bas+r_bas_deta,r_bas_deta,2*p3d.pi
    )
    basket_tailor = p3d.Cone(
        p3d.Vec3(x_bas,y_bas,0),
        p3d.Vec3(x_bas,y_bas,H_board),
        r_bas+r_bas_deta,r_bas+r_bas_deta,
    )
    basket_connect = p3d.Box(
        p3d.Vec3(x_bas,y_bas-r_bas/2,z_bas+r_bas_deta),
        p3d.Vec3(x_bas,y_bas-r_bas/2,z_bas-r_bas_deta),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        d_bas_board,r_bas,
        d_bas_board,r_bas,
    )
    basket_connect = p3d.substract(p3d.substract(basket_connect,basket_tailor),basket_ring)
    basket = p3d.combine(basket_ring,basket_connect,board,frame)
    # 模型组合
    court = p3d.combine(
        ground,
        basket,
        p3d.rotation(p3d.Vec3(0,0,1),p3d.pi)*basket
    )
    court = p3d.rotation(p3d.Vec3(0,0,1),alpha)*court
    data['球场长'] = int(l_court*2)
    data['球场宽'] = b_court*1
    data['篮球场A'] = court
    
if __name__ == "__main__":
    data = p3d.P3DData({
        '球场旋转角度':0,
        '球场长':0,
        '球场宽':0,
        '场布分类': '辅助设施' ,
        '构件类型': '简易体育设施' ,
        '构件名称': '篮球场' ,
    })
    data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('篮球场A',show = True)
    data.setup('球场旋转角度',obvious = True,group = '布置参数')
    data.setup('球场长',obvious = True,readonly = True,group = '球场参数')
    data.setup('球场宽',obvious = True,readonly = True,group = '球场参数')
    data.setup('场布分类', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件类型', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件名称',obvious=True)
    data['replace'] = courtA
    courtA(data)
    p3d.launchData(data)    


















