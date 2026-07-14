from pyp3d import *
import math

def circularWorkpiece(data):
    R = data['环半径']
    r = data['管口半径']
    H = data['高度控制参数']
    alta = data['管口缩小参数']
    L = data['长度控制参数']

    contour = []
    contour_temp = []
    contours = []

    for i in range(L):
        for T in linspace(0, pi*2, 18):
            contour.append(Vec3((r-alta*i)*math.cos(T),0,(r-alta*i)*math.sin(T)))
        for c in contour:
            contour_temp.append(translation(Vec3(0,0,-H*i))
                * rotation(Vec3(0,0,1), i*pi/36)
                * translation(Vec3(R+(r-alta*i),0,0)) * c)
        contours.append(contour_temp)
        contour = []
        contour_temp = []
    
    circularWorkpiece = RuledSweepPlus(contours).color(0.5,0.5,0.5,1)
    data['环形工件'] = circularWorkpiece

if __name__ == "__main__":
    data = P3DData({
        '环半径': 1000,
        '管口半径': 200,
        '高度控制参数':2,
        '管口缩小参数':1.5,
        '长度控制参数':60,
        '构件名称':'环形工件'
    })
    data.set_view(0,0)
    data.setup('环形工件',  show=True)
    data.setup('环半径',  obvious=True, description='环半径')
    data.setup('管口半径',  obvious=True, description='管口半径')
    data.setup('高度控制参数',  obvious=True, description='高度控制参数')
    data.setup('管口缩小参数',  obvious=True, description='管口缩小参数')
    data.setup('长度控制参数',  obvious=True, description='长度控制参数')
    data.setup('构件名称',obvious=True)
    data['replace'] = circularWorkpiece
    circularWorkpiece(data)
    launchData(data)