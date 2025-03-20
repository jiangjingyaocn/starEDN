import os

# 指定目录路径
dir_path = "/Users/jjy/Desktop/Method/EDNNew/data/blockage"
# dir_path = "/Users/jjy/Desktop/Method/EDNNew/data/selectedall"

# 遍历目录中的所有文件
for filename in os.listdir(dir_path):
    if filename.endswith(".png"):  # 找到所有 .png 文件
        old_path = os.path.join(dir_path, filename)
        new_path = os.path.join(dir_path, filename[:-4] + ".jpg")  # 修改后缀
        os.rename(old_path, new_path)  # 重命名文件

print("所有 .png 文件已成功修改为 .jpg")