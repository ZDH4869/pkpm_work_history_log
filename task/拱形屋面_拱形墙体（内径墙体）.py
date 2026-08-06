from pyp3d import *

class 拱形屋面_单拱(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件名称']=Attr('拱形屋面_单拱', obvious = True, readonly = False)
        self['外拱形半径']=Attr(8000.0, obvious = True, readonly = False)
        self['弦长']=Attr(13000.0, obvious = True)
        self['拱墙厚度'] = Attr(500.0, obvious = True)
        self['拱墙宽度']=Attr(5000.0, obvious = True)
        self['拱顶底墙高']=Attr(5500.0, obvious = True)
        self['屋面厚度']=Attr(200.0, obvious = True)
       
        self['拱形屋面_单拱'] = Attr(None, show = True)
        
        self.replace()

    @export
    def replace(self): 
        L = self['弦长']
        R = self['外拱形半径']
        W  = self['拱墙厚度']
        wall_height = self['拱顶底墙高']
        offset = self['拱墙宽度']
        H = self['屋面厚度']

        # ================================================================
        # 公共计算：拱矢高与圆弧角度
        # 圆心位于 (L/2, -z0)，半径 R
        # 弦两端点 A(0,0) 和 B(L,0)，弧线 A→B 顺时针经拱顶
        # ================================================================
        z0 = math.sqrt(R**2 - (L/2)**2)  # 拱矢高(正值)
        angle_pos = math.atan2(z0, L/2)
        angle_start = math.pi - angle_pos
        span = angle_start - angle_pos

        # ================================================================
        # 拱形矩形壳体 (Section + Sweep沿Y轴拉伸)
        #
        # 最终模型坐标系:
        #   弦两端在 (0,0,0) 和 (L,0,0), 弧圆心位于 (L/2, -z0), 半径 R
        #   A  = 拱顶曲线起点 = (0, 0, 0)
        #   B  = 拱顶曲线终点 = (L, 0, 0)
        #   A1 = A 沿 Z 偏移 -wall_height = (0, 0, -wall_height)
        #   B1 = B 沿 Z 偏移 -wall_height = (L, 0, -wall_height)
        #
        # 封闭截面: A →(弧线CW)→ B → B1 → A1 → A
        # 拉伸方向: Y轴, 起点0 → 终点W
        # ================================================================
        弧线_cw = translate(L/2, -z0) * rotate(angle_start) * scale(R, R) * Arc(-span)

        截面_矩形拱 = Section(
            Vec2(0, 0),
            弧线_cw,
            Vec2(L, 0),
            Vec2(L, -wall_height),
            Vec2(0, -wall_height),
        )

        截面_XOZ = rotx(pi/2) * 截面_矩形拱
        拉伸路径 = Line(Vec3(0, 0, 0), Vec3(0, W, 0))
        矩形壳体 = Sweep(截面_XOZ, 拉伸路径)

        # ================================================================
        # 拱形屋面壳体 (Section + Sweep沿Y轴拉伸)
        # 在XOY面创建拱形壳体截面 → rotx转XOZ → 沿Y轴正向拉伸W
        # 外弧与矩形壳体顶部弧线使用完全相同的Arc定义，保证拟合精度一致
        # ================================================================
        # 内弧端点计算
        inner_half = math.sqrt((R - H)**2 - (L/2)**2)
        y_inner_end = -z0 + inner_half
        inner_angle_pos = math.atan2(inner_half, L/2)
        
        # 外弧: 与矩形壳体顶部弧线完全相同的定义
        弧线_outer = translate(L/2, -z0) * rotate(angle_start) * scale(R, R) * Arc(-span)
        
        # 内弧: 从 (L, y_inner_end) 到 (0, y_inner_end) 逆时针
        弧线_inner = translate(L/2, -z0) * rotate(inner_angle_pos) * scale(R-H, R-H) * Arc(pi - 2*inner_angle_pos)
        
        # 封闭截面: (0,0) → 外弧 → (L,0) → (L,y_inner_end) → 内弧 → (0,y_inner_end) → 闭合
        截面_拱形壳体 = Section(
            Vec2(0, 0),
            弧线_outer,
            Vec2(L, 0),
            Vec2(L, y_inner_end),
            弧线_inner,
            Vec2(0, y_inner_end),
        )
        
        # 截面从XOY旋转到XOZ平面，沿Y轴正向拉伸W
        截面_XOZ_壳体 = rotx(pi/2) * 截面_拱形壳体
        拉伸路径_壳体 = Line(Vec3(0, 0, 0), Vec3(0, W, 0))
        拱形壳体 = Sweep(截面_XOZ_壳体, 拉伸路径_壳体)

        # ================================================================
        # 全屋切墙布尔体: 将矩形壳体掏空为墙体，再减去拱形壳体形成拱壳凹槽
        #   截面在 XOY 面绘制，沿 Z 轴从 R 拉伸到 -wall_height
        #   截面角点位于 (wall_thickness, wall_thickness)，
        #   X 向宽度 = L - 2*wall_thickness，Y 向长度 = W - 2*wall_thickness
        # ================================================================
        切墙路径 = Line(Vec3(0, 0, R), Vec3(0, 0, -wall_height))
        全屋切墙截面 = Section(
            Vec2(0+offset, 0),
            Vec2(L, 0),
            Vec2(L, W),
            Vec2(0+offset, W),
        )
        矩形壳体_结果 = 矩形壳体 - Sweep(全屋切墙截面, 切墙路径) - 拱形壳体

        self['拱形屋面_单拱'] = 矩形壳体_结果


# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_单拱()
    place(FinalGeometry)