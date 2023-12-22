import hj212_mod  # Assuming hj212_mod.py is in the same directory  
import queue
  
# Example usage:  
processor = hj212_mod.DataProcessor('udpdef.json')  
  
received_data_queue = queue.Queue()

# Start the receiver in a thread
processor.run_receiver(received_data_queue)

# Simulate processing of received data
while True:
    if not received_data_queue.empty():
        # Process received data
        data = received_data_queue.get()
        print("Received Data:", data)
        # Perform further processing as needed
