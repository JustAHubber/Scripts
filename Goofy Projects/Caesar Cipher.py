def caesar_cipher(text, shift, mode):
    # Create an empty string to store the result
    result = ""

    for char in text:
        if char.isalpha():
            # Determine whether to encode or decode based on the 'mode' parameter
            if mode == "encode":
                shifted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            elif mode == "decode":
                shifted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            result += shifted_char
        else:
            # Keep non-alphabetical characters unchanged
            result += char

    return result

# Read input from the user
text = input("Enter text: ").upper()  # Convert input to uppercase
shift = int(input("Enter the shift value: "))
mode = input("Enter 'encode' or 'decode': ").lower()

# Check if the mode input is valid
if mode not in ["encode", "decode"]:
    print("Invalid mode. Please enter 'encode' or 'decode'.")
else:
    # Apply the Caesar cipher based on the mode
    result = caesar_cipher(text, shift, mode)
    print("Result:", result)