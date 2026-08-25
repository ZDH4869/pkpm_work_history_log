from pyp3d import *

# 扭面模型：从矩形截面渐变到平行四边形截面
# 初始截面为矩形，最终截面为平行四边形（高度方向倾角 30°）
# 两截面底部宽度重合，沿扫掠路径方向通过 Loft 连接

class 扭面(Component):
    def __init__(self):
        Component.__init__(self)
        self['截面宽度'] = Attr(500.0, obvious=True)
        self['截面高度'] = Attr(3000.0, obvious=True)
        self['扫掠长度'] = Attr(5000.0, obvious=True)
        self['倾角'] = Attr(30.0, obvious=True)
        self['扭面'] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        W = self['截面宽度']
        H = self['截面高度']
        L = self['扫掠长度']
        tilt = self['倾角'] * pi / 180.0

        # 顶部在 X 方向的偏移量（由倾斜角度决定）
        dx = H * tan(tilt)

        # --- 初始截面：矩形 (z=0) ---
        # 四个角点按逆时针排列：左下 → 右下 → 右上 → 左上
        section_start = Section(
            Vec2(0, 0),     # 左下
            Vec2(W, 0),     # 右下
            Vec2(W, H),     # 右上
            Vec2(0, H)      # 左上
        )

        # --- 最终截面：平行四边形 (z=L) ---
        # 底部与初始截面重合，顶部沿 X 方向偏移 dx
        section_end = Section(
            Vec2(0, 0),     # 左下（与初始截面底部重合）
            Vec2(W, 0),     # 右下（与初始截面底部重合）
            Vec2(W + dx, H),  # 右上（偏移后）
            Vec2(dx, H)     # 左上（偏移后）
        )

        # 两截面放样：初始 → 最终，沿 Z 轴方向渐变
        self['扭面'] = Loft(
            section_start,
            translate(0, 0, L) * section_end
        )


if __name__ == "__main__":
    FinalGeometry = 扭面()
    place(FinalGeometry)
