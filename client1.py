import struct
import binascii
from md5_custom import MD5
from server import verify  # Import the server's verify function

def md5_to_state(mac_hex):
    raw = binascii.unhexlify(mac_hex)
    return struct.unpack('<4I', raw)

def md5_padding(msg_len):
    padding = b'\x80'
    padding += b'\x00' * ((56 - (msg_len + 1) % 64) % 64)
    padding += struct.pack('<Q', msg_len * 8)
    return padding

def perform_attack():
    intercepted_message = b"amount=100&to=alice"
    intercepted_mac = "614d28d808af46d3702fe35fae67267c"  # Replace with actual MAC from server output

    data_to_append = b"&admin=true"
    key_len = 14

    total_len = key_len + len(intercepted_message)
    padding = md5_padding(total_len)

    forged_message = intercepted_message + padding + data_to_append

    a, b, c, d = md5_to_state(intercepted_mac)

    md5 = MD5()
    md5.set_state(a, b, c, d)
    md5.set_message_length(total_len + len(padding))
    md5.update(data_to_append)

    forged_mac = md5.hexdigest()

    print("Forged message:", forged_message)
    print("Forged MAC:", forged_mac)

    # Now verify with server's verify method
    if verify(forged_message, forged_mac):
        print("\n✓ Success! Server accepted the forged MAC.")
    else:
        print("\n✗ Failure! Server rejected the forged MAC.")

if __name__ == "__main__":
    perform_attack()
