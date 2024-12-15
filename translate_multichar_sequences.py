from collections import defaultdict

def translate_multichar_sequences(alphabet, input_text):
    # alphabet = dict mapping input sequences to output sequences, eg
    # {
    #   'abc': 'z',
    #   'a': 'zy',
    #   'def': 'x',
    #   'gh': 'w',
    # }
    # input_text = str

    # verify alhpabet
    for k in alphabet:
        assert k, f'alphabet cannot contain an empty string:, "{k}"->"{alphabet[k]}", {alphabet}'

    # stabilize alphabet order to guarantee output order in case one key is a substring of another
    alphabet_stable_order = sorted(alphabet, key=lambda x: (len(x), x))

    output_text = ''
    replacements_made = defaultdict(int)  # {input sequence: int}
    sequences_without_alphabet_transation = ['']
    while(input_text):
        for seq in alphabet_stable_order:
            if input_text.startswith(seq):
                output_text += alphabet[seq]
                input_text = input_text[len(seq):]

                replacements_made[seq] +=1

                if sequences_without_alphabet_transation[-1]:
                    sequences_without_alphabet_transation.append('')

                break
        else:
            output_text += input_text[0]
            sequences_without_alphabet_transation[-1] += input_text[0]
            input_text = input_text[1:]

    return output_text, sequences_without_alphabet_transation, replacements_made
