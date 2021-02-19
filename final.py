import sys
import copy
def decoder():

    sta = 0
    global alphabet
    alphabet = []
    global table
    table = []
    global prewords
    prewords = {}
    global words
    words = []
    LenWr = 0
    flag = 0
    global f
    f = sys.stdin.read()
    global lines
    global sizeOfCw
    lines = f.split('\n')
    global smwords
    smwords = {}
    global checkin
    checkin = {}
    lgwords = []
    global has
    has = 0

    #with open(sys.argv[1], "r") as file:
    #    for line in file:
    for line in lines[:len(lines)-1]:
            #print (line)
            if sta == 0:
                cleanline = line.replace("\n","")
                parts = cleanline.split(";")
                if len(parts) != 3 or parts[0] == '' or parts[1] == '' or parts[2] == '':
                    #print (1)
                    return "NO"
                sizeOfAlphabet = int(parts[0])
                numberOfWords = int(parts[1])
                sizeOfCw = int(parts[2])
                sta=1

            elif sta == 1:
                cleanline = line.replace("\n", "")
                parts = cleanline.split(";")
                if len(parts)!= int(sizeOfAlphabet):
                    #print (2)
                    return "NO"
                for i in parts:
                    alphabet.append(i)
                sta = 2

            elif sta == 2 and len(line) <= 1:
                cleanline = line.replace("\n", "")
                if cleanline == '#':
                    has = 1
                return "YES"

            elif len(line) > 1 and line[1] == ';' and sta>1:
                flag = 1
                cleanline = line.replace("\n", "")
                parts = cleanline.split(";")
                table.append(parts)
                for i in parts:
                    if not(i == '#' or i == '_'):
                        #print (3)
                        return "NO"
                if len(parts) != int(sizeOfCw):
                    #print (4)
                    return "NO"
                sta = 3

            elif line != '':
                cleanline = line.replace("\n", "")
                if flag == 0:
                    #print (5)
                    return "NO"
                if len(cleanline)>int(sizeOfCw):
                    #print(6)
                    return "NO"

                for i in cleanline:
                    if i not in alphabet:
                        #print(7)
                        return "NO"
                #if len(cleanline) not in words:
                #    words[len(cleanline)] = [cleanline]
                #else:
                #    words[len(cleanline)].append(cleanline)
                for i in range(len(cleanline)):
                    if cleanline[:i+1] not in prewords and len(cleanline) == sizeOfCw:
                        prewords[cleanline[:i+1]] = len(cleanline)
                words.append(cleanline)
                LenWr += 1


    if len(table) != sizeOfCw:
        #print(8)
        return "NO"
    if LenWr != numberOfWords:
        #print(9)
        return "NO"


    for word in words:
        if len(word) == sizeOfCw:
                lgwords.append(word)
    #print (lgwords)

    for word in words:
        if len(word) != sizeOfCw:
            if len(word) not in smwords:
                smwords[len(word)] = [word]
            else:
                smwords[len(word)].append(word)
        
    for i in range(sizeOfCw):
        vert = []
        count = 0
        for j in range(sizeOfCw):
            if table[j][i] == '#' and j == 0:
                vert.append('#')
            elif table[j][i] == '#':
                if count != 0:
                    vert.append(count)
                vert.append('#')
                count = 0
            elif j == sizeOfCw - 1 and table[j][i] == '_':
                vert.append(count+1)
            elif table[j][i] == '_':
                count += 1
                
        if vert[0] != sizeOfCw:
            alldi = 1
            douvert = []
            douvert.append(vert)
            while (alldi != 0):
                alldi = 0
                #print (douvert)
                for k in range(len(douvert[0])):
                    if type(douvert[0][k]) == int:
                        alldi = 1
                        num = douvert[0][k]
                        temp = copy.deepcopy(douvert[0])
                        
                        for m in range(len(smwords[num])):
                            temp[k] = smwords[num][m]
                            douvert.append(temp)
                            temp = copy.deepcopy(douvert[0])
                        del douvert[0]
                        break

            for g in range(len(douvert)):
                k = ''.join(douvert[g])
                #print (k)
                for n in range(len(k)):
                    if k[:n+1] not in prewords:
                        prewords[k[:n+1]] = len(k)

                            
    for j in range(sizeOfCw):
        vert = []
        count = 0
        for i in range(sizeOfCw):
            if table[j][i] == '#' and i == 0:
                vert.append('#')
            elif table[j][i] == '#':
                if count != 0:
                    vert.append(count)
                vert.append('#')
                count = 0
            elif i == sizeOfCw - 1 and table[j][i] == '_':
                vert.append(count+1)
            elif table[j][i] == '_':
                count += 1

        #print (vert)
        if vert[0] != sizeOfCw:
            alldi = 1
            douvert = []
            douvert.append(vert)
            while (alldi != 0):
                alldi = 0
                for k in range(len(douvert[0])):
                    if type(douvert[0][k]) == int:
                        alldi = 1
                        num = douvert[0][k]
                        temp = copy.deepcopy(douvert[0])
                        
                        for m in range(len(smwords[num])):
                            temp[k] = smwords[num][m]
                            douvert.append(temp)
                            temp = copy.deepcopy(douvert[0])
                        del douvert[0]
                        break
            for g in range(len(douvert)):
                k = ''.join(douvert[g])
                if j not in checkin:
                    checkin[j] = [k]
                else:
                    checkin[j].append(k)

    for f in range(sizeOfCw):
        if f not in checkin:
            checkin[f] = lgwords


    return "YES"

#####################################################


def DP(checklist, count):
    lala = copy.deepcopy(checklist)
    for i in range(len(checkin[count-1])):
        for j in range(sizeOfCw):
            checklist[j] += checkin[count-1][i][j]
        #print (str(count-1) + '_', end='+')
        #print (checklist)
        judge = 1
        for wo in checklist:
            if wo not in prewords:
                judge = 0
                break
        if judge == 0:
            for j in range(sizeOfCw):
                checklist[j] = checklist[j][:len(checklist[j])-1]
            #print (checklist)
        else:
            #print (checklist)
            if count == sizeOfCw:
                #global hehe
                #hehe = checklist
                for k in range(sizeOfCw):
                    for j in range(sizeOfCw):
                        if j == sizeOfCw-1:
                            print (checklist[j][k], end='')
                        else:
                            print (checklist[j][k] + ';', end='')
                    print ()
                exit()
                return checklist
            else:
                #print (str(count-1) + '!', end='')
                if DP(checklist, count+1) == []:
                    #print (str(count-1) + '?', end='')
                    continue
                else:
                    return DP(checklist, count+1)
    for j in range(sizeOfCw):
        checklist[j] = checklist[j][:len(checklist[j])-1]
    return []
    

if decoder() == 'NO':
    print("NO")
else:
    if sizeOfCw == 1:
        if has == 0:
            print (alphabet[0])
        else:
            print ('#')
    else:
        NoSo = 1
        for i in range(len(checkin[0])):
            checklist = list(checkin[0][i])
            jug = DP(checklist, 2)
            if jug != []:
                NoSo = 0
                for k in range(sizeOfCw):
                    for j in range(sizeOfCw):
                        if j == sizeOfCw-1:
                            print (jug[j][k], end='')
                        else:
                            print (jug[j][k] + ';', end='')
                    print ()
                break
        if NoSo == 1:
            print ("NO")


#print (prewords.keys())
#print (checkin)
    
'''
def DP(checklist, count):
    for i in range(len(words)):
        temp = checklist.copy()
        for j in range(sizeOfCw):
            checklist[j] += words[i][j]
        judge = 1
        for wo in checklist:
            if wo not in prewords:
                judge = 0
                break
        if judge == 0:
            checklist = temp.copy()
        elif judge == 1 and count == sizeOfCw:
            return checklist
        else:
            return DP(checklist, count+1)
    return []
    

if decoder()=='NO':
    print("NO")
else:
    if sizeOfCw == 1:
        print(alphabet[0])
    else:
        NoSo = 1
        for i in range(len(words)):
            checklist = list(words[i])
            jug = DP(checklist, 2)
            if jug != []:
                NoSo = 0
                for i in range(sizeOfCw):
                    for j in range(sizeOfCw):
                        if j == sizeOfCw-1:
                            print (jug[j][i], end='')
                        else:
                            print (jug[j][i] + ';', end='')
                    print ()
                break
        if NoSo == 1:
            print ("NO")

#print (table)
'''


    
