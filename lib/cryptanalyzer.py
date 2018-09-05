# Mitchell Palmer
# Updated: 7/1/18

# sets
L_ALPHA = "abcdefghijklmnopqrstuvwxyz"
U_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMERICALS = "1234567890"
SYMBOLS = "!@#$%^&*()_+" + "`~{[}]_-+=|\\\"':;?/>.<,"
SPACE = " "


class cipher:
    def __init__(self, name, cod, sod, words):
        self.name = name  # str, cipher name
        self.codc = cod  # dic, character occurrence percentage
        self.sodc = sod  # dic, set occurrence percentage
        self.word_booc = words  # boo, are there multiple words


def chars(ctext, total_number_of_chars):
    cod = {}
    for char in ctext:
        if char in cod.keys():
            cod[char] += 1
        else:
            cod[char] = 1
    # change to percentage based
    for c in cod:
        cod[c] = cod[c] / total_number_of_chars
    return cod  # character occurance dictionary


def sets(ctext, total_number_of_chars):
    sod = {L_ALPHA: 0, U_ALPHA: 0, NUMERICALS: 0, SYMBOLS: 0, SPACE: 0}
    for char in ctext:
        for s in sod:
            if char in s:
                sod[s] += 1
                break
    # change to percentage based
    for s in sod:
        sod[s] = sod[s] / total_number_of_chars
    return sod  # set occurance dictionary


def words(ctext, delimeter=" "):
    word_list = ctext.split(delimeter)
    if len(word_list) > 1:
        return True
    else:
        return False


def cryptanalysis(ctext):  # strig
    # analyse encoded text
    total_number_of_chars = len(ctext)
    cod = chars(ctext, total_number_of_chars)
    sod = sets(ctext, total_number_of_chars)
    word_boo = words(ctext)

    # name, cod, sod, words
    binary = cipher("binary", {"1": 10, "0": 10, " ": 5, "OTHER": 0},
                    {L_ALPHA: 0, U_ALPHA: 0, NUMERICALS: 10, SYMBOLS: 0, SPACE: 5}, {True: 5, False: 5})
    b64 = cipher("b64", {"OTHER": 5}, {L_ALPHA: 5, U_ALPHA: 5, NUMERICALS: 5, SYMBOLS: 0, SPACE: 0},
                 {True: 0, False: 10})
    morse = cipher("morse", {".": 10, "-": 10, " ": 5, "OTHER": 0},
                   {L_ALPHA: 0, U_ALPHA: 0, NUMERICALS: 0, SYMBOLS: 10, SPACE: 5}, {True: 10, False: 0})
    singlebyteXOR = cipher("singlebyteXOR", {"OTHER": 5}, {L_ALPHA: 5, U_ALPHA: 5, NUMERICALS: 5, SYMBOLS: 0, SPACE: 0},
                           {True: 0, False: 10})
    subtypeciphers = cipher("subtypeciphers", {"OTHER": 5},
                            {L_ALPHA: 10, U_ALPHA: 10, NUMERICALS: 0, SYMBOLS: 0, SPACE: 5}, {True: 10, False: 5})
    hashsearch = cipher("hashsearch", {"OTHER": 5}, {L_ALPHA: 5, U_ALPHA: 5, NUMERICALS: 5, SYMBOLS: 0, SPACE: 0},
                        {True: 0, False: 10})

    cipher_list = [binary, b64, morse, singlebyteXOR, subtypeciphers, hashsearch]
    # Reinforcement machine learning?
    # if it gets the correct code add +.01 to the value, otherwise -.01 (or something along those lines...)
    weights = {}
    for cp in cipher_list:
        score = 5

        # Update score with value of cod
        for char in cod:
            if char in cp.codc.keys():
                score += cp.codc[char] * cod[char]
            else:
                score += cp.codc["OTHER"] * cod[char]
        score = score / 2

        # Update score with value of sod
        for s in sod:
            score += cp.sodc[s] * sod[s]
        score = score / 2

        # Update score with value of words
        if word_boo == True:
            score = (score + cp.word_booc[True]) / 2
        else:
            score = (score + cp.word_booc[False]) / 2

        # additional indicators: b64
        if cp.name == "b64":
            # b64 will add '=' to make it divisible by 4
            if (len(ctext) % 4) == 0:
                if "=" in ctext[-4:-1]:
                    score = (score + 20) / 2
                else:
                    score = (score + 8) / 2
            else:
                score = (score - 5) / 2
        else:
            if (len(ctext) % 4) == 0:
                if "=" in ctext[-4:-1]:
                    score = (score - 5) / 2
        # additional indicators: singlebyteXOR
        if ctext[0:2] == "1b":
            if cp.name == "singlebyteXOR":
                score = (score + 20) / 2
            else:
                score = (score + 0) / 2
        else:
            if cp.name == "singlebyteXOR":
                score = (score - 5) / 2
        # additional indicators:	hashsearch
        if total_number_of_chars % 16 == 0:
            if cp.name == "hashsearch":
                score = (score + 10) / 2
            elif cp.name != "binary":
                score = (score - 2) / 2
        else:
            if cp.name == "hashsearch":
                score = (score - 5) / 2

        # subtypeciphers includes caesar, atbash, simplesub, vigenere
        if cp.name == "subtypeciphers":
            weights["caesar"] = score
            weights["atbash"] = score - 0.5
            weights["vigenere"] = score - 0.75
            weights["reversetext"] = score - 1
            weights["simplesub"] = score - 1.5
        else:
            weights[cp.name] = score
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # print(weights)
    # print(sorted(weights, key=weights.get, reverse=True))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    return [sorted(weights, key=weights.get, reverse=True), weights]

# cryptanalysis(input("Enter code: "))
