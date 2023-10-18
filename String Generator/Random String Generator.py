import random
import string
import concurrent.futures
from tqdm import tqdm

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

def generate_random_strings(length, amount):
    total_chars = length * amount
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = []
        for s in tqdm(executor.map(generate_random_string, [length] * amount), total=total_chars, unit="char"):
            results.append(s)
            tqdm.write(f"Generated {len(results)} strings ({len(results)*length} chars)")
    return results

def save_strings_to_files(strings, base_filename):
    for i, s in enumerate(tqdm(strings, desc="Saving strings to files", unit="file")):
        filename = f"{base_filename}{i}.txt"
        with open(filename, 'w') as f:
            f.write(s)

if __name__ == '__main__':
    length = int(input("Enter the length of the strings: "))
    amount = int(input("Enter the number of strings to generate: "))
    random_strings = generate_random_strings(length, amount)
    save_strings_to_files(random_strings, "random_string_")
