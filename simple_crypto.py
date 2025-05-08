# simple_crypto.py (or to be added to client/server later)

def caesar_encrypt(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher.
    Letters (a-z, A-Z) are shifted. Numbers and symbols are unchanged.
    """
    encrypted_text = []
    for char in plaintext:
        if 'a' <= char <= 'z':
            shifted_char_code = ord(char) + shift
            if shifted_char_code > ord('z'):
                shifted_char_code -= 26 # Wrap around the alphabet
            encrypted_text.append(chr(shifted_char_code))
        elif 'A' <= char <= 'Z':
            shifted_char_code = ord(char) + shift
            if shifted_char_code > ord('Z'):
                shifted_char_code -= 26 # Wrap around the alphabet
            encrypted_text.append(chr(shifted_char_code))
        else:
            encrypted_text.append(char) # Non-alphabetic characters are not encrypted
    return "".join(encrypted_text)

def caesar_decrypt(ciphertext, shift):
    """
    Decrypts ciphertext encrypted with a Caesar cipher.
    This is the inverse of caesar_encrypt.
    """
    decrypted_text = []
    for char in ciphertext:
        if 'a' <= char <= 'z':
            shifted_char_code = ord(char) - shift
            if shifted_char_code < ord('a'):
                shifted_char_code += 26 # Wrap around the alphabet
            decrypted_text.append(chr(shifted_char_code))
        elif 'A' <= char <= 'Z':
            shifted_char_code = ord(char) - shift
            if shifted_char_code < ord('A'):
                shifted_char_code += 26 # Wrap around the alphabet
            decrypted_text.append(chr(shifted_char_code))
        else:
            decrypted_text.append(char) # Non-alphabetic characters are not decrypted
    return "".join(decrypted_text)

# --- Example Usage (for testing the functions directly) ---
if __name__ == "__main__":
    # This part only runs if you execute this file directly (e.g., python simple_crypto.py)
    # It won't run if you import these functions into another file.
    
    shared_key = 3 # Our secret shift value
    original_message = "Hello, World! This is a test 123."

    print(f"Original Message: {original_message}")

    encrypted_message = caesar_encrypt(original_message, shared_key)
    print(f"Encrypted Message (shift {shared_key}): {encrypted_message}")

    decrypted_message = caesar_decrypt(encrypted_message, shared_key)
    print(f"Decrypted Message (shift {shared_key}): {decrypted_message}")

    print("-" * 20)
    
    another_message = "Python Chat App ROCKS ZzZ!"
    print(f"Original Message: {another_message}")
    encrypted_alt = caesar_encrypt(another_message, 5) # Using a different shift
    print(f"Encrypted Message (shift 5): {encrypted_alt}")
    decrypted_alt = caesar_decrypt(encrypted_alt, 5)
    print(f"Decrypted Message (shift 5): {decrypted_alt}")