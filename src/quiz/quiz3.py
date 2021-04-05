#THIS CODE WAS MY OWN WORK,
#IT WAS WRITTEN WITHOUT CONSULTING ANY SOURCES
#OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.
#Wali Khan 2308097
import pickle
from collections import Counter
from typing import List, Tuple, Dict, Any

DUMMY = '!@#$'


def read_data(filename: str):
    data, sentence = [], []
    fin = open(filename)

    for line in fin:
        l = line.split()
        if l:
            sentence.append((l[0], l[1]))
        else:
            data.append(sentence)
            sentence = []

    return data


def to_probs(model: Dict[Any, Counter]) -> Dict[str, List[Tuple[str, float]]]:
    probs = dict()
    for feature, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        probs[feature] = [(label, count/total) for label, count in ts]
    return probs


def evaluate(data: List[List[Tuple[str, str]]], *args):
    total, correct = 0, 0
    for sentence in data:
        tokens, gold = tuple(zip(*sentence))
        pred = [t[0] for t in predict(tokens, *args)]
        total += len(tokens)
        correct += len([1 for g, p in zip(gold, pred) if g == p])
    accuracy = 100.0 * correct / total
    return accuracy


def create_cw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for word, pos in sentence:
            model.setdefault(word, Counter()).update([pos])
    return to_probs(model)

def create_cnw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the next/current word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault(next_word, Counter()).update([curr_pos])
            model.setdefault(word, Counter()).update([curr_pos])
    return to_probs(model)

def create_cpw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the prev/current word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            prev_word = sentence[i-1][0] if i > 0 else DUMMY
            model.setdefault(prev_word, Counter()).update([curr_pos])
            model.setdefault(word, Counter()).update([curr_pos])
    return to_probs(model)

def create_pwp_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the word /pred pos and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (word, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i-1][1] if i > 0 else DUMMY
            model.setdefault(prev_pos, Counter()).update([curr_pos])
            model.setdefault(word, Counter()).update([curr_pos])
    return to_probs(model)




def create_pp_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous POS tag and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i-1][1] if i > 0 else DUMMY
            model.setdefault(prev_pos, Counter()).update([curr_pos])
    return to_probs(model)

def create_np_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the next POS tag and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            next_pos = sentence[i+1][1] if i+1 < len(sentence) else DUMMY
            model.setdefault(next_pos, Counter()).update([curr_pos])
    return to_probs(model)

def create_ppp_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous previous POS tag and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i-2][1] if i > 0 else DUMMY
            model.setdefault(prev_pos, Counter()).update([curr_pos])
    return to_probs(model)

def create_nnp_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the next next POS tag and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            next_pos = sentence[i+2][1] if i+2 < len(sentence) else DUMMY
            model.setdefault(next_pos, Counter()).update([curr_pos])
    return to_probs(model)




def create_pw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_word = sentence[i-1][0] if i > 0 else DUMMY
            model.setdefault(prev_word, Counter()).update([curr_pos])
    return to_probs(model)

def create_ppw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous previous word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_prev_word = sentence[i-2][0] if i > 0 else DUMMY
            model.setdefault(prev_prev_word, Counter()).update([curr_pos])
    return to_probs(model)


def create_nw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the next word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault(next_word, Counter()).update([curr_pos])
    return to_probs(model)

def create_nnw_dict(data: List[List[Tuple[str,str]]]) -> Dict[str, List[Tuple[str,float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the next next word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            next_next_word = sentence[i+2][0] if i+2 < len(sentence) else DUMMY
            model.setdefault(next_next_word, Counter()).update([curr_pos])
    return to_probs(model)



def train(trn_data: List[List[Tuple[str, str]]], dev_data: List[List[Tuple[str, str]]]) -> Tuple:
    """
    :param trn_data: the training set
    :param dev_data: the development set
    :return: a tuple of all parameters necessary to perform part-of-speech tagging
    """
    cw_dict = create_cw_dict(trn_data)
    pp_dict = create_pp_dict(trn_data)
    pw_dict = create_pw_dict(trn_data)
    ppw_dict = create_ppw_dict(trn_data)
    nw_dict = create_nw_dict(trn_data)
    nnw_dict = create_nnw_dict(trn_data)
    np_dict = create_np_dict(trn_data)
    nnp_dict = create_nnp_dict(trn_data)
    ppp_dict = create_ppp_dict(trn_data)
    cnw_dict = create_cnw_dict(trn_data)
    cpw_dict = create_cpw_dict(trn_data)
    pwp_dict = create_pwp_dict(trn_data)
    best_acc, best_args = -1, None
    grid = [-1.0, 0.5, 1.0]
    grid2 = [0.5, 1.0]

    cw_weight = 1.5
#     pp_weight = 0.5
#     pw_weight = 0.5
#     nw_weight = 0.5
    np_weight = 0.1
    ppp_weight = 0.1
    nnp_weight = 0.1
    nnw_weight = 0.5
    cnw_weight = 1.0
#     cpw_weight = 0.1
    for pp_weight in grid2:
        for pw_weight in grid2:
            for nw_weight in grid2:
                for ppw_weight in grid:
                    for cpw_weight in grid:
                        for pwp_weight in grid:
                            args = (cw_dict, pp_dict, pw_dict, ppw_dict, nw_dict, nnw_dict, np_dict, nnp_dict, ppp_dict, cnw_dict, cpw_dict, pwp_dict, cw_weight, pp_weight, pw_weight, nw_weight, ppw_weight, nnw_weight, np_weight, nnp_weight, ppp_weight, cnw_weight, cpw_weight, pwp_weight)
                            acc = evaluate(dev_data, *args)
                            print('{:5.2f}% - cw: {:3.1f}, pp: {:3.1f}, pw: {:3.1f}, nw: {:3.1f}, ppw: {:3.1f}, nnw: {:3.1f}, np: {:3.1f}, nnp: {:3.1f}, ppp: {:3.1f}, cnw: {:3.1f}, cpw: {:3.1f}, pwp: {:3.1f}'.format(acc, cw_weight, pp_weight, pw_weight, nw_weight, ppw_weight, nnw_weight, np_weight, nnp_weight, ppp_weight, cnw_weight, cpw_weight, pwp_weight))
                            if acc > best_acc: best_acc, best_args = acc, args

    return best_args


def predict(tokens: List[str], *args) -> List[Tuple[str, float]]:
    cw_dict, pp_dict, pw_dict, ppw_dict, nw_dict, nnw_dict, np_dict, nnp_dict, ppp_dict, cnw_dict, cpw_dict, pwp_dict, cw_weight, pp_weight, pw_weight, nw_weight, ppw_weight, nnw_weight, np_weight, nnp_weight, ppp_weight, cnw_weight, cpw_weight, pwp_weight = args
    output = []

    for i in range(len(tokens)):
        scores = dict()
        curr_word = tokens[i]
        prev_pos = output[i-1][0] if i > 0 else DUMMY
        next_pos = output[i+1][0] if i+1 < len(output) else DUMMY
        prev_word = tokens[i-1] if i > 0 else DUMMY
        next_word = tokens[i+1] if i+1 < len(tokens) else DUMMY
        
        prev_prev_pos = output[i-1][0] if i > 0 else DUMMY
        next_next_pos = output[i+2][0] if i+2 < len(output) else DUMMY
        prev_prev_word = tokens[i-2] if i > 0 else DUMMY
        next_next_word = tokens[i+2] if i+2 < len(tokens) else DUMMY
        
        
        for pos, prob in cw_dict.get(curr_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * cw_weight

        for pos, prob in pp_dict.get(prev_pos, list()):
            scores[pos] = scores.get(pos, 0) + prob * pp_weight
            
        for pos, prob in ppp_dict.get(prev_prev_pos, list()):
            scores[pos] = scores.get(pos, 0) + prob * ppp_weight
            
        for pos, prob in np_dict.get(next_pos, list()):
            scores[pos] = scores.get(pos, 0) + prob * np_weight
            
        for pos, prob in nnp_dict.get(next_next_pos, list()):
            scores[pos] = scores.get(pos, 0) + prob * nnp_weight
            
        for pos, prob in pw_dict.get(prev_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * pw_weight
        
        for pos, prob in ppw_dict.get(prev_prev_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * ppw_weight

        for pos, prob in nnw_dict.get(next_next_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * nnw_weight
            
        for pos, prob in nw_dict.get(next_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * nw_weight

        for pos, prob in cnw_dict.get(curr_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * cnw_weight
            
        for pos, prob in cpw_dict.get(curr_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * cpw_weight
        
        for pos, prob in pwp_dict.get(curr_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * pwp_weight

        o = max(scores.items(), key=lambda t: t[1]) if scores else ('XX', 0.0)
        output.append(o)

    return output


if __name__ == '__main__':
    path = './'  # path to the cs329 directory
    trn_data = read_data(path + 'dat/pos/wsj-pos.trn.gold.tsv')
    dev_data = read_data(path + 'dat/pos/wsj-pos.dev.gold.tsv')
    model_path = path + 'src/quiz/quiz3.pkl'

    # save model
    args = train(trn_data, dev_data)
    pickle.dump(args, open(model_path, 'wb'))
    # load model
    args = pickle.load(open(model_path, 'rb'))
    print(evaluate(dev_data, *args))





