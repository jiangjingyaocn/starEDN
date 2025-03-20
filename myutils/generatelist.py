import os

# 设置图片目录路径
image_dir = '/Users/jjy/Desktop/Method/EDNNew/data/selectedall'
output_file = '/Users/jjy/Desktop/Method/EDNNew/data/selectedall.txt'

# 获取目录下所有的图片文件
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

# 将图片路径写入到文件，并为每个jpg文件添加对应的png文件路径
with open(output_file, 'w') as f:
    for image_file in image_files:
        # 获取原图片路径
        image_path = os.path.join(image_dir, image_file)

        # 处理jpg文件，替换为png文件路径
        if image_file.lower().endswith('.jpg'):
            image_path_png = os.path.splitext(image_path)[0] + '.png'
            f.write(image_path + ' ' + image_path_png + '\n')
        else:
            f.write(image_path + '\n')

print(f"所有图片路径已存储到 {output_file}")

# import os
#
# # 设置图片目录路径
# image_dir = 'data/DUT-OMRON'
# output_file = 'data/DUT-OMRON.txt'
#
# # 获取目录下所有的图片文件
# image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
#
# # 将图片路径写入到文件
# with open(output_file, 'w') as f:
#     for image_file in image_files:
#         image_path = os.path.join(image_dir, image_file)
#         f.write(image_path + '\n')
#
# print(f"所有图片路径已存储到 {output_file}")