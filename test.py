import chardet

with open('C:\\Users\\ALJP18540403\\Desktop\\改善人間\\金子依頼\\輝度時系列.csv', 'rb') as file:
    result = chardet.detect(file.read())
    print(result)
