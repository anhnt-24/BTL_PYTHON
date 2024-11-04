import os
import uuid
from datetime import datetime
import string
import random

# Định dạng ngày
def dateHdl(date):
    date=datetime.strftime(date,"%Y-%m-%d")
    return date

# Chuyển chuỗi thành kiểu ngày tháng
def strToDate(str):
    date=datetime.strptime(str,"%Y-%m-%d")
    return date

# Hiện thị ra tên viết hoa chữ cái đầu
def nameHdl(name):
    return name.title()

# Ẩn một phần Email
def emailHdl(email):
    try:
        if(email):
            name,domain= email.split('@')
            hidden_name=name[0] + '*' * (len(name) - 2) + name[-1] if len(name) > 2 else name
            return hidden_name+'@' + domain
    except:
        return None


# Ẩn một phần số điện thoại
def phoneHdl(phone):
    try:
        return '*'*(len(phone)- 4)+ phone[-4:]
    except:
        return None

# Xử lí upload file
def fileHdl(instance, filename):
    filename,ext = filename.split('.')
    new_filename = f"{uuid.uuid4()}_{filename}.{ext}"
    class_name = instance.__class__.__name__
    folder_name = f"{class_name}"
    return os.path.join('', folder_name, new_filename)

 # Tạo một xâu ngẫu nhiên có độ dài là length
def generate_random_string(length):
    letters = string.ascii_letters + string.digits 
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

# Tạo mã đơn hàng
def generate_custom_uuid(id_user):
    day = datetime.now().strftime('%Y%m%d')
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    custom_uuid = f"{day}{id_user}{random_string}"
    return custom_uuid