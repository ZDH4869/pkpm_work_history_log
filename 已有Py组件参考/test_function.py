# 测试get_parameter_by_marque函数

unit_parameter = {
    'CLF6':[5.9,1500,'侧风',0,2.43,55,600,600,2000,210],
    'CLF8':[7.6,2000,'侧风',0,3.02,55,850,600,2000,230],
    'CLF10':[10,2500,'侧风',0,4.01,60,850,600,2000,230],
    'CLF16':[15.5,4000,'侧风',0,5.92,62,1300,700,2000,340],
    'CLF21':[20.8,5000,'侧风',0,8.5,64,1300,700,2000,370],
    'CLF25':[24.3,6500,'侧风',0,9.64,65,1700,700,2120,585],
    'CLF32':[30.8,8000,'侧风',0,12.14,65,1700,700,2120,615],
    'CLF42':[41.5,10000,'侧风',0,16.2,64,1900,850,2230,690]}

marque_list = [
    'CLF6','CLF8','CLF10','CLF16',
    'CLF21','CLF25','CLF32','CLF42']

def get_parameter_by_marque(marque):
    m1_list=[]
    m2_list=[]
    m3_list=[]
    m4_list=[]
    m5_list=[]
    m6_list=[]
    m7_list=[]
    m8_list=[]
    m9_list=[]
    m10_list=[]    

    for i in range(len(marque_list)):
        m1_list.append(unit_parameter.get(marque_list[i])[0])
        m2_list.append(unit_parameter.get(marque_list[i])[1])
        m3_list.append(unit_parameter.get(marque_list[i])[2])
        m4_list.append(unit_parameter.get(marque_list[i])[3])
        m5_list.append(unit_parameter.get(marque_list[i])[4])
        m6_list.append(unit_parameter.get(marque_list[i])[5])
        m7_list.append(unit_parameter.get(marque_list[i])[6])
        m8_list.append(unit_parameter.get(marque_list[i])[7])
        m9_list.append(unit_parameter.get(marque_list[i])[8])
        m10_list.append(unit_parameter.get(marque_list[i])[9])

    # 循环结束后再获取参数值和返回
    M1=m1_list[marque_list.index(marque)]
    M2=m2_list[marque_list.index(marque)]
    M3=m3_list[marque_list.index(marque)]
    M4=m4_list[marque_list.index(marque)]
    M5=m5_list[marque_list.index(marque)]
    M6=m6_list[marque_list.index(marque)]
    M7=m7_list[marque_list.index(marque)]
    M8=m8_list[marque_list.index(marque)]
    M9=m9_list[marque_list.index(marque)]
    M10=m10_list[marque_list.index(marque)]
    
    return M1,M2,M3,M4,M5,M6,M7,M8,M9,M10

# 测试函数
print("Testing get_parameter_by_marque function...")
for marque in marque_list:
    params = get_parameter_by_marque(marque)
    print(f"{marque}: {params}")

print("\nTest completed successfully!")
