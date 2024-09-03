# Enter your python code.
import os
import json
from common.Logger import logger
from quickfaas.awsiot import awsiot_publish
from quickfaas.global_dict import get_global_parameter
global_parameter = get_global_parameter()
def main(message,wizard_api):

    # os.remove("tmp_payload.json")
    # os.remove("first_serial.txt")
    timestamp = message["values"]["SMU01_Controller"]["mb001"]["timestamp"]
    timestampMsec = message["values"]["SMU01_Controller"]["mb001"]["timestampMsec"]

    if "SMU01_Controller" in message["values"]:
        serial_file_name = "first_serial.txt" 
        tmp_file_name = "tmp_payload.json"
        
        list_i = [] #ใช้ตอน debug เสร็จแล้วลบได้เลย
        Serial_list = []
        formatted_data = {} # สร้างตัวแปรสำหรับ tmp file
        power_list = []
        
        if not os.path.exists(serial_file_name):
            with open(serial_file_name, 'w') as file:

                for i in range(len(message["values"]["SMU01_Controller"]) - 2):
                    if i % 4 == 0:   
                        key = f'mb{i+1:03d}'
                        list_i.append(key) #ใช้ตอน debug เสร็จแล้วลบได้เลย
                        Serial_list.append(int(message["values"]["SMU01_Controller"][key]["raw_data"]))

                        formatted_data[str(Serial_list[-1])] = {} # เพิ่ม key ที่ยังไม่มีค่าเข้าไปใน dictionary

                # แปลง list เป็น string
                str_Serial_list = ",".join(map(str, Serial_list))

                # with open(serial_file_name, 'w') as file:
                #     file.write(str_Serial_list)
                #     file.close()
                file.write(str_Serial_list)
                file.close()

        # อ่านไฟล์ที่เก็บค่า Serial number 
        with open(serial_file_name, 'r') as file:
            serial_number = file.read().split(",")
            file.close()
   
        for i in range(len(message["values"]["SMU01_Controller"]) - 2):
            if i % 4 == 0:   
                key = f'mb{i+1:03d}'
                list_i.append(key) #ใช้ตอน debug เสร็จแล้วลบได้เลย
                Serial_list.append(str(message['values']['SMU01_Controller'][key]['raw_data']))

                formatted_data[str(Serial_list[-1])] = {} # เพิ่ม key ที่ยังไม่มีค่าเข้าไปใน dictionary
                data_count = 0

            else:
                key = f'mb{i+1:03d}'
                formatted_data[str(Serial_list[-1])][str(data_count)] = message['values']['SMU01_Controller'][key] # เพิ่ม values เข้าไปใน dictionary
                data_count += 1

        # แปลง list เป็น string
        # str_Serial_list = ",".join(map(str, Serial_list))

        # เขียน tmp file ในรูปแบบ json
        with open(tmp_file_name, 'w') as file:
            json.dump(formatted_data, file, indent=4)
            file.close()
        # เสร็จสื้นกระบวรการ save files

        # เริ่มอ่านไฟล์เพื่อเช็คว่า serail number ตรงกับของเดิมหรือไม่
        with open(tmp_file_name, 'r') as file:
            tmp_payload = json.load(file)
            file.close()

        serial_number_check_list = []
        # serial_number_list = []
        new_payload = {
            "values": {
                "SMU01_Controller": {}
            }
        }
        # เช็คว่า Serial ที่อ่านเข้ามาใหม่อยู่ใน list ของ Serial เดิมที่เก็บไว้หรือไม่
        serial_number_count = 0
        tmp_payload_count = 0
        false_index_serial_number = None
        false_index_serial_list = None

        # ------------------------
        # เช็คว่ามีการเปลี่ยน Controller หรือไม่
        new_card = False

        for i in Serial_list:
            if not i in serial_number:
                new_card = True
                false_index_serial_list = Serial_list.index(i)
            
        for i in serial_number:
            if not i in Serial_list:
                false_index_serial_number = serial_number.index(i)

        if new_card:
            serial_number[false_index_serial_number] = Serial_list[false_index_serial_list]
            str_serial_number = ",".join(map(str, serial_number))

            with open(serial_file_name, 'w') as file:
                file.write(str_serial_number)
                file.close()

        # อ่านไฟล์ที่เก็บค่า Serial number 
        with open(serial_file_name, 'r') as file:
            serial_number = file.read().split(",")
            file.close()

        # ถ้ามีการเปลี่ยน Controller ใหม่ save ไฟล์ serial number ใหม่เรียบร้อย
        #------------------------

        for j in range(len(message["values"]["SMU01_Controller"]) - 2):
            new_key = f'mb{j+1:03d}'
            if j % 4 == 0:   
                new_payload["values"]["SMU01_Controller"][new_key] = {
                    "raw_data": serial_number[serial_number_count],
                    "timestamp": timestamp,
                    "status": 1,
                    "timestampMsec": timestampMsec
                }

                power_list.append(tmp_payload[serial_number[serial_number_count]]["0"]["raw_data"] * tmp_payload[serial_number[serial_number_count]]["1"]["raw_data"])
                serial_number_count += 1
                # print(power_list)

            else:
                new_payload["values"]["SMU01_Controller"][new_key] = tmp_payload[serial_number[serial_number_count - 1]][str((j%4)-1)]

        # update ค่าที่เรียงใหม่เข้าไปใน message
        for i in range(len(message["values"]["SMU01_Controller"]) - 2):
            new_key = f'mb{i+1:03d}'
            message["values"]["SMU01_Controller"][new_key] = new_payload["values"]["SMU01_Controller"][new_key]
       
        # add ค่า power ที่คำณวนเข้าไปใน message
        data_range = len(message["values"]["SMU01_Controller"])
        for i in range(len(power_list)):
            new_key = f'mb{i+1+data_range:03d}'
            # print("new key", new_key)
            power_data = {
                new_key: {
                    "raw_data": power_list[i],
                    "timestamp": timestamp,
                    "status": 1,
                    "timestampMsec": timestampMsec
                }
            }
            message["values"]["SMU01_Controller"].update(power_data)
        # data = power_list

        # สร้าง object input power
        new_key = f'mb{data_range+len(power_list)+1:03d}'
        power_data = {
            new_key: {
                "raw_data": message["values"]["SMU01_Controller"][f'mb{data_range-1:03d}']["raw_data"] * message["values"]["SMU01_Controller"][f'mb{data_range:03d}']["raw_data"],
                "timestamp": timestamp,
                "status": 1,
                "timestampMsec": timestampMsec
            }
        }
        message["values"]["SMU01_Controller"].update(power_data)
        
    data = {
        **message,
        'mac_address': global_parameter.get('MAC').replace(":", "").upper()
    }
    logger.debug(message)
    awsiot_publish(__topic__, json.dumps(data), __qos__)