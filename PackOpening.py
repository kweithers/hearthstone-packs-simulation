import random
#initialize dictionary of probabilities 
probs = {}
probs['common'] = .7014
probs['rare'] = .2151
probs['epic'] = .0419
probs['legendary'] = .01
probs['golden_common'] = .0149
probs['golden_rare'] = .0133
probs['golden_epic'] = .0025
probs['golden_legendary'] = .0009
#generate the rarity of a card, given a dictionary of probabilities
def generate_rarity(dct):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
#generate a card, given its rarity
#49 commons, 36 rares, 27 epics, 23 legendaries
def generate_card(rarity):
    if rarity == 'common':
        return random.randint(1,49)
    if rarity == 'rare':
        return random.randint(50,85)
    if rarity == 'epic':
        return random.randint(86,112)
    if rarity == 'legendary':
        return random.randint(113,135)
    if rarity == 'golden_common':
        return random.randint(1+135,49+135)
    if rarity == 'golden_rare':
        return random.randint(50+135,85+135)
    if rarity == 'golden_epic':
        return random.randint(86+135,112+135)
    if rarity == 'golden_legendary':
        return random.randint(113+135,135+135)
#open a pack of five cards
def open_pack(dct,collection):
    pack = []
    for i in range(5):
        new_rarity = generate_rarity(dct)
        #no dupe leggos
        if new_rarity in ['legendary','golden_legendary']:
            while True:
                lego = generate_card(new_rarity)
                if collection.get(lego % 135) < 1:
                    pack.append(lego)
                    break
        else:
            pack.append(generate_card(new_rarity))
    return pack
#disenchant function for goldens and extras
def disenchant(card_num):
    if card_num <= 49:
        return 5
    elif card_num <= 85:
        return 20
    elif card_num <= 112:
        return 100
    elif card_num <= 135:
        return 400
    elif card_num <= 49+135:
        return 50
    elif card_num <= 85+135:
        return 100
    elif card_num <= 112+135:
        return 400
    elif card_num <= 135+135:
        return 1600  
num_packs = []    
for k in range(10000):
    full_set = False
    remaining_cost = 40*49*2 + 100*36*2 + 400*27*2 + 1600*23
    dust = 0
    packs = 0
    collection = {}
    for i in range(1,136):
        collection[i] = 0
    while not full_set:
        packs +=1
        new_pack = open_pack(probs,collection) 
        for i in new_pack:
            #disenchant all goldens..
            if i > 135:
                dust += disenchant(i)
            elif (i >= 113 and i <=135):
                if collection.get(i) < 1:
                    collection[i] +=1
                    remaining_cost -= 1600
                else:
                    dust += disenchant(i)
            elif (i >= 86 and i <=112):
                if collection.get(i) < 2:
                    collection[i] +=1
                    remaining_cost -= 400
                else:
                    dust += disenchant(i)
            elif (i >= 50 and i <=85):
                if collection.get(i) < 2:
                    collection[i] +=1
                    remaining_cost -= 100
                else:
                    dust += disenchant(i)
            elif (i >= 1 and i <=49):
                if collection.get(i) < 2:
                    collection[i] +=1
                    remaining_cost -= 40
                else:
                    dust += disenchant(i)
        if dust >= remaining_cost:
            full_set = True
    num_packs.append(packs)
import matplotlib.pyplot as plt
plt.hist(num_packs)
plt.show()
import pandas
the_df = pandas.DataFrame(num_packs)
print the_df.describe()