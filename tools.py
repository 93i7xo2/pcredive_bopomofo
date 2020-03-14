import json
from math import factorial as fac

with open('data.json') as f:
    mapping_list = json.load(f)

bopomopo_character_set = ['ㄓ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄙ', 'ㄚ', 'ㄛ', 'ㄜ', 'ㄞ', 'ㄟ', 'ㄠ', 'ㄡ', 'ㄢ', 'ㄣ', 'ㄤ', 'ㄥ', 'ㄦ', 'ㄧ',
                          'ㄧㄚ', 'ㄧㄝ', 'ㄧㄠ', 'ㄧㄡ', 'ㄧㄢ', 'ㄧㄣ', 'ㄧㄤ', 'ㄧㄥ', 'ㄨ', 'ㄨㄚ', 'ㄨㄛ', 'ㄨㄟ', 'ㄨㄢ', 'ㄨㄣ',
                          'ㄨㄤ', 'ㄨㄥ', 'ㄩ', 'ㄩㄝ', 'ㄩㄢ', 'ㄩㄣ']

''' Calculate binomial coefficient xCy = x! / (y! (x-y)!)
'''


def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom


def findHead(filterSymbol, sort=True):
    # Input a single character of bopomofo
    # Return Pair list or Empty list
    if filterSymbol in ['ㄓ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄙ']:
        filterSymbol = ['ㄓ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄙ']
    else:
        filterSymbol = [filterSymbol]

    def fun(v):
        if v["head"] in filterSymbol:
            return True
        else:
            return False
    result = list(filter(fun, mapping_list))

    if sort is True:
        switcher = {
            "normal": 0,
            "great": 1,
            "puricone": 2
        }
        result = sorted(
            result, key=lambda i: switcher[i["property"]], reverse=True)
    return result


def findPair(head, info):
    # Given that you know the head, how much possibility will the given info appear?

    # find all pairs
    pairs = findHead(head)
    tail = None
    if len(list(filter(lambda x: x["info"] == info, pairs))) > 0:
        tail = list(filter(lambda x: x["info"] == info, pairs))[0]["tail"]

    # seperate pairs into different groups: normal, great, puricone
    n = list(filter(lambda x: x["property"] == "normal", pairs))
    g = list((filter(lambda x: x["property"] == "great", pairs)))
    p = list(filter(lambda x: x["property"] == "puricone", pairs))

    n_count = len(n)
    g_count = len(g)
    p_count = len(p)

    n_tail_count = len(list(filter(lambda x: x["info"] == info, n)))
    g_tail_count = len(list(filter(lambda x: x["info"] == info, g)))
    p_tail_count = len(list(filter(lambda x: x["info"] == info, p)))

    n_x_count = min(2, len(n))
    g_x_count = min(3, len(g))
    p_x_count = min(1, len(p))

    probability = 1 - \
        (binomial(n_count-n_tail_count, n_x_count)/binomial(n_count, n_x_count)) * \
        (binomial(g_count-g_tail_count, g_x_count)/binomial(g_count, g_x_count)) * \
        (binomial(p_count-p_tail_count, p_x_count)/binomial(p_count, p_x_count))

    return (probability, tail)


def coff_pc(head):
    # find all pairs
    pairs = findHead(head)

    # seperate pairs into different groups: normal, great, puricone
    n = list(filter(lambda x: x["property"] == "normal", pairs))
    g = list((filter(lambda x: x["property"] == "great", pairs)))
    p = list(filter(lambda x: x["property"] == "puricone", pairs))

    n_x_count = min(2, len(n))
    g_x_count = min(3, len(g))
    p_x_count = min(1, len(p))

    return 1/(n_x_count+g_x_count+p_x_count)


# Create lookup table for  function findPairInRound
findPairInRoundTableKeys = set([l["info"] for l in mapping_list])
findPairInRoundTable = {}
for b in bopomopo_character_set:
    findPairInRoundTable[b] = {}
    for k in findPairInRoundTableKeys:
        findPairInRoundTable[b][k] = {}
        for r in range(30):
            findPairInRoundTable[b][k][str(r)] = None


def findPairInRound(head, target_info, round):
    # 如果對方丟個head進來，九宮格還沒出現，有多大機率出現info，而且如果是嘉夜的回合，嘉夜剛好選到info
    # lookup  table
    tmp =  findPairInRoundTable[head][target_info][str(round)] 
    if tmp is not None:
        return tmp

    # final round
    if round >= 15:
        findPairInRoundTable[head][target_info][round] = findPair(
            head, target_info)  # save
        return findPair(head, target_info)

    matching_pairs = findHead(head, target_info)
    if len(list(filter(lambda x: x["info"] == target_info, matching_pairs))) == 0:
        # The info not in the current round
        p = 0
        t = None
        for pair in matching_pairs:
            # Find the maximum possibility
            # In this case, pair["tail"] = t1, we call this function to get possibility
            p1, t1 = findPair(pair["head"], pair["info"])
            p2, t2 = findPairInRound(t1, target_info, round + 1)
            p_ = p1*p2
            t_ = t2
            if round % 2 == 0:
                # カヤ
                p_ = p_ * coff_pc(pair["head"])
            if p_ > p:
                p = p_
                t = t_

        findPairInRoundTable[head][target_info][str(round)] = (p, t)  # save
        return p, t
    else:
        # The info is in the current round
        p, t = findPair(head, target_info)
        if round % 2 == 0:
            # カヤ
            p = p * coff_pc(head)
        findPairInRoundTable[head][target_info][str(round)] = (p, t)  # save
        return (p, t)
