from tkinter import *
import os,re
from PIL import Image, ImageTk

index = 1
w_box = 1200  # 期望图像显示的大小（窗口大小）
h_box = 1200
flash_flag =10
def show_pic():
    global index
    # 这三行用来获取后缀
    files = os.listdir(r'D:\nHentai\1347395')
    files_num = len(files)
    suffix = files[0].rsplit(".")[-1]
    # index 检查
    if index>files_num:
        index -=1
    if index<1:
        index += 1
    # 定义序列
    pil_image = Image.open(r'D:\nHentai\1347395' + '\\' + str(index)+"."+suffix)
    pil_image_resized = resize(w_box, h_box, pil_image)  # 缩放图像让它保持比例，同时限制在一个矩形框范围内  【调用函数，返回整改后的图片】
    img = ImageTk.PhotoImage(pil_image_resized)
    PILImage.config(image=img)
    PILImage.image = img #keep a reference
    root.title(str(index) + "\\" + str(files_num))

def broad_key(event):
    # print("event.keycode =", event.keycode)
    if event.keycode==39:
        up()
    elif event.keycode==37:
        down()

def resize( w_box, h_box, pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片
    w, h = pil_image.size #获取图像的原始大小
    f1 = 1.0*w_box/w
    f2 = 1.0*h_box/h
    factor = min([f1, f2])
    width = int(w*factor)
    height = int(h*factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def up():
    global index
    index+=1
    show_pic()

def down():
    global index
    index -= 1
    show_pic()

def wh_update(event):
    global w_box
    global h_box
    global flash_flag
    flash_flag -= 1
    w_box = event.width
    h_box = event.height
    if flash_flag==0:
        show_pic()
        flash_flag=10

if __name__ == "__main__":
    root = Tk()
    # 初始化名字
    root.title('nHentai终端')
    # 初始化显示控件
    PILImage = Label(root)
    PILImage.pack()
    # 第一次显示，先充一充场面
    show_pic()
    # 定义了上下切换按钮
    # Button(root,text='上一张',command=down).pack()
    # Button(root,text='下一张',command=up).pack()
    root.bind("<Configure>",wh_update)  # 回溯调用
    root.bind("<Key>", broad_key)  # 回溯调用
    root.mainloop()
