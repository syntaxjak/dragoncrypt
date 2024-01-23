import secrets
import os

# Function to generate a random non-repeating pattern for encryption/decryption
def generate_random_pattern(length, max_shift):
    return [secrets.randbelow(max_shift) + 1 for _ in range(length)]

# Cache substitution maps for all possible shifts for bytes
def cache_substitution_maps(max_shift, is_letter_map=False):
    cache = {}
    for shift in range(max_shift):
        shifted_bytes = list(range(shift, max_shift)) + list(range(shift))
        cache[shift] = {i: shifted_bytes[i] for i in range(max_shift)}
    return cache

# Updated encryption function using the cache for bytes data
def encrypt_bytes_with_pattern(data_bytes, pattern, substitution_map_cache):
    result = bytearray()
    for i, byte in enumerate(data_bytes):
        shift = pattern[i % len(pattern)]
        new_byte = substitution_map_cache[shift][byte]
        result.append(new_byte)
    return bytes(result)

# Function to expand a keyword using parameters derived from itself
def lengthen_keyword(keyword, desired_length):
    expanded_keyword = keyword
    while len(expanded_keyword) < desired_length:
        # Take the last character for transformation to avoid influence from ONLY initial keyword
        last_char = expanded_keyword[-1]
        # Calculate parameters based on the full range of byte values
        multiplier = ord(last_char) % 10 + 1
        adder = ord(last_char) * ord(last_char) % 256
        new_char_value = (ord(last_char) * multiplier + adder) % 256
        expanded_keyword += chr(new_char_value)
    expanded_keyword = expanded_keyword[:desired_length]
    return expanded_keyword

# Functions to apply and reverse Vigenère cipher for numbers in the pattern
def vigenere_cipher_for_numbers(pattern, keyword):
    keyword_numbers = [(ord(char) - ord('A')) for char in keyword.upper()]
    keyword_length = len(keyword_numbers)
    max_shift = 256  # We have 256 possible byte values
    vigenere_pattern = [(shift + keyword_numbers[i % keyword_length]) % max_shift for i, shift in enumerate(pattern)]
    return vigenere_pattern

def inv_vigenere_cipher_for_numbers(pattern, keyword):
    keyword_numbers = [(ord(char) - ord('A')) for char in keyword.upper()]
    keyword_length = len(keyword_numbers)
    max_shift = 256  # We have 256 possible byte values, this line was missing
    original_pattern = [(shift - keyword_numbers[i % keyword_length]) % max_shift for i, shift in enumerate(pattern)]
    return original_pattern

# Function to read file as bytes
def read_file_as_bytes(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Function to save encrypted data and pattern to file
def save_encrypted_data_and_pattern(encrypted_data, encrypted_pattern, output_file_path):
    with open(output_file_path, 'wb') as file:
        # First, write the length of the encrypted pattern (4 bytes, big endian)
        file.write(len(encrypted_pattern).to_bytes(4, byteorder='big'))
        # Then write the encrypted pattern itself
        file.write(bytes(encrypted_pattern))
        # Finally, write the encrypted data
        file.write(encrypted_data)

# Main function to encrypt file
def encrypt_file(file_path, output_file_path, keyword):
    expanded_keyword = lengthen_keyword(keyword, 256)  # Use expanded keyword
    file_bytes = read_file_as_bytes(file_path)
    file_pattern = generate_random_pattern(len(file_bytes), 255)
    byte_substitution_map_cache = cache_substitution_maps(256, False)
    encrypted_file_bytes = encrypt_bytes_with_pattern(file_bytes, file_pattern, byte_substitution_map_cache)
    vigenere_encrypted_pattern = vigenere_cipher_for_numbers(file_pattern, expanded_keyword)  # Use expanded keyword
    save_encrypted_data_and_pattern(encrypted_file_bytes, vigenere_encrypted_pattern, output_file_path)
    print(f"File '{file_path}' encrypted successfully as '{output_file_path}'")
    print(f"Keyword needed for decryption: {keyword}")  # Keep original keyword for user

# Function to decrypt bytes data using a pattern and caches
def decrypt_bytes_with_pattern(encrypted_data_bytes, decrypted_pattern, substitution_map_cache):
    result = bytearray()
    for i, byte in enumerate(encrypted_data_bytes):
        shift = decrypted_pattern[i % len(decrypted_pattern)]
        original_byte = substitution_map_cache[-shift % 256][byte]
        result.append(original_byte)
    return bytes(result)

# Function to load encrypted data and encrypted pattern from file
def load_encrypted_data_and_pattern(input_file_path):
    with open(input_file_path, 'rb') as file:
        # First, read the length of the encrypted pattern (it is stored in the first 4 bytes of the file)
        pattern_length = int.from_bytes(file.read(4), byteorder='big')
        # Then, read the encrypted pattern
        encrypted_pattern = list(file.read(pattern_length))
        # Finally, read the encrypted data (the rest of the file)
        encrypted_data = file.read()
    return encrypted_data, encrypted_pattern

# Function to decrypt file using expanded keyword
def decrypt_file(input_file_path, output_file_path, keyword):
    expanded_keyword = lengthen_keyword(keyword, 256)  # Use expanded keyword
    encrypted_data, vigenere_encrypted_pattern = load_encrypted_data_and_pattern(input_file_path)
    decrypted_pattern = inv_vigenere_cipher_for_numbers(vigenere_encrypted_pattern, expanded_keyword)  # Use expanded keyword
    byte_substitution_map_cache = cache_substitution_maps(256, False)
    decrypted_data = decrypt_bytes_with_pattern(encrypted_data, decrypted_pattern, byte_substitution_map_cache)
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)
    print(f"File decrypted successfully as '{output_file_path}'")

# Example usage for encryption and decryption
file_path_to_encrypt = "/home/killswitch/testfile.txt"
output_encrypted_file_path = "/home/killswitch/testfile.bin"
encryption_keyword = "SECRETKEY"
encrypt_file(file_path_to_encrypt, output_encrypted_file_path, encryption_keyword)

input_encrypted_file_path = output_encrypted_file_path
output_decrypted_file_path = "/home/killswitch/testfile.decrypted.txt"
decrypt_file(input_encrypted_file_path, output_decrypted_file_path, encryption_keyword)