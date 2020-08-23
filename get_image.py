
import boto3

def get_member(member_name):

    if member_name == "Kwon Eunbi":
        return "Kwon_Eunbi"
    
    elif member_name == "Sakura Miyawaki":
        return "Sakura_Miyawaki"

    elif member_name == "Hyewon Kang":
        return "Hyewon_Kang"
        
    elif member_name == "Yena Choi":
        return "Yena_Choi"

    elif member_name == "Cheyeon Lee":
        return "Cheyeon_Lee"
        
    elif member_name == "Chewon Kim":
        return "Chewon_Kim"

    elif member_name == "Minju Kim":
        return "Minju_Kim"

    elif member_name == "Nako Yabuki":
        return "Nako_Yabuki"

    elif member_name == "Hitomi Honda":
        return "Hitomi_Honda"

    elif member_name == "Yuri Choi":
        return "Yuri_Choi"

    elif member_name == "Yujin Ahn":
        return "Yujin_Ahn"

    elif member_name == "Wonyoung Chang":
        return "Wonyoung_Chang"
    else:
        return None

filename = 'img.jpg'

member_name = get_member(input("Input a member name:"))
id = int(input("ID:"))
print("Member:", member_name)
print("id:", id)

import boto3

s3_client = boto3.client('s3')

BUCKET = 'izonebucket'
OBJECT = 'IZONE/{}/pic_{}.jpg'.format(member_name, id)

url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': BUCKET, 'Key': OBJECT},
    ExpiresIn=300)

print(url)


