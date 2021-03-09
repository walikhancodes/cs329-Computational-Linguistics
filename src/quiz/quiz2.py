# ========================================================================
# Copyright 2020 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
#THIS CODE WAS MY OWN WORK,
#IT WAS WRITTEN WITHOUT CONSULTING ANY SOURCES
#OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.
#Wali Khan 2308097


from typing import Set, Optional, List
from nltk.corpus.reader import Synset
from nltk.corpus import wordnet as wn

def antonyms(sense: str) -> Set[Synset]:
    """
    :param sense: the ID of the sense (e.g., 'dog.n.01').
    :return: a set of Synsets representing the union of all antonyms of the sense as well as its synonyms.
    """
    walk = wn.synset(sense)
    walk_lemmas = walk.lemmas()
    result = set()
    for x in walk_lemmas:
        i = x.antonyms()
        for y in i:
            result.add(y.synset())
        result = result | result
    return result



def paths(sense_0: str, sense_1: str) -> List[List[Synset]]:
    # TODO: to be updated
    path1 = []
    path2 = []
    walk1 = wn.synset(sense_0)
    walk2 = wn.synset(sense_1)
    a = walk1.hypernym_paths()
    b = walk2.hypernym_paths()
    lch = walk1.lowest_common_hypernyms(walk2)
    final = []
    for hypernym in lch:
        for syn_list in a:
            i = next((i for i, syn in enumerate(syn_list) if syn == hypernym), -1)
            if i >= 0: path1.append(syn_list[i:])
        for syn_list in b:
            i = next((i for i, syn in enumerate(syn_list) if syn == hypernym), -1)
            if i >= 0: path2.append(syn_list[i:])
    
    # REMOVING DUPLICATE SYN LISTS 
    path11 = []
    path22 = []
    for j in path1:
        if j not in path11:
            path11.append(j)
    for k in path2:
        if k not in path22:
            path22.append(k)
    newpath1 =[]
    for listOfSyns1 in path11:
        listOfSyns1.reverse()
        newpath1.append(listOfSyns1) 
    for thisList in newpath1:
        for list2 in path22:
            size2 = len(list2)
            size1 = len(thisList) -1
            walk1 = thisList[size1]
            walk2 = list2[0]
            if walk1 == walk2:
                final.append(thisList + list2[1:size2])
    return final


if __name__ == '__main__':
    print(antonyms('nonspecific.a.01'))
    print(antonyms('end.v.02'))
    print(antonyms('purchase.v.01'))
    print(antonyms('dog.n.01'))
    
    print()
    for path in paths('body.n.09', 'sidereal_day.n.01'):
        print([s.name() for s in path])
    print()
    for path in paths('boy.n.01', 'girl.n.01'):
        print([s.name() for s in path])
    print()
    for path in paths('dog.n.01', 'cat.n.01'):
        print([s.name() for s in path])


