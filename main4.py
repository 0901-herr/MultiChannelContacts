import pandas as pd
import re

file = pd.read_csv('train.csv')
POI_lst = []
address_lst = []

def extract_POI():
    for i in range(len(file) // 2):
        POI_street = file.loc[i, "POI/street"]
        POI_lst.append(POI_street[:POI_street.index("/")])
        address_lst.append(POI_street[POI_street.index("/"):])

raw_address = file["raw_address"]
l = 1000 #len(file) // 2
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

        POI = POI_lst[index].split()
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

                            if POI_start_point+POI_length > len(addr):
                                continue
                            else:
                                break

                    POI_end_point = POI_start_point + POI_length - 1

                    for i in range(POI_start_point, POI_end_point+1):
                        if addr[i] != POI[i - POI_start_point]:
                            word_lst[addr[i]] = POI[i - POI_start_point]
                            if addr[i] not in word_lst:
                                used_words.append(addr[i])
                                print("UPDATE WORD: " + str(addr[i]) + " -- " + str(POI[i - POI_start_point]))

                if street_length > 0:
                    for i in range(street_length):
                        word_index = addr.index(street_address[i])
                        street_start_point = word_index - i

                        if street_start_point+street_length > len(addr):
                            continue
                        else:
                            break
                    street_end_point = street_start_point + street_length - 1

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

                            if POI_start_point+POI_length > len(addr):
                                continue
                            else:
                                break

                    POI_end_point = POI_start_point + POI_length - 1

                    # print(index, addr, POI)
                    # print(POI_start_point, POI_end_point)
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

filt = (file["id"] > 1000) & (file["id"] < 2000)
test = file[filt]
predict_POI_lst = []

def predict_sol():
    for index in range(len(test)):
        predict_POI_lst.append([])
        raw_address = test.loc[index+1001, "raw_address"]

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

        else:
            POI = ""
            for rgx in regex_lst:
                search = re.search(rgx, raw_address)
                if search and len(search.group(1).strip().split()) > 1:
                    print("REGEX: " + str(rgx))
                    POI = search.group(1).strip()
                    break
            predict_POI_lst[index] = [index, " ".join(POI) + "/" + " ".join(street)]

        print("INDEX: " + str(index))
        print("RAW ADDRESS: " + str(raw_address))
        print("PREDICT: " + str(predict_POI_lst[index]))
        print()

extract_POI()
check_raw_addr_pattern()
predict_sol()

# print(regex_lst)
# for i in range(len(predict_POI_lst)):
#     print(i, predict_POI_lst[i])

final = pd.DataFrame([], columns=['id', 'POI/street'])
final['id'] = pd.to_numeric(final['id'], downcast='integer')

final.to_csv('address_elem_extraction.csv')


















