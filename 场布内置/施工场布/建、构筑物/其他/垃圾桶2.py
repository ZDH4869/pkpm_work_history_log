import pyp3d as p3d

def lashdef(data:p3d.P3DData)->None:
    # 参数赋值
    r_bucket = 300
    b_bucket = 10       # 筒壁厚度
    h_bucket = data['垃圾桶高度']

    r_concave = r_bucket-80     # 下凹平面半径
    h_concave = 50              # 下凹深度
    r_concave_sphere= ((r_concave)**2+(h_concave)**2)/(2*h_concave)     # 下凹球半径
    r_hole = r_bucket/2         # 筒口半径
    alpha = data['垃圾桶旋转角度']/180*p3d.pi


    bucket_cone = p3d.Cone(
        p3d.Vec3(0,0,0),
        p3d.Vec3(0,0,h_bucket),
        r_bucket,r_bucket
    )
    sphere_concave = p3d.Sphere(
        p3d.Vec3(0,0,h_bucket+r_concave_sphere-h_concave),
        r_concave_sphere
    )
    hole = p3d.Cone(
        p3d.Vec3(0,0,b_bucket),
        p3d.Vec3(0,0,h_bucket),
        r_hole,r_hole
    )
    bucket_concave = p3d.substract(bucket_cone,sphere_concave)
    bucket_concave_hole = p3d.substract(bucket_concave,hole).color(50/255,205/255,50/255,1)

    shell_outer = p3d.Sphere(
        p3d.Vec3(0,0,h_bucket),
        r_bucket
    )
    shell_inner = p3d.Sphere(
        p3d.Vec3(0,0,h_bucket),
        r_bucket-b_bucket
    )
    shell_tailor = p3d.Extrusion(
    [    p3d.Vec3(r_bucket,0,h_bucket),
        p3d.Vec3(r_bucket,0,h_bucket+r_bucket),
        p3d.Vec3(-r_bucket,0,h_bucket+r_bucket),
        p3d.Vec3(-r_bucket,0,h_bucket),
        p3d.Vec3(r_bucket,0,h_bucket),],p3d.Vec3(0,r_bucket,0)
    )
    shell = p3d.substract(shell_outer,shell_inner)
    shell = p3d.intersection(shell,shell_tailor).color(50/255,205/255,50/255,1)
    lash = p3d.combine(shell,bucket_concave_hole)
    lash = p3d.rotation(p3d.Vec3(0,0,1),alpha)*lash
    data['垃圾桶半径'] = r_bucket
    data['垃圾桶口半径'] = r_hole
    data['垃圾桶'] = lash   

if __name__ == "__main__":
    data = p3d.P3DData({
        '垃圾桶旋转角度':0,
        '垃圾桶高度':600,
        '垃圾桶半径':0,
        '垃圾桶口半径':0,
        '场布分类': '辅助设施' ,
        '构件类型': '垃圾存放' ,
        '构件名称': '垃圾桶2' ,
    })
    # data.set_view = (-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('垃圾桶',show = True)
    data.setup('垃圾桶旋转角度',obvious = True,group = '布置参数')
    data.setup('垃圾桶高度',obvious = True,group = '外观参数')
    data.setup('垃圾桶半径',obvious = True,readonly = True,group = '外观参数')
    data.setup('垃圾桶口半径',obvious = True,readonly = True,group = '外观参数')
    data.setup('场布分类', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件类型', obvious=True, readonly = True, group='类型参数(固定)')
    data.setup('构件名称',obvious=True)
    
    data['replace'] = lashdef
    lashdef(data)

    p3d.launchData(data)    
