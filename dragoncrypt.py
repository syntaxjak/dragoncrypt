import os

# Function to perform a perfect shuffle
def perfect_shuffle(deck):
    mid = (len(deck) + 1) // 2
    return [deck[i // 2] if i % 2 == 0 else deck[i // 2 + mid] for i in range(len(deck))]

# Define a corrected unshuffle function
def unshuffle(deck):
    unshuffled_deck = [None] * len(deck)
    mid = len(deck) // 2
    unshuffled_deck[:mid] = deck[::2]
    unshuffled_deck[mid:] = deck[1::2]
    return unshuffled_deck

def get_shuffle_count_from_keyword(keyword, pattern_length):
    return sum(ord(char) for char in keyword.lower()) % pattern_length

# Function to generate a random pattern for encryption/decryption using /dev/random
def generate_random_pattern(length, max_shift):
    pattern = []
    with open("/dev/random", "rb") as f:
        for _ in range(length):
            # Read just enough bytes to cover max_shift
            num_bytes = (max_shift.bit_length() + 7) // 8
            random_bytes = f.read(num_bytes)
            random_int = int.from_bytes(random_bytes, byteorder='big') % max_shift + 1
            pattern.append(random_int)
    return pattern

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
        state = sum(ord(c) for c in expanded_keyword)  # Simple cumulative state
        last_char = expanded_keyword[-1]
        # Calculate parameters potentially more influenced by cumulative state
        multiplier = (ord(last_char) + state) % 10 + 1
        adder = (ord(last_char) + state) * (ord(last_char) + state) % 256
        new_char_value = (ord(last_char) * multiplier + adder + state) % 256
        expanded_keyword += chr(new_char_value)
    return expanded_keyword[:desired_length]
    
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
    shuffle_count = get_shuffle_count_from_keyword(keyword, len(keyword))  # Get shuffle count from the original keyword
    
    shuffled_keyword_list = list(expanded_keyword)
    for _ in range(shuffle_count):
        shuffled_keyword_list = perfect_shuffle(shuffled_keyword_list)
    shuffled_keyword = ''.join(shuffled_keyword_list)
    
    file_bytes = read_file_as_bytes(file_path)
    file_pattern = generate_random_pattern(len(file_bytes), 255)
    byte_substitution_map_cache = cache_substitution_maps(256, False)
    encrypted_file_bytes = encrypt_bytes_with_pattern(file_bytes, file_pattern, byte_substitution_map_cache)
    
    # Use shuffled keyword for the Vigenère cipher on the pattern
    vigenere_encrypted_pattern = vigenere_cipher_for_numbers(file_pattern, shuffled_keyword)
    
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
    shuffle_count = get_shuffle_count_from_keyword(keyword, len(keyword))  # Get shuffle count from the original keyword
    expanded_keyword = lengthen_keyword(keyword, 256)  # Expand keyword first, without shuffling
    
    # Load the vigenere_encrypted_pattern before unshuffling the expanded keyword
    encrypted_data, vigenere_encrypted_pattern = load_encrypted_data_and_pattern(input_file_path)
    
    # Apply inverse Vigenère cipher on the encrypted pattern using the shuffled keyword
    shuffled_keyword_list = list(expanded_keyword)
    for _ in range(shuffle_count):
        shuffled_keyword_list = perfect_shuffle(shuffled_keyword_list)  # Shuffle the keyword for decryption
    shuffled_keyword = ''.join(shuffled_keyword_list)
    
    decrypted_pattern = inv_vigenere_cipher_for_numbers(vigenere_encrypted_pattern, shuffled_keyword)
    
    # After the encrypted pattern is converted, unshuffle the expanded keyword for further decryption
    for _ in range(shuffle_count):
        shuffled_keyword_list = unshuffle(shuffled_keyword_list)
    unshuffled_keyword = ''.join(shuffled_keyword_list)
    
    byte_substitution_map_cache = cache_substitution_maps(256, False)
    
    # Use the decrypted pattern to decrypt the data
    decrypted_data = decrypt_bytes_with_pattern(encrypted_data, decrypted_pattern, byte_substitution_map_cache)
    
    # Save the decrypted data
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)
    
    print(f"File decrypted successfully as '{output_file_path}'")
    

# Example usage for encryption and decryption
#file_path_to_encrypt = "/home/killswitch/testfile.txt"
#output_encrypted_file_path = "/home/killswitch/testfile.bin"
#encryption_keyword = "SECRETKEY"
#encrypt_file(file_path_to_encrypt, output_encrypted_file_path, encryption_keyword)

#input_encrypted_file_path = output_encrypted_file_path
#output_decrypted_file_path = "/home/killswitch/testfile.decrypted.txt"
#decrypt_file(input_encrypted_file_path, output_decrypted_file_path, encryption_keyword)
