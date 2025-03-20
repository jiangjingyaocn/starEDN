import sys
import os
import time
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QScrollArea, QGridLayout, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import demo  # 直接导入 demo.py
from argparse import Namespace
from PIL import Image


class ImagePredictorGUI(QWidget):
    def __init__(self):
        super().__init__()

        # 窗口标题
        self.setWindowTitle("批量图片预测界面")
        self.setGeometry(100, 100, 1000, 600)

        # 按钮
        self.upload_btn = QPushButton("上传图片", self)
        self.run_btn = QPushButton("运行预测", self)

        # 绑定按钮事件
        self.upload_btn.clicked.connect(self.upload_images)
        self.run_btn.clicked.connect(self.run_predictions)

        # 创建滚动区域，用于展示多个图片对比
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        # 显示预测信息的标签
        self.info_label = QLabel("预测信息将在此显示", self)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 总布局管理
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.run_btn)

        layout.addLayout(button_layout)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.info_label)  # 预测信息在最下方

        self.setLayout(layout)

        # 存储当前上传的图片列表
        self.image_paths = []
        self.predicted_paths = {}

    def upload_images(self):
        """ 选择多张图片 """
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "Images (*.png *.jpg *.jpeg)")

        if file_paths:
            self.image_paths = file_paths
            self.predicted_paths.clear()
            self.display_images()
            self.info_label.setText(f"已选择 {len(self.image_paths)} 张图片")

    def run_predictions(self):
        """ 调用 demo.main 批量运行预测 """
        if not self.image_paths:
            self.info_label.setText("请先上传图片")
            return

        self.info_label.setText("正在运行预测，请稍等...")
        start_time = time.time()  # 记录开始时间

        for idx, image_path in enumerate(self.image_paths):
            # 构造 demo.py 需要的参数
            args = Namespace(
                arch="starnet_s1",
                example_dir=os.path.dirname(image_path) + "/",  # 只传入目录
                width=384,
                height=384,
                gpu=False,
                pretrained="pretrained/model_4-starnet_s1.pth"
            )

            # 运行 demo.py 的 main 函数
            demo.main(args)

            # 预测后的文件名
            file_root, ext = os.path.splitext(image_path)
            save_path = file_root + "_edn.png"

            # 等待文件生成（最多 5 秒）
            for _ in range(50):  # 每次等待 0.1s，总共 5 秒
                if os.path.exists(save_path):
                    break
                time.sleep(0.1)

            if os.path.exists(save_path):
                self.predicted_paths[image_path] = save_path  # 存储原图和预测图的对应关系

        # 计算预测总时间
        elapsed_time = time.time() - start_time

        # 显示预测结果
        if self.predicted_paths:
            self.display_images()
            self.info_label.setText(f"预测完成！共 {len(self.predicted_paths)} 张图片\n"
                                    f"总处理时间: {elapsed_time:.2f} 秒")
        else:
            self.info_label.setText("预测失败，请检查！")

    def display_images(self):
        """ 在界面上显示原图和预测图，并排排列 """
        # 清空布局
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for idx, img_path in enumerate(self.image_paths):
            # 显示原图
            orig_label = QLabel()
            orig_pixmap = QPixmap(img_path)
            orig_pixmap = orig_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)  # 调整大小
            orig_label.setPixmap(orig_pixmap)
            orig_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            orig_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            # 显示预测图（如果已存在）
            pred_label = QLabel()
            if img_path in self.predicted_paths:
                pred_pixmap = QPixmap(self.predicted_paths[img_path])
                pred_pixmap = pred_pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)
                pred_label.setPixmap(pred_pixmap)
            else:
                pred_label.setText("等待预测")

            pred_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pred_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            # 添加到网格布局中
            self.grid_layout.addWidget(orig_label, idx, 0)  # 原图在左
            self.grid_layout.addWidget(pred_label, idx, 1)  # 预测图在右

            # 显示图片信息（分辨率）
            img = Image.open(img_path)
            info_label = QLabel(f"{os.path.basename(img_path)}\n尺寸: {img.width}x{img.height}")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(info_label, idx, 2)

        self.scroll_widget.setLayout(self.grid_layout)


# 运行 GUI
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImagePredictorGUI()
    window.show()
    sys.exit(app.exec())