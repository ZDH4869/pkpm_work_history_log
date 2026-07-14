import pyp3d as p3d

def lashdef(data:p3d.P3DData)->None:
    # 尺寸复制
    h_bucket = 1000
    b_bucket_bottom = 500
    b_bucket_top = 700
    b_bucket = 20               # 厚度
    h_lid = 60
    r_lidaxis = 10
    r_wheel = 100
    # 桶盖旋转轴定位
    y_axis = (b_bucket_bottom+b_bucket_top)*0.5+2*b_bucket+r_lidaxis
    z_axis = h_bucket
    x_word = 30
    y_word = 30
    h_word = 300
    theta = -data['桶盖打开角度']/180*p3d.pi
    alpha = data['垃圾桶旋转角度']/180*p3d.pi

    # 桶身外围
    bucket_outer_box = p3d.Box(
        p3d.Vec3(0,0,0),
        p3d.Vec3(-(b_bucket_top-b_bucket_bottom)/2,-(b_bucket_top-b_bucket_bottom)/2,h_bucket),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        b_bucket_bottom,
        b_bucket_bottom,
        b_bucket_top,
        b_bucket_top,
        )
    # 外径圆角
    fillet_outer = p3d.Cone(
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,0),
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,h_bucket),
        (2**0.5)/2*b_bucket_bottom-50,
        (2**0.5)/2*b_bucket_top-50,
    )
    bucket_outer = p3d.intersection(bucket_outer_box,fillet_outer)
    # 桶身内圈
    bucket_inner_box = p3d.Box(
        p3d.Vec3(b_bucket+0.01,b_bucket,b_bucket),
        p3d.Vec3(-(b_bucket_top-b_bucket_bottom)/2+b_bucket-0.01,-(b_bucket_top-b_bucket_bottom)/2+b_bucket,h_bucket),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        b_bucket_bottom-2*b_bucket,
        b_bucket_bottom-2*b_bucket,
        b_bucket_top-2*b_bucket,
        b_bucket_top-2*b_bucket,
        )
    # 内圈圆角
    fillet_inner = p3d.Cone(
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,0-0.01),
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,h_bucket+0.01),
        (2**0.5)/2*(b_bucket_bottom-2*b_bucket)-50,
        (2**0.5)/2*(b_bucket_top-2*b_bucket)-50,
    )
    bucket_inner = p3d.translation(p3d.Vec3(0,0,0.01)) * p3d.intersection(bucket_inner_box,fillet_inner)
    # 外圈减内圈生成桶身
    bucket = p3d.substract(bucket_outer,bucket_inner).color(0,120/255,0,1)
    # 桶口平台
    scarf_box = p3d.Box(
        p3d.Vec3(-(b_bucket_top-b_bucket_bottom)/2-b_bucket*2,-(b_bucket_top-b_bucket_bottom)/2-b_bucket*2,h_bucket-b_bucket-20),
        p3d.Vec3(-(b_bucket_top-b_bucket_bottom)/2-b_bucket*2,-(b_bucket_top-b_bucket_bottom)/2-b_bucket*2,h_bucket-20),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        b_bucket_top+4*b_bucket,
        b_bucket_top+4*b_bucket,
        b_bucket_top+4*b_bucket,
        b_bucket_top+4*b_bucket,
        )
    scarf_fillet = p3d.Cone(
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,0-0.01),
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,h_bucket+0.01),
        (2**0.5)/2*(b_bucket_top+4*b_bucket)-50,
        (2**0.5)/2*(b_bucket_top+4*b_bucket)-50,
        )
    scarf = p3d.intersection(scarf_box,scarf_fillet)
    scarf = p3d.substract(scarf,bucket_outer).color(0,120/255,0,1)
    # 桶盖
    lid_box = p3d.Box(
        p3d.Vec3(-(b_bucket_top-b_bucket_bottom)/2-b_bucket,-(b_bucket_top-b_bucket_bottom)/2-b_bucket,h_bucket-20),
        p3d.Vec3(-(b_bucket_top-b_bucket_bottom)/2-b_bucket,-(b_bucket_top-b_bucket_bottom)/2-b_bucket,h_bucket+h_lid),
        p3d.Vec3(1,0,0),
        p3d.Vec3(0,1,0),
        b_bucket_top+2*b_bucket,
        b_bucket_top+2*b_bucket,
        b_bucket_top+2*b_bucket,
        b_bucket_top+2*b_bucket,
        )
    lib_fillet = p3d.Cone(
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,0-0.01),
        p3d.Vec3(b_bucket_bottom/2,b_bucket_bottom/2,h_bucket+h_lid+0.01),
        (2**0.5)/2*(b_bucket_top+2*b_bucket)-50,
        (2**0.5)/2*(b_bucket_top+2*b_bucket)-50,
    )
    lid = p3d.intersection(lid_box,lib_fillet)
    lid = p3d.substract(lid,bucket_outer)
    # 桶盖旋转轴
    lidaxis = p3d.Cone(
        p3d.Vec3(0-0.01,y_axis,z_axis),
        p3d.Vec3(b_bucket_bottom+0.01,y_axis,z_axis),
        r_lidaxis,
        r_lidaxis,
    )
    # 连接环
    lidring = p3d.substract(
        p3d.Cone(
            p3d.Vec3(b_bucket_bottom/6,y_axis,z_axis),
            p3d.Vec3(b_bucket_bottom/6+b_bucket,y_axis,z_axis),
            r_lidaxis*1.5,
            r_lidaxis*1.5,
    ),lidaxis
    )
    # 轴_桶身连接块
    lid_connect_bucket = p3d.LineString(
        [p3d.Vec3(b_bucket_bottom/6,y_axis+r_lidaxis*1.5,z_axis),
        p3d.Vec3(b_bucket_bottom/6,y_axis+r_lidaxis*1.5,z_axis-20),
        p3d.Vec3(b_bucket_bottom/6,y_axis-r_lidaxis,z_axis-20-b_bucket),
        p3d.Vec3(b_bucket_bottom/6,y_axis-r_lidaxis*1.5,z_axis-20),
        p3d.Vec3(b_bucket_bottom/6,y_axis-r_lidaxis*1.5,z_axis),
        p3d.Vec3(b_bucket_bottom/6,y_axis+r_lidaxis*1.5,z_axis),
        ]
    )
    lid_connect_bucket = p3d.ExtrusionPlus([p3d.ContourLine([lid_connect_bucket])],p3d.Vec3(20,0,0))
    lid_connect_bucket = p3d.combine(
        lidring,
        p3d.substract(lid_connect_bucket,lidring),
        p3d.translation(p3d.Vec3(b_bucket_bottom*4/6,0,0))*lidring,
        p3d.translation(p3d.Vec3(b_bucket_bottom*4/6,0,0))*p3d.substract(lid_connect_bucket,lidring)
    )
    # 轴_桶盖连接件
    lid_connect_lid = p3d.LineString(
        [p3d.Vec3(b_bucket_bottom/6,y_axis,z_axis-r_lidaxis*1.5),
        p3d.Vec3(b_bucket_bottom/6,y_axis-r_lidaxis-2*b_bucket,z_axis-r_lidaxis*1.5),
        p3d.Vec3(b_bucket_bottom/6,y_axis-r_lidaxis-2*b_bucket,z_axis+r_lidaxis*1.5),
        p3d.Vec3(b_bucket_bottom/6,y_axis,z_axis+r_lidaxis*1.5),
        p3d.Vec3(b_bucket_bottom/6,y_axis,z_axis-r_lidaxis*1.5),]
    )
    lid_connect_lid = p3d.ExtrusionPlus([p3d.ContourLine([lid_connect_lid])],p3d.Vec3(20,0,0))
    lid_connect_lid = p3d.substract(lid_connect_lid,lidaxis)
    lid_connect_lid = p3d.combine(
        p3d.translation(p3d.Vec3(b_bucket_bottom*1/6,0,0))*lidring,
        p3d.translation(p3d.Vec3(b_bucket_bottom*1/6,0,0))*p3d.substract(lid_connect_lid,lidring),
        p3d.translation(p3d.Vec3(b_bucket_bottom*3/6,0,0))*lidring,
        p3d.translation(p3d.Vec3(b_bucket_bottom*3/6,0,0))*p3d.substract(lid_connect_lid,lidring)
    )

    lid = p3d.combine(lid,lid_connect_lid).color(0,120/255,0,1)
    bucket = p3d.combine(bucket,lid_connect_bucket,scarf).color(0,120/255,0,1)
    # bucket = p3d.substract(bucket,p3d.translation(p3d.Vec3(0,y_axis,z_axis))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi/2)*p3d.translation(p3d.Vec3(0,-y_axis,-z_axis))*lid
    # ).color(0,120/255,0,1)
    bucket = p3d.combine(bucket,lidaxis)
    # 盖子打开角度
    # lid = p3d.translation(p3d.Vec3(0,y_axis,z_axis))*p3d.rotation(p3d.Vec3(1,0,0),theta)*p3d.translation(p3d.Vec3(0,-y_axis,-z_axis))*lid
    # 车轮轴
    wheelaxis = p3d.Cone(
        p3d.Vec3(-2*b_bucket,b_bucket_bottom+2*b_bucket,r_wheel),
        p3d.Vec3(b_bucket_bottom+2*b_bucket,b_bucket_bottom+2*b_bucket,r_wheel),
        r_lidaxis,
        r_lidaxis,
    )
    # 车轮
    wheel = p3d.Cone(
        p3d.Vec3(-2*b_bucket,b_bucket_bottom+2*b_bucket,r_wheel),
        p3d.Vec3(-b_bucket,b_bucket_bottom+2*b_bucket,r_wheel),
        r_wheel,
        r_wheel,
    )
    wheel = p3d.substract(wheel,wheelaxis)
    wheel = p3d.combine(wheel,p3d.translation(b_bucket_bottom+3*b_bucket,0,0)*wheel).color(0,0,0,1)
    wheel_connect = p3d.translation(p3d.Vec3(0,-y_axis+b_bucket_bottom+2*b_bucket,-h_bucket+r_wheel))*lid_connect_lid
    wheel = p3d.combine(wheel,wheel_connect,wheelaxis)
    # 文字
    text = p3d.Text("保护环境 从我做起",x_word,y_word, "黑体").color(0.9,0.9,0.9, 1)
    text = p3d.translation(p3d.Vec3(0.5*(b_bucket_bottom-x_word*12), -h_word/10, h_word-5))*p3d.rotation(p3d.Vec3(1,0,0),p3d.pi*0.532)*text


    lash = p3d.combine(text,wheel,lid,bucket)
    lash = p3d.translation(p3d.Vec3(-b_bucket_bottom/2,-b_bucket_bottom/2,0))*lash
    lash = p3d.rotation(p3d.Vec3(0,0,1),alpha)*lash
    data['垃圾桶口长'] = b_bucket_top-2*b_bucket
    data['垃圾桶口宽'] = b_bucket_top-2*b_bucket
    data['垃圾桶高'] = h_bucket+h_lid
    data['垃圾桶'] = lash    

if __name__ == "__main__":
    data = p3d.P3DData({
        '垃圾桶旋转角度':0,
        '桶盖打开角度':0,
        '垃圾桶口长':0,
        '垃圾桶口宽':0,
        '垃圾桶高':0,
        '场布分类': '辅助设施' ,
        '构件类型': '垃圾存放' ,
        '构件名称': '垃圾桶1' ,

    })
    data.set_view = (0.125*p3d.pi,0.125*p3d.pi)
    data.setup('垃圾桶',show = True)
    data.setup('垃圾桶旋转角度',obvious = True,group = '布置参数')
    data.setup('桶盖打开角度',obvious = True,readonly = True,group = '外观参数')
    data.setup('垃圾桶口长',obvious = True,readonly = True,group = '外观参数')
    data.setup('垃圾桶口宽',obvious = True,readonly = True,group = '外观参数')
    data.setup('垃圾桶高',obvious = True,readonly = True,group = '外观参数')
    data.setup('场布分类', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件类型', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件名称',obvious=True)


    data['replace'] = lashdef
    lashdef(data)
    p3d.launchData(data)    