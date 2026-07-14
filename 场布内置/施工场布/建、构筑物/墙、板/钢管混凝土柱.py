import pyp3d as p3d
import math

from pyp3d import *

def replace_Cone(data:p3d.P3DData)->None:
    d=data['柱直径']
    t=data['钢管厚度']
    h=data['柱高度']

    #定义截面
    Cone=p3d.Cone(p3d.Vec3(0,0,0),\
        p3d.Vec3(0,0,h),\
        (d/2-t),(d/2-t))
    data['混凝土']=Cone.color(190/255,190/255,190/255,1)
    outer=p3d.Ellipse(p3d.Vec3(0,0,0),\
        p3d.Vec3(d/2,0,0),\
        p3d.Vec3(0,d/2,0),\
        0,math.pi*2)
    inner=p3d.Ellipse(p3d.Vec3(0,0,0),\
        p3d.Vec3((d/2-t),0,0),\
        p3d.Vec3(0,(d/2-t),0),\
        0,math.pi*2)
    A1=p3d.ContourLine([outer])
    A2=p3d.ContourLine([inner])
    data['钢管']=p3d.ExtrusionPlus([A1,-A2],p3d.Vec3(0,0,h)).color(255/255,255/255,255/255,0.8)   

if __name__ == "__main__":
    data = p3d.P3DData({
        '柱直径': 500,
        '钢管厚度': 20,
        '柱高度': 2000,
        '构件名称':'钢管混凝土柱'
    })

    #设置视角
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    #输出构件
    data.setup('钢管', show=True)
    data.setup('混凝土', show=True)
    #设置可调属性
    data.setup('柱直径', obvious=True, group='截面属性', description='柱直径')
    data.setup('钢管厚度', obvious=True, group='截面属性', description='钢管厚度')
    data.setup('柱高度', obvious=True, group='高度', description='柱高度')
    data.setup('构件名称',obvious=True)
    
    #设置replace算子 
    data['replace'] = replace_Cone
    replace_Cone(data)
    
    # 发射数据到实例模板库
    p3d.launchData(data)
