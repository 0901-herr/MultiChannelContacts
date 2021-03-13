import pandas as pd

file = pd.read_csv('train.csv')
POI_lst = []

def extract_POI():
    for i in range(len(file) // 2):
        POI = file.loc[i, "POI/street"]
        POI_lst.append(POI[:POI.index("/")])

raw_address = file["raw_address"]
l = 1000 #len(file) // 2
dlt_word_lst = []
regex_lst = []
contain_words_lst = []
word_lst = {}  # store words that need to be updated

# check POI position in raw address

def check_raw_addr_pattern():
    for index in range(0, l):
        raw_address = file.loc[index, "raw_address"]
        addr = raw_address.split(",")
        addr = "".join(addr).split()
        POI = POI_lst[index].split()
        street_adrress = []
        used_words = [p for p in POI] + [s for s in street_adrress]
        updated_word = []

        if "," in addr:
            if len(addr) > 1:
                POI_length = len(POI)
                POI_start_point = 0

                if POI_length > 0:
                    for i in range(POI_length):
                        if POI[i] in addr:
                            word_index = addr.index(POI[i])  # index is the pos of the word in the raw address
                            POI_start_point = word_index - i
                            break

                    POI_end_point = POI_start_point + POI_length - 1
                    POI_index_lst = []

                    # PRINTING STATION
                    print(addr)
                    print(POI)

                    for i in range(POI_start_point, POI_end_point+1):
                        POI_index_lst.append(i)
                        if addr[i] != POI[i - POI_start_point]:
                            word_lst[addr[i]] = POI[i - POI_start_point]
                            used_words.append(addr[i])
                            print("UPDATE WORD: " + str(addr[i]) + " -- " + str(POI[i - POI_start_point]))

                    # store the unused element in the raw addr
                    part_adr_index_lst = [i for i in range(len(addr)) if addr[i] not in used_words]

                    for i in part_adr_index_lst:
                        print("REMOVE WORD: " + str(addr[i]))
                        dlt_word_lst.append(addr[i])

                    for word in POI:
                        if word not in contain_words_lst:
                            contain_words_lst.append(word)

                else:
                    for i in range(len(addr)):
                        if addr[i] not in dlt_word_lst:
                            dlt_word_lst.append(addr[i])
        else:
            pass


filt = (file["id"] > 1000) & (file["id"] < 2000)
test = file[filt]
predict_POI_lst = []

def predict_sol():
    for index in range(len(test)):
        predict_POI_lst.append([])
        raw_address = test.loc[index, "raw_address"]

        if "," in raw_address:
            adr_lst = raw_address.split(",")
            POI = []

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
                    break

            for i in range(len(POI)):
                if POI[i] in word_lst:
                    POI[i] = word_lst[POI[i]]

            predict_POI_lst[index] = "".join(POI)
        else:
            predict_POI_lst.append("".join(POI))


extract_POI()
check_raw_addr_pattern()
predict_sol()

for i in range(len(predict_POI_lst)):
    print(POI_lst)



























