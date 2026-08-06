from pyp3d import *
class 拱形屋面_单拱(Component):
    def __init__(self):
        Component.__init__(self)
        self['构件名称']=Attr('拱形屋面_单拱', obvious = True, readonly = False)
        self['拱形半径']=Attr(1360.0, obvious = True, readonly = False)
        self['弦长']=Attr(1800.0, obvious = True)
        self['屋面长度'] = Attr(3000.0, obvious = True)
        self['屋面厚度']=Attr(60.0, obvious = True)

        # 分组：布尔位置
        self['布尔位置']=Attr("无", obvious = True, readonly = False, combo= ["无","前左","前右","后左","后右"], group='布尔位置')
        self['布尔长']=Attr(900.0, obvious = True, group='布尔位置') 
        self['布尔宽']=Attr(400.0, obvious = True, group='布尔位置') 

        # 分组：墙体
        self['墙体开关']=Attr("无", obvious = True, readonly = False, combo= ["无","前左","前右","后左","后右"], group='布尔位置')
        self['拱顶底墙高']=Attr(900.0, obvious = True, group='布尔位置') 
        self['墙体厚度']=Attr(400.0, obvious = True, group='布尔位置') 
       
        self['拱形屋面_单拱'] = Attr(None, show = True)
        
        self.replace()
    @export
    def replace(self): 
        L = self['弦长']
        R = self['拱形半径']
        H  = self['屋面厚度']
        W  = self['屋面长度']
        W_y = self['布尔长']
        L_x = self['布尔宽']
        布尔位置 = self['布尔位置']
        
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
        # 拱形屋面壳体 (Section + Sweep沿Y轴拉伸)
        # 在XOY面创建拱形壳体截面 → rotx转XOZ → 沿Y轴正向拉伸W
        # 外弧与拱形屋面_最终精度调整.py矩形壳体顶部弧线使用完全相同的Arc定义
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
        最终模型 = Sweep(截面_XOZ_壳体, 拉伸路径_壳体)

        if 布尔位置 == "前左":
            布尔体 = translate(0,0,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 最终模型-布尔体
        elif 布尔位置 == "前右":
            布尔体 = translate(L-L_x,0,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 最终模型-布尔体
        elif 布尔位置 == "后左":
            布尔体 = translate(0,W-W_y,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 最终模型-布尔体
        elif 布尔位置 == "后右":
            布尔体 = translate(L-L_x,W-W_y,-H*2)*scale(L_x,W_y,R)*Cube()
            self['拱形屋面_单拱'] = 最终模型-布尔体
        else:
            # 对拱形壳体做一次微量布尔运算，使其与矩形壳体经历相同的布尔处理流程，
            # 保证两者拱形曲线的拟合精度一致
            _dummy = translate(L/2, W/2, y_inner_end/2) * scale(0.001, 0.001, 0.001) * Cube()
            self['拱形屋面_单拱'] = 最终模型 - _dummy
               

       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_单拱()
    place(FinalGeometry)
