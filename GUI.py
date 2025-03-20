import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import demo  # 直接导入 demo.py
from argparse import Namespace
from PIL import Image


class ImagePredictorGUI(QWidget):
    def __init__(self):
        super().__init__()

        # 窗口标题
        self.setWindowTitle("图片检测界面")
        self.setGeometry(100, 100, 700, 500)

        # 按钮
        self.upload_btn = QPushButton("上传图片", self)
        self.run_btn = QPushButton("运行检测", self)

        # 显示图片的标签
        self.uploaded_image_label = QLabel("上传的图片", self)
        self.uploaded_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.predicted_image_label = QLabel("检测结果", self)
        self.predicted_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 显示检测信息的标签
        self.info_label = QLabel("检测信息将在此显示", self)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 绑定按钮事件
        self.upload_btn.clicked.connect(self.upload_image)
        self.run_btn.clicked.connect(self.run_prediction)

        # 布局管理
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.run_btn)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.uploaded_image_label)
        image_layout.addWidget(self.predicted_image_label)

        layout.addLayout(button_layout)
        layout.addLayout(image_layout)
        layout.addWidget(self.info_label)  # 检测信息在最下方

        self.setLayout(layout)

        # 存储当前上传的图片路径
        self.current_image = None

    def upload_image(self):
        """ 选择单张图片 """
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg)")

        if file_path:
            self.current_image = file_path
            self.display_image(self.uploaded_image_label, self.current_image)
            self.info_label.setText(f"已上传：{os.path.basename(file_path)}")

    def run_prediction(self):
        """ 调用 demo.main 运行检测 """
        if not self.current_image:
            self.info_label.setText("请先上传图片")
            return

        self.info_label.setText("正在运行检测，请稍等...")
        start_time = time.time()  # 记录开始时间

        # 构造 demo.py 需要的参数
        args = Namespace(
            arch="starnet_s1",
            example_dir=os.path.dirname(self.current_image) + "/",  # 只传入目录
            width=384,
            height=384,
            gpu=False,
            pretrained="pretrained/model_25-starnet_s1.pth"
        )

        # 运行 demo.py 的 main 函数
        demo.main(args)

        # 检测后的文件名
        file_root, ext = os.path.splitext(self.current_image)
        save_path = file_root + "_edn.png"

        # 等待文件生成（最多 5 秒）
        for _ in range(50):  # 每次等待 0.1s，总共 5 秒
            if os.path.exists(save_path):
                break
            time.sleep(0.1)

        # 计算检测时间
        elapsed_time = time.time() - start_time

        # 检查文件是否生成
        if os.path.exists(save_path):
            self.display_image(self.predicted_image_label, save_path)

            # 获取图片尺寸
            img = Image.open(save_path)
            width, height = img.size

            self.info_label.setText(f"检测完成: {os.path.basename(self.current_image)}\n"
                                    f"图片尺寸: {width} x {height}\n"
                                    f"处理时间: {elapsed_time:.2f} 秒")
        else:
            self.info_label.setText("检测失败，请检查！")

    def display_image(self, label, image_path):
        """ 在 QLabel 上显示图片 """
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)  # 调整大小
        label.setPixmap(pixmap)
        label.repaint()  # 强制刷新 UI


# 运行 GUI
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImagePredictorGUI()
    window.show()
    sys.exit(app.exec())