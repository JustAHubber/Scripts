import time

def Main():   
    modeSelect = str.upper(input("""Please select a mode: 
(1) Binary
(2) Hex
(3) Text
Selection: """))
    
    conversionString = input("Please enter the string to convert: ") 
    if modeSelect in ["1", "BINARY"]: convertedString=Binary(conversionString, convertedString="")
    elif modeSelect in ["2", "HEX"]: convertedString=Hex(conversionString, convertedString="")
    elif modeSelect in ["3", "TEXT"]: convertedString=Text(conversionString, convertedString="")
    else: 
        print("Error: Invalid mode selected.")
        Main()
    
    print(f"Your converted string is: {convertedString}")
    time.sleep(2); print("\n")

def Binary(conversionString, convertedString):
    for char in conversionString:
        if char in ["0", "1"]:
            if char == "0": convertedString+="1"
            else: convertedString+="0"
        else:
            print("Error: Ensure your string is valid for method of conversion.")
            Main()
    return convertedString

def Hex(conversionString, convertedString):
    try: 
        conversionString = str(bin(int(conversionString, 16)))
    except:
        print("Error: Ensure your string is valid for method of conversion.")
        Main()
    for char in conversionString[2:]:
        if char in ["0", "1"]:
            if char == "0": convertedString+="1"
            else: convertedString+="0"
        else:
            print("Error: Something went wrong during hex to binary conversion.")
            Main()
    convertedString = hex(int(convertedString, 2))
    return convertedString[2:].upper()

def Text(conversionString, convertedString):
    convertedStringHex = ""
    for char in conversionString:
        tempString = ""
        binChar = str(bin(ord(char)))[2:].zfill(8)
        for char in binChar:
            if char == "0": tempString+="1"
            else: tempString+="0"
        convertedString+=chr(int(tempString, 2))
        convertedStringHex+=hex(int(tempString, 2))[2:].upper()+" "
    print(f"Your converted string in Hexadecimal is: {convertedStringHex}")
    return convertedString

while True:
    if __name__ == "__main__":
        print("""-----------------------------------------------------
Welcome to the NOT Converter; Created by Logan Heath.
-----------------------------------------------------""")
        Main()