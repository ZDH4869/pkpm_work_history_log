import pyp3d as p3d
import math
def peidianxiang(data:p3d.P3DData)->None:
    BD = data['箱体宽度']
    BW = data['箱体长度']
    BH = data['箱体高度']
    DL = data['箱门长度']
    DW = data['箱门宽度']
    DJ = data['箱门与箱顶距离']
    SH = data['脚部高度']
    RC1 = data['箱体正面红色值']
    GC1 = data['箱体正面绿色值']    
    BC1 = data['箱体正面蓝色值']    
    RC2 = data['箱体侧面红色值']    
    GC2 = data['箱体侧面绿色值']    
    BC2 = data['箱体侧面蓝色值']    
    RC3 = data['箱体背面红色值']    
    GC3 = data['箱体背面绿色值']    
    BC3 = data['箱体背面蓝色值']
    RR = data['整体朝向角度°']
    #箱门不能大于箱体
    if DW > BW:
         DW = BW
    if DL > BH-DJ:
         DL = BH-DJ
    #正背脚部支架
    stand1 = p3d.Extrusion((p3d.Vec3(0,0,0),p3d.Vec3(0,0,SH),p3d.Vec3(15,0,SH),p3d.Vec3(15,0,15),p3d.Vec3(35,0,15),p3d.Vec3(SH-15,0,SH),p3d.Vec3(SH,0,SH),p3d.Vec3(40,0,0)),p3d.Vec3(0,1,0)).color(169/255,169/255,169/255,1)
    stand2 = p3d.translation(p3d.Vec3(0,BD+1,0)) * stand1
    stand3 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*180/180) * stand1
    stand3 = p3d.translation(p3d.Vec3(BW,1,0)) * stand3
    stand4 = p3d.translation(p3d.Vec3(0,BD-1,0)) * stand3
    #侧面脚部支架
    stand5 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*90/180) * stand1
    stand5 = p3d.translation(p3d.Vec3(1,0,0)) * stand5
    stand6 = p3d.translation(p3d.Vec3(BW-1,0,0)) * stand5
    stand7 = p3d.rotation(p3d.Vec3(0,0,1),p3d.pi*270/180) * stand1
    stand7 = p3d.translation(p3d.Vec3(0,BD,0)) * stand7
    stand8 = p3d.translation(p3d.Vec3(BW-1,0,0)) * stand7
    stands = p3d.combine(stand1,stand2,stand3,stand4,stand5,stand6,stand7,stand8)
    #箱体部分
    Box1 = p3d.Extrusion((p3d.Vec3(1,0,SH),p3d.Vec3(BW-1,0,SH),p3d.Vec3(BW-1,0,SH+BH),p3d.Vec3(1,0,SH+BH)),p3d.Vec3(0,BD-2,0)).color(RC3/255,GC3/255,BC3/255,1)
    Box4 = p3d.Extrusion((p3d.Vec3(0,1,SH+1),p3d.Vec3(1,1,SH+1),p3d.Vec3(1,1,SH+BH-1),p3d.Vec3(0,1,SH+BH-1)),p3d.Vec3(0,BD,0)).color(RC2/255,GC2/255,BC2/255,1)
    Box3 = p3d.Extrusion((p3d.Vec3(BW-1,1,SH+1),p3d.Vec3(BW,1,SH+1),p3d.Vec3(BW,1,SH+BH-1),p3d.Vec3(BW-1,1,SH+BH-1)),p3d.Vec3(0,BD,0)).color(RC2/255,GC2/255,BC2/255,1)
    Box2 = p3d.Extrusion((p3d.Vec3(1,BD-1,SH+1),p3d.Vec3(BW-1,BD-1,SH+1),p3d.Vec3(BW-1,BD-1,SH+BH-1),p3d.Vec3(1,BD-1,SH+BH-1)),p3d.Vec3(0,1,0)).color(RC1/255,GC1/255,BC1/255,1)
    #闪电图标
    lighting = p3d.Extrusion((p3d.Vec3(BW/2,BD+1,SH+BH-DJ-DL/2-100),p3d.Vec3(BW/2-17,BD+1,SH+BH-DJ-DL/2-100+100),p3d.Vec3(BW/2+50,BD+1,SH+BH-DJ-DL/2-100-33),p3d.Vec3(BW/2-5,BD+1,SH+BH-DJ-DL/2-100-33),p3d.Vec3(BW/2+17,BD+1,SH+BH-DJ-DL/2-100-166),p3d.Vec3(BW/2-50,BD+1,SH+BH-DJ-DL/2-100)),p3d.Vec3(0,1,0)).color(236/255,240/255,22/255,1)
    #门把手与合页
    handle = p3d.Extrusion((p3d.Vec3((BW+DW)/2-30,BD+1,SH+BH-DJ-DL/2-40),p3d.Vec3((BW+DW)/2-30,BD+21,SH+BH-DJ-DL/2-30),p3d.Vec3((BW+DW)/2-30,BD+21,SH+BH-DJ-DL/2+30),p3d.Vec3((BW+DW)/2-30,BD+1,SH+BH-DJ-DL/2+40),p3d.Vec3((BW+DW)/2-30,BD+1,SH+BH-DJ-DL/2+35),p3d.Vec3((BW+DW)/2-30,BD+16,SH+BH-DJ-DL/2+30),p3d.Vec3((BW+DW)/2-30,BD+16,SH+BH-DJ-DL/2-30),p3d.Vec3((BW+DW)/2-30,BD+1,SH+BH-DJ-DL/2-35)),p3d.Vec3(-20,0,0)).color(RC1/255,GC1/255,BC1/255,1)
    hinge = p3d.RotationalSweep([p3d.Vec3(0,0,0),p3d.Vec3(5,0,0),p3d.Vec3(5,0,50),p3d.Vec3(0,0,50)],p3d.Vec3(0,0,0),p3d.Vec3(0,0,1),1*p3d.pi).color(RC1/255,GC1/255,BC1/255,1)
    hinge= p3d.translation(p3d.Vec3((BW-DW)/2,BD+2,SH+BH-DJ-DL/4-50))*hinge
    hinge2= p3d.translation(p3d.Vec3(0,0,-DL/2))*hinge
    #文字
    text= p3d.Text("低压配电箱",60,60).color(236/255,240/255,22/255,1)
    text= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text
    text= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text
    text= p3d.translation(p3d.Vec3(BW/2+213,BD+2,SH+BH-DJ-DL/2-100+325))*text
    text2= p3d.Text("有电危险",50,50).color(236/255,240/255,22/255,1)
    text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text2
    text2= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text2
    text2= p3d.translation(p3d.Vec3(BW/2+145,BD+2,SH+BH-DJ-DL/2-100-250))*text2
    #箱门
    Door1 = p3d.Extrusion((p3d.Vec3((BW-DW)/2,BD,SH+BH-DJ-DL),p3d.Vec3(DW+(BW-DW)/2,BD,SH+BH-DJ-DL),p3d.Vec3(DW+(BW-DW)/2,BD,SH+BH-DJ),p3d.Vec3((BW-DW)/2,BD,SH+BH-DJ)),p3d.Vec3(0,1,0)).color(RC1/255,GC1/255,BC1/255,1)
    data['配电箱'] = p3d.combine(stands,Box1,Box2,Box3,Box4,Door1,lighting,text,text2,handle,hinge,hinge2)
    data['配电箱']= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*data['配电箱']
    data['配电箱']= p3d.translation(p3d.Vec3(BW,BD,0))*data['配电箱']
    data['配电箱']= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*RR/180)*data['配电箱']
if __name__ == "__main__":
    data = p3d.P3DData({
        '箱体长度':650,
        '箱体宽度':350,
        '箱体高度':1300,
        '箱门长度':900,
        '箱门宽度':550,
        '箱门与箱顶距离':100,
        '脚部高度':100,
        '箱体正面红色值':0,
        '箱体正面绿色值':94,
        '箱体正面蓝色值':55,
        '箱体侧面红色值':255,
        '箱体侧面绿色值':0,
        '箱体侧面蓝色值':0,
        '箱体背面红色值':169,
        '箱体背面绿色值':169,
        '箱体背面蓝色值':169,
        '整体朝向角度°':0,
        '场布分类':'构筑物',
        '构件类型':'电气设备',
        '构件名称':'二级低压配电箱',
    })
    # data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('配电箱', show = True)
    data.setup('箱体宽度', obvious = True, group='箱体')
    data.setup('箱体长度', obvious = True, group='箱体')
    data.setup('箱体高度', obvious = True, group='箱体')
    data.setup('箱门长度', obvious = True, group='箱门',description = '箱门长不能大于箱体高')
    data.setup('箱门宽度', obvious = True, group='箱门',description = '箱门宽不能大于箱体宽')
    data.setup('箱门与箱顶距离', obvious = True, group='箱门')
    data.setup('脚部高度', obvious = True, group='脚部')
    data.setup('箱体正面红色值', obvious = True, group='箱体正面颜色')
    data.setup('箱体正面绿色值', obvious = True, group='箱体正面颜色')
    data.setup('箱体正面蓝色值', obvious = True, group='箱体正面颜色')
    data.setup('箱体侧面红色值', obvious = True, group='箱体侧面颜色')
    data.setup('箱体侧面绿色值', obvious = True, group='箱体侧面颜色')
    data.setup('箱体侧面蓝色值', obvious = True, group='箱体侧面颜色')
    data.setup('箱体背面红色值', obvious = True, group='箱体背面颜色')
    data.setup('箱体背面绿色值', obvious = True, group='箱体背面颜色')
    data.setup('箱体背面蓝色值', obvious = True, group='箱体背面颜色')
    data.setup('整体朝向角度°', obvious = True, group='整体')
    data.setup('场布分类', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件类型', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件名称',obvious=True)
    data['replace'] = peidianxiang
    peidianxiang(data)
    p3d.launchData(data)