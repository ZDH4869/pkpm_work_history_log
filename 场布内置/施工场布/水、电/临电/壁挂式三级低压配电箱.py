import pyp3d as p3d
import math
def peidianxiang(data:p3d.P3DData)->None:
    BD = data['箱体深度']
    BW = data['箱体宽度']
    BH = data['箱体高度']
    DL1 = data['上半箱门长度']
    DL2 = data['下半箱门长度']
    DL3 = data['小箱门长度']
    DW1 = data['上半箱门宽度']
    DW2 = data['下半箱门宽度']
    DW3 = data['小箱门宽度']
    DJ = data['上半箱门与箱顶及与下半箱门距离']
    RC1 = data['箱体红色值']
    GC1 = data['箱体绿色值']    
    BC1 = data['箱体蓝色值']    
    RR = data['整体朝向角度°']
    AH = data['整体离地高度']
    #箱门不能大于箱体
    if DW1 > BW:
         DW1 = BW
    if DW2 > BW:
         DW2 = BW
    if DL2 > BH-DJ-DJ-DL1:
         DL2 = BH-DJ-DJ-DL1
    if DW3 > DW2:
         DW3 = DW2
    if DL3 > DL2:
         DL3 = DL2             
    #箱体部分
    Box1 = p3d.Extrusion((p3d.Vec3(1,0,0),p3d.Vec3(BW-1,0,0),p3d.Vec3(BW-1,0,BH),p3d.Vec3(1,0,BH)),p3d.Vec3(0,BD-2,0)).color(RC1/255,GC1/255,BC1/255,1)
    #箱门
    Door1 = p3d.Extrusion((p3d.Vec3((BW-DW1)/2,BD,BH-DJ-DL1),p3d.Vec3(DW1+(BW-DW1)/2,BD,BH-DJ-DL1),p3d.Vec3(DW1+(BW-DW1)/2,BD,BH-DJ),p3d.Vec3((BW-DW1)/2,BD,BH-DJ)),p3d.Vec3(0,1,0)).color(RC1/255,GC1/255,BC1/255,1)
    Door2 = p3d.Extrusion((p3d.Vec3((BW-DW2)/2,BD,BH-DJ-DL1-DJ-DL2),p3d.Vec3(DW2+(BW-DW2)/2,BD,BH-DJ-DL1-DJ-DL2),p3d.Vec3(DW2+(BW-DW2)/2,BD,BH-DJ-DL1-DJ),p3d.Vec3((BW-DW2)/2,BD,BH-DJ-DL1-DJ)),p3d.Vec3(0,1,0)).color(RC1/255,GC1/255,BC1/255,1)
    Door3 = p3d.Extrusion((p3d.Vec3((BW-DW3)/2,BD,BH-DJ-DL1-DJ-DL2/2+DL3/2),p3d.Vec3(DW3+(BW-DW3)/2,BD,BH-DJ-DL1-DJ-DL2/2+DL3/2),p3d.Vec3(DW3+(BW-DW3)/2,BD,BH-DJ-DL1-DJ-DL2/2-DL3/2),p3d.Vec3((BW-DW3)/2,BD,BH-DJ-DL1-DJ-DL2/2-DL3/2)),p3d.Vec3(0,2,0)).color(RC1/255,GC1/255,BC1/255,1)
    #箱顶檐
    head = p3d.Extrusion((p3d.Vec3(0,0,BH),p3d.Vec3(BW,0,BH),p3d.Vec3(BW,0,BH+10),p3d.Vec3(0,0,BH+10)),p3d.Vec3(0,BD+40,0)).color(RC1/255,GC1/255,BC1/255,1)
    #文字
    text= p3d.Text("5",50,50).color(236/255,240/255,22/255,1)
    text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text
    text= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text
    text= p3d.translation(p3d.Vec3(BW/2+35,BD+2,BH-DJ-DL1/2))*text
    text2= p3d.Text("有电危险",50,50).color(236/255,240/255,22/255,1)
    text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text2
    text2= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text2
    text2= p3d.translation(p3d.Vec3(BW/2+140,BD+2,BH-DJ-DL1/2-100))*text2

    data['配电箱'] = p3d.combine(Box1,Door1,Door2,Door3,text,text2,head)
    data['配电箱'] = p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*data['配电箱']
    data['配电箱'] = p3d.translation(p3d.Vec3(BW,BD,0))*data['配电箱']
    data['配电箱'] = p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*RR/180)*data['配电箱']
    data['配电箱'] = p3d.translation(p3d.Vec3(0,0,AH))*data['配电箱']
if __name__ == "__main__":
    data = p3d.P3DData({
        '箱体深度':350,
        '箱体宽度':650,
        '箱体高度':1300,
        '上半箱门长度':700,
        '下半箱门长度':450,
        '小箱门长度':200,
        '上半箱门宽度':600,
        '下半箱门宽度':600,
        '小箱门宽度':300,
        '上半箱门与箱顶及与下半箱门距离':50,
        '箱体红色值':0,
        '箱体绿色值':94,
        '箱体蓝色值':55,
        '整体朝向角度°':0,
        '整体离地高度':0,
        '场布分类':'构筑物',
        '构件类型':'电气设备',
        '构件名称':'壁挂式三级低压配电箱',
    })
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('配电箱', show = True)
    data.setup('箱体深度', obvious = True, group='箱体')
    data.setup('箱体宽度', obvious = True, group='箱体')
    data.setup('箱体高度', obvious = True, group='箱体')
    data.setup('上半箱门长度', obvious = True, group='上半箱门')
    data.setup('下半箱门长度', obvious = True, group='下半箱门')
    data.setup('小箱门长度', obvious = True, group='小箱门')
    data.setup('上半箱门宽度', obvious = True, group='上半箱门')
    data.setup('下半箱门宽度', obvious = True, group='下半箱门')
    data.setup('小箱门宽度', obvious = True, group='小箱门')
    data.setup('上半箱门与箱顶及与下半箱门距离', obvious = True, group='箱门')
    data.setup('箱体红色值', obvious = True, group='箱体颜色')
    data.setup('箱体绿色值', obvious = True, group='箱体颜色')
    data.setup('箱体蓝色值', obvious = True, group='箱体颜色')
    data.setup('整体朝向角度°', obvious = True, group='整体')
    data.setup('整体离地高度', obvious = True, group='整体')
    data.setup('场布分类', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件类型', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件名称',obvious=True)
    data['replace'] = peidianxiang
    peidianxiang(data)
    p3d.launchData(data)