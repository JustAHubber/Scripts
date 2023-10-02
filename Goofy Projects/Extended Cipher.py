import binascii

def caesar_cipher(text, shift):
  # Caesar cipher the input text and shift each character by the given amount.
  cipher = ""
  for char in text:
    if char.isalpha():
      shift_char = chr((ord(char.lower()) - 97 + shift) % 26 + 97)
      if char.isupper():
        shift_char = shift_char.upper()
      cipher += shift_char
    else:
      cipher += char
  return cipher

def ascii_convert(text):
  # Convert the input text to its ASCII equivalent.
  ascii_text = ""
  for char in text:
    ascii_text += "{:03d}".format(ord(char))
  return ascii_text

def xor(text, key):
  # Exclusive OR the input text with the given key.
  xored_text = ""
  for i, char in enumerate(text):
    xored_char = chr(ord(char) ^ ord(key[i % len(key)]))
    xored_text += xored_char
  return xored_text

def hex_convert(text):
  # Convert the input text to hexadecimal.
  hex_text = binascii.hexlify(text.encode("utf-8")).decode("utf-8")
  return hex_text

def encrypt(text, shift, key):
  # Encrypt the input text by Caesar ciphering it, converting it to ASCII,
  # Exclusive ORing it with the key and converting it to hexadecimal. 
  # The hexadecimal string is then reversed.
  ciphered_text = caesar_cipher(text, shift)
  ascii_text = ascii_convert(ciphered_text)
  xored_text = xor(ascii_text, key)
  hex_text = hex_convert(xored_text)
  reversed_hex = hex_text[::-1]
  return reversed_hex

def decrypt(text, shift, key):
  # Decrypt the input text by reversing the hexadecimal string,
  # converting it from hexadecimal, Exclusive ORing it with the key, 
  # converting it from ASCII and Caesar deciphering it.
  reversed_hex = text[::-1]
  hex_text = bytes.fromhex(reversed_hex).decode("utf-8")
  xored_text = xor(hex_text, key)
  ascii_text = ""
  for i in range(0, len(xored_text), 3):
    ascii_text += chr(int(xored_text[i:i+3]))
  deciphered_text = caesar_cipher(ascii_text, -shift)
  return deciphered_text

def main():
  # Ask the user if they want to encrypt or decrypt
  mode = input("Encrypt (e) or decrypt (d)? ")
  if mode == "e":
    text = input("Enter the text to encrypt: ")
    shift = int(input("Enter the Caesar shift amount: "))
    key = input("Enter the key for the XOR operation: ")
    encrypted_text = encrypt(text, shift, key)
    print("Encrypted text:", encrypted_text)
  elif mode == "d":
    text = input("Enter the text to decrypt: ")
    shift = int(input("Enter the Caesar shift amount: "))
    key = input("Enter the key for the XOR operation: ")
    decrypted_text = decrypt(text, shift, key)
    print("Decrypted text:", decrypted_text)
  else:
    print("Invalid mode. Please enter 'encrypt' or 'decrypt'.")
    main()

if __name__ == "__main__":
  main()

input()
