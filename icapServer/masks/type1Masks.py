
import random,string,re


#               TYPE 1 FILTERS : MEANING DOES NOT MATTER

def getIndices(data,prefix,suffix):
    pref = re.compile(prefix)
    suf = re.compile(suffix)  
    mpref = pref.finditer(data)
    msuf = suf.finditer(data)
    for mp,ms in zip(mpref,msuf):
        start = mp.span()[1]
        end = ms.span()[0]
        return(start,end)


# 1. Numbers Only Data

def numbersOnlyData(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices(string.digits, k = length))
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices(string.digits, k = length))
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            factor1,factor2 = random.randint(1,10),random.randint(100,500)
            mdata = str(int(pidata) * factor1 + factor2)[:length]
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])

        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])
        

# 2. Characters Only Data

def charsOnlyData(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices(string.ascii_lowercase, k = length))
                #mdata = "<span style='color:red;'>" + mdata + "</span>"
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices(string.ascii_lowercase, k = length))
                mdata = "<span style='color:red;'>" + mdata + "</span>"
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices(string.ascii_lowercase, k = length))
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])


        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])

# 3. Numbers + Chars Data

def numbersAndChars(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices(string.ascii_lowercase + string.digits, k = length)) 
                #mdata = "<span style='color:red;'>" + mdata + "</span>"
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices(string.ascii_lowercase + string.digits, k = length)) 
                mdata = "<span style='color:red;'>" + mdata + "</span>"
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices(string.ascii_lowercase + string.digits, k = length))
            #mdata = "<span style='color:red;'>" + mdata + "</span>" 
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])

        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])


# 4. Mask with Special Characters

def maskWithAsterix(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('*', k = length))
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('*', k = length))
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices('*', k = length)) 
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])

        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])



def maskWithHash(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('#', k = length))
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('#', k = length))
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices('#', k = length)) 
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])


        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])



def reduceMaskWithAsterix(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('*', k = length//2))
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('*', k = length//2))
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices('*', k = length//2)) 
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])


        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])



def reduceMaskWithHash(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('#', k = length//2))
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                mdata = ''.join(random.choices('#', k = length//2))
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices('#', k = length//2)) 
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])


        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])


def partialMaskWithAsterix(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                no = random.choice(range(length//4,length//2))
                mdata = ''
                for i in range(length):
                    if i%no == 0:
                        mdata += pidata[i]
                    else:
                        mdata += '*'
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                no = random.choice(range(length//4,length//2))
                mdata = ''
                for i in range(length):
                    if i%no == 0:
                        mdata += pidata[i]
                    else:
                        mdata += '*'
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            no = random.choice(range(length//4,length//2))
            mdata = ''
            for i in range(length):
                if i%no == 0:
                    mdata += pidata[i]
                else:
                    mdata += '*'
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])


        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])



def partialMaskWithHash(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                no = random.choice(range(length//4,length//2))
                mdata = ''
                for i in range(length):
                    if i%no == 0:
                        mdata += pidata[i]
                    else:
                        mdata += '#'
                #mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                l.append(pidata)
            for pidata in l:
                length = len(pidata)
                no = random.choice(range(length//4,length//2))
                mdata = ''
                for i in range(length):
                    if i%no == 0:
                        mdata += pidata[i]
                    else:
                        mdata += '#'
                mdata = "<span style='color:red;'>" + mdata + "</span>" 
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            no = random.choice(range(length//4,length//2))
            mdata = ''
            for i in range(length):
                if i%no == 0:
                    mdata += pidata[i]
                else:
                    mdata += '#'
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])


        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])



# 5. Mask Emails

def emailData(encoding,content,prefix,suffix,unmask):
    try:
        data = content.decode(encoding)
        mask_pairs = []

        if suffix == 'ASM':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                print(pidata)
                index1,index2 = pidata.index('@'),pidata.index('.')
                l.append([pidata,index1,index2])
            for row in l:
                pidata = row[0]
                index1 = row[1]
                index2 = row[2]
                length = len(pidata)
                mdata = ''.join(random.choices(string.ascii_lowercase, k = length)) 
                mdata = mdata[:index1] + '@' + mdata[index1 + 1:]
                mdata = mdata[:index2] + '.' + mdata[index2 + 1:]
                #mdata = "<span style='color:red;'>" + mdata + "</span>"
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        elif suffix == 'ASMRED':
            pattern = re.compile(prefix)
            matches = pattern.finditer(data)
            l = []
            for m in matches:
                start,end = m.span()[0],m.span()[1]
                pidata = data[start:end]
                print(pidata)
                index1,index2 = pidata.index('@'),pidata.index('.')
                l.append([pidata,index1,index2])
            for row in l:
                pidata = row[0]
                index1 = row[1]
                index2 = row[2]
                length = len(pidata)
                mdata = ''.join(random.choices(string.ascii_lowercase, k = length)) 
                mdata = mdata[:index1] + '@' + mdata[index1 + 1:]
                mdata = mdata[:index2] + '.' + mdata[index2 + 1:]
                mdata = "<span style='color:red;'>" + mdata + "</span>"
                print("Replacing : "+pidata+" With : "+mdata)
                data = data.replace(pidata,mdata,1)
                mask_pairs.append([pidata,mdata])

        else:
            start,end = getIndices(data,prefix,suffix)
            pidata = data[start:end]
            length = len(pidata)
            mdata = ''.join(random.choices(string.ascii_lowercase, k = length))
            #mdata = "<span style='color:red;'>" + mdata + "</span>"
            print("Replacing : "+pidata+" With : "+mdata)
            data = data.replace(pidata,mdata,1)
            mask_pairs.append([pidata,mdata])

        if unmask:
            return(bytes(data,encoding),mask_pairs)
        else:
            return(bytes(data,encoding),['0'])
    except Exception as e:
        return(content,['0'])
