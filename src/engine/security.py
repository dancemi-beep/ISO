import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class SecurityEngine:
    """加密與解讀引擎，用於保護 ISMS 範本 (Know-how)。"""
    
    def __init__(self, key=None):
        # 預設密鑰 (生產環境建議配合機器指紋或環境變數)
        default_secret = b"isms-doc-gen-secret-2024"
        salt = b"iso-27001-salt"
        
        if not key:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(default_secret))
            
        self.fernet = Fernet(key)

    def encrypt_data(self, data: bytes) -> bytes:
        """加密二進位數據。"""
        return self.fernet.encrypt(data)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """解密二進位數據。"""
        return self.fernet.decrypt(encrypted_data)

    def encrypt_file(self, src_path, dest_path):
        """加密檔案並儲存。"""
        with open(src_path, 'rb') as f:
            data = f.read()
        encrypted = self.encrypt_data(data)
        with open(dest_path, 'wb') as f:
            f.write(encrypted)

    def decrypt_to_memory(self, encrypted_path):
        """解密檔案內容並返回 BytesIO。"""
        import io
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.decrypt_data(encrypted_data)
        return io.BytesIO(decrypted_data)

if __name__ == "__main__":
    # 簡單自我測試
    engine = SecurityEngine()
    original = b"Hello ISO 27001"
    enc = engine.encrypt_data(original)
    dec = engine.decrypt_data(enc)
    assert original == dec
    print("SecurityEngine: 自我測試通過")
