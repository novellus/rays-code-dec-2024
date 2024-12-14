# https://en.wikipedia.org/wiki/Letter_frequency
# Relative frequency in English language texts
english_char_frequency = {
'A':   8.2 / 100.0,
'B':   1.5 / 100.0,
'C':   2.8 / 100.0,
'D':   4.3 / 100.0,
'E':   12.7 / 100.0,
'F':   2.2 / 100.0,
'G':   2.0 / 100.0,
'H':   6.1 / 100.0,
'I':   7.0 / 100.0,
'J':   0.15 / 100.0,
'K':   0.77 / 100.0,
'L':   4.0 / 100.0,
'M':   2.4 / 100.0,
'N':   6.7 / 100.0,
'O':   7.5 / 100.0,
'P':   1.9 / 100.0,
'Q':   0.095 / 100.0,
'R':   6.0 / 100.0,
'S':   6.3 / 100.0,
'T':   9.1 / 100.0,
'U':   2.8 / 100.0,
'V':   0.98 / 100.0,
'W':   2.4 / 100.0,
'X':   0.15 / 100.0,
'Y':   2.0 / 100.0,
'Z':   0.074 / 100.0,
}

english_char_frequency_list = sorted(english_char_frequency.items(), key=lambda x: -x[1])

