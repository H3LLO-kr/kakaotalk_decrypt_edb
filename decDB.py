import base64

# It is not a library that is essential for the alternative code.
import hashlib

from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def generate_pragma(uuid, modelName, serialNumber):
    # Hardcoded key (must be 16, 24, or 32 bytes long)
    key = b"hardcoded bytes array"
    
    # Initialization vector (IV)
    iv = bytes([0] * 16)
    
    # Concatenate uuid, modelName, and serialNumber
    pragma = f"{uuid}|{modelName}|{serialNumber}"
    
    # Encrypt pragma using AES128 CBC PKCS#7
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # padding_length = 16 - (len(pragma) % 16)
    # pragma += bytes([padding_length]) * padding_length
    encrypted_pragma = cipher.encrypt(pad(pragma.encode(), AES.block_size))
    
    # Encode the SHA512 hash of the encrypted pragma using Base64
    hashed_pragma = hashlib.sha512(encrypted_pragma).digest()
    encoded_hashed_pragma = base64.b64encode(hashed_pragma)
    # Calculate SHA512 hash of the encrypted pragma
    # hashed_pragma = SHA512.new()
    # hashed_pragma.update(encrypted_pragma)
    # encoded_hashed_pragma = hashed_pragma.digest()
    
    return encoded_hashed_pragma.decode()

def generate_key_and_iv(pragma, userId):
    # Concatenate pragma and userId to generate key
    key = pragma + userId
    
    # Repeat key until its length reaches 512
    while len(key) < 512:
        key += key
    
    # Trim key to 512 bytes
    key = key[:512]
    
    # Calculate MD5 hash of the key
    key_hash = hashlib.md5(key.encode()).digest()
    
    # Encode the key_hash using Base64 and calculate MD5 hash of it to generate IV
    iv = hashlib.md5(base64.b64encode(key_hash)).digest()
    
    return key_hash, iv

def decrypt_database(key, iv, encDB):
    decDB = b''  # 데이터베이스를 빈 바이트 문자열로 초기화
    i = 0
    while i < len(encDB):
        # Decrypt each 4096 bytes block using AES128 CBC without padding
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encDB[i:i+4096])
        
        # Unpad the decrypted data
        # decrypted_data = unpad(decrypted_data, AES.block_size)
        
        # Append the decrypted data to decDB
        decDB += decrypted_data
        
        i += 4096
    
    return decDB

def read_encrypted_data_from_file(input_filename):
    with open(input_filename, 'rb') as f:
        encDB = f.read()
    return encDB

def save_to_file(decDB, output_filename):
    with open(output_filename, 'wb') as f:
        f.write(decDB)

# Example usage1:
#uuid = "example_uuid"
#modelName = "example_modelName"
#serialNumber = "example_serialNumber"
#pragma = generate_pragma(uuid, modelName, serialNumber)
#print("Generated Pragma:", pragma.hex())

# Example usage2:
#userId = "example_userId"
#key, iv = generate_key_and_iv(pragma, userId)
#print("Generated Key:", key.hex())
#print("Generated IV:", iv.hex())

# Example usage4:
#input_filename = 'input_filename'  # input file name
#encDB = read_encrypted_data_from_file(input_filename)

# Example usage3:
#decDB = decrypt_database(key, iv, encDB)

# Example usage5:
#output_filename = 'output_filename'  # output file name
#save_to_file(decDB, output_filename)
#print(f"Decrypted data saved to {output_filename}")

# ----------------------------------------------------------------------
# full example usage:
# key = 'hardcoded byte array' in the generate_pragma function
# reg : HKEY_CURRENT_USER\Software\Kakao\KakaoTalk\DeviceInfo\20230613-224538-107
uuid = "sys_uuid"
modelName = "hdd_model"
serialNumber = "hdd_serial"

pragma = generate_pragma(uuid, modelName, serialNumber)
print("Generated Pragma: ", pragma.hex())

# reg : HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{c4def0e5-d3ee-4e8a-adf9-df1ba48a4f5a}
userId = "c4def0e5-d3ee-4e8a-adf9-df1ba48a4f5a"
key, iv = generate_key_and_iv(pragma, userId)
print("Generated Key: ", key.hex())
print("Generated IV: ", iv.hex())

input_filename = 'input_filename'
encDB = read_encrypted_data_from_file(input_filename)

decDB = decrypt_database(key, iv, encDB)

output_filename = 'output_filename'ee
save_to_file(decDB, output_filename)
print("Decrypted data saved to ", output_filename)

# ----------------------------------------------------------------------
