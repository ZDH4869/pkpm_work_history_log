from pyp3d import *

# 螺钉模型：等截面三角形螺纹，通过 Loft 螺旋放样生成
# 芯柱外径 200mm，螺纹截面为腰长 20mm、顶角 60° 的等腰三角形

class 螺钉(Component):
    def __init__(self):
        Component.__init__(self)
        self['芯柱直径'] = Attr(200.0, obvious=True)
        self['腰长'] = Attr(20.0, obvious=True)
        self['顶角'] = Attr(60.0, obvious=True)
        self['螺纹条数'] = Attr(10, obvious=True)
        self['每圈截面数'] = Attr(36, obvious=True)
        self['螺钉'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        D_core = self['芯柱直径']
        L_waist = self['腰长']
        angle_deg = self['顶角']
        N_threads = int(self['螺纹条数'])
        N_per_turn = int(self['每圈截面数'])

        R = D_core / 2.0  # 芯柱半径 = 100

        # --- 三角形几何计算 ---
        # 等腰三角形：腰长 L_waist，顶角 angle_deg
        half_angle = (angle_deg / 2.0) * pi / 180.0   # 半顶角（弧度）
        base = 2.0 * L_waist * sin(half_angle)         # 底边长 = 螺距
        height = L_waist * cos(half_angle)              # 齿高

        # 螺距 = 底边长
        pitch = base

        # --- 三角形截面：底边贴在芯柱表面，顶点朝外 ---
        # 在 XY 平面定义（X→径向, Y→轴向），绕 X 旋转 90° 后落入 XZ 平面
        section = rotate(Vec3(1, 0, 0), 0.5 * pi) * Section(
            Vec2(R + height, 0),        # 齿尖：径向最外端，轴向居中
            Vec2(R, -base / 2.0),       # 齿底：芯柱表面，轴向下方
            Vec2(R, base / 2.0)         # 齿底：芯柱表面，轴向上方
        )

        # --- 螺旋阵列 + Loft 放样 ---
        total_angle = N_threads * 2.0 * pi              # 总旋转角度
        z_per_rad = pitch / (2.0 * pi)                   # 每弧度升高量
        step_angle = 2.0 * pi / N_per_turn               # 步进角度

        sections = []
        for angle in linspace(0, total_angle, int(total_angle / step_angle)):
            z = z_per_rad * angle
            positioned = translate(0, 0, z) * (rotz(angle) * section)
            sections.append(positioned)

        screw = Loft(*sections)
        screw.smooth = True

        self['螺钉'] = screw


if __name__ == "__main__":
    FinalGeometry = 螺钉()
    place(FinalGeometry)
