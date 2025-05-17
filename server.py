#server.py
import hashlib
SECRET_KEY = b'supersecretkey' # Unknown to attacker
def generate_mac(message: bytes) -> str:
 return hashlib.md5(SECRET_KEY + message).hexdigest()
def verify(message: bytes, mac: str) -> bool:
 expected_mac = generate_mac(message)
 return mac == expected_mac
def main():
 # Example message
 message = b"amount=100&to=alice"
 mac = generate_mac(message)
 print("=== Server Simulation ===")
 print(f"Original message: {message.decode()}")
 print(f"MAC: {mac}")
 print("\n--- Verifying legitimate message ---")
 if verify(message, mac):
  print("MAC verified successfully. Message is authentic.\n")
 # Simulated attacker-forged message
 forged_message = b"amount=100&to=alice" + b"&admin=true"
 forged_mac = mac # Attacker provides same MAC (initially)
 print("--- Verifying forged message ---")
 if verify(forged_message, forged_mac):
  print("MAC verified successfully (unexpected).")
 else:
  print("MAC verification failed (as expected).")
if __name__ == "__main__":
 main()
## `client.py` (Attacker script)
import sys
def perform_attack():
 # TODO: Your attack code goes here
 # You have intercepted: message and its mac
 intercepted_message = b"amount=100&to=alice"
 intercepted_mac = "..." # From server.py output
 # Your goal: append data and compute valid forged MAC
 data_to_append = b"&admin=true"
 forged_message = b"" # Replace with your forged message
 forged_mac = "" # Replace with your forged MAC
 print("Forged message:", forged_message)
 print("Forged MAC:", forged_mac)
if __name__ == "__main__":
 perform_attack()
