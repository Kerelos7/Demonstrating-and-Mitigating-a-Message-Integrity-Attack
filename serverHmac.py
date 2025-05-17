#serverHmac.py
import hmac
import hashlib

SECRET_KEY = b'supersecretkey'  # Same key, but now used securely

def generate_hmac(message: bytes) -> str:
    """Generate secure HMAC using SHA-256"""
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    """Verify HMAC securely (constant-time comparison)"""
    expected_mac = generate_hmac(message)
    return hmac.compare_digest(mac, expected_mac)

def main():
    # Legitimate message
    message = b"amount=100&to=alice"
    mac = generate_hmac(message)
    
    print("== Secure Server (HMAC) ==")
    print(f"Original message: {message.decode()}")
    print(f"HMAC: {mac}")
    
    print("\n--- Verifying legitimate message ---")
    if verify(message, mac):
        print("✓ HMAC verified. Message is authentic.\n")
    
    # Attempt the same attack (will fail)
    forged_message = b"amount=100&to=alice\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00&admin=truee"  # From earlier attack
    forged_mac = "c45e48256adc8c6d991b951876ec6819"               # From earlier attack
    
    print("--- Verifying forged message ---")
    if verify(forged_message, forged_mac):
        print("✓ HMAC verified (THIS WOULD BE BAD!)")
    else:
        print("✗ HMAC verification failed (expected, because HMAC is secure)")

if __name__ == "__main__":
 main()