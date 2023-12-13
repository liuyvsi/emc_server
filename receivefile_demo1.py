import socket
import json
# from hj212_mod import NetworkProtocol, read_protocol_from_file
import hj212_mod

# Initialize UDP socket
UDP_IP = '0.0.0.0'  # Replace with your receiver's IP or use 'localhost'
UDP_PORT = 12345  # Replace with the same port used in the sender program
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Initialize NetworkProtocol
protocol_data = hj212_mod.read_protocol_from_file('packdef.json')
network_protocol = hj212_mod.NetworkProtocol(protocol_data)

received_segments = []

# Receive and collect segments
while True:
    data, _ = sock.recvfrom(4096)
    if not data:
        break
    content_data = network_protocol.unpack(data.decode('utf-8'))
    
 
    # Check if it's the last segment
    segment_data = json.loads(content_data)
    received_segments.append(segment_data)
    if segment_data.get('PNUM') == segment_data.get('PNO'):
        break

# Close the socket after receiving all segments
sock.close()

# Initialize JSONSegmenter
reconstructed_data = hj212_mod.JSONSegmenter(ST='', CN='', PW='', MN='')

# Reconstruct the segments
reconstructed_content = reconstructed_data.concatenate_segments(received_segments)
print(f"debug-： {reconstructed_content}")



with open('reconstructed_file.txt', 'w') as file:
    file.write(reconstructed_content)
