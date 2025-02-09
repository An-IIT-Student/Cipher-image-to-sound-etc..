import base64
import binascii
import codecs
import cv2
import numpy as np
import scipy.io.wavfile as wav
from itertools import cycle
from PIL import Image
import stegano
from stegano.lsb import reveal

def xor_decrypt(data, key):
    return bytes(b ^ k for b, k in zip(data, cycle(key)))

def analyze_image(image_path):
    img = Image.open(image_path)
    pixels = np.array(img)
    print(f"Image Size: {img.size}, Mode: {img.mode}")
    
    try:
        hidden_text = reveal(image_path)
        if hidden_text:
            print(f"Hidden Message (LSB): {hidden_text}")
    except:
        print("No LSB-steganography found.")
    
    return pixels

def decode_cipher(text):
    ciphers = {}
    
    try:
        ciphers['Base64'] = base64.b64decode(text).decode()
    except:
        pass
    
    try:
        ciphers['Hex'] = binascii.unhexlify(text).decode()
    except:
        pass
    
    try:
        ciphers['ROT13'] = codecs.decode(text, 'rot_13')
    except:
        pass
    
    return ciphers

def image_to_sound(image_path, output_wav):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    pixels = np.array(img)
    sound_wave = pixels.flatten().astype(np.int16)  # Convert pixel data to sound wave
    wav.write(output_wav, 44100, sound_wave)  # Save as a .wav file
    print(f"Sound file saved: {output_wav}")

# Example Usage
if __name__ == "__main__":
    text = "U29tZSBzZWNyZXQgdGV4dA=="  # Example Base64
    results = decode_cipher(text)
    for k, v in results.items():
        print(f"{k}: {v}")
    
    # Analyze Image
    pixels = analyze_image("example.png")
    
    # Convert Image to Sound
    image_to_sound("example.png", "output.wav")
