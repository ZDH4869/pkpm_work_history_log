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
        self['拱顶底墙高']=Attr(2000.0, obvious = True, group='墙体')
        self['墙体厚度']=Attr(60.0, obvious = True, group='墙体')
       
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
        wall_height = self['拱顶底墙高']      # A1/B1 沿 Z 轴的偏移量(mm)
        wall_thickness = self['墙体厚度']      # 墙体厚度(mm)
        
        # ================================================================
        # 公共计算：拱矢高与圆弧角度
        # 圆心位于 (L/2, -z0)，半径 R
        # 弦两端点 A(0,0) 和 B(L,0)，弧线 A→B 顺时针经拱顶
        # ================================================================
        z0 = math.sqrt(R**2 - (L/2)**2)  # 拱矢高(正值) = 1019.6
        angle_pos = math.atan2(z0, L/2)       # B 相对圆心的角度 ≈ 0.847 rad
        angle_start = math.pi - angle_pos      # A 相对圆心的角度 ≈ 2.295 rad
        span = angle_start - angle_pos         # 顺时针弧跨度 = π - 2*angle_pos ≈ 1.448 rad
        
        # ================================================================
        # 第一部分：拱形屋面壳体 (Section + Sweep沿Y轴拉伸)
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
        # 第二部分：拱形矩形壳体 (Section + Sweep)
        #
        # 基于最终模型坐标系:
        #   弦两端在 (0,0,0) 和 (L,0,0), 弧圆心位于 (L/2, -z0), 半径 R
        #   A  = 拱顶曲线起点 = (0, 0, 0)
        #   B  = 拱顶曲线终点 = (L, 0, 0)
        #   A1 = A 沿 Z 偏移 -wall_height = (0, 0, -wall_height)
        #   B1 = B 沿 Z 偏移 -wall_height = (L, 0, -wall_height)
        #
        # 封闭截面: A →(弧线CW)→ B → B1 → A1 → A
        # 拉伸方向: Y轴, 起点0 → 终点W (与拱形壳体Y范围一致)
        #
        # 弧线使用公共计算的角度参数(angle_start, span)，与拱形壳体外弧完全一致
        # ================================================================
        # 顺时针弧线 A→B (经拱顶):
        # Arc(-span): 单位弧顺时针走 span 弧度; rotate(angle_start) 使起点对准 A 方向
        弧线_cw = translate(L/2, -z0) * rotate(angle_start) * scale(R, R) * Arc(-span)

        # 组合截面: A(0,0) → 弧线CW → B(L,0) → B1(L,-wall_height) → A1(0,-wall_height) → A(0,0)
        截面_矩形拱 = Section(
            Vec2(0, 0),
            弧线_cw,
            Vec2(L, 0),
            Vec2(L, -wall_height),
            Vec2(0, -wall_height),
        )

        # 将截面从 XOY 旋转到 XOZ 平面，沿 Y 轴拉伸 W
        截面_XOZ = rotx(pi/2) * 截面_矩形拱
        拉伸路径 = Line(Vec3(0, 0, 0), Vec3(0, W, 0))
        矩形壳体 = Sweep(截面_XOZ, 拉伸路径)

        # ================================================================
        # 第三部分：布尔开口 (分别作用于两个独立部件)
        #
        # 开窗布尔体: 用于在拱形壳体+矩形壳体上开窗洞
        #   布尔体 Z 向拉伸 = R + wall_height，确保贯穿拱形壳体+矩形壳体全高
        #
        # 切墙布尔体: 用于将矩形壳体掏空为厚度=wall_thickness的墙体
        #   截面在 XOY 面绘制，沿 Z 轴从 R 拉伸到 -wall_height
        #   全屋切墙布尔体: 布尔位置=="无"时应用，无窗口挖空
        #   开窗切墙布尔体: 布尔位置==前左/前右/后左/后右时应用，带窗口挖空
        # ================================================================
        # 切墙布尔体公共拉伸路径: 沿 Z 轴从拱形半径到负的拱顶底墙高
        切墙路径 = Line(Vec3(0, 0, R), Vec3(0, 0, -wall_height))

        # ================================================================
        # 镜像变换: 以 (L/2, W/2, 0) 为临时坐标原点
        #   center_x = L/2 (0.5*弦长, X轴方向)
        #   center_y = W/2 (0.5*拉伸长度, Y轴方向)
        # 前右切墙截面为基础截面，通过镜像对称得到其他三个方向的切墙截面:
        #   前左切墙截面 = 前右切墙截面 关于 Y轴 对称 (翻转X, new_x = L - x)
        #   后右切墙截面 = 前右切墙截面 关于 X轴 对称 (翻转Y, new_y = W - y)
        #   后左切墙截面 = 后右切墙截面 关于 Y轴 对称 (翻转X, new_x = L - x)
        # 对称规则: center_x - x = x' - center_x → x' = L - x
        #           center_y - y = y' - center_y → y' = W - y
        # ================================================================

        # 前右切墙截面 (基础截面)
        # 截面逆时针 QWERTYQ: Q(左下) → W(左窗边,底) → E(左窗边,窗顶) → R(右窗边,窗顶) → T(右上) → Y(左上) → Q
        前右切墙截面 = Section(
            Vec2(wall_thickness, wall_thickness),                          # Q
            Vec2(L - L_x - wall_thickness, wall_thickness),                # W
            Vec2(L - L_x - wall_thickness, wall_thickness + W_y),          # E
            Vec2(L - wall_thickness, wall_thickness + W_y),                # R
            Vec2(L - wall_thickness, W - wall_thickness),                  # T
            Vec2(wall_thickness, W - wall_thickness),                      # Y
        )

        # 前左切墙截面 = 前右关于Y轴对称: 翻转X, new_x = L - x, new_y = y
        前左切墙截面 = Section(
            Vec2(L - wall_thickness, wall_thickness),                                    # Q
            Vec2(L - (L - L_x - wall_thickness), wall_thickness),                        # W
            Vec2(L - (L - L_x - wall_thickness), wall_thickness + W_y),                  # E
            Vec2(L - (L - wall_thickness), wall_thickness + W_y),                        # R
            Vec2(L - (L - wall_thickness), W - wall_thickness),                          # T
            Vec2(L - wall_thickness, W - wall_thickness),                                # Y
        )

        # 后右切墙截面 = 前右关于X轴对称: 翻转Y, new_x = x, new_y = W - y
        后右切墙截面 = Section(
            Vec2(wall_thickness, W - wall_thickness),                                    # Q
            Vec2(L - L_x - wall_thickness, W - wall_thickness),                          # W
            Vec2(L - L_x - wall_thickness, W - (wall_thickness + W_y)),                  # E
            Vec2(L - wall_thickness, W - (wall_thickness + W_y)),                        # R
            Vec2(L - wall_thickness, W - (W - wall_thickness)),                          # T
            Vec2(wall_thickness, W - (W - wall_thickness)),                              # Y
        )

        # 后左切墙截面 = 后右关于Y轴对称: 翻转X, new_x = L - x, new_y = y
        后左切墙截面 = Section(
            Vec2(L - wall_thickness, W - wall_thickness),                                # Q
            Vec2(L - (L - L_x - wall_thickness), W - wall_thickness),                    # W
            Vec2(L - (L - L_x - wall_thickness), W - (wall_thickness + W_y)),            # E
            Vec2(L - (L - wall_thickness), W - (wall_thickness + W_y)),                  # R
            Vec2(L - (L - wall_thickness), W - (W - wall_thickness)),                    # T
            Vec2(L - wall_thickness, W - (W - wall_thickness)),                          # Y
        )

        if 布尔位置 == "前左":
            # 开窗布尔体 (前左: X=0~L_x, Y=0~W_y)
            # 布尔体为上部拱顶开窗，布尔体1为下部墙体开窗
            布尔体 = translate(0,0,-H*2)*scale(L_x,W_y,R)*Cube()
            布尔体1 = translate(0,0,-H*2)*scale(L_x,W_y,-wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体 - 布尔体1
            # 前左切墙截面 = 前右切墙截面 关于 YOZ面(Y轴) 对称
            矩形壳体_结果 = 矩形壳体 - 布尔体 - 布尔体1 - Sweep(前左切墙截面, 切墙路径)

        elif 布尔位置 == "前右":
            # 开窗布尔体 (前右: X=L-L_x~L, Y=0~W_y)
            # 布尔体为上部拱顶开窗，布尔体1为下部墙体开窗
            布尔体 = translate(L-L_x,0,-H*2)*scale(L_x,W_y,R)*Cube()
            布尔体1 = translate(L-L_x,0,-H*2)*scale(L_x,W_y,-wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体 - 布尔体1
            # 前右切墙截面 (基础截面)
            矩形壳体_结果 = 矩形壳体 - 布尔体 - 布尔体1 - Sweep(前右切墙截面, 切墙路径)

        elif 布尔位置 == "后左":
            # 开窗布尔体 (后左: X=0~L_x, Y=W-W_y~W)
            # 布尔体为上部拱顶开窗，布尔体1为下部墙体开窗
            布尔体 = translate(0,W-W_y,-H*2)*scale(L_x,W_y,R)*Cube()
            布尔体1 = translate(0,W-W_y,-H*2)*scale(L_x,W_y,-wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体 - 布尔体1
            # 后左切墙截面 = 后右切墙截面 关于 YOZ面(Y轴) 对称
            矩形壳体_结果 = 矩形壳体 - 布尔体 - 布尔体1 - Sweep(后左切墙截面, 切墙路径)

        elif 布尔位置 == "后右":
            # 开窗布尔体 (后右: X=L-L_x~L, Y=W-W_y~W)
            # 布尔体为上部拱顶开窗，布尔体1为下部墙体开窗
            布尔体 = translate(L-L_x,W-W_y,-H*2)*scale(L_x,W_y,R)*Cube()
            布尔体1 = translate(L-L_x,W-W_y,-H*2)*scale(L_x,W_y,-wall_height)*Cube()
            拱形壳体_结果 = 拱形壳体 - 布尔体 - 布尔体1
            # 后右切墙截面 = 前右切墙截面 关于 XOZ面(X轴) 对称
            矩形壳体_结果 = 矩形壳体 - 布尔体 - 布尔体1 - Sweep(后右切墙截面, 切墙路径)

        else:
            # 布尔位置 == "无": 不开窗，仅应用全屋切墙布尔体
            # 对拱形壳体做一次微量布尔运算，使其与矩形壳体经历相同的布尔处理流程，
            # 保证两者拱形曲线的拟合精度一致
            # 微小立方体(0.001mm)位于壳体内部，不影响实际几何形状
            _dummy = translate(L/2, W/2, y_inner_end/2) * scale(0.001, 0.001, 0.001) * Cube()
            拱形壳体_结果 = 拱形壳体 - _dummy
            # 全屋切墙布尔体: 全屋矩形截面(无窗口挖空)，沿 Z 轴从 R 到 -wall_height 拉伸
            # 截面角点位于 (wall_thickness, wall_thickness)，
            # X 向宽度 = L - 2*wall_thickness，Y 向长度 = W - 2*wall_thickness
            全屋切墙截面 = Section(
                Vec2(wall_thickness, wall_thickness),
                Vec2(L - wall_thickness, wall_thickness),
                Vec2(L - wall_thickness, W - wall_thickness),
                Vec2(wall_thickness, W - wall_thickness),
            )
            矩形壳体_结果 = 矩形壳体 - Sweep(全屋切墙截面, 切墙路径)

        # 两个独立部件组合输出 (combine 不做布尔合并，保留各自属性)
        self['拱形屋面_单拱'] = combine(拱形壳体_结果, 矩形壳体_结果)
               

       
# 输出模型
if __name__ == "__main__":
    FinalGeometry = 拱形屋面_单拱()
    place(FinalGeometry)