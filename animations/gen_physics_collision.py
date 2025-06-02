import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 参数
m1 = 1.0  # 物体1的质量
m2 = 5.0  # 物体2的质量 (修改为不同质量)
r1 = 0.1  # 物体1的半径
r2 = 0.2  # 物体2的半径 (修改为更大)

# 初始条件
x1_0 = -0.5  # 物体1的初始x坐标
y1_0 = 0.0   # 物体1的初始y坐标
v1x_0 = 0.5  # 物体1的初始x速度 (修改为更快)
v1y_0 = 0.0  # 物体1的初始y速度

x2_0 = 0.5   # 物体2的初始x坐标
y2_0 = 0.0   # 物体2的初始y坐标
v2x_0 = -0.5 # 物体2的初始x速度 (修改为更快)
v2y_0 = 0.0  # 物体2的初始y速度

# 模拟时间参数
dt = 0.01    # 时间步长
T = 10.0     # 总模拟时间
num_frames = int(T / dt)

# 存储位置和速度
x1_history = []
y1_history = []
x2_history = []
y2_history = []

v1x_history = []
v1y_history = []
v2x_history = []
v2y_history = []

# 当前状态
x1, y1 = x1_0, y1_0
x2, y2 = x2_0, y2_0
v1x, v1y = v1x_0, v1y_0
v2x, v2y = v2x_0, v2y_0

# 碰撞后速度（完全弹性碰撞）
def calculate_post_collision_velocities(m1, v1x, v1y, m2, v2x, v2y, normal_x, normal_y):
    # 相对速度
    v_rel_x = v1x - v2x
    v_rel_y = v1y - v2y

    # 沿碰撞法线的相对速度分量
    v_rel_dot_n = v_rel_x * normal_x + v_rel_y * normal_y

    # 如果物体正在分离，则不处理碰撞
    if v_rel_dot_n > 0:
        return v1x, v1y, v2x, v2y

    # 沿碰撞法线方向的速度变化量
    impulse_magnitude = -2 * v_rel_dot_n / (1/m1 + 1/m2)

    # 更新速度
    new_v1x = v1x + impulse_magnitude / m1 * normal_x
    new_v1y = v1y + impulse_magnitude / m1 * normal_y
    new_v2x = v2x - impulse_magnitude / m2 * normal_x
    new_v2y = v2y - impulse_magnitude / m2 * normal_y

    return new_v1x, new_v1y, new_v2x, new_v2y

# 模拟过程
for i in range(num_frames):
    # 存储当前状态
    x1_history.append(x1)
    y1_history.append(y1)
    x2_history.append(x2)
    y2_history.append(y2)
    v1x_history.append(v1x)
    v1y_history.append(v1y)
    v2x_history.append(v2x)
    v2y_history.append(v2y)

    # 预测下一时刻位置
    next_x1 = x1 + v1x * dt
    next_y1 = y1 + v1y * dt
    next_x2 = x2 + v2x * dt
    next_y2 = y2 + v2y * dt

    # 检查碰撞
    dist_sq = (next_x1 - next_x2)**2 + (next_y1 - next_y2)**2
    if dist_sq <= (r1 + r2)**2:
        # 发生碰撞，计算碰撞点和法线
        # 为了简化，我们假设碰撞发生在当前时间步长内，并回溯到碰撞发生的时间点
        # 这是一个简化的处理，更精确的物理模拟需要更复杂的碰撞时间计算
        
        # 计算碰撞法线
        normal_x = (next_x1 - next_x2)
        normal_y = (next_y1 - next_y2)
        norm = np.sqrt(normal_x**2 + normal_y**2)
        if norm != 0:
            normal_x /= norm
            normal_y /= norm
        else:
            # 如果距离为0，随机一个法线方向避免除以零
            normal_x = 1.0
            normal_y = 0.0

        # 计算碰撞后的速度
        v1x, v1y, v2x, v2y = calculate_post_collision_velocities(m1, v1x, v1y, m2, v2x, v2y, normal_x, normal_y)

    # 更新位置
    x1 += v1x * dt
    y1 += v1y * dt
    x2 += v2x * dt
    y2 += v2y * dt

# 设置绘图
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal', adjustable='box')

circle1 = plt.Circle((x1_history[0], y1_history[0]), r1, fc='blue')
circle2 = plt.Circle((x2_history[0], y2_history[0]), r2, fc='red')

ax.add_patch(circle1)
ax.add_patch(circle2)

def init():
    circle1.set_center((x1_history[0], y1_history[0]))
    circle2.set_center((x2_history[0], y2_history[0]))
    return circle1, circle2

def animate(i):
    circle1.set_center((x1_history[i], y1_history[i]))
    circle2.set_center((x2_history[i], y2_history[i]))
    return circle1, circle2

ani = animation.FuncAnimation(fig, animate, frames=num_frames, init_func=init, blit=True, interval=dt*1000)

# 保存动画
output_path = '/Users/zhengxueke/Desktop/zxkzzq.github.io-main/animations/physics_collision.mp4' # 修改保存路径
print(f"正在保存动画到 {output_path}...")
ani.save(output_path, fps=int(1/dt), writer='ffmpeg')
print("动画保存完成！")

plt.show()