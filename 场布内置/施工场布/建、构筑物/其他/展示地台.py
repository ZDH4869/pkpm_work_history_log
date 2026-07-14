from pyp3d import *
import pyp3d as p3d
def test_box(data:p3d.P3DData)->None:
    Box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box2=p3d.Box(p3d.Vec3(data['底座平台长度']*0.5-data['底座垫块边长'],0,0),p3d.Vec3(data['底座平台长度']*0.5-data['底座垫块边长'],0,data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box3=p3d.Box(p3d.Vec3(data['底座平台长度']-data['底座垫块边长'],0,0),p3d.Vec3(data['底座平台长度']-data['底座垫块边长'],0,data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box4=p3d.Box(p3d.Vec3(0,data['底座平台宽度']*0.5-data['底座垫块边长'],0),p3d.Vec3(0,data['底座平台宽度']*0.5-data['底座垫块边长'],data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box5=p3d.Box(p3d.Vec3(0,data['底座平台宽度']-data['底座垫块边长'],0),p3d.Vec3(0,data['底座平台宽度']-data['底座垫块边长'],data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box6=p3d.Box(p3d.Vec3(data['底座平台长度']*0.5-data['底座垫块边长'],data['底座平台宽度']-data['底座垫块边长'],0),p3d.Vec3(data['底座平台长度']*0.5-data['底座垫块边长'],data['底座平台宽度']-data['底座垫块边长'],data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box7=p3d.Box(p3d.Vec3(data['底座平台长度']-data['底座垫块边长'],data['底座平台宽度']-data['底座垫块边长'],0),p3d.Vec3(data['底座平台长度']-data['底座垫块边长'],data['底座平台宽度']-data['底座垫块边长'],data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box8=p3d.Box(p3d.Vec3(data['底座平台长度']-data['底座垫块边长'],data['底座平台宽度']*0.5-data['底座垫块边长'],0),p3d.Vec3(data['底座平台长度']-data['底座垫块边长'],data['底座平台宽度']*0.5-data['底座垫块边长'],data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长'],data['底座垫块边长']).color(67/255,142/255,219/255,1)
    Box9=p3d.Box(p3d.Vec3(0,0,data['底座垫块边长']),p3d.Vec3(0,0,data['底座平台高度']+data['底座垫块边长']),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),data['底座平台长度'],data['底座平台宽度'],data['底座平台长度'],data['底座平台宽度']).color(67/255,142/255,219/255,1)
    
    data['展示地台']= p3d.combine(Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8,Box9)
    B=data['旋转角度']
    B1=p3d.rotation(p3d.Vec3(0,0,1),(p3d.pi/180)*B)*data['展示地台']
    data['展示地台']=B1
if __name__ == "__main__":
    data=p3d.P3DData({
        '场布分类':'辅助设施',
        '构件类型':'施工管理、技术（标准工艺等）展示区域',
        '构件名称':'展示地台',
        '底座垫块边长': 50,
        '底座平台长度': 2400,
        '底座平台宽度': 2000,
        '底座平台高度': 50,
        '旋转角度':0
        })
    data.setup('展示地台',show = True)
    data.setup('场布分类',obvious=True, readonly=True,group='公共属性', description='场布分类')
    data.setup('构件类型',obvious=True, readonly=True,group='公共属性', description='构件类型')
    
    
    data.setup('底座垫块边长' , obvious = True ,group='底座垫块参数' , description ='边长')
    data.setup('底座平台长度',obvious = True,group='底座平台参数' , description ='长')
    data.setup('底座平台宽度',obvious = True,group='底座平台参数' , description ='宽')
    data.setup('底座平台高度',obvious = True,group='底座平台参数' , description ='高度')
    data.setup('旋转角度',obvious=True,group='旋转位置',description='旋转角度')
    data.setup('构件名称',obvious=True)
    data['replace'] = test_box
    test_box(data)
    p3d.launchData(data)