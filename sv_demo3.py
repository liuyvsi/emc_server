import hj212_mod  # Assuming hj212_mod.py is in the same directory  
  
# Example usage:  
processor = hj212_mod.DataProcessor('udpdef.json')  
  
while True:  # Infinite loop  
    # Receiving data  
    received_content = processor.receive_data()  
      
    # Check if received_content indicates the end condition  
    if received_content == 'end_condition':  
        break  # Exit the infinite loop  
      
    print("Received Content:", received_content)
