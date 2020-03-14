import time
import tools
import json

t = time.time()
findPairInRoundTableKeys = set([l["info"] for l in tools.mapping_list])
count1 = 0
for b in tools.bopomopo_character_set:
    count1= count1 +1
    count2 = 0
    for k in findPairInRoundTableKeys:
        count2= count2 +1
        print("%d/%d %d/%d"%( \
            count2, \
            len(findPairInRoundTableKeys), \
            count1, \
            len(tools.bopomopo_character_set)))
        for r in range(16):
            tools.findPairInRound(b,k,r)
with open("findPairInRoundTable.json","w", encoding='utf8') as f:
    json.dump(tools.findPairInRoundTable, f, ensure_ascii=False)
print("Elapsed time: %.3f sec"%(time.time()-t,))