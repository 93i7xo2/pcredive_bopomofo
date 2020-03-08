# Usage
打開android debugging

```
# for python script
apt install python3-opencv
python3 -m pip install matplotlib

# for scrcpy
sudo apt install  libsdl2-image-2.0-0

# create ramdisk
mkdir /tmp/ramfs
sudo mount -t ramfs ramfs /tmp/ramfs
sudo chmod o+rwx /tmp/ramfs

# run
./run.sh
```

# Test
```
make test
```

# Note
1. `scrcpy`顯示手機畫面附加點擊功能，會讀取`x`,`y`做為滑鼠點擊座標
2. `main.py`會讀取`scrcpy`存下的畫面進行辨識
    ```python
    python3 ./main.py --input=[image_path] --output_x=[output_x] --output_y=[output_y]
    ```
    image_path: 欲讀取的圖片位置
    output_x: 點擊座標存放位置
    output_y: 同上