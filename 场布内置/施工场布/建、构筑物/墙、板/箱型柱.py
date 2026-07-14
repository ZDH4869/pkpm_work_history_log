import pyp3d as p3d
import math
#箱型柱

def replace_operator(data:p3d.P3DData)->None:
    l=data['截面长度']
    w=data['截面宽度']
    t=data['截面厚度']
    h=data['柱高度']

    #定义截面
    outer=p3d.LineString([p3d.Vec3(0,0,0),\
        p3d.Vec3(l,0,0),\
        p3d.Vec3(l,w,0),\
        p3d.Vec3(0,w,0)])
    inner=p3d.LineString([p3d.Vec3(t,t,0),\
        p3d.Vec3(l-t,t,0),\
        p3d.Vec3(l-t,w-t,0),\
        p3d.Vec3(t,w-t,0)])
    A1=p3d.ContourLine([outer])
    A2=p3d.ContourLine([inner])
    data['箱型柱']=p3d.ExtrusionPlus([A1,-A2],p3d.Vec3(0,0,h)).color(1,1,0,0.5)

if __name__ == "__main__":
    data = p3d.P3DData({
        '截面长度': 500,
        '截面宽度': 500,
        '截面厚度': 25,
        '柱高度': 2000, 
        '构件名称':'箱型柱'
    })

    #设置视角
    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    #输出构件
    data.setup('箱型柱', show=True)
    #设置可调属性
    data.setup('截面长度', obvious=True, group='截面属性', description='截面长度')
    data.setup('截面宽度', obvious=True, group='截面属性', description='截面宽度')
    data.setup('截面厚度', obvious=True, group='截面属性', description='截面厚度')
    data.setup('柱高度', obvious=True, group='高度', description='柱高度')
    data.setup('构件名称',obvious=True)
    
    #设置replace算子 
    data['replace'] = replace_operator
    replace_operator(data)
    
    # 发射数据到实例模板库
    p3d.launchData(data)
