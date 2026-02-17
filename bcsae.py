import os
import hashlib
import getpass
import math
import zlib
from pathlib import Path
from PIL import Image

# Attempt to import tqdm, provide a fallback if not installed
try:
    from tqdm import tqdm
except ImportError:
    print("Warning: tqdm library not found. Progress bars will not be shown.")
    print("You can install it using: pip install tqdm")
    # Define a dummy tqdm so the script runs without it
    def tqdm(iterable, **kwargs):
        return iterable

SALT_LEN = 16
MARKER = b'BCSAE-MK' # This marker was in your original code, keeping it.

def derive_keystream(passphrase: str, salt: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        h = hashlib.sha256()
        h.update(passphrase.encode('utf-8'))
        h.update(salt)
        h.update(counter.to_bytes(4, 'big'))
        out.extend(h.digest())
        counter += 1
    return bytes(out[:length])

def invert_bits(ba: bytearray):
    for i in range(len(ba)):
        ba[i] ^= 0xFF

def caesar_shift(ba: bytearray, shift: int):
    for i in range(len(ba)):
        ba[i] = (ba[i] + shift) & 0xFF

def encrypt_bytes(data: bytes, passphrase: str) -> (bytes, bytes):
    ba = bytearray(data)
    # These operations are fast, no progress bar needed.
    invert_bits(ba)
    caesar_shift(ba, +3)
    invert_bits(ba)
    caesar_shift(ba, +1)

    salt = os.urandom(SALT_LEN)
    ks_payload = derive_keystream(passphrase, salt, len(ba))
    
    # --- Progress Bar Added Here for the main encryption loop ---
    for i in tqdm(range(len(ba)), desc="Encrypting data ", unit="B", unit_scale=True, ncols=100):
        ba[i] ^= ks_payload[i]

    print("Compressing data with zlib...")
    compressed = zlib.compress(bytes(ba), level=9)
    return compressed, salt

def decrypt_bytes(enc_data: bytes, passphrase: str, salt: bytes) -> bytes:
    print("Decompressing data with zlib...")
    decompressed_data = zlib.decompress(enc_data)
    ba = bytearray(decompressed_data)
    
    ks_payload = derive_keystream(passphrase, salt, len(ba))
    
    # --- Progress Bar Added Here for the main decryption loop ---
    for i in tqdm(range(len(ba)), desc="Decrypting data ", unit="B", unit_scale=True, ncols=100):
        ba[i] ^= ks_payload[i]
        
    caesar_shift(ba, -1)
    invert_bits(ba)
    caesar_shift(ba, -3)
    invert_bits(ba)
    return bytes(ba)

def pack_filename_header(filename: str) -> bytes:
    name_bytes = filename.encode('utf-8')
    length = len(name_bytes)
    return length.to_bytes(2, 'big') + name_bytes

def unpack_filename_header(data: bytes) -> (str, bytes):
    length = int.from_bytes(data[:2], 'big')
    name = data[2:2+length].decode('utf-8')
    remaining = data[2+length:]
    return name, remaining

def bytes_to_image(enc_bytes: bytes) -> Image.Image:
    n = len(enc_bytes)
    pad_len = (3 - n % 3) % 3
    enc_bytes += b'\x00' * pad_len
    n_pixels = len(enc_bytes) // 3
    w = math.ceil(n_pixels ** 0.5)
    h = math.ceil(n_pixels / w)
    
    pixels = []
    # --- Progress Bar Added Here for pixel list creation ---
    print("Preparing pixel data...")
    for i in tqdm(range(0, len(enc_bytes), 3), desc="Converting to RGB", unit="px", unit_scale=True, ncols=100):
        pixels.append(tuple(enc_bytes[i:i+3]))
        
    while len(pixels) < w*h:
        pixels.append((0,0,0))
        
    img = Image.new('RGB', (w, h))
    print("Placing pixel data into image...")
    img.putdata(pixels)
    return img

def image_to_bytes(img: Image.Image) -> bytes:
    print("Extracting pixel data from image...")
    # --- Progress Bar Added Here for reading pixels ---
    pixels = list(tqdm(img.getdata(), desc="Reading pixels   ", total=img.width*img.height, unit="px", unit_scale=True, ncols=100))
    data = bytearray()
    for r,g,b in pixels:
        data.extend([r,g,b])
    return bytes(data)

def encrypt_file_to_image(in_path: Path, passphrase: str = None) -> Path:
    print(f"Reading file: {in_path} ({in_path.stat().st_size} bytes)")
    data = in_path.read_bytes()
    if passphrase is None:
        passphrase = getpass.getpass("Enter passphrase: ")
        
    enc_bytes, salt = encrypt_bytes(data, passphrase)
    header = pack_filename_header(in_path.name)
    final_bytes = salt + header + enc_bytes
    
    img = bytes_to_image(final_bytes)
    
    out_path = in_path.with_suffix('.png')
    print(f"Saving image to {out_path}...")
    img.save(out_path, format='PNG', optimize=True)
    print(f"✅ Encrypted -> {out_path}")
    return out_path

def decrypt_image_to_file(img_path: Path, passphrase: str = None, out_dir: Path = None) -> Path:
    print(f"Opening image: {img_path}")
    img = Image.open(img_path)
    
    enc_bytes = image_to_bytes(img)
    
    salt = enc_bytes[:SALT_LEN]
    remainder = enc_bytes[SALT_LEN:]
    # This might fail if padding bytes are read incorrectly, a known issue with this header design
    try:
        filename, payload = unpack_filename_header(remainder)
    except Exception as e:
        print(f"Error: Could not unpack header. The file might be corrupted or not a valid BCSAE image. Details: {e}")
        return

    if passphrase is None:
        passphrase = getpass.getpass("Enter passphrase: ")
        
    try:
        data = decrypt_bytes(payload, passphrase, salt)
    except zlib.error:
        print("Decryption failed: Incorrect passphrase or corrupted zlib data.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during decryption: {e}")
        return

    if out_dir is None:
        out_path = img_path.parent / filename
    else:
        out_path = out_dir / filename
        
    print(f"Writing decrypted file to {out_path}...")
    out_path.write_bytes(data)
    print(f"✅ Decrypted -> {out_path}")
    return out_path

def main():
    import argparse
    p = argparse.ArgumentParser(description="BCSAE PNG Encryption for Binary Files")
    p.add_argument("mode", choices=["e","d"], help="'e' encrypt, 'd' decrypt")
    p.add_argument("input", help="input file path or PNG")
    p.add_argument("--pass", dest="passphrase", help="passphrase (optional)")
    p.add_argument("--outdir", help="output directory for decrypted file (optional)")
    args = p.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print("File not found:", in_path)
        return

    if args.mode == "e":
        encrypt_file_to_image(in_path, passphrase=args.passphrase)
    else:
        if args.outdir and not Path(args.outdir).is_dir():
            print(f"Error: Output directory '{args.outdir}' does not exist.")
            return
        decrypt_image_to_file(in_path, passphrase=args.passphrase, out_dir=Path(args.outdir) if args.outdir else None)

if __name__ == "__main__":
    main()
