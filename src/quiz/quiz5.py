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
import glob
import os
from types import SimpleNamespace
from typing import Iterable, Tuple, Any, List, Set

import ahocorasick


def create_ac(data: Iterable[Tuple[str, Any]]) -> ahocorasick.Automaton:
    """
    Creates the Aho-Corasick automation and adds all (span, value) pairs in the data and finalizes this matcher.
    :param data: a collection of (span, value) pairs.
    """
    AC = ahocorasick.Automaton(ahocorasick.STORE_ANY)

    for span, value in data:
        if span in AC:
            t = AC.get(span)
        else:
            t = SimpleNamespace(span=span, values=set())
            AC.add_word(span, t)
        t.values.add(value)

    AC.make_automaton()
    return AC


def read_gazetteers(dirname: str) -> ahocorasick.Automaton:
    data = []
    for filename in glob.glob(os.path.join(dirname, '*.txt')):
        label = os.path.basename(filename)[:-4]
        for line in open(filename):
            data.append((line.strip(), label))
    return create_ac(data)


def match(AC: ahocorasick.Automaton, tokens: List[str]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param AC: the finalized Aho-Corasick automation.
    :param tokens: the list of input tokens.
    :return: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    """
    smap, emap, idx = dict(), dict(), 0
    for i, token in enumerate(tokens):
        smap[idx] = i
        idx += len(token)
        emap[idx] = i
        idx += 1

    # find matches
    text = ' '.join(tokens)
    spans = []
    for eidx, t in AC.iter(text):
        eidx += 1
        sidx = eidx - len(t.span)
        sidx = smap.get(sidx, None)
        eidx = emap.get(eidx, None)
        if sidx is None or eidx is None: continue
        spans.append((t.span, sidx, eidx + 1, t.values))

    return spans


def remove_overlaps(entities: List[Tuple[str, int, int, Set[str]]]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    :return: a list of entities where each entity is represented by a tuple of (span, start index, end index, value set)
    """
    # TODO: to be updated
    final = []
    i = 0
    j = 1
    while i < len(entities) - 1 and j < len(entities):
        startI = entities[i][1]
        endI = entities[i][2]
        startJ = entities[j][1]
        endJ = entities[j][2]
        if startJ < endI and endI != endJ:
            if entities[j] not in final:
                final.append(entities[j])
        if endJ == endI and startI < startJ:
            if entities[i] not in final:
                final.append(entities[i])
        if startJ == endI and startI < startJ and endI < endJ:
            if entities[i] not in final and entities[j] not in final:
                final.append(entities[i])
                final.append(entities[j])
        i+=1
        j+=1
    return final 


def to_bilou(tokens: List[str], entities: List[Tuple[str, int, int, str]]) -> List[str]:
    """
    :param tokens: a list of tokens.
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a named entity tag
    :return: a list of named entity tags in the BILOU notation with respect to the tokens
    """
    # TODO: to be updated
    final = []
    ebank = []
    for i in entities:
        walk = i[0]
        e = walk.split()
        for x in e:
            ebank.append(x)
    k = 0
    while k < len(tokens):
        if tokens[k] in ebank:
            walk = tokens[k]
            for n in entities:
                sidx = n[1]
                eidx = n[2]
                tag = n[3]
                if walk in n[0] and k == sidx and k+1 == eidx:
                    final.append("U-"+tag)
                    sidx = 0
                    eidx = 0
                elif walk in n[0] and k==sidx and eidx > k+1:
                    final.append("B-"+tag)
                    sidx = 0
                    eidx = 0
                elif walk in n[0] and k+1 == eidx:
                    final.append('L-'+tag)
                elif walk in n[0] and k > sidx and k < eidx:
                    final.append('I-'+tag)
            k+=1
        else:
            final.append("O")
            k+=1
    return final


if __name__ == '__main__':
    gaz_dir = 'dat/ner'
    AC = read_gazetteers('dat/ner')

    tokens = 'Atlantic City of Georgia'.split()
    entities = match(AC, tokens)
    entities = remove_overlaps(entities)
    print(entities)

    tokens = 'South Korea United States'.split()
    entities = match(AC, tokens)
    entities = remove_overlaps(entities)
    print(entities)
    tokens = 'Jinho is a professor at Emory University in the United States of America'.split()
    entities = [
      ('Jinho', 0, 1, 'PER'),
      ('Emory University', 5, 7, 'ORG'),
      ('United States of America', 9, 13, 'LOC')
    ]
    tags = to_bilou(tokens, entities)
    for token, tag in zip(tokens, tags): print(token, tag) 


