# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
from collections import defaultdict

vocab = defaultdict(int)
pos = set()

def load_train(train_list):
    for file_name in train_list:
        sentences = split_sent(file_name)
        for sent in sentences:
            for word_p in sent:
                pos.add(word_p[1])
                vocab[word_p[0]] += 1

def split_sent(training_file):
    result = [[]]
    file = open(training_file, 'r')
    sent_index = 0
    while (True):
        word_p = file.readline()
        if len(word_p) == 0:
            break
        word_p = word_p.strip('\n').split(' : ')
        result[sent_index].append(word_p)
        if word_p[0] == '.' or word_p[0] == '?':
            sent_index += 1
            result.append([])
    return result[0: -1]


def pi_freq_trans_freq_emis_freq(train_list):
    load_train(train_list)

    pi_freq = defaultdict(int)
    trans_freq = {}
    emis_freq = {}
    for p in pos:
        trans_freq[p] = defaultdict(int)
        emis_freq[p] = defaultdict(int)

    for file_name in train_list:
        sentences = split_sent(file_name)
        for sent in sentences:
            if sent != []:
                pi_freq[sent[0][1]] += 1
            for i in range(len(sent) - 1):
                trans_freq[sent[i][1]][sent[i + 1][1]] += 1
            for w_p in sent:
                emis_freq[w_p[1]][w_p[0]] += 1

    for p1 in pos:
        for p2 in pos:
            if p2 not in trans_freq[p1]:
                trans_freq[p1][p2] = 0

    for p in pos:
        for v in vocab:
            if v not in emis_freq[p]:
                emis_freq[p][v] = 0.000001

    return [pi_freq, trans_freq, emis_freq]

def freq_to_prob(d):
    prob_dist = {}
    sum_freq = sum(d.values())
    for p, freq in d.items():
        prob_dist[p] = freq / sum_freq
    return prob_dist


def viterbi_algo(transition, emission, pi, obs):
    viterbi = defaultdict(dict)
    back_pointers = defaultdict(dict)
    N = len(transition)
    T = len(obs)
    allstates = transition.keys()
    for t in range(0, T):
        for state in allstates:
            if obs[t][0] not in emission[state]:
                emission[state][obs[t][0]] = 0.000001

    for state in allstates:
        if obs[0][0] in emission[state] and state in pi:
            viterbi[0][state] = pi[state] * emission[state][obs[0][0]]
            back_pointers[0][state] = '<s>'
        else:
            viterbi[0][state] = 0
            back_pointers[0][state] = '<s>'

    def argmax(t, s):
        max_prob, argmax_pre_state = 0, 0
        for i in allstates:
            p = viterbi[t - 1][i] * transition[i][s] * emission[s][obs[t][0]]
            if p > max_prob:
                max_prob = p
                argmax_pre_state = i

        return max_prob, argmax_pre_state
    for t in range(1, T):
        for state in allstates:
            max_prob, argmax_pre_state = argmax(t, state)
            viterbi[t][state] = max_prob
            back_pointers[t][state] = argmax_pre_state
    max_prob_final_state, max_prob = None, 0
    for s in allstates:
        if viterbi[T - 1][s] > max_prob:
            max_prob_final_state = s
            max_prob = viterbi[T - 1][s]

    best_path = [max_prob_final_state]
    for t in range(T - 1, 0, -1):
        try:
            prev_state = back_pointers[t][best_path[-1]]
            best_path.append(prev_state)
        except:
            best_path.append(None)
    best_path = list(reversed(best_path))
    return best_path


def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    three_freq = pi_freq_trans_freq_emis_freq(training_list)
    pi_prob = freq_to_prob(three_freq[0])
    transition_prob = {}
    for p, freq_dis in three_freq[1].items():
        transition_prob[p] = freq_to_prob(freq_dis)
    emission_prob = {}
    for p, freq_dis in three_freq[2].items():
        emission_prob[p] = freq_to_prob(freq_dis)

    sentences = split_sent(test_file)
    f = open(output_file, 'a+')
    for sent in sentences:
        path = viterbi_algo(transition_prob, emission_prob, pi_prob, sent)
        for i in range(len(sent)):
            content = sent[i][0] + ' ' + ':' + ' ' + path[i] + '\n'
            f.write(content)
    f.close()


if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")
    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"



    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    print("output_file: " + output_file)



    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)

