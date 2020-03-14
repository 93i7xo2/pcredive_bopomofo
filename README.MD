# Prerequisites
```
# for python script
python3 -m pip install matplotlib
python3 pip install opencv-python
```

# Usage
Enable android debugging
Open `scrcpy`
```
make build
make run
make clean
```

# Test
```
make test
```

# Note
`main.py`用螢幕截圖存下畫面進行辨識
```python
python3 ./main.py --input=[image_path]
```
image_path: 欲讀取的圖片位置
