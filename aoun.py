# Enter your python code.
import os
import json
from common.Logger import logger
from quickfaas.awsiot import awsiot_publish
from quickfaas.global_dict import get_global_parameter
global_parameter = get_global_parameter()
def main(message,wizard_api):

    if "SMU01_Controller" in message["values"]:
        serial_file_name = "first_serial.txt" 
        tmp_file_name = "tmp_payload.json"
        if not os.path.exists(serial_file_name):
            with open(serial_file_name, 'w') as file:
                file.close()

        list_i = [] #ใช้ตอน debug เสร็จแล้วลบได้เลย
        Serial_list = []
        formatted_data = {} # สร้างตัวแปรสำหรับ tmp file
   
        for i in range(len(message["values"]["SMU01_Controller"]) - 2):
            if i % 4 == 0:   
                key = f'mb{i+1:03d}'
                list_i.append(key) #ใช้ตอน debug เสร็จแล้วลบได้เลย
                Serial_list.append(int(message["values"]["SMU01_Controller"][key]["raw_data"]))

                formatted_data[str(Serial_list[-1])] = {} # เพิ่ม key ที่ยังไม่มีค่าเข้าไปใน dictionary
                data_count = 0

            else:
                key = f'mb{i+1:03d}'
                formatted_data[str(Serial_list[-1])][str(data_count)] = message["values"]["SMU01_Controller"][key] # เพิ่ม values เข้าไปใน dictionary
                data_count += 1

        # เขียน tmp file ในรูปแบบ json
        with open(tmp_file_name, 'w') as file:
            json.dump(formatted_data, file, indent=4)
            file.close()


        str_Serial_list = ",".join(map(str, Serial_list))

        with open(serial_file_name, 'w') as file:
            file.write(str_Serial_list)
            file.close()
        # เสร็จสื้นกระบวรการ save files

        # เริ่มอ่านไฟล์เพื่อเช็คว่า serail number ตรงกับของเดิมหรือไม่
        with open(tmp_file_name, 'r') as file:
            data = json.load(file)
            file.close()

        # data = formatted_data
    # data = {
    #     **message,
    #     'mac_address': global_parameter.get('MAC').replace(":", "").upper()
    # }
    logger.debug(message)
    awsiot_publish(__topic__, json.dumps(data), __qos__)