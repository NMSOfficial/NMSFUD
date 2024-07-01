import base64
import marshal
import zlib
import random
import string

def random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Orijinal kodu bir string olarak sakla
original_code = '''
KODUYAPIŞTIR
'''

# Kodu sıkıştır ve base64 ile encode et
compressed_code = zlib.compress(original_code.encode())
encoded_code = base64.b64encode(compressed_code).decode()

# Decode ve dekompres fonksiyonları
decode_function = '''
import base64
import zlib

encoded_code = "{}"
compressed_code = base64.b64decode(encoded_code)
original_code = zlib.decompress(compressed_code).decode()
exec(original_code)
'''.format(encoded_code)

# Rastgele değişken adları kullan
obfuscated_code = decode_function.replace('encoded_code', random_string(10)).replace('compressed_code', random_string(10)).replace('original_code', random_string(10))

# Obfuscated kodu dosyaya yaz
with open("obfuscated_keylogger.py", "w") as f:
    f.write(obfuscated_code)
