# copied from hj212_mod.py
# copied from segtes1.py 
# filename： hj212_mod.py

import json


class NetworkProtocol:
    def __init__(self, protocol_json):
        self.protocol = protocol_json['package']

    def pack(self, data_to_pack):
        # Generate length and CRC based on data_to_pack
        length = str(len(data_to_pack)).zfill(4)
        # Calculate CRC
        crc = self.generate_crc(data_to_pack)  # Generate CRC value
        
        packed_data = ""
        for section in self.protocol:
            if "head" in section:
                packed_data += section["head"]
            elif "length" in section:
                packed_data += length
            elif "content" in section:
                packed_data += data_to_pack
            elif "crc" in section:
                packed_data += crc
            elif "tail" in section:
                packed_data += section["tail"]

        return packed_data

    def unpack(self, packed_data):
        unpacked = {}
        index = 0
        content_length = 0
        for section in self.protocol:
            if "head" in section:
                unpacked["head"] = packed_data[index:index + section["max_length"]]
            elif "length" in section:
                unpacked["length"] = packed_data[index:index + section["max_length"]]
                content_length = int(unpacked['length'])
            elif "content" in section:
                unpacked["content"] = packed_data[index:index + content_length]
                section["max_length"] = content_length
            elif "crc" in section:
                unpacked["crc"] = packed_data[index:index + section["max_length"]]
                crc_value = self.generate_crc(unpacked["content"])
                if unpacked["crc"] != crc_value:
                    raise ValueError("CRC check failed! Data may be corrupted.")
            elif "tail" in section:
                unpacked["tail"] = packed_data[index:index + section["max_length"]]
            index += section["max_length"]

        return unpacked["content"]

    @staticmethod
    def generate_crc(data):
        crc = 0xFFFF  # 初始化为 0xFFFF
        poly = 0xA001  # CRC-16 的多项式

        for byte in data:
            crc ^= ord(byte)
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1

        return format(crc & 0xFFFF, '04X')  # 返回 16 位的 CRC 值，以十六进制格式


def read_protocol_from_file(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

class JSONSegmenter:
    def __init__(self, ST, CN, PW, MN):
        self.data = {
            "QN": "YYYYMMDDHHMMSSZZZ",
            "ST": ST,
            "CN": CN,
            "PW": PW,
            "MN": MN,
            "Flag": "0",
            "PNUM": "0001",
            "PNO": "0001",
            "CP": "xxxxxxxxxxx"
        }

    def segment_data(self, input_str):
        if len(input_str) > 946:
            segmented_data = []
            segments = [input_str[i:i + 946] for i in range(0, len(input_str), 946)]
            self.data["PNUM"] = str(len(segments)).zfill(4)

            for idx, segment in enumerate(segments, start=1):
                temp_data = self.data.copy()
                temp_data["PNO"] = str(idx).zfill(4)
                temp_data["CP"] = segment
                segmented_data.append(temp_data)

            return segmented_data
        else:
            self.data["CP"] = input_str
            return [self.data]
  
    @staticmethod
    def concatenate_segments(segmented_json):
        # Sort segments based on 'PNO' value
        
        print(segmented_json) #debug
        sorted_segments = sorted(segmented_json, key=lambda x: int(x["PNO"]))
        concatenated_cp = ""

        for segment in sorted_segments:
            concatenated_cp += segment["CP"]

        return concatenated_cp

