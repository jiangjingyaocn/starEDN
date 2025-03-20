#!/bin/bash

#NAMES=('model_1-starnet_s1')
#!/bin/bash

# 生成模型名称数组
NAMES=()
#for i in {1..50}
#do
#  NAMES+=("model_${i}-starnet_s1")
#done

# 生成模型名称数组
NAMES=()
for i in 1 6 11 16 21 26 31 36
do
  NAMES+=("model_${i}-starnet_s1")
done

# 输出数组
echo "${NAMES[@]}"

for NAME in "${NAMES[@]}"
do
  PYTHONPATH=$(pwd):$PYTHONPATH  python3 scripts/test.py --pretrained pretrained/$NAME.pth \
                                      --savedir ./salmaps/$NAME/ \

done
