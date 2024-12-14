# inputs
import csv
import itertools
from pprint import pprint
import tabulate

from collections import defaultdict
from matplotlib import pyplot as plt

# local inputs
from charfrequency import *
from pairwise import *
from translate_multichar_sequences import *



# inputs
f = open('input2.txt')
rays_text = f.read()
f.close()



# first order statistics
char_distribution = defaultdict(int)
for char in rays_text:
    char_distribution[char] += 1

# normalize char frequencys
char_freq_norm = sorted(char_distribution.items(), key=lambda x: -x[1])
total = float(sum([x for _,x in char_freq_norm]))
char_freq_norm = [(char, freq / total) for char, freq in char_freq_norm]
char_freq_order = [char for char, freq in char_freq_norm]

print(f'num characters in Ray’s text: {len(char_distribution)}')
print(f'normalized distribution of characters in Ray’s text: {char_freq_norm}')
print(f'ratio of highest frequency character to next highest: {char_freq_norm[0][1] / char_freq_norm[1][1]}')

# renormalize without the most frequent character
char_freq_norm2 = char_freq_norm[1:]
total = float(sum([x for _,x in char_freq_norm2]))
char_freq_norm2 = [(char, freq / total) for char, freq in char_freq_norm2]

# plot
plt.figure()
plt.title('character frequency, in decreasing order')
plt.xlabel('arbitrary character ID')
plt.ylabel('frequency, normalized')

x, y = list(zip(*[(i, char_freq_norm2[i][1]) for i in range(len(char_freq_norm2)) if i > 0]))
plt.plot(x, y, c='red', label='Ray’s text')

x, y = list(zip(*[(i+1, english_char_frequency_list[i][1]) for i in range(len(english_char_frequency_list))]))
plt.plot(x, y, c='blue', label='english text')

plt.legend(loc='upper right')



# second order statistics
# eg 'b' follows 'a' what percentage of the time
# P(X_(i+1) = b | X_i = a)
second_order_distribution = defaultdict(lambda : defaultdict(int))
for a, b in pairwise(rays_text):
    second_order_distribution[a][b] += 1

# verify all character combinations are accounted for
for c1 in char_freq_order:
    for c2 in char_freq_order:
        second_order_distribution[c1][c2] += 0

# normalize stats
total = 0
for c1 in char_freq_order:
    for c2 in char_freq_order:
        total += second_order_distribution[c1][c2]
total = float(total)

second_order_distribution_norm = []  # just numbers, in the nested order of char_freq_order
for c1 in char_freq_order:
    c1_dist = []
    for c2 in char_freq_order:
        c1_dist.append(second_order_distribution[c1][c2] / total)
    second_order_distribution_norm.append(c1_dist)

# print 2nd order stats to file (too big for console)
headers = char_freq_order
rows = []
for i, c1 in enumerate(char_freq_order):
    # truncate numbers to 4 sigfigs
    row_label = c1
    row_data = [f'{n:0.5f}' for n in second_order_distribution_norm[i]]
    rows.append([row_label] + row_data)

f = open('2nd order stats.txt', 'w')
f.write('Second order character distribution, ie P(X_(i+1) = b | X_i = a) where "x_i" is rows in this table\n')
f.write('Second character\n')
f.write(tabulate.tabulate(rows, headers=headers, tablefmt='pipe'))
f.close()

with open('2nd order stats.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([''] + headers)
    for row in rows:
        writer.writerow(row)



# character groups with fixed group width
char_groups_fixed = defaultdict(lambda: defaultdict(int))  # { width : {'ab':1, 'cd':15, ...} }
for width in range(1,10):
    i = 0
    while i + width <= len(rays_text):
        code = rays_text[i: i + width]
        assert len(code) == width
        char_groups_fixed[width][code] += 1
        i += width
f = open('char_groups.txt', 'w')
for width in range(1, max(char_groups_fixed)):
    f.write(f'Num width {width} groups: {len(char_groups_fixed[width])}\n')
    f.write(f'{sorted(char_groups_fixed[width].items(), key=lambda x: (-x[1], x[0]))}')
    f.write(f'\n\n\n')
f.close()



# character groups with variable group width
char_groups_sliding = defaultdict(lambda: defaultdict(int))  # { width : {'ab':1, 'cd':15, ...} }
for width in range(1,20):
    i = 0
    while i + width <= len(rays_text):
        code = rays_text[i: i + width]
        assert len(code) == width
        char_groups_sliding[width][code] += 1
        i += 1
f = open('char_groups_sliding.txt', 'w')
for width in range(1, max(char_groups_sliding)):
    f.write(f'Num width {width} groups: {len(char_groups_sliding[width])}\n')
    f.write(f'{sorted(char_groups_sliding[width].items(), key=lambda x: (-x[1], x[0]))}')
    f.write(f'\n\n\n')
f.close()



# analysis of all possible multicharacter to space assignments
possible_codes = []
for width in range(1,4):
    codes_at_width = char_groups_sliding[width].items()
    codes_at_width = sorted(codes_at_width, key=lambda x: (-x[1], x[0]))  # order by length and then frequency in Ray's text
    codes_at_width = [x[0] for x in codes_at_width]
    possible_codes += codes_at_width

stats = defaultdict(dict)  # {width: {key: value}}
for code in possible_codes:
    code_width = len(code)
    alphabet = {code: ' '}
    translated_text, _, replacements_made = translate_multichar_sequences(alphabet, rays_text)
    words = translated_text.split(' ')
    word_lengths = [len(x) for x in words]

    stats[code]['num_words'] = len(words)
    stats[code]['num_spaces'] = replacements_made[code]
    stats[code]['ratio_code_replacements_to_text_len'] = len(code) * replacements_made[code] / len(rays_text)
    stats[code]['avg_word_length'] = sum(word_lengths) / len(words)
    stats[code]['norm_avg_word_length'] = stats[code]['avg_word_length'] / code_width

f = open('assignments to spaces.txt', 'w')
for code in possible_codes:  # maintain order
    f.write(f"Code '{code}'\n")
    pprint(stats[code], stream=f)
    f.write(f"\n\n\n")
f.close()



# analysis of all possible multicharacter to space and "the" phonetic assignments
# the (phonetically) = ðə
# possible_codes = []
# for width in range(1,4):
#     codes_at_width = char_groups_sliding[width].items()
#     codes_at_width = sorted(codes_at_width, key=lambda x: (-x[1], x[0]))  # order by length and then frequency in Ray's text
#     codes_at_width = [x[0] for x in codes_at_width]
#     possible_codes += codes_at_width

# stats = defaultdict(dict)  # {width: {key: value}}
# for code_space in possible_codes:
#     for code_the in possible_codes:  # TODO should be two codes, one for θ and one for i
#         if code_the != code_space:
#             code_width_space = len(code_space)
#             code_width_the = len(code_the)
#             alphabet = {code_space: ' ', code_the: 'ðə'}
#             translated_text, _, replacements_made = translate_multichar_sequences(alphabet, rays_text)
#             words = translated_text.split(' ')
#             word_lengths = [len(x) for x in words]

#             stats_key = (code_space, code_the)

#             stats[stats_key]['num_words'] = len(words)
#             stats[stats_key]['num_spaces'] = replacements_made[code_space]
#             stats[stats_key]['num_the'] = replacements_made[code_the]
#             stats[stats_key]['ratio_space_code_replacements_to_text_len'] = len(code_space) * replacements_made[code_space] / len(rays_text)
#             stats[stats_key]['ratio_the_code_replacements_to_text_len'] = len(code_the) * replacements_made[code_the] / len(rays_text)
#             stats[stats_key]['avg_word_length'] = sum(word_lengths) / len(words)
#             stats[stats_key]['number_of_"the "'] = translated_text.count('ðə ')

# f = open('assignments to spaces and the.txt', 'w')
# for code in possible_codes:  # maintain order  # TODO new iterates
#     f.write(f"Code '{code}'\n")
#     pprint(stats[code], stream=f)
#     f.write(f"\n\n\n")
# f.close()



# analysis2 of all possible multicharacter to space and "the" phonetic assignments
max_seq_length = 1
target_seq = ['ð', 'ə', ' ']  # "the "
secret_target_seq = [' ', 'ð', 'ə', ' ']  # " the "

possible_code_lengths = list(itertools.product(range(1, max_seq_length + 1), repeat = len(target_seq)))
possible_alphabets = []
for code_lens in possible_code_lengths:
    total_seq_len = sum(code_lens)
    seqs_at_width = char_groups_sliding[total_seq_len].items()
    seqs_at_width = sorted(seqs_at_width, key=lambda x: (-x[1], x[0]))  # order by length and then frequency in Ray's text
    seqs_at_width = [x[0] for x in seqs_at_width]

    for total_seq in seqs_at_width:
        alphabet = {}
        i_subseq = 0
        for i_target, target_char in enumerate(target_seq):
            target_code_len = code_lens[i_target]
            code = total_seq[i_subseq: i_subseq + target_code_len]
            if code in alphabet: break  
            alphabet[code] = target_char
            i_subseq += target_code_len

            # print('--C--', target_char, target_code_len, i_subseq, target_seq, alphabet)
            # if len(possible_alphabets) > 204: break

        # discard sequences which result in duplicate codes
        if len(alphabet) == len(target_seq):
            print('--D--', f'{repr(total_seq)}', alphabet)
            possible_alphabets.append(alphabet)
sys.exit()
stats = defaultdict(dict)  # {serialized alphabet: {key: value}}
for i_alphabet, alphabet in enumerate(possible_alphabets):
    print('--B--', i_alphabet, alphabet)
    reverse_alphabet = {b:a for a,b in alphabet.items()}
    code_width_space = len(reverse_alphabet[' '])
    translated_text, _, replacements_made = translate_multichar_sequences(alphabet, rays_text)
    words = translated_text.split(' ')
    word_lengths = [len(x) for x in words]

    stats_key = frozenset(sorted(alphabet.items(), key=lambda x: x[1]))
    stats[stats_key]['num_words'] = len(words)
    stats[stats_key]['num_spaces'] = replacements_made[reverse_alphabet[' ']]
    stats[stats_key]['ratio_space_replacements_to_text_len'] = code_width_space * replacements_made[reverse_alphabet[' ']] / len(rays_text)
    stats[stats_key]['avg_word_length'] = sum(word_lengths) / len(words)
    stats[stats_key]['norm_avg_word_length'] = stats[stats_key]['avg_word_length'] / code_width
    stats[stats_key][f'num_target_seq "{"".join(target_seq)}"'] = rays_text.count(''.join(target_seq))
    stats[stats_key][f'num_secret_target_seq "{"".join(secret_target_seq)}"'] = rays_text.count(''.join(secret_target_seq))

f = open('assignments to spaces and the.txt', 'w')
for alphabet in possible_alphabets:  # maintain order
    f.write(f"alphabet '{alphabet}'\n")
    pprint(stats[frozenset(sorted(alphabet.items(), key=lambda: x[1]))], stream=f)
    f.write(f"\n\n\n")
f.close()



# systematically analyzing all possible multicharacter alphabetic translations
lower_letters = 'abcdefghijklmnopqrstuvwxyz'
upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
punctuation = '.,"-?:!;' + "'"
white_space = ' '
target_alpha_chars = lower_letters + upper_letters + numbers + punctuation + ' '

phonetic_consonants = ['m', 'n', 'ŋ', 'p', 't', 'tʃ', 'k', 'b', 'd', 'dʒ', 'ɡ', 'f', 'θ', 's', 'ʃ', 'x', 'h', 'v', 'ð', 'z', 'ʒ', 'w', 'l', 'r', 'j', 'w']
phonetic_vowels = ['æ', 'ɑ', 'ɪ', 'ɛ', 'ʌ', 'ʊ', 'eɪ', 'oʊ', 'i', 'u', 'aɪ', 'ɔɪ', 'aʊ', 'ɜr', 'ɑr', 'ɔr', 'ɪr', 'ɛr', 'ʊr', 'ə', 'ər']  # GA


# multicharacter alphabetic translation
# tmp = translate_multichar_sequences({'ll': ' '}, rays_text)
# print(tmp)
# f = open('tmp.txt', 'w')
# f.write(tmp[0])
# f.close()



# plt.show()
