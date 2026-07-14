import pyp3d as p3d 
import math

def test_NQ(data:p3d.P3DData)->None:
     
     B = data['片距'] # 片距
     D = data['散热器长度'] # 散热器长度
     E = data['散热器宽度'] # 散热器宽度
     F = data['接管长度'] # 接管长度
     H = data['接口半径'] # 接口半径
     I = data['壁厚'] # 壁厚
     L = data['中心距'] # 中心距
     C = L+55 # 散热器高度

     # 帽子
     box10 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,B), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), B, E, B, E) 
     box11 = p3d.Box(p3d.Vec3(0,0,0), p3d.Vec3(0,0,B), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), B/6, E-B/6*2, B/6, E-B/6*2) 
     K1 = p3d.translation(p3d.Vec3(B/6/2,B/6,0)) * box11
     K2 = p3d.translation(p3d.Vec3(B/6/2+B/6+B/6,B/6,0)) * box11
     K3 = p3d.translation(p3d.Vec3(B/6/2+B/6+B/6+B/6+B/6,B/6,0)) * box11
     K = p3d.combine(K1,K2,K3)
     MZ1 = p3d.substract(box10,K)
     MZ2 = p3d.translation(p3d.Vec3(0,0,C-B)) * MZ1
     MZ = p3d.combine(MZ1,MZ2)
     # p3d.createGeometry(MZ)

     # 暖气片
     box20 = p3d.Box(p3d.Vec3(0.05,B/6/2,B), p3d.Vec3(0.05,B/6/2,C-B), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), B-0.1, E-B/6, B-0.1, E-B/6)  
     # p3d.createGeometry(box20)
     Cone1 = p3d.Cone(p3d.Vec3(B/6*2,B/6,B),p3d.Vec3(B/6*2,B/6,C-B),B/6,B/6)
     Cone2 = p3d.translation(p3d.Vec3(B/6*2,0,0)) * Cone1
     box21 = p3d.Box(p3d.Vec3(B/6*2,0,B), p3d.Vec3(B/6*2,0,C-B), p3d.Vec3(1,0,0), p3d.Vec3(0,1,0), B-B/6*4, B/6,  B-B/6*4, B/6) 
     TC1 = p3d.combine(Cone1,Cone2,box21)
     # p3d.createGeometry(TC1)
     TC2 = p3d.translation(p3d.Vec3(B,E,0)) * p3d.rotation(p3d.Vec3(0,0,1),p3d.pi) * TC1
     # p3d.createGeometry(TC2)
     NQP = p3d.combine(box20,TC1,TC2)

     # 接口
     JK1 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(-F,0,0),H,H)
     JK2 = p3d.Cone(p3d.Vec3(0,0,0),p3d.Vec3(-F,0,0),H-I,H-I)
     JK3 = p3d.substract(JK1,JK2)
     JK4 = p3d.translation(p3d.Vec3(0,E/2,(C-L)/2)) * JK3
     JK5 = p3d.translation(p3d.Vec3(0,0,L)) * JK4
     JK6 = p3d.translation(p3d.Vec3(D+H,0,0)) * JK4
     JK7 = p3d.translation(p3d.Vec3(D+H,0,0)) * JK5
     JK = p3d.combine(JK4,JK5,JK6,JK7)
     # p3d.createGeometry(JK)

     # 组装暖气片
     NQ1 = p3d.combine(NQP,MZ)
     N = math.floor(D/B)
     points1 = p3d.linspace(p3d.Vec3(0,0,0),p3d.Vec3(D-B,0,0),N)
     NQ = [] 
     for point in points1:
         NQ.append(p3d.translation(point) * NQ1)
     # p3d.createGeometry(NQ)
     data['一个暖气'] = p3d.combine(NQ,JK)

if __name__ == "__main__":
    data = p3d.P3DData({
        '边距': '片距/2',
        '片距': 40,
        '散热器高度': '中心距+55',
        '散热器长度': 600,
        '散热器宽度': 60,
        '接管长度': 10,
        '接口管径': '2*接口半径',
        '接口半径': 7.5,
        '壁厚': 2,
        '中心距': 545,
        '构件名称':'电暖气'
    })


    data.set_view(-0.125*p3d.pi,-0.125*p3d.pi)
    data.setup('一个暖气', show=True)
    data.setup('边距', obvious=True, group='暖气', description='边距')
    data.setup('片距', obvious=True, group='暖气', description='片距')
    data.setup('散热器高度', obvious=True, group='暖气', description='散热器高度')
    data.setup('散热器长度', obvious=True, group='暖气', description='散热器长度')
    data.setup('散热器宽度', obvious=True, group='暖气', description='散热器宽度')
    data.setup('接管长度', obvious=True, group='暖气', description='接管长度')
    data.setup('接口管径', obvious=True, group='暖气', description='接口管径')
    data.setup('接口半径', obvious=True, group='暖气', description='接口半径')
    data.setup('壁厚', obvious=True, group='暖气', description='壁厚')
    data.setup('中心距', obvious=True, group='暖气', description='中心距')
    data.setup('构件名称',obvious=True)

    data['replace'] = test_NQ
    test_NQ(data)
    p3d.launchData(data)