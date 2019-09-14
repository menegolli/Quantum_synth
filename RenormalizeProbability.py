#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def RenormalizeCell(listForMusic):
    '''
    Redistributes the measurements that are going outside the range [0, 11].
    '''
    lst_todel = []
    # Removes the useless 
    for idx, i in enumerate(listForMusic):
        if (int(i.split(" ")[0]) > 11):
            lst_todel.append(idx)
    lst_todel.sort(reverse=True)
    for i_todel in lst_todel:
        listForMusic.pop(i_todel)
    # Renormalizes the probability
    overall_sum = 0.
    tmp_list_int = []
    tmp_list_prob = []
    for i in listForMusic:
        tmp_list_prob.append(float(i.split(" ")[1]))
        tmp_list_int.append(int(i.split(" ")[0]))
    overall_prob = sum(tmp_list_prob)
    tmp_list_prob = [i/overall_prob for i in tmp_list_prob]
    # Rewrites the list
    NewListForMusic = []
    for idx in range(len(tmp_list_int)):
        NewListForMusic.append("%d %.3f" % (tmp_list_int[idx], tmp_list_prob[idx]))
    return NewListForMusic

def RedistributeCell(listForMusic):
    '''
    Redistributes the measurements that are going outside the range [0, 11]
    based on the following mapping: the probability of the combination associated
    to integer 12 is given to the first four integers, the combination associated
    to the integer 12 to the second four integers and so on.
    '''
    # Removes the useless 
    probability_to_redistributed = [0., 0., 0., 0.]
    for idx, i in enumerate(listForMusic):
        if (idx == 12):
            probability_to_redistributed[0] = float(i)/3.
        elif (idx == 13):
            probability_to_redistributed[1] = float(i)/3.
        elif (idx == 14):
            probability_to_redistributed[2] = float(i)/3.
        elif (idx == 15):
            probability_to_redistributed[3] = float(i)/3.
    newlistForMusic = listForMusic[:12]
    # Renormalizes the probability
    for idx in range(len(newlistForMusic)):
        if (0 <= idx <= 2):
            newlistForMusic[idx] = '{:05.3f}'.format(float(newlistForMusic[idx])+probability_to_redistributed[0])
        elif (3 <= idx <= 5):
            newlistForMusic[idx] = '{:05.3f}'.format(float(newlistForMusic[idx])+probability_to_redistributed[1])
        elif (6 <= idx <= 8):
            newlistForMusic[idx] = '{:05.3f}'.format(float(newlistForMusic[idx])+probability_to_redistributed[2])
        elif (9 <= idx <= 11):
            newlistForMusic[idx] = '{:05.3f}'.format(float(newlistForMusic[idx])+probability_to_redistributed[3])

    return newlistForMusic
