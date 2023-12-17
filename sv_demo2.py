import socket
import hj212_mod  # Assuming hj212_mod.py is in the same directory

# Example usage:
processor = hj212_mod.DataProcessor('udpdef.json')

# Receiving data
received_content = processor.receive_data()
print("Received Content:", received_content)
