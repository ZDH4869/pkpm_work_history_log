from pyp3d import *


class 支撑排架(Component):
    def __init__(self):
        Component.__init__(self)

        # ============================== 基本参数 ==============================
        self['设备名称'] = Attr('支罐体排架', obvious=True, readonly=False, group='专业属性')

        # 排架几何参数（排架矩形截面：长=X方向，宽=Y方向，形心位于全局原点）
        self['排架长度'] = Attr(900, obvious=True, group='排架')
        self['排架宽度'] = Attr(800, obvious=True, group='排架')
        # 排架高度=模型总高（框架高度+支撑垫厚度），初始值1010=框架1000+垫厚10；
        # 用户修改该参数时仅改变框架高度，支撑垫厚度保持=角钢厚度不变（方案B）
        self['排架高度'] = Attr(1010, obvious=True, group='排架')

        # L型角钢截面参数（水平距离=X方向肢长，竖向高度=Y方向肢长，厚度=截面宽度）
        self['等直角钢边长'] = Attr(40, obvious=True, group='角钢截面')
        self['厚度'] = Attr(10, obvious=True, group='角钢截面')
        self['倒角半径'] = Attr(8, obvious=True, group='角钢截面')

        self['模型'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        # ============================== 读取参数 ==============================
        L    = self['排架长度']             # 排架矩形长度（X方向）
        W    = self['排架宽度']             # 排架矩形宽度（Y方向）
        总高 = self['排架高度']             # 模型总高 = 框架高度 + 支撑垫厚度（Z方向）
        hL   = self['等直角钢边长']       # L型截面水平肢长度
        vL   = hL                        # L型截面竖向肢高度
        tL   = self['厚度']              # L型截面厚度（截面宽度，也即支撑垫厚度）
        rL   = self['倒角半径']          # L型截面内拐角倒角半径
        H    = 总高 - tL                  # 框架高度 = 排架高度(总高) - 支撑垫厚度

        # ============================== 参数校验 ==============================
        if L <= 0 or W <= 0 or H <= 0:
            print('参数错误：排架长度、宽度必须大于0，排架高度(总高)必须大于支撑垫厚度')
            return
        if hL <= 0 or vL <= 0 or tL <= 0:
            print('参数错误：L型截面水平距离、竖向高度、厚度必须大于0')
            return
        if rL < 0 or tL + rL >= hL or tL + rL >= vL:
            print('参数错误：L型截面倒角半径不能为负，且厚度+倒角半径必须小于水平距离与竖向高度')
            return

        # ============================== 第0步：L型角钢截面 ==============================
        # 截面位于xoy面，外侧拐点(0,0)，水平肢沿+X(长hL)，竖向肢沿+Y(高vL)，厚度tL
        # 内拐角(tL,tL)处做半径rL的内圆角倒角（保留参考代码钢结构构件的倒角设计）
        if rL > 0:
            lineL = Line(
                Vec2(0, 0), Vec2(hL, 0), Vec2(hL, tL), Vec2(tL + rL, tL),
                translate(tL + rL, tL + rL) * rotz(-pi/2) * scale(rL) * Arc(-pi/2),
                Vec2(tL, tL + rL), Vec2(tL, vL), Vec2(0, vL), Vec2(0, 0)
            )
        else:
            lineL = Line(
                Vec2(0, 0), Vec2(hL, 0), Vec2(hL, tL), Vec2(tL, tL),
                Vec2(tL, vL), Vec2(0, vL), Vec2(0, 0)
            )
        sectionL = Section(lineL)

        # ============================== 第0.5步：翻转后的L型角钢截面（仅水平支撑柱使用） ==============================
        # 经用户确认，将原始L型截面绕通过中心的水平轴(X方向)翻转180°（截面1→截面2，y→vL−y）
        # 原"水平距离"肢(底部水平板)翻转到顶部(y∈[vL−tL,vL])，竖向肢保持在左侧(x∈[0,tL])
        # 保持逆时针绕向与原始截面一致；仅用于水平支撑柱，竖向支撑柱仍用原始sectionL
        if rL > 0:
            lineL2 = Line(
                Vec2(0, 0), Vec2(tL, 0), Vec2(tL, vL - tL - rL),
                translate(tL + rL, vL - tL - rL) * rotz(pi) * scale(rL) * Arc(-pi/2),
                Vec2(tL + rL, vL - tL), Vec2(hL, vL - tL), Vec2(hL, vL), Vec2(0, vL), Vec2(0, 0)
            )
        else:
            lineL2 = Line(
                Vec2(0, 0), Vec2(tL, 0), Vec2(tL, vL - tL),
                Vec2(hL, vL - tL), Vec2(hL, vL), Vec2(0, vL), Vec2(0, 0)
            )
        sectionL2 = Section(lineL2)

        # ============================== 第1步：竖向支撑柱（4根） ==============================
        # L型截面(xoy面，法线+Z)沿+Z拉伸(排架高度)，截面拐点与排架矩形四角点重合
        # 四角点截面绕Z旋转不同角度，使L型凹角开口朝排架内部
        vline = Line(Vec3(0, 0, 0), Vec3(0, 0, H))
        竖向柱后左 = trans(-L/2, -W/2, 0) * Sweep(sectionL, vline)
        竖向柱前左 = trans(L/2, -W/2, 0) * rotz(pi/2) * Sweep(sectionL, vline)
        竖向柱前右 = trans(L/2, W/2, 0) * rotz(pi) * Sweep(sectionL, vline)
        竖向柱后右 = trans(-L/2, W/2, 0) * rotz(-pi/2) * Sweep(sectionL, vline)

        # ============================== 第2步：顶部水平支撑柱（4根） ==============================
        # 翻转后的L型截面(sectionL2)在z=框架顶面下方vL处（z=H-vL平面），沿排架矩形四边扫掠，
        # 形成顶面位于z=H的顶部水平支撑柱（原由底部水平柱沿+Z平移复制得到，现直接构建，几何一致）
        顶部水平柱后 = Sweep(trans(-L/2, W/2, H - vL) * rotx(pi/2) * sectionL2,
                            Line(Vec3(-L/2, W/2, H - vL), Vec3(-L/2, -W/2, H - vL)))
        顶部水平柱前 = Sweep(trans(L/2, W/2, H - vL) * rotx(-pi/2) * rotz(pi) * sectionL2,
                            Line(Vec3(L/2, W/2, H - vL), Vec3(L/2, -W/2, H - vL)))
        顶部水平柱右 = Sweep(trans(L/2, W/2, H - vL) * roty(-pi/2) * rotz(-pi/2) * sectionL2,
                            Line(Vec3(L/2, W/2, H - vL), Vec3(-L/2, W/2, H - vL)))
        顶部水平柱左 = Sweep(trans(-L/2, -W/2, H - vL) * roty(pi/2) * rotz(pi/2) * sectionL2,
                            Line(Vec3(-L/2, -W/2, H - vL), Vec3(L/2, -W/2, H - vL)))

        # ============================== 第3步：三角形支撑板（8块） ==============================
        # 在矩形框架四个视图面（前/后/左/右）的左上、右上角点绘制等腰直角三角形支撑板：
        # 直角顶点=角点（z=H），水平直角边沿该视图面顶部水平柱方向、指向同视图面另一角点，
        # 竖直直角边沿-Z（竖向柱方向），边长=0.25*排架高度（经用户确认）
        # 截面沿该视图面所在轴线拉伸，拉伸距离=角钢截面厚度tL，厚度方向朝排架内侧
        a = 0.25 * H   # 三角形支撑板边长

        三角板_前_左上 = Extrusion(
            [Vec3(L/2, -W/2, H), Vec3(L/2, -W/2 + a, H), Vec3(L/2, -W/2, H - a)],
            Vec3(-tL, 0, 0))
        三角板_前_右上 = Extrusion(
            [Vec3(L/2, W/2, H), Vec3(L/2, W/2 - a, H), Vec3(L/2, W/2, H - a)],
            Vec3(-tL, 0, 0))
        三角板_后_左上 = Extrusion(
            [Vec3(-L/2, W/2, H), Vec3(-L/2, W/2 - a, H), Vec3(-L/2, W/2, H - a)],
            Vec3(tL, 0, 0))
        三角板_后_右上 = Extrusion(
            [Vec3(-L/2, -W/2, H), Vec3(-L/2, -W/2 + a, H), Vec3(-L/2, -W/2, H - a)],
            Vec3(tL, 0, 0))
        三角板_左_左上 = Extrusion(
            [Vec3(-L/2, -W/2, H), Vec3(-L/2 + a, -W/2, H), Vec3(-L/2, -W/2, H - a)],
            Vec3(0, tL, 0))
        三角板_左_右上 = Extrusion(
            [Vec3(L/2, -W/2, H), Vec3(L/2 - a, -W/2, H), Vec3(L/2, -W/2, H - a)],
            Vec3(0, tL, 0))
        三角板_右_左上 = Extrusion(
            [Vec3(L/2, W/2, H), Vec3(L/2 - a, W/2, H), Vec3(L/2, W/2, H - a)],
            Vec3(0, -tL, 0))
        三角板_右_右上 = Extrusion(
            [Vec3(-L/2, W/2, H), Vec3(-L/2 + a, W/2, H), Vec3(-L/2, W/2, H - a)],
            Vec3(0, -tL, 0))

        # ============================== 第4步：柱脚正方形支撑垫（4块） ==============================
        # 正方形截面位于xoy面，边长=角钢截面边长+60（60为固定值），厚度=角钢截面厚度tL，
        # 以各竖向柱L型截面外框中心为中心（居中包覆柱脚），向下放置（z∈[-tL,0]，垫于柱脚下方）
        s   = hL + 60   # 正方形支撑垫边长
        s2  = s / 2.0   # 半边长
        支撑垫_后左 = Extrusion(
            [Vec3(-L/2 + hL/2 - s2, -W/2 + hL/2 - s2, 0),
             Vec3(-L/2 + hL/2 + s2, -W/2 + hL/2 - s2, 0),
             Vec3(-L/2 + hL/2 + s2, -W/2 + hL/2 + s2, 0),
             Vec3(-L/2 + hL/2 - s2, -W/2 + hL/2 + s2, 0)],
            Vec3(0, 0, -tL))
        支撑垫_前左 = Extrusion(
            [Vec3(L/2 - hL/2 - s2, -W/2 + hL/2 - s2, 0),
             Vec3(L/2 - hL/2 + s2, -W/2 + hL/2 - s2, 0),
             Vec3(L/2 - hL/2 + s2, -W/2 + hL/2 + s2, 0),
             Vec3(L/2 - hL/2 - s2, -W/2 + hL/2 + s2, 0)],
            Vec3(0, 0, -tL))
        支撑垫_前右 = Extrusion(
            [Vec3(L/2 - hL/2 - s2, W/2 - hL/2 - s2, 0),
             Vec3(L/2 - hL/2 + s2, W/2 - hL/2 - s2, 0),
             Vec3(L/2 - hL/2 + s2, W/2 - hL/2 + s2, 0),
             Vec3(L/2 - hL/2 - s2, W/2 - hL/2 + s2, 0)],
            Vec3(0, 0, -tL))
        支撑垫_后右 = Extrusion(
            [Vec3(-L/2 + hL/2 - s2, W/2 - hL/2 - s2, 0),
             Vec3(-L/2 + hL/2 + s2, W/2 - hL/2 - s2, 0),
             Vec3(-L/2 + hL/2 + s2, W/2 - hL/2 + s2, 0),
             Vec3(-L/2 + hL/2 - s2, W/2 - hL/2 + s2, 0)],
            Vec3(0, 0, -tL))

        # ============================== 布尔相加全部构件并平移至插入点 ==============================
        # 插入点=竖向支撑柱的前面左上角点=(L/2,-W/2,H)，整体平移使插入点落到全局原点(0,0,0)
        self['模型'] = trans(-L/2, W/2, -H) * (
            竖向柱后左 + 竖向柱前左 + 竖向柱前右 + 竖向柱后右
            + 顶部水平柱后 + 顶部水平柱前 + 顶部水平柱右 + 顶部水平柱左
            + 三角板_前_左上 + 三角板_前_右上 + 三角板_后_左上 + 三角板_后_右上
            + 三角板_左_左上 + 三角板_左_右上 + 三角板_右_左上 + 三角板_右_右上
            + 支撑垫_后左 + 支撑垫_前左 + 支撑垫_前右 + 支撑垫_后右
        )


if __name__ == "__main__":
    FinalGeometry = 支撑排架()
    place(FinalGeometry)
