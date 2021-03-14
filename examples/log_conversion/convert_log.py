import sys
import os
from an_packet_protocol import AN_Decoder, AN_Packet, an_packet_decode

if __name__ == '__main__':
    # Checks enough arguments in command for log conversion. Otherwise prompts user on use.
    if (len(sys.argv) != 2):
        print(f"Usage - program FileName\nExample - convert_log.py test_log.anpp")
        exit()
    file_name = str(sys.argv[1])

in_file = open(file_name, "rb")

data = in_file.read()
in_file.close()

out_file = open("anpp_separate_bytes.anpp", "w")

an_packet = AN_Packet()
decoder_array = AN_Decoder()

decoder_array.add_data(data)

for x in range(len(data)):
#for x in range(30):
    print(len(decoder_array.buffer))
    if (len(decoder_array.buffer)) == 0:
        break
    an_packet, decoder_array = an_packet_decode(decoder_array)
    if (an_packet is not None):
        out_file.writelines(str(an_packet.id) + ", " + str(an_packet.length) + ", " + str(an_packet.header) + ", " + str(an_packet.data) + "\n\n")

out_file.close()