import json
from common.Logger import logger
from quickfaas.awsiot import awsiot_publish
from quickfaas.global_dict import get_global_parameter
import os  # นำเข้าโมดูล os เพื่อใช้ฟังก์ชันที่เกี่ยวข้องกับระบบไฟล์

global_parameter = get_global_parameter()


def main(message, wizard_api):  # wizard_api
    file_raw = "raw_data.json"
    payload = {}
    '''
    # Battery 1
    bettery1_v = message["values"]["Battery_1"]["mb001"]["raw_data"]
    bettery1_a = message["values"]["Battery_1"]["mb002"]["raw_data"]
    bettery1_soc = message["values"]["Battery_1"]["mb003"]["raw_data"]
    # Battery 2
    bettery2_v = message["values"]["Battery_2"]["mb001"]["raw_data"]
    bettery2_a = message["values"]["Battery_2"]["mb002"]["raw_data"]
    bettery2_soc = message["values"]["Battery_2"]["mb003"]["raw_data"]
    # Battery 3
    bettery3_v = message["values"]["Battery_3"]["mb001"]["raw_data"]
    bettery3_a = message["values"]["Battery_3"]["mb002"]["raw_data"]
    bettery3_soc = message["values"]["Battery_3"]["mb003"]["raw_data"]
    # Battery 4
    bettery4_v = message["values"]["Battery_4"]["mb001"]["raw_data"]
    bettery4_a = message["values"]["Battery_4"]["mb002"]["raw_data"]
    bettery4_soc = message["values"]["Battery_4"]["mb003"]["raw_data"]
    # cal
    bettery_avg_v = ((bettery1_v + bettery2_v + bettery3_v + bettery4_v)) / 4
    bettery_avg_a = ((bettery1_a + bettery2_a + bettery3_a + bettery4_a)) / 4
    bettery_avg_soc = ((bettery1_soc + bettery2_soc + bettery3_soc + bettery4_soc)) / 4
    '''
    # Payload SMU01_Controller
    for i in range(1, 31):  # ตั้งแต่ 1 ถึง 30
        key = f"mb{i:03d}"  # สร้าง key ในรูปแบบ mb001, mb002, ..., mb030
        payload.update({key: message["values"]["SMU01_Controller"][key]["raw_data"]})
    with open(file_raw, "w") as file:  # สร้างไฟล์เปล่า
        file.write(json.dumps(payload, indent=4))  # บันทึกข้อมูลพร้อมการจัดรูปแบบ
        file.close()
        # เปิดไฟล์ในโหมดอ่าน ('r') และกำหนด encoding เป็น 'utf-8'
    # ใช้ with เพื่อให้แน่ใจว่าไฟล์จะถูกปิดหลังจากใช้งานเสร็จ
    with open(file_raw, "r", encoding="utf-8") as file:
        raw_data = json.load(file)  # อ่านข้อมูลจากไฟล์ JSON และแปลงเป็น Python dictionary
        # return data  # คืนค่าข้อมูลที่อ่านได้กลับไป 
   
    '''
    mb004_obj = message["values"]["Battery_4"]["mb003"].copy()
    message["values"]["Battery_4"].update(
        {
            "mb004": {
                "raw_data": bettery_avg_v,
                "timestamp": mb004_obj["timestamp"],
                "status": mb004_obj["status"],
            }
        }
    )
    message["values"]["Battery_4"].update(
        {
            "mb005": {
                "raw_data": bettery_avg_a,
                "timestamp": mb004_obj["timestamp"],
                "status": mb004_obj["status"],
            }
        }
    )
    message["values"]["Battery_4"].update(
        {
            "mb006": {
                "raw_data": bettery_avg_soc,
                "timestamp": mb004_obj["timestamp"],
                "status": mb004_obj["status"],
            }
        }
    )
    '''

    def check_and_write_to_file(file_path_Input_Serial_Number, jsonRaw_data):

        # ตรวจสอบว่าไฟล์มีอยู่ไหม
        if not os.path.exists(file_path_Input_Serial_Number):
            print(
                f"File '{file_path_Input_Serial_Number}' does not exist. Creating file..."
            )

            with open(file_path_Input_Serial_Number, "w") as file:  # สร้างไฟล์เปล่า
                file.write(
                    str(jsonRaw_data["mb001"])
                    + ","
                    + str(jsonRaw_data["mb005"])
                    + ","
                    + str(jsonRaw_data["mb009"])
                    + ","
                    + str(jsonRaw_data["mb013"])
                    + ","
                    + str(jsonRaw_data["mb017"])
                    + ","
                    + str(jsonRaw_data["mb021"])
                    + ","
                    + str(jsonRaw_data["mb025"])
                )
                file.close()

    def serial_check(Input_Serial_Number, Input_RawData):
        index_raw = ["mb001", "mb005", "mb009", "mb013", "mb017", "mb021", "mb025"]
        index_list = []

        with open(Input_Serial_Number, "r", encoding="utf-8") as file:
            # เปิดไฟล์ในโหมดอ่าน ('r') และกำหนด encoding เป็น 'utf-8'
            # ใช้ with เพื่อให้แน่ใจว่าไฟล์จะถูกปิดหลังจากใช้งานเสร็จ

            data = file.read().split(
                ","
            )  # อ่านข้อมูลจากไฟล์ JSON และแปลงเป็น Python dictionary
            file.close()

            for i in range(len(index_raw)):
                if str(Input_RawData[index_raw[i]]) in data:
                    #print(str(Input_RawData[index_raw[i]]))
                    #print(data[i])
                    index_list.append(data.index(str(Input_RawData[index_raw[i]])))
                else:
                    print(
                        f"Value '{str(Input_RawData[index_raw[i]])}' at index {i} (index_raw[{i}]) not found in data"
                    )
                    print(data[i])
                    New_device = str(Input_RawData[index_raw[i]])

            print(index_list)

            for i in range(0, 7):
                if not i in index_list:
                    data[i] = New_device
            #print(data)
            str_data = ""
            for i in data:
                str_data += i + ","
            str_data = str_data[:-1]
            #print(str_data)

            with open(Input_Serial_Number, "w") as file:
                file.write(str_data)
                file.close()

            #print("aaaaaaaaaaaaaaaaaa")
            #print(str(Input_RawData[index_raw[0]]))

            return data

    def Tmp_payload(jsonRaw_data):
        Tmp_file = "Tmp_payload.json"
        payload = {
            str(jsonRaw_data["mb001"]): {
                "1": jsonRaw_data["mb002"],
                "2": jsonRaw_data["mb003"],
                "3": jsonRaw_data["mb004"],
            },
            str(jsonRaw_data["mb005"]): {
                "1": jsonRaw_data["mb006"],
                "2": jsonRaw_data["mb007"],
                "3": jsonRaw_data["mb008"],
            },
            str(jsonRaw_data["mb009"]): {
                "1": jsonRaw_data["mb010"],
                "2": jsonRaw_data["mb011"],
                "3": jsonRaw_data["mb012"],
            },
            str(jsonRaw_data["mb013"]): {
                "1": jsonRaw_data["mb014"],
                "2": jsonRaw_data["mb015"],
                "3": jsonRaw_data["mb016"],
            },
            str(jsonRaw_data["mb017"]): {
                "1": jsonRaw_data["mb018"],
                "2": jsonRaw_data["mb019"],
                "3": jsonRaw_data["mb020"],
            },
            str(jsonRaw_data["mb021"]): {
                "1": jsonRaw_data["mb022"],
                "2": jsonRaw_data["mb023"],
                "3": jsonRaw_data["mb024"],
            },
            str(jsonRaw_data["mb025"]): {
                "1": jsonRaw_data["mb026"],
                "2": jsonRaw_data["mb027"],
                "3": jsonRaw_data["mb028"],
            },
        }

        with open(Tmp_file, "w") as file:  # สร้างไฟล์เปล่า
            file.write(
                json.dumps(payload, indent=4)
            )  # บันทึกข้อมูลพร้อมการจัดรูปแบบ (indentation) 4 ช่องว่าง
            file.close()

        return payload

    def PayloadToSend(OG_payload, serial_list, rawdata):
        New_Payload = {
            "values": {
                "SMU01_Controller": {
                    "mb001": {"raw_data": serial_list[0]},
                    "mb002": {"raw_data": OG_payload[serial_list[0]]["1"]},
                    "mb003": {"raw_data": OG_payload[serial_list[0]]["2"]},
                    "mb004": {"raw_data": OG_payload[serial_list[0]]["3"]},
                    "mb031": {
                        "raw_data": (
                            OG_payload[serial_list[0]]["1"]
                            * OG_payload[serial_list[0]]["2"]
                        )
                    },
                    "mb005": {"raw_data": serial_list[1]},
                    "mb006": {"raw_data": OG_payload[serial_list[1]]["1"]},
                    "mb007": {"raw_data": OG_payload[serial_list[1]]["2"]},
                    "mb008": {"raw_data": OG_payload[serial_list[1]]["3"]},
                    "mb032": {
                        "raw_data": (
                            OG_payload[serial_list[1]]["1"]
                            * OG_payload[serial_list[1]]["2"]
                        )
                    },
                    "mb009": {"raw_data": serial_list[2]},
                    "mb010": {"raw_data": OG_payload[serial_list[2]]["1"]},
                    "mb011": {"raw_data": OG_payload[serial_list[2]]["2"]},
                    "mb012": {"raw_data": OG_payload[serial_list[2]]["3"]},
                    "mb033": {
                        "raw_data": (
                            OG_payload[serial_list[2]]["1"]
                            * OG_payload[serial_list[2]]["2"]
                        )
                    },
                    "mb013": {"raw_data": serial_list[3]},
                    "mb014": {"raw_data": OG_payload[serial_list[3]]["1"]},
                    "mb015": {"raw_data": OG_payload[serial_list[3]]["2"]},
                    "mb016": {"raw_data": OG_payload[serial_list[3]]["3"]},
                    "mb034": {
                        "raw_data": (
                            OG_payload[serial_list[3]]["1"]
                            * OG_payload[serial_list[3]]["2"]
                        )
                    },
                    "mb017": {"raw_data": serial_list[4]},
                    "mb018": {"raw_data": OG_payload[serial_list[4]]["1"]},
                    "mb019": {"raw_data": OG_payload[serial_list[4]]["2"]},
                    "mb020": {"raw_data": OG_payload[serial_list[4]]["3"]},
                    "mb035": {
                        "raw_data": (
                            OG_payload[serial_list[4]]["1"]
                            * OG_payload[serial_list[4]]["2"]
                        )
                    },
                    "mb021": {"raw_data": serial_list[5]},
                    "mb022": {"raw_data": OG_payload[serial_list[5]]["1"]},
                    "mb023": {"raw_data": OG_payload[serial_list[5]]["2"]},
                    "mb024": {"raw_data": OG_payload[serial_list[5]]["3"]},
                    "mb036": {
                        "raw_data": (
                            OG_payload[serial_list[5]]["1"]
                            * OG_payload[serial_list[5]]["2"]
                        )
                    },
                    "mb025": {"raw_data": serial_list[6]},
                    "mb026": {"raw_data": OG_payload[serial_list[6]]["1"]},
                    "mb027": {"raw_data": OG_payload[serial_list[6]]["2"]},
                    "mb028": {"raw_data": OG_payload[serial_list[6]]["3"]},
                    "mb037": {
                        "raw_data": (
                            OG_payload[serial_list[6]]["1"]
                            * OG_payload[serial_list[6]]["2"]
                        )
                    },
                    "mb029": {"raw_data": (rawdata["mb029"])},
                    "mb030": {"raw_data": (rawdata["mb030"])},
                    "mb038": {"raw_data": (rawdata["mb029"]) * (rawdata["mb030"])},
                }
            }
        }
        return New_Payload

    Input_Serial_Number_Check = "Serial_Number.txt"
    check_and_write_to_file(Input_Serial_Number_Check, raw_data)
    serial_list = serial_check(Input_Serial_Number_Check, raw_data)
    OG_payload = Tmp_payload(raw_data)
    Final_payload = PayloadToSend(OG_payload, serial_list, raw_data)
    data = {
        **Final_payload,
        "mac_address": global_parameter.get("MAC").replace(":", "").upper(),
    }
    logger.debug(message)
    logger.debug(data)
    awsiot_publish(__topic__, json.dumps(data), __qos__)
