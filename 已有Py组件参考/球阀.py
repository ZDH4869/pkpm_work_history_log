from pyp3d import *
import math

class 球阀(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 主要尺寸参数 ==========
        self['公称直径'] = Attr(100.0, obvious=True)
        self['阀体总长'] = Attr(400.0, obvious=True)
        self['阀腔直径'] = Attr(160.0, obvious=True)
        self['法兰外径'] = Attr(180.0, obvious=True)
        self['法兰厚度'] = Attr(20.0, obvious=True)
        self['法兰螺栓孔直径'] = Attr(18.0, obvious=True)
        self['法兰螺栓孔数量'] = Attr(8, obvious=True)
        self['法兰螺栓分布圆直径'] = Attr(145.0, obvious=True)
        
        # ========== 阀杆参数 ==========
        self['阀杆直径'] = Attr(40.0, obvious=True)
        self['阀杆高度'] = Attr(100.0, obvious=True)
        
        # ========== 执行器参数 ==========
        self['执行器宽度'] = Attr(120.0, obvious=True)
        self['执行器长度'] = Attr(80.0, obvious=True)
        self['执行器高度'] = Attr(60.0, obvious=True)
        
        # ========== 其他参数 ==========
        self['管道壁厚'] = Attr(8.0, obvious=True)
        self['法兰间距'] = Attr(10.0, obvious=True)  # 中间两片法兰之间的间隙
        
        # ========== 模型显示参数 ==========
        self['球阀'] = Attr(None, show=True)
        
        self.replace()
    
    @export
    def replace(self):
        # 获取参数值
        DN = self['公称直径']  # 管道内径
        L_total = self['阀体总长']  # 总长度
        D_chamber = self['阀腔直径']  # 阀腔外径
        D_flange = self['法兰外径']  # 法兰外径
        T_flange = self['法兰厚度']  # 法兰厚度
        D_bolt = self['法兰螺栓孔直径']  # 螺栓孔直径
        N_bolt = self['法兰螺栓孔数量']  # 螺栓孔数量
        D_bolt_circle = self['法兰螺栓分布圆直径']  # 螺栓分布圆直径
        D_stem = self['阀杆直径']  # 阀杆直径
        H_stem = self['阀杆高度']  # 阀杆高度
        W_actuator = self['执行器宽度']  # 执行器宽度
        L_actuator = self['执行器长度']  # 执行器长度
        H_actuator = self['执行器高度']  # 执行器高度
        T_pipe = self['管道壁厚']  # 管道壁厚
        gap = self['法兰间距']  # 中间法兰间隙
        
        # 计算管道外径
        D_pipe_outer = DN + 2 * T_pipe
        
        # 计算各部分长度
        # 总长度 = 左端法兰 + 左管道 + 阀腔左法兰 + 间隙 + 阀腔右法兰 + 右管道 + 右端法兰
        # 简化：左右对称，中间阀腔区域
        L_end_pipe = (L_total - 4 * T_flange - gap) / 4  # 两端管道段长度
        L_chamber = (L_total - 4 * T_flange - gap) / 2 + gap  # 阀腔区域长度（包含中间法兰）
        
        # ========== 1. 创建法兰几何体 ==========
        def create_flange_with_holes(x_pos):
            """创建带螺栓孔的法兰盘"""
            # 法兰主体 - 使用圆柱体
            flange_body = Cone(
                Vec3(x_pos, 0, 0),
                Vec3(x_pos + T_flange, 0, 0),
                D_flange / 2
            )
            
            # 创建螺栓孔
            holes = None
            for i in range(N_bolt):
                angle = 2 * math.pi * i / N_bolt
                bolt_x = x_pos + T_flange / 2  # 螺栓孔位于法兰中心
                bolt_y = (D_bolt_circle / 2) * math.cos(angle)
                bolt_z = (D_bolt_circle / 2) * math.sin(angle)
                
                hole = Cone(
                    Vec3(bolt_x - T_flange/2 - 1, bolt_y, bolt_z),
                    Vec3(bolt_x + T_flange/2 + 1, bolt_y, bolt_z),
                    D_bolt / 2
                )
                
                if holes is None:
                    holes = hole
                else:
                    holes = holes + hole
            
            # 布尔减：法兰减去螺栓孔
            if holes is not None:
                return flange_body - holes
            return flange_body
        
        # ========== 2. 创建管道段 ==========
        def create_pipe_segment(x_start, length):
            """创建管道段（外径圆柱减去内径圆柱）"""
            x_end = x_start + length
            # 管道外圆柱
            pipe_outer = Cone(
                Vec3(x_start, 0, 0),
                Vec3(x_end, 0, 0),
                D_pipe_outer / 2
            )
            # 管道内孔
            pipe_inner = Cone(
                Vec3(x_start - 1, 0, 0),
                Vec3(x_end + 1, 0, 0),
                DN / 2
            )
            return pipe_outer - pipe_inner
        
        # ========== 3. 创建阀腔 ==========
        def create_valve_chamber(x_start, length):
            """创建阀腔（球形体）"""
            x_end = x_start + length
            # 阀腔主体 - 使用圆柱或球体形状
            # 这里使用圆柱体作为阀腔主体
            chamber_outer = Cone(
                Vec3(x_start, 0, 0),
                Vec3(x_end, 0, 0),
                D_chamber / 2
            )
            # 阀腔内孔
            chamber_inner = Cone(
                Vec3(x_start - 1, 0, 0),
                Vec3(x_end + 1, 0, 0),
                DN / 2
            )
            return chamber_outer - chamber_inner
        
        # ========== 4. 创建阀杆 ==========
        def create_valve_stem():
            """创建阀杆"""
            # 阀杆位于阀腔顶部中心
            stem = Cone(
                Vec3(0, D_chamber/2, 0),
                Vec3(0, D_chamber/2 + H_stem, 0),
                D_stem / 2
            )
            return stem
        
        # ========== 5. 创建执行器 ==========
        def create_actuator():
            """创建执行器（顶部控制盒）"""
            # 执行器底座
            base_y = D_chamber/2 + H_stem
            
            # 执行器主体 - 使用立方体
            actuator_body = translate(0, base_y + H_actuator/2, 0) * \
                          scale(L_actuator, H_actuator, W_actuator) * Cube()
            
            # 创建执行器顶部的梯形结构
            top_y = base_y + H_actuator
            # 顶部较小的立方体
            top_part = translate(0, top_y + H_actuator*0.3/2, 0) * \
                       scale(L_actuator*0.7, H_actuator*0.3, W_actuator*0.7) * Cube()
            
            return actuator_body + top_part
        
        # ========== 6. 组装球阀各部件 ==========
        
        # 左端法兰（最左侧）
        x_left_end = -L_total / 2
        flange_left_end = create_flange_with_holes(x_left_end)
        
        # 左端管道
        x_left_pipe = x_left_end + T_flange
        pipe_left = create_pipe_segment(x_left_pipe, L_end_pipe)
        
        # 左中间法兰（阀腔左侧）
        x_left_middle = x_left_pipe + L_end_pipe
        flange_left_middle = create_flange_with_holes(x_left_middle)
        
        # 阀腔区域
        x_chamber = x_left_middle + T_flange
        chamber = create_valve_chamber(x_chamber, L_chamber)
        
        # 右中间法兰（阀腔右侧）
        x_right_middle = x_chamber + L_chamber
        flange_right_middle = create_flange_with_holes(x_right_middle)
        
        # 右端管道
        x_right_pipe = x_right_middle + T_flange
        pipe_right = create_pipe_segment(x_right_pipe, L_end_pipe)
        
        # 右端法兰（最右侧）
        x_right_end = x_right_pipe + L_end_pipe
        flange_right_end = create_flange_with_holes(x_right_end)
        
        # 阀杆
        stem = create_valve_stem()
        
        # 执行器
        actuator = create_actuator()
        
        # ========== 7. 组合所有部件 ==========
        valve_body = combine(
            flange_left_end,
            pipe_left,
            flange_left_middle,
            chamber,
            flange_right_middle,
            pipe_right,
            flange_right_end,
            stem,
            actuator
        )
        
        # 设置颜色
        # 阀体使用蓝色系
        valve_colored = valve_body.color(0.4, 0.6, 0.8, 1.0)
        
        self['球阀'] = valve_colored


if __name__ == "__main__":
    FinalGeometry = 球阀()
    place(FinalGeometry)
