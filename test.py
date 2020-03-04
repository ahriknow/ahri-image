# import sqlite3

# if __name__ == '__main__':
#     conn = sqlite3.connect('./Image/db.sqlite3')
#     c = conn.cursor()
#     msql = '''select image from `store` where `name`=? and `index`=?'''
#     para = ('1', '1')
#     c.execute(msql, para)
#     values = c.fetchone()
#     c.close()
#     conn.close()
#     if values:
#         print(values[0])
# import pytesseract
# from PIL import Image

# img = Image.open('/font.png')
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# text = pytesseract.image_to_string(img, lang='chi_sim')
