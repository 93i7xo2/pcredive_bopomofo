
import time
import tools
import json

p, t = tools.findPair('ㄦ', '看到隆起來的手臂肌肉了嗎？那就是二頭肌。')
print(p, t)  # 1.0 ㄧ
p, t = tools.findPair('ㄦ', '紅色又酸酸甜甜的水果。')
print(p, t)  # 0.0 None
p, t = tools.findPair('ㄩ', '主要是避雨用的傘。')
print(p, t)  # 0.5 ㄢ

print(tools.coff_pc('ㄦ'))  # 0.5

with open("findPairInRoundTable.json") as f:
    tools.findPairInRoundTable = json.load(f)
t = time.time()
possibility, _ = tools.findPairInRound('ㄓ', '海軍使用的軍用船隻。', 1)
print("%.1f %% %.3f sec"%(possibility*100,time.time()-t,))