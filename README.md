# d4killer

## 进度情况
- Jul 24
  - 项目开始，完成基础架构
  - 实现鼠标遍历所有物品格
  - 实现第一个装备位截图
  - TODO 优化截图逻辑
  - TODO 自定义物品筛选逻辑
  - TODO 实现模糊匹配 https://blog.51cto.com/u_15091060/2671840

## 本地配置

**暂时只支持N卡用户 需自行安装CUDA工具 （CPU也可运行，如果不介意速度 比人眼看还慢lol）**

本地运行需要电脑安装Python 3.11, 请到官网安装最新版本：https://www.python.org/downloads/

## 需要的包

### Numpy & OpenCV
numpy用来搭配OpenCV处理图片达到更好的识别率
### pyautogui
用来实现操作鼠标键盘
### PIL
用来实现截图操作

```
pip3 install numpy
pip3 install opencv-python
pip3 install pyautogui
```

### EasyOCR
本地的OCR，请参考JaidedAI官方配置（注意先安装torch）
https://github.com/JaidedAI/EasyOCR

## 使用
后台运行本程序
```
python d4killer
```

以窗口全屏运行游戏。在游戏中打开装备栏后按backspace鼠标会自动遍历全部物品并自动把垃圾表极为垃圾。
考虑到OCR精度还请自己再扫一眼 lol

### 判定流程

**第一层整体判断**
1. 先祖以下均判定为垃圾
2. 武器装等低于800判定为垃圾
3. 其他部位装等低于760判定为垃圾

**第二层针对职业和流派判断**
must - 必须全部存在，否则判定为垃圾。每条记1分。
t0 - 加一分
t1 - 不得分
如果最够得分超过2则保留

### 词条优先级结构
```json
{
  "BARB": {
    "arsenal": {
      "头盔": {
        "must": [],
        "t0": [],
        "t1":[]
      }
    }
  }
}
```



