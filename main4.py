import pandas as pd
import re

file = pd.read_csv('train.csv')
POI_lst = []
address_lst = []

def extract_POI():
    for i in range(len(file)):
        POI_street = file.loc[i, "POI/street"]
        POI_lst.append(POI_street[:POI_street.index("/")])
        address_lst.append(POI_street[POI_street.index("/"):])

raw_address = file["raw_address"]
l = len(file) #// 2
dlt_word_lst = []
# street_dlt_word_lst = []
regex_lst = []
POI_contain_words_lst = []
street_contain_words_lst = []
word_lst = {}  # store words that need to be updated

# check POI position in raw address

def check_raw_addr_pattern():
    for index in range(0, l):
        raw_address = file.loc[index, "raw_address"]
        addr = raw_address.split(",")
        addr = "".join(addr).split()

        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

        POI = POI_lst[index].split()
        if "," in POI:
            loc = POI.index(",")
            POI.pop(loc)

        street_address = address_lst[index].split()
        used_words = [p for p in POI] + [s for s in street_address]

        if "," in addr:
            if len(addr) > 1:
                POI_length = len(POI)
                POI_start_point = 0

                street_length = len(street_address)
                street_start_point = 0

                if POI_length > 0:
                    for i in range(POI_length):
                        if POI[i] in addr:
                            word_index = addr.index(POI[i])  # index is the pos of the word in the raw address
                            POI_start_point = word_index - i
                            break
                        elif POI[i] in list(word_lst.values()):
                            x = list(word_lst.values()).index(POI[i])
                            if list(word_lst.keys())[x] in addr:
                                word_index = addr.index(list(word_lst.keys())[x])  # index is the pos of the word in the raw address
                                POI_start_point = word_index - i
                            if POI_start_point+len(POI) > len(addr):
                                continue
                            else:
                                break

                    if POI_start_point + POI_length > len(addr):
                        POI_start_point = 0
                    POI_end_point = POI_start_point + POI_length - 1
                    if POI_end_point >= len(addr):
                        POI_end_point = len(addr)-1

                    for i in range(POI_start_point, POI_end_point+1):
                        if addr[i] != POI[i - POI_start_point]:
                            word_lst[addr[i]] = POI[i - POI_start_point]
                            if addr[i] not in word_lst:
                                used_words.append(addr[i])
                                print("UPDATE WORD: " + str(addr[i]) + " -- " + str(POI[i - POI_start_point]))

                if street_length > 0:
                    for i in range(street_length):
                        if street_address[i] in addr:
                            word_index = addr.index(street_address[i])
                            street_start_point = word_index - i
                            break
                        elif street_address[i] in list(word_lst.values()):
                            x = list(word_lst.values()).index(POI[i])
                            if list(word_lst.keys())[x] in addr:
                                word_index = addr.index(list(word_lst.keys())[x])  # index is the pos of the word in the raw address
                                street_start_point = word_index - i
                            if street_start_point+len(POI) > len(addr):
                                continue
                            else:
                                break
                    if street_start_point + POI_length > len(addr):
                        street_start_point = 0
                    street_end_point = street_start_point + street_length - 1
                    if street_end_point >= len(addr):
                        street_end_point = len(addr)-1


                    for i in range(street_start_point, street_end_point+1):
                        if addr[i] != street_address[i - street_start_point]:
                            word_lst[addr[i]] = street_address[i - street_start_point]
                            if addr[i] not in word_lst:
                                used_words.append(addr[i])
                                print("UPDATE WORD: " + str(addr[i]) + " -- " + str(POI[i - street_start_point]))

                # store unused element of raw addr in dlt lst
                part_adr_index_lst = [i for i in range(len(addr)) if addr[i] not in used_words]

                for i in part_adr_index_lst:
                    print("REMOVE WORD: " + str(addr[i]))
                    dlt_word_lst.append(addr[i])

                # for word in POI:
                #     if word not in POI_contain_words_lst:
                #         POI_contain_words_lst.append(word)
                #
                # for word in street_address:
                #     if word not in street_contain_words_lst:
                #         street_contain_words_lst.append(word)

        else:
            if len(addr) > 1:
                POI_length = len(POI)
                POI_start_point = 0

                if POI_length > 0:
                    for i in range(POI_length):
                        if POI[i] in addr:
                            word_index = addr.index(POI[i])  # index is the pos of the word in the raw address
                            POI_start_point = word_index - i
                            if POI_start_point+len(POI) > len(addr):
                                print("CONTINUE")
                                continue
                            else:
                                break
                        elif POI[i] in list(word_lst.values()):
                            x = list(word_lst.values()).index(POI[i])
                            # print(addr)
                            # print(POI[i], list(word_lst.keys())[x])
                            print("ELIF")
                            if list(word_lst.keys())[x] in addr:
                                word_index = addr.index(list(word_lst.keys())[x])  # index is the pos of the word in the raw address
                                POI_start_point = word_index - i
                                break
                        else:
                            POI_start_point = 0

                    if POI_start_point + POI_length > len(addr):
                        POI_start_point = 0
                    POI_end_point = POI_start_point + POI_length - 1
                    if POI_end_point >= len(addr):
                        POI_end_point = len(addr)-1

                    print(index, addr, POI)
                    print(POI_start_point, POI_end_point)
                    # print(POI_start_point > 0, POI_end_point < POI_length-1)
                    # print()

                    for i in range(POI_start_point, POI_end_point+1):
                        if addr[i] != POI[i - POI_start_point]:
                            word_lst[addr[i]] = POI[i - POI_start_point]
                            if addr[i] not in word_lst:
                                used_words.append(addr[i])
                                print("UPDATE WORD: " + str(addr[i]) + " -- " + str(POI[i - POI_start_point]))

                    if POI_start_point > 0 and POI_end_point < len(addr)-1:  # not the first and not the last
                        s = re.sub("[^a-zA-Z0-9]+", "", addr[POI_start_point - 1])
                        e = re.sub("[^a-zA-Z0-9]+", "", addr[POI_end_point + 1])
                        regex = str(s) + "(.*?)" + str(e)
                        if regex not in regex_lst:
                            regex_lst.append(regex)

                    elif POI_start_point == 0 and POI_end_point+1 <= len(addr)-1:
                        e = re.sub("[^a-zA-Z0-9]+", "", addr[POI_end_point + 1])
                        if len(e) > 2:
                            regex = "^(.*?)" + str(e)
                            if regex not in regex_lst:
                                regex_lst.append(regex)
                        # print("TYPE 2: " + str(regex))
                        # print()

# filt = (file["id"] > 1000) & (file["id"] < 2000)
test = pd.read_csv('test.csv') #file[filt]
predict_POI_lst = []

def predict_sol():
    for index in range(len(test)):
        predict_POI_lst.append([])
        raw_address = test.loc[index, "raw_address"]

        if "," in raw_address:
            adr_lst = raw_address.split(",")
            POI = []
            street = []
            remove_part = None

            # POI
            for adr in adr_lst:
                adr_part = adr.split()
                n = len(adr_part)//2
                count = 0
                i = 0

                while count < n and i < len(adr_part):
                    if adr_part[i] in dlt_word_lst:
                        count += 1
                    i += 1

                if count < n:
                    POI = adr_part
                    remove_part = adr_lst.index(adr)
                    break

            # street
            print("adr_lst: " + str(adr_lst))
            if remove_part != None:
                print("remove part: " + str(adr_lst[remove_part]))
                adr_lst.pop(remove_part)

            for adr in adr_lst:
                adr_part = adr.split()
                # print("adr_part: " + str(adr_part))
                n = len(adr_part) // 2
                count = 0
                i = 0

                while count < n and i < len(adr_part):
                    if adr_part[i] in dlt_word_lst:
                        count += 1
                    i += 1

                if count < n:
                    street = adr_part
                    break

            for i in range(len(POI)):
                if POI[i] in word_lst:
                    POI[i] = word_lst[POI[i]]

            for i in range(len(street)):
                if street[i] in word_lst:
                    street[i] = word_lst[street[i]]

            predict_POI_lst[index] = [index, " ".join(POI) + "/" + " ".join(street)]
            print(predict_POI_lst[index])
        else:
            POI = ""
            street = []
            for rgx in regex_lst:
                search = re.search(rgx, raw_address)
                if search and len(search.group(1).strip().split()) > 1:
                    print("REGEX: " + str(rgx))
                    POI = search.group(1).strip()
                    break

            POI_start_point = 0
            adr_lst = "".join(raw_address.split(",")).split()
            print("adr_lst: " + str(adr_lst))

            if POI != "":
                POI_lst = POI.split()
                for i in range(len(POI_lst)):
                    if POI[i] in adr_lst:
                        word_index = adr_lst.index(POI[i])  # index is the pos of the word in the raw address
                        POI_start_point = word_index - i
                        break
                    elif POI[i] in list(word_lst.values()):
                        x = list(word_lst.values()).index(POI[i])
                        if list(word_lst.keys())[x] in adr_lst:
                            word_index = adr_lst.index(list(word_lst.keys())[x])  # index is the pos of the word in the raw address
                            POI_start_point = word_index - i
                        if POI_start_point + len(POI) > len(adr_lst):
                            continue
                        else:
                            break
                if POI_start_point + len(POI_lst) > len(adr_lst):
                    POI_start_point = 0
                POI_end_point = POI_start_point + len(POI_lst) - 1
                if POI_end_point >= len(adr_lst):
                    POI_end_point = len(adr_lst) - 1
                POI_end_point = POI_start_point + len(POI_lst) - 1
                # POI_index_lst = [i for i in range(len(adr_lst)) if i not in range(POI_start_point, POI_end_point+1)]

                if POI_start_point > 0:
                    count = 0
                    for i in range(0, POI_start_point):
                        if adr_lst[i] not in dlt_word_lst:
                            street += [str(adr_lst[i])]
                            count += 1
                    if count < 1:
                        for i in range(POI_end_point, len(adr_lst)):
                            if adr_lst[i] not in dlt_word_lst:
                                street += [str(adr_lst[i])]
                                count += 1
                else:
                    for i in range(POI_end_point, len(adr_lst)):
                        if adr_lst[i] not in dlt_word_lst:
                            street += [str(adr_lst[i])]
            # else:

            predict_POI_lst[index] = [index, "".join(POI) + "/" + " ".join(street)]
            print(predict_POI_lst[index])

        print("INDEX: " + str(index))
        print("RAW ADDRESS: " + str(raw_address))
        print("PREDICT: " + str(predict_POI_lst[index]))
        print()

extract_POI()
check_raw_addr_pattern()
predict_sol()

# print(predict_POI_lst[0:500])
# print(regex_lst)
# for i in range(len(predict_POI_lst)):
#     print(i, predict_POI_lst[i])

final = pd.DataFrame(predict_POI_lst, columns=['id', 'POI/street'])
final['id'] = pd.to_numeric(final['id'], downcast='integer')

print(final.head())
print(final.tail())
final.to_csv('address_elem_extraction.csv')


















