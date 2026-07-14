import pyp3d as p3d
import math
def peidianxiang(data:p3d.P3DData)->None:
    BD = data['箱体深度']
    BW = data['箱体宽度']
    BH = data['箱体高度']
    DL = data['左右箱门长度']
    DW1 = data['左半箱门宽度']

    DJ = data['箱门与箱顶距离']
    SH = data['脚部高度']
    BTF = data['顶盖前后延伸']
    BTL = data['顶盖左右延伸']
    RC1 = data['箱体红色值']
    GC1 = data['箱体绿色值']    
    BC1 = data['箱体蓝色值']    
    RR = data['整体朝向角度°']
    #箱门不能大于箱体
    if DW1 > BW:
         DW1 = BW
    if DL > BH-DJ:
         DL = BH-DJ
    #脚部
    stand1 = p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(40,0,0),p3d.Vec3(40,1,0),p3d.Vec3(1,1,0),p3d.Vec3(1,40,0),p3d.Vec3(0,40,0)),p3d.Vec3(-30,0,-SH)).color(RC1/255,GC1/255,BC1/255,1)
    stand2 = p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(40,0,0),p3d.Vec3(40,1,0),p3d.Vec3(1,1,0),p3d.Vec3(1,40,0),p3d.Vec3(0,40,0)),p3d.Vec3(0,-30,-SH)).color(RC1/255,GC1/255,BC1/255,1)
    stand2 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*90/180) * stand2
    stand3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*180/180) * stand1
    stand4 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*180/180) * stand2
    stand2 = p3d.translation(p3d.Vec3(BW,0,0)) * stand2
    stand3 = p3d.translation(p3d.Vec3(BW,BD,0)) * stand3
    stand4 = p3d.translation(p3d.Vec3(0,BD,0)) * stand4
    
    #箱体部分
    Box1 = p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(BW,0,0),p3d.Vec3(BW,0,BH),p3d.Vec3(0,0,BH)),p3d.Vec3(0,BD,0)).color(RC1/255,GC1/255,BC1/255,1)
    #箱门
    Door1 = p3d.Extrusion((p3d.Vec3(BW,BD,BH-DJ-DL),p3d.Vec3(BW-DW1,BD,BH-DJ-DL),p3d.Vec3(BW-DW1,BD,BH-DJ),p3d.Vec3(BW,BD,BH-DJ)),p3d.Vec3(0,2,0)).color(RC1/255,GC1/255,BC1/255,1)
    Door2 = p3d.Extrusion((p3d.Vec3(0,BD,BH-DJ-DL),p3d.Vec3(BW-DW1,BD,BH-DJ-DL),p3d.Vec3(BW-DW1,BD,BH-DJ),p3d.Vec3(0,BD,BH-DJ)),p3d.Vec3(0,2,0)).color(RC1/255,GC1/255,BC1/255,1)

    #箱顶檐
    head = p3d.Extrusion((p3d.Vec3(-BTL,-BTF,BH),p3d.Vec3(BW+BTL,-BTF,BH),p3d.Vec3(BW+BTL,BD+BTF,BH),p3d.Vec3(-BTL,BD+BTF,BH)),p3d.Vec3(0,0,10)).color(RC1/255,GC1/255,BC1/255,1)
    #文字
    text= p3d.Text("6",90,90).color(236/255,240/255,22/255,1)
    text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text
    text= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text
    text= p3d.translation(p3d.Vec3(BW-DW1/2+35,BD+3,BH-DJ-DL/2))*text
    text2= p3d.Text("有电危险",50,50).color(236/255,240/255,22/255,1)
    text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text2
    text2= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text2
    text2= p3d.translation(p3d.Vec3(BW-DW1/2+140,BD+3,BH-DJ-DL/2-100))*text2

    data['配电箱'] = p3d.combine(stand1,stand2,stand3,stand4,Box1,Door1,Door2,text,text2,head)
    data['配电箱'] = p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*data['配电箱']
    data['配电箱'] = p3d.translation(p3d.Vec3(BW,BD,SH))*data['配电箱']
    data['配电箱'] = p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*RR/180)*data['配电箱']
if __name__ == "__main__":
    data = p3d.P3DData({
        '箱体深度':350,
        '箱体宽度':950,
        '箱体高度':1300,
        '左右箱门长度':1200,
        '左半箱门宽度':600,
        '场布分类':'构筑物',
        '构件类型':'电气设备',
        '构件名称':'落地式三级低压配电箱',
        '箱门与箱顶距离':20,
        '脚部高度':300,
        '顶盖前后延伸':50,
        '顶盖左右延伸':50,
        '箱体红色值':0,
        '箱体绿色值':94,
        '箱体蓝色值':55,
        '整体朝向角度°':0,
    })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('配电箱', show = True)
    data.setup('箱体深度', obvious = True, group='箱体')
    data.setup('箱体宽度', obvious = True, group='箱体')
    data.setup('箱体高度', obvious = True, group='箱体')
    data.setup('左右箱门长度', obvious = True, group='箱门')
    data.setup('左半箱门宽度', obvious = True, group='箱门')
    data.setup('箱门与箱顶距离', obvious = True, group='箱门')
    data.setup('脚部高度', obvious = True, group='脚部')
    data.setup('顶盖前后延伸', obvious = True, group='顶盖')
    data.setup('顶盖左右延伸', obvious = True, group='顶盖')
    data.setup('箱体红色值', obvious = True, group='箱体颜色')
    data.setup('箱体绿色值', obvious = True, group='箱体颜色')
    data.setup('箱体蓝色值', obvious = True, group='箱体颜色')
    data.setup('整体朝向角度°', obvious = True, group='整体')
    data.setup('场布分类', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件类型', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件名称',obvious=True)
    data['replace'] = peidianxiang
    peidianxiang(data)
    p3d.launchData(data)