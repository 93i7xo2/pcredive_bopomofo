# RAMDISK使用教學
mkdir /tmp/ramfs
sudo mount -t ramfs ramfs /tmp/ramfs
sudo chmod o+rwx /tmp/ramfs

# Build
```
apt install python3-opencv
python3 -m pip install matplotlib
```
# Test
```
make test
```

# USAGE
1. scrcpy顯示手機畫面
    ```
    ./scrcpy
    ```
    改過的scrcpy會將畫面存放在`somewhere`、並讀取`x`,`y`做為滑鼠點擊座標，`x`,`y`皆為0時不點擊

2. 辨識小程式
    讀取scrcpy存下的畫面進行辨識
    ```python
    python3 ./main.py --input=[image_path] --output_x=[output_x] --output_y=[output_y]
    ```
    image_path: 欲讀取的圖片位置
    output_x: 點擊座標存放位置
    output_y: 同上

# Example
```
./scrcpy
python3 ./main.py --input=/tmp/ramfs/iamge --output_x=/tmp/ramfs/nextord-x --output_y=/tmp/ramfs/nextord-y
```