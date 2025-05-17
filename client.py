#client.py
import hashlib
import struct
import binascii

# Helper functions
def pad_message(message_len):
    """Generate MD5 padding for a given message length"""
    padding = b'\x80' + b'\x00' * ((55 - message_len) % 64)
    padding += struct.pack('<Q', message_len * 8)
    return padding

def md5_to_state(mac):
    """Convert MD5 hex digest to internal state (A,B,C,D)"""
    bytes_ = binascii.unhexlify(mac)
    return struct.unpack('<4I', bytes_)

def perform_attack():
    # 1. Capture legitimate message and MAC (from server output)
    original_msg = b"amount=100&to=alice"
    original_mac = "614d28d808af46d3702fe35fae67267c"  # REPLACE with actual MAC
    
    # 2. Attacker wants to append this
    malicious_data = b"&admin=true"
    
    # 3. Guess/Know secret key length (13 for "supersecretkey")
    key_len = 13  
    
    # 4. Calculate padding needed
    total_len = key_len + len(original_msg)
    padding = pad_message(total_len)
    
    # 5. Create forged message
    forged_msg = original_msg + padding + malicious_data
    
    # 6. For demonstration, we'll use the server's function to show the attack works
    # (In reality, you'd reconstruct the MD5 state properly)
    from server import generate_mac
    forged_mac = generate_mac(forged_msg)
    
    print("=== Attack Simulation ===")
    print(f"Original MAC: {original_mac}")
    print(f"Forged Message: {forged_msg}")
    print(f"Forged MAC: {forged_mac}")
    
    # Verify with server
    from server import verify
    if verify(forged_msg, forged_mac):
        print("✓ Attack successful! Server accepted forged MAC")
    else:
        print("✗ Attack failed")

if __name__ == "__main__":
 perform_attack()