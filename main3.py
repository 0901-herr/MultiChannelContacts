import pandas as pd

file = pd.read_csv('train.csv')

POI_lst = []

# extract POI
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

for index in range(0, l):
    raw_address = file.loc[index, "raw_address"]
    addr_comma = raw_address.split(",")
    # print("addr_comma: " + str(addr_comma))
    addr = "".join(addr_comma).split()  # raw address in array
    # print("addr: " + str(addr))
    addr_elem_index = []

    s = 0
    e = 0

    for i in range(len(addr_comma)):
        addr_elem_index.append([])
        part_addr_lst = addr_comma[i].split()
        part_addr_length = len(part_addr_lst)
        e = s + part_addr_length - 1
        addr_elem_index[i] = [s, e]
        s = e + 1

    # print("addr_elem_index: " + str(addr_elem_index))

    POI = []

    if "," in raw_address:
        POI = POI_lst[index].split()

        if len(addr) > 1:
            POI_length = len(POI)
            POI_start_point = 0
            POI_end_point = 0
            word_index = 0

            print("PASS 1")

            if POI_length > 0:

                for i in range(POI_length):
                    if POI[i] in addr:
                        word_index = addr.index(POI[i])  # index is the pos of the word in the raw address
                        POI_start_point = word_index - i
                        break

                print("PASS 2")

                POI_end_point = POI_start_point + POI_length - 1
                POI_in_adr_pos = 0

                for i in range(len(addr_elem_index)):
                    if addr_elem_index[i][-1] >= POI_end_point:
                        POI_in_adr_pos = i
                        break

                print("PASS 3")

                check_addr_part = addr_comma[POI_in_adr_pos].split()

                # POI start - POI end
                POI_index_lst = []

                # print(POI_index_lst, part_adr_index_lst)
                print(addr)
                print(POI, check_addr_part)
                print(POI_start_point, POI_end_point)

                for i in range(POI_start_point, POI_end_point+1):
                    POI_index_lst.append(i)
                    # check POI in  addr
                    print(i)
                    if check_addr_part[i - POI_start_point] != POI[i - POI_start_point]:
                        word_lst[check_addr_part[i-POI_start_point]] = POI[i - POI_start_point]

                print("PASS 4")

                # store the unused element in the raw addr
                start = addr_elem_index[POI_in_adr_pos][0]
                end = addr_elem_index[POI_in_adr_pos][1]
                part_adr_index_lst = [i for i in range(start, end+1) if i not in POI_index_lst]

                for i in part_adr_index_lst:
                    dlt_word_lst.append(check_addr_part[i-POI_start_point])

                print("PASS 5")

                for word in POI:
                    if word not in contain_words_lst:
                        contain_words_lst.append(word)

            else:
                for i in range(len(addr)):
                    if addr[i] not in dlt_word_lst:
                        dlt_word_lst.append(addr[i])
    else:
        pass  # None

for i in range(len(dlt_word_lst)):
    print(i, dlt_word_lst)
