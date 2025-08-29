import numpy as np
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
from PIL import Image
import io
import json
import struct

class ZSecureEncryption:
    """Advanced Z-Secure encryption using chaos theory and biometric key derivation"""
    
    def __init__(self):
        self.backend = default_backend()
        self.key_length = 32  # 256 bits
        self.iv_length = 16   # 128 bits
        self.chaos_iterations = 1000
        
    def generate_key_from_biometrics(self, face_encoding, email):
        """Generate encryption key from facial biometrics and email"""
        try:
            # Convert face encoding to bytes
            face_bytes = face_encoding.tobytes()
            
            # Combine with email for additional entropy
            email_bytes = email.encode('utf-8')
            combined_data = face_bytes + email_bytes
            
            # Apply chaos-based key derivation
            chaos_key = self._apply_chaos_algorithm(combined_data)
            
            # Use PBKDF2 for final key derivation
            salt = hashlib.sha256(email_bytes).digest()[:16]
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=self.key_length,
                salt=salt,
                iterations=100000,
                backend=self.backend
            )
            
            final_key = kdf.derive(chaos_key)
            return final_key
            
        except Exception as e:
            print(f"Error generating key from biometrics: {e}")
            return None
    
    def _apply_chaos_algorithm(self, data):
        """Apply chaos-based algorithm for key enhancement"""
        try:
            # Lorenz attractor parameters
            sigma = 10.0
            rho = 28.0
            beta = 8.0/3.0
            
            # Initial conditions from data
            x = sum(data[::3]) % 1000 / 1000.0
            y = sum(data[1::3]) % 1000 / 1000.0
            z = sum(data[2::3]) % 1000 / 1000.0
            
            dt = 0.01
            chaos_sequence = []
            
            for i in range(self.chaos_iterations):
                # Lorenz equations
                dx = sigma * (y - x)
                dy = x * (rho - z) - y
                dz = x * y - beta * z
                
                x += dx * dt
                y += dy * dt
                z += dz * dt
                
                # Convert to bytes
                chaos_val = int((abs(x) * abs(y) * abs(z)) * 1000000) % 256
                chaos_sequence.append(chaos_val)
            
            # XOR with original data
            result = bytearray()
            for i, byte in enumerate(data):
                chaos_byte = chaos_sequence[i % len(chaos_sequence)]
                result.append(byte ^ chaos_byte)
            
            # Hash the result
            return hashlib.sha256(bytes(result)).digest()
            
        except Exception as e:
            print(f"Error in chaos algorithm: {e}")
            return hashlib.sha256(data).digest()
    
    def encrypt_image(self, image_path, key):
        """Encrypt image using Z-secure algorithm"""
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Generate random IV
            iv = secrets.token_bytes(self.iv_length)
            
            # Create cipher
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            encryptor = cipher.encryptor()
            
            # Pad data to multiple of 16 bytes
            padded_data = self._pad_data(image_data)
            
            # Encrypt
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            # Create encrypted image metadata
            metadata = {
                'encrypted': True,
                'algorithm': 'Z-Secure-v2',
                'timestamp': str(np.datetime64('now')),
                'iv': base64.b64encode(iv).decode('utf-8')
            }
            
            # Combine metadata and encrypted data
            metadata_bytes = json.dumps(metadata).encode('utf-8')
            metadata_length = struct.pack('>I', len(metadata_bytes))
            
            final_data = b'ZSEC' + metadata_length + metadata_bytes + encrypted_data
            
            # Save encrypted image
            output_path = os.path.join('processed', f"encrypted_{os.path.basename(image_path)}")
            with open(output_path, 'wb') as f:
                f.write(final_data)
            
            return output_path
            
        except Exception as e:
            print(f"Error encrypting image: {e}")
            return None
    
    def decrypt_image(self, encrypted_path, key):
        """Decrypt image using Z-secure algorithm"""
        try:
            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Check signature
            if not encrypted_data.startswith(b'ZSEC'):
                raise ValueError("Invalid encrypted file format")
            
            # Extract metadata
            metadata_length = struct.unpack('>I', encrypted_data[4:8])[0]
            metadata_bytes = encrypted_data[8:8+metadata_length]
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            
            # Extract IV and encrypted data
            iv = base64.b64decode(metadata['iv'])
            cipher_data = encrypted_data[8+metadata_length:]
            
            # Create cipher
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            
            # Decrypt
            padded_data = decryptor.update(cipher_data) + decryptor.finalize()
            
            # Remove padding
            original_data = self._unpad_data(padded_data)
            
            # Save decrypted image
            output_path = os.path.join('processed', f"decrypted_{os.path.basename(encrypted_path)}")
            with open(output_path, 'wb') as f:
                f.write(original_data)
            
            return output_path
            
        except Exception as e:
            print(f"Error decrypting image: {e}")
            return None
    
    def _pad_data(self, data):
        """Pad data to multiple of 16 bytes using PKCS7"""
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_data(self, padded_data):
        """Remove PKCS7 padding"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def update_key(self, old_key, new_face_encoding, email):
        """Update encryption key with new biometric data"""
        try:
            new_key = self.generate_key_from_biometrics(new_face_encoding, email)
            return new_key
        except Exception as e:
            print(f"Error updating key: {e}")
            return None
    
    def verify_encrypted_file(self, file_path):
        """Verify if file is encrypted with Z-secure"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
            return header == b'ZSEC'
        except Exception as e:
            print(f"Error verifying file: {e}")
            return False
    
    def get_file_metadata(self, encrypted_path):
        """Extract metadata from encrypted file"""
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data.startswith(b'ZSEC'):
                return None
            
            metadata_length = struct.unpack('>I', encrypted_data[4:8])[0]
            metadata_bytes = encrypted_data[8:8+metadata_length]
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return None
