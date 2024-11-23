# bin2rap 20241123

import os
import struct

# Root directory of the script
root_directory = os.path.dirname(os.path.abspath(__file__))

# Input binary file
input_bin_file = os.path.join(root_directory, "rap.bin")

# Output directory for .rap files
output_rap_directory = os.path.join(root_directory, "bin2rap")

# Log file
log_file = os.path.join(root_directory, "bin_log.txt")

# Magic number to identify each entry
MAGIC_NUMBER = b"\xFA\xF0\xFA\xF0" + b"\x00" * 12

# Parse the binary file and create .rap files
def parse_rap_bin(input_bin_file, output_rap_directory, log_file):
    # Ensure the output directory exists
    os.makedirs(output_rap_directory, exist_ok=True)

    with open(input_bin_file, "rb") as bin_file, open(log_file, "w") as log:
        while True:
            # Read the magic number and padding
            magic = bin_file.read(len(MAGIC_NUMBER))
            if not magic:
                break  # End of file

            # Verify the magic number
            if magic != MAGIC_NUMBER:
                log.write("Invalid magic number detected in the binary file.\n")
                raise ValueError("Invalid magic number detected in the binary file.")

            # Read the CONTENT_ID (36 bytes)
            content_id_bytes = bin_file.read(36)
            content_id = content_id_bytes.decode().rstrip("\x00")

            # Read the 12 bytes of padding after CONTENT_ID
            bin_file.read(12)

            # Read the 16-byte value
            rap_content = bin_file.read(16)

            # Create the .rap file with the CONTENT_ID as filename
            rap_filename = f"{content_id}.rap"
            rap_path = os.path.join(output_rap_directory, rap_filename)

            with open(rap_path, "wb") as rap_file:
                rap_file.write(rap_content)

            # Log in the format: CONTENT_ID:16 byte value in hex
            log.write(f"{content_id}:{rap_content.hex()}\n")

# Parse the rap.bin file and create .rap files
parse_rap_bin(input_bin_file, output_rap_directory, log_file)
