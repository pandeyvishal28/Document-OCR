import re


def adhaar_read(text):
    res = text.split()
    name = None
    dob = None
    adh = None
    sex = None
    address = None
    code = None
    nameline = []
    dobline = []
    text0 = []
    text1 = []
    text2 = []

    lines = text.split('\n')

    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n', '')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if 'female' in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"

    text1 = list(filter(None, text1))
    text0 = text1[:]

    ad = []

    # return text0
    for i, data in enumerate(text0):
        pin_pattern = '[0-9]'
        if 'DOB' in data or 'DO8' in data:
            dob, l = data, i
            name = text0[l - 1]
            # print(name)
        elif 'MALE' in data or 'FEMALE' in data:
            gen = data
        elif 'Address' in data or 'address' in data:
            n = i
            ad.append(text0[n + 1])
            ad.append(text0[n + 2])

            if re.search(pin_pattern, text0[n + 3]):
                pin = text0[n + 3]
            else:
                pin = text0[n + 4]
                ad.append(text0[n + 3])

    try:

        # Cleaning first names
        # name = text0[0]
        name = name.rstrip()
        name = name.lstrip()
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")
        name = re.sub('[^a-zA-Z] +', ' ', name)

        # Cleaning DOB
        dob = dob[-10:]
        dob = dob.rstrip()
        dob = dob.lstrip()
        dob = dob.replace('l', '/')
        dob = dob.replace('L', '/')
        dob = dob.replace('I', '/')
        dob = dob.replace('i', '/')
        dob = dob.replace('|', '/')
        dob = dob.replace('\"', '/1')
        dob = dob.replace(":", "")
        dob = dob.replace(" ", "")

        # Cleaning Adhaar number details
        aadhar_number = ''
        for word in res:
            if len(word) == 4 and word.isdigit():
                aadhar_number = aadhar_number + word + ' '
        # if len(aadhar_number)>=14:
        #    print("Aadhar number is :"+ aadhar_number)
        # else:
        #    print("Aadhar number not read")

        adh = aadhar_number[0:14]

        # Cleaning Address
        address = str(ad)
        address = address.rstrip()
        address = address.lstrip()
        address = address.replace('[', '')
        address = address.replace(']', '')
        address = address.replace("|", '')
        address = address.replace('5', 'S')
        address = address.replace('0', 'O')
        address = address.replace("'", '')
        address = address.replace(",,", ',')
        address = address.replace("8", "B")
        address = address.replace("0", "D")
        address = address.replace("6", "G")
        address = address.replace("1", "I")
        # start address from s/o or w/o or d/o or c/o and remove anything before that

        address = re.sub(".*[CSWcswo]:[ /]*[A-Za-z]*", "", address)

        # Cleaning Pin code

        code = pin
        try:
            code = code.split(" ")
        except:
            code = code.split("-")
        code = code[-1]
        code = code.replace("B", "8")
        code = code.replace("D", "0")
        code = code.replace("G", "6")
        code = code.replace("S", "5")
        code = code.replace("I", "1")
        code = code.replace("[", " ")
        code = code.replace("]", " ")

        # code = str(code)
        # if re.sub('[0-9] +', ' ', code):
        # code = code

    except:
        pass

    data = {}
    data['Name'] = name
    data['Date of Birth'] = dob
    data['Adhaar Number'] = adh
    data['Sex'] = sex
    data['Address'] = address
    data['Pin Code'] = code
    data['ID Type'] = "Adhaar"
    return data


