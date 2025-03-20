import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# 创建 FontProperties 对象
font_path = '/System/Library/Fonts/Hiragino Sans GB.ttc'
if os.path.exists(font_path):
    font = fm.FontProperties(fname=font_path)
else:
    font = None
    print(f"字体文件 {font_path} 不存在，使用默认字体。")

# 年份
years = list(range(2010, 2024))

# 排水管道长度（单位：万公里）
lengths = [36.96, 41.41, 43.91, 46.49, 51.12, 53.96, 57.66, 63.03, 68.35, 74.40, 80.27, 87.23, 91.35, 92.25]

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制折线图
plt.plot(years, lengths, marker='o', linestyle='-', color='b')

# 设置纵坐标轴的最低刻度为0
plt.ylim(bottom=0,top = 100)

# 在每个数据点上方显示对应的值，偏移量为0.5万公里
for x, y in zip(years, lengths):
    plt.text(x, y + 1.5, f'{y:.2f}', ha='center', va='bottom', fontproperties=font)

# 添加标题和标签
plt.title('2010年至2023年中国城市排水管道总长度', fontproperties=font)
plt.xlabel('年份', fontproperties=font)
plt.ylabel('排水管道总长度（万公里）', fontproperties=font)

# 显示网格
plt.grid(True)

# 指定保存路径和文件名
save_path = '/Users/jjy/Desktop/Method/EDNNew/results'
file_name = 'paishuiguanwangqushi.png'
full_path = os.path.join(save_path, file_name)

# 保存图像
plt.savefig(full_path, dpi=300, bbox_inches='tight')

# 显示图形
plt.show()