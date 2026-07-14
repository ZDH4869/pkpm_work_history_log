import pyp3d as p3d
import math

def peidianfang(data:p3d.P3DData)->None:
     BYH = 10 # 百叶厚度
     BYK = 40  # 百叶宽度
     BYJ = 50  # 百叶间距
     FW = 30       # 门框厚度
     HD = data['房间宽度']
     HW = data['房间长度']
     HH = data['房间高度']
     HT = data['墙体厚度']
     BH = data['底座高度']
     DH = data['房门高度']
     WL = data['窗户长度']
     DW = data['房门宽度']
     WW = data['窗户宽度']
     DJ = data['窗户与门顶距离']+FW
     RC1 = data['外墙及房门红色值']
     RC2 = data['房顶红色值']
     GC1 = data['外墙及房门绿色值']    
     GC2 = data['房顶绿色值']    
     BC1 = data['外墙及房门蓝色值']    
     BC2 = data['房顶蓝色值']    
     RR = data['整体朝向角度°']

     #房门不能大于房间，窗户不能大于房门
     if DH > HH:
          DH = HH
     if DW > HW:
          DW = HW
     if WW > DW:
          WW = DW
     if WL > DH-DJ:
          WL = DH-DJ       
     #房门
     Door2 = p3d.Extrusion([p3d.Vec3((HW-DW)/2,0,0),p3d.Vec3(DW+(HW-DW)/2,0,0),p3d.Vec3(DW+(HW-DW)/2,0,DH),p3d.Vec3((HW-DW)/2,0,DH)],p3d.Vec3(0,HT,0))
     Door_sub = p3d.Extrusion([p3d.Vec3((HW-DW)/2+FW,0,0),p3d.Vec3(DW+(HW-DW)/2-FW,0,0),p3d.Vec3(DW+(HW-DW)/2-FW,0,DH-FW),p3d.Vec3((HW-DW)/2+FW,0,DH-FW)],p3d.Vec3(0,HT,0))
     Door_frame = p3d.substract(Door2,Door_sub).color(RC1/255,GC1/255,BC1/255,1)
     Door = p3d.Extrusion([p3d.Vec3((HW-DW)/2,2,0),p3d.Vec3(DW+(HW-DW)/2,2,0),p3d.Vec3(DW+(HW-DW)/2,2,DH),p3d.Vec3((HW-DW)/2,2,DH)],p3d.Vec3(0,0.5*HT,0)).color(RC1/255,GC1/255,BC1/255,1)
     window = p3d.Extrusion([p3d.Vec3((HW-WW)/2,0,DH-DJ),p3d.Vec3(WW+(HW-WW)/2,0,DH-DJ),p3d.Vec3(WW+(HW-WW)/2,0,DH-DJ-WL),p3d.Vec3((HW-WW)/2,0,DH-DJ-WL)],p3d.Vec3(0,0.5*HT,0))
     Door = p3d.substract(Door,window).color(RC1/255,GC1/255,BC1/255,1)
     window_outer = p3d.Extrusion([p3d.Vec3((HW-WW)/2-FW,0,DH-DJ+FW),p3d.Vec3(WW+(HW-WW)/2+FW,0,DH-DJ+FW),p3d.Vec3(WW+(HW-WW)/2+FW,0,DH-DJ-WL-FW),p3d.Vec3((HW-WW)/2-FW,0,DH-DJ-WL-FW)],p3d.Vec3(0,0.5*HT,0))
     Window_frame = p3d.substract(window_outer,window).color(RC1/255,GC1/255,BC1/255,0.1)
     BY = p3d.rotation(p3d.Vec3(1,0,0),-p3d.pi/5)*p3d.Box(p3d.Vec3(0,-0.5*BYH,-0.5*BYK),p3d.Vec3(WW,-0.5*BYH,-0.5*BYK),p3d.Vec3(0,1,0),p3d.Vec3(0,0,1),BYH,BYK,BYH,BYK)
     n = int(WL/BYJ)
     BYJ = WL / n 
     BY_List = p3d.combine()
     for i  in range(n-1):
          BY_List.append(p3d.translation(p3d.Vec3(0,0,-BYJ*i))*BY)
     BY = p3d.translation(p3d.Vec3((HW-WW)/2,0,DH-DJ-BYJ))*p3d.combine(BY_List)
     
     #房间及底座部分
     Box1 = p3d.Extrusion([p3d.Vec3(0,0,0),p3d.Vec3(HW,0,0),p3d.Vec3(HW,0,HH),p3d.Vec3(0,0,HH)],p3d.Vec3(0,HD,0))
     Box_sub = p3d.Extrusion([p3d.Vec3(HT,HT,HT),p3d.Vec3(HW-HT,HT,HT),p3d.Vec3(HW-HT,HT,HH),p3d.Vec3(HT,HT,HH)],p3d.Vec3(0,HD-2*HT,0))
     Box1 = p3d.substract(Box1,Box_sub)
     Box1 = p3d.substract(Box1,Door2).color(RC1/255,GC1/255,BC1/255,1)
     Box2 = p3d.Extrusion([p3d.Vec3(50,50,-BH),p3d.Vec3(HW-50,50,-BH),p3d.Vec3(HW-50,50,0),p3d.Vec3(50,50,0)],p3d.Vec3(0,HD-100,0)).color(150/255,150/255,150/255,1)

     #房顶
     head = p3d.Extrusion([p3d.Vec3(-40,-40,HH),p3d.Vec3(HW+40,-40,HH),p3d.Vec3(HW+40,-40,HH+50),p3d.Vec3(HW/2,-40,HH+150),p3d.Vec3(-40,-40,HH+50)],p3d.Vec3(0,HD+80,0)).color(RC2/255,GC2/255,BC2/255,1)
     #文字
     text2= p3d.Text("有电危险",90,90).color(236/255,240/255,22/255,1)
     text2= p3d.rotation(p3d.Vec3(1, 0, 0),p3d.pi*0.5)*text2
     text2= p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*1)*text2
     text2= p3d.translation(p3d.Vec3(HW/4,HD+2,HH-HH/4))*text2

     data['配电房'] = p3d.translation(p3d.Vec3(-50,-50,BH))*p3d.combine(Box1,Box2,Door_frame,Door,Window_frame,BY,text2,head)
     data['配电房'] = p3d.rotation(p3d.Vec3(0, 0, 1),p3d.pi*RR/180)*data['配电房']
if __name__ == "__main__":
    data = p3d.P3DData({
        '房间宽度':1500,
        '房间长度':3000,
        '房间高度':2200,
        '墙体厚度':100,
        '房门高度':2050,
        '窗户长度':900,
        '房门宽度':960,
        '窗户宽度':600,
        '窗户与门顶距离':50,
        '底座高度':150,
        '外墙及房门红色值':222,
        '外墙及房门绿色值':222,
        '外墙及房门蓝色值':222,
        '房顶红色值':0,
        '房顶绿色值':139,
        '房顶蓝色值':208,
        '场布分类':'构筑物',
        '构件类型':'电气设备',
        '整体朝向角度°':0,
        '构件名称':'组合式变压器配电房'
    })
#     data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('配电房', show = True)
    data.setup('房间宽度', obvious = True, group='房间')
    data.setup('房间长度', obvious = True, group='房间')
    data.setup('房间高度', obvious = True, group='房间')
    data.setup('墙体厚度', obvious = True, group='房间')
    data.setup('底座高度', obvious = True, group='底座')
    data.setup('房门高度', obvious = True, group='房门')
    data.setup('窗户长度', obvious = True, group='窗户')
    data.setup('房门宽度', obvious = True, group='房门')
    data.setup('窗户宽度', obvious = True, group='窗户')
    data.setup('窗户与门顶距离', obvious = True, group='窗户')
    data.setup('外墙及房门红色值', obvious = True, group='外墙及房门颜色')
    data.setup('外墙及房门绿色值', obvious = True, group='外墙及房门颜色')
    data.setup('外墙及房门蓝色值', obvious = True, group='外墙及房门颜色')
    data.setup('房顶红色值', obvious = True, group='房顶颜色')
    data.setup('房顶绿色值', obvious = True, group='房顶颜色')
    data.setup('房顶蓝色值', obvious = True, group='房顶颜色')
    data.setup('整体朝向角度°', obvious = True, group='整体')
    data.setup('场布分类', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件类型', obvious=True, readonly=True,group='类型参数')    
    data.setup('构件名称',obvious=True)
    data['replace'] = peidianfang
    peidianfang(data)
    p3d.launchData(data)