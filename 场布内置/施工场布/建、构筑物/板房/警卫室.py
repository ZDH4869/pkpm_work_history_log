"""
    1. 定义门卫室底座
    2. 定义门卫室墙身
    3. 定义窗户
    4. 定义门卫室顶棚
"""

import pyp3d as p3d
from pyp3d import *
def guard(data:p3d.P3DData)->None:
    length = data['横墙长']         # 警卫室长
    wide = data['纵墙长']           # 警卫室宽度
    height = data['墙高']           # 警卫室高度
    w_t = data['墙厚']              # 墙厚度
    f_t = data['底座厚度']          # 底座厚度
    f_ts = data['底座伸出墙边']     # 底座伸出墙边距离
    d_w = data['门宽']             # 警卫室门宽度
    d_h = data['门高']             # 警卫室门高度
    w_h = data['窗高']              # 窗户高度
    w_w = data['窗宽']              # 窗户宽度
    w_tg = data['窗台高度']         # 窗台高宽
    rot = data['旋转角度']      # 旋转角度
    canopy_h = data['屋顶厚度']   # 屋顶厚度
    canopy_s = data['屋顶伸出墙边距离']   # 屋顶伸出墙边距离
    d_dw = data['门右侧距离墙外边缘']   # 门右侧距离墙外边缘
    window_sd = data['横墙窗距离墙边缘']                     # 南面窗距离墙边缘
    w_fw = 50       # 门框与窗框宽度
    w_fh = 50       # 门框与窗框厚度
    glass_t = 10    # 玻璃厚度

    red = (1,0,0,1)  
    white = (0.9,0.9,0.9,1) 
    green = (0,1,0,1)  
    black = (0.5,0.5,0.5,1)
    white_g =(0.9,0.9,0.9,0.1)
    blue = (0,0,0.9,1)

    # 横墙长限制
    if length < wide:
        length = wide+100
        data['横墙长'] = length
    # 墙高的限制
    if height<2300:
        height = 2300
        data['墙高'] = height
    
    # 门高的限制
    if d_h>height:
        d_h = height
        data['门高'] = height
    # 门宽的限制
    if d_w > 1200:
        d_w = 1200
        data['门宽'] = d_w
    if d_w < 600:
        d_w = 600
        data['门宽'] = d_w

    # 窗高限制
    if w_tg > 1200:
        w_tg = 1200
        data['窗台高度'] = w_tg
    # 窗高限制
    if w_h>height-w_tg:
        w_h = height-w_tg
        data['窗高'] = w_h
    # 纵墙窗宽限制
    if w_w>wide:
        w_w = wide
        data['窗宽'] = w_w
    # 窗边距限制
    if window_sd + w_w+w_fw >length - d_w - d_dw:
        window_sd = length - d_w - d_dw - w_w-w_fw
        data['横墙窗距离墙边缘'] = window_sd
    
    

   
    # 1. 定义门卫室底座
    foundation = p3d.Box(p3d.Vec3(-f_ts,-f_ts,0), p3d.Vec3(-f_ts,-f_ts,-f_t), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), 
                    length+2*f_ts, wide+2*f_ts, length+2*f_ts, wide+2*f_ts).color(black) 
    # p3d.createGeometry(foundation)

    # 2.1 定义门卫室墙身
    wall_base1 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,height), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), length,w_t, length, w_t).color(white)
    wall_door = p3d.Box(p3d.Vec3(length-d_dw,0,0), p3d.Vec3(length-d_dw,0,d_h), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), -d_w, w_t, -d_w, w_t).color(white)
    wall_base2 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,height), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0),w_t,wide ,w_t,wide).color(white)
    wall_1 = p3d.substract(wall_base1,wall_door)            # wall_1表示去除门后的墙体

    # 2.2 定义卫室门
    door_frame1= p3d.Box(p3d.Vec3(0,-0.5*w_fh,0), p3d.Vec3(0,0.5*w_fh,0), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), 
                    d_w, d_h, d_w, d_h).color(white)
    door_frame2= p3d.Box(p3d.Vec3(w_fw,-0.5*w_fh,w_fw), p3d.Vec3(w_fw,0.5*w_fh,w_fw), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), 
                    d_w-2*w_fw, d_h-2*w_fw, d_w-2*w_fw, d_h-2*w_fw).color(white)
    door_frame3= p3d.Box(p3d.Vec3(w_fw,-0.5*w_fh,d_h/2-w_fw), p3d.Vec3(w_fw,0.5*w_fh,d_h/2-w_fw), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), 
                    d_w-2*w_fw, w_fw, d_w-2*w_fw, w_fw).color(white)
    door_outframe = p3d.substract(door_frame1, door_frame2)
    door_window = p3d.Box(p3d.Vec3(w_fw,-0.5*glass_t,d_h/2), p3d.Vec3(w_fw,0.5*glass_t,d_h/2), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), 
                    d_w-2*w_fw, d_h/2, d_w-2*w_fw, d_h/2).color(white_g)
    inner_board = p3d.Box(p3d.Vec3(w_fw,0,0), p3d.Vec3(w_fw,0.5*w_fh,0), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), 
                    d_w-2*w_fw, d_h/2, d_w-2*w_fw, d_h/2).color(white)
    door =  p3d.translation(p3d.Vec3(length-d_w-d_dw,0,0))*p3d.combine(door_window,inner_board,door_outframe,door_frame3)

    # 3.1 定义窗
    window_frame1= p3d.Box(p3d.Vec3(-w_fw,-0.5*w_fh,-w_fw), p3d.Vec3(-w_fw,0.5*w_fh,-w_fw), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), 
                    w_w+2*w_fw, w_h+2*w_fw, w_w+2*w_fw, w_h+2*w_fw).color(white)
    window_frame2= p3d.Box(p3d.Vec3(0,-0.5*w_fh,0), p3d.Vec3(0,0.5*w_fh,0), p3d.Vec3(1,0,0), p3d.Vec3(0,0,1), w_w, w_h, w_w, w_h).color(white)
    window_frame = p3d.substract(window_frame1, window_frame2)
    wall_remove1 =  p3d.translation(p3d.Vec3(window_sd,0,w_tg))*window_frame1
    window_glass1 = p3d.Box(p3d.Vec3(0,-glass_t,0),p3d.Vec3(0,0,0),p3d.Vec3(1,0,0), p3d.Vec3(0,0,1),w_w/2,w_h,w_w/2,w_h).color(white_g)
    windows_glass2 = p3d.translation(p3d.Vec3(w_w/2,-glass_t,0))*window_glass1.color(white_g)
    windows_base = p3d.combine(window_frame,window_glass1,windows_glass2)           # 窗base原点
    # 3.2 将窗移动至指定位置
    windows1 =  p3d.translation(p3d.Vec3(window_sd,0,w_tg))*windows_base
    windows2_rot = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*0.5)*windows_base
    windows2 = p3d.translation(p3d.Vec3(0,(wide-w_w)/2,w_tg))*windows2_rot  # 西面窗
    wall_remove2 = p3d.translation(p3d.Vec3(0,(wide-w_w)/2,w_tg))*p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*0.5)*window_frame1
    wall_w1 = p3d.substract(wall_base2 ,wall_remove2)    

    wall_s =p3d.substract(wall_1,wall_remove1)          # wall_south 南面墙
    wall_w = p3d.combine(wall_w1 ,windows2)       # wall_west 西面墙 
    wall_n = p3d.translation(p3d.Vec3(0,wide-w_t,0))*wall_base1     # wall_north 北面墙 
    wall_e = p3d.translation(p3d.Vec3(length-w_t,0,0))*wall_w       # wall_west 西面墙 

    # p3d.createGeometry(wall_s)

    # 4. 定义门卫室顶棚
    canopy_body = p3d.Box(p3d.Vec3(-canopy_s,-canopy_s,height), p3d.Vec3(-canopy_s,-canopy_s,height+canopy_h), 
                p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), length+2*canopy_s, wide+2*canopy_s, length+2*canopy_s, wide+2*canopy_s).color(blue) 
    # p3d.createGeometry(canopy_body)
    FG = p3d.rotation(Vec3(0,0,1),rot*p3d.pi/180)*p3d.combine(canopy_body,door,wall_s,wall_w,wall_n,wall_e,windows1,windows2,foundation)
    data['警卫室'] = FG

if __name__ == "__main__":
    data = p3d.P3DData({
        '横墙长': 3000 ,
        '纵墙长': 2000,
        '墙高': 2300,
        '墙厚': 20,
        '门宽': 800,
        '门高': 2100,
        '窗高': 600,
        '窗宽': 900,
        '窗台高度':1000,
        '旋转角度':0,
        '底座厚度':30,
        '底座伸出墙边':30,
        '屋顶厚度':50,
        '屋顶伸出墙边距离':100,
        '门右侧距离墙外边缘':100,
        '横墙窗距离墙边缘':200,
        '构件名称':'警卫室'
        })
    
    # data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    # 输出构件
    data.setup('警卫室', show=True)
    # 设置可调整属性
    data.setup('横墙长', obvious=True, group='总尺寸', description='——————')
    data.setup('纵墙长', obvious=True, group='总尺寸', description='—————')
    data.setup('墙高', obvious=True, group='总尺寸', description='—————')
    data.setup('底座厚度', obvious=True, group='底座尺寸', description='—————')
    data.setup('底座伸出墙边', obvious=True, group='底座尺寸', description='—————')
    data.setup('门宽', obvious=True, group='门尺寸', description='—————')
    data.setup('门高', obvious=True, group='门尺寸', description='—————')
    data.setup('门右侧距离墙外边缘', obvious=True, group='门尺寸', description='—————')
    data.setup('窗高', obvious=True, group='窗尺寸', description='—————')
    data.setup('窗宽', obvious=True, group='窗尺寸', description='—————')
    data.setup('窗台高度', obvious=True, group='窗尺寸', description='—————')
    data.setup('横墙窗距离墙边缘', obvious=True, group='窗尺寸', description='—————')
    data.setup('屋顶厚度', obvious=True, group='屋顶', description='—————')
    data.setup('屋顶伸出墙边距离', obvious=True, group='屋顶', description='—————')
    data.setup('旋转角度', obvious=True, group='转角', description='—————')
    data.setup('构件名称',obvious=True)

    # 设置replace算子
    data['replace'] = guard
    guard(data)
    p3d.launchData(data)
    # 发射数据到实例模板库