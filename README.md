# starEDN
### Requirements

* python 3.6+
* pytorch >=1.6, torchvision, OpenCV-Python, tqdm

Simply using:
````
pip install -r requirements.txt
````
to install all requirements.

### Data Preparing

[reference](https://github.com/yuhuan-wu/EDN)
After completion of downloading, extract the data and put them to `./data/` folder:

```
unzip SOD_datasets.zip -O ./data
```

## Training and Testing
- Download the pretrained starnet_s1 model[sttarnet_s1](https://github.com/ma-xu/Rewrite-the-Stars/tree/main/imagenet) and put it into `pretrained/` folder.

### Train

If you cannot run `bash scripts/prepare_data.sh`, please first download the imagenet pretrained models and put them to `pretrained` folder:
It is very simple to train our network. We have prepared a script to train starEDN:
```
bash ./scripts/train.sh
```

#### Generate Saliency Maps

After preparing the pretrained models, it is also very simple to generate saliency maps via EDN-VGG16/EDN-R50/EDN-Lite/EDN-LiteEX:

```
bash ./tools/test.sh
```

The scripts will automatically generate saliency maps on the `salmaps/` directory.

### Demo

We provide some examples for quick run:
````
python demo.py
````

## Acknowledgments
- **EDN Project**: The core of this project is largely derived from the [EDN](https://github.com/yuhuan-wu/EDN) and [StarNet](https://github.com/ma-xu/Rewrite-the-Stars/tree/main) codebase. We have made minor adjustments for our specific use case. 
````
@ARTICLE{wu2022edn,
  title={EDN: Salient object detection via extremely-downsampled network},
  author={Wu, Yu-Huan and Liu, Yun and Zhang, Le and Cheng, Ming-Ming and Ren, Bo},
  journal={IEEE Transactions on Image Processing},
  year={2022}
}

@ARTICLE{wu2021mobilesal,
  author={Wu, Yu-Huan and Liu, Yun and Xu, Jun and Bian, Jia-Wang and Gu, Yu-Chao and Cheng, Ming-Ming},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}, 
  title={MobileSal: Extremely Efficient RGB-D Salient Object Detection}, 
  year={2021},
  doi={10.1109/TPAMI.2021.3134684}
}
@inproceedings{ma2024rewrite,
    title={Rewrite the Stars},
    author={Xu Ma and Xiyang Dai and Yue Bai and Yizhou Wang and Yun Fu},
    booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year={2024}
}
````
