import tkinter as tk, os
from PIL import Image, ImageTk

def resize( w_box, h_box, pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片
  w, h = pil_image.size #获取图像的原始大小
  f1 = 1.0*w_box/w
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)


class Application(tk.Frame):
    def __init__(self, master=None):
        self.w_box = 500  # 期望图像显示的大小（窗口大小）
        self.h_box = 700
        self.files = os.listdir(r'D:\nHentai\1347395')
        self.index = 0
        pil_image = Image.open(r'D:\nHentai\1347395' + '\\' + self.files[self.index])
        pil_image_resized = resize(self.w_box, self.h_box, pil_image)  # 缩放图像让它保持比例，同时限制在一个矩形框范围内  【调用函数，返回整改后的图片】
        self.img = ImageTk.PhotoImage(pil_image_resized)
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.lblImage = tk.Label(self)
        self.lblImage['image'] = self.img
        self.lblImage.pack()
        self.f = tk.Frame()
        self.f.pack()
        self.btnPrev = tk.Button(self.f, text='上一张', command=self.prev)
        self.btnPrev.pack(side=tk.LEFT)
        self.btnNext = tk.Button(self.f, text='下一张', command=self.next)
        self.btnNext.pack(side=tk.LEFT)

    def prev(self):
        self.showfile(-1)

    def next(self):
        self.showfile(1)

    def showfile(self, n):
        self.index += n
        if self.index < 0:
            self.index = len(self.files) - 1
        if self.index > (len(self.files) - 1):
            self.index = 0
        pil_image = Image.open(r'D:\nHentai\1347395' + '\\' + self.files[self.index])
        pil_image_resized = resize(self.w_box, self.h_box, pil_image)  # 缩放图像让它保持比例，同时限制在一个矩形框范围内  【调用函数，返回整改后的图片】
        self.img = ImageTk.PhotoImage(pil_image_resized)
        self.lblImage['image'] = self.img

    # 动态更新窗体的长和宽
    def WHup(self,event):
        self.w_box = event.width
        self.h_box = event.height



root = tk.Tk()
root.title('终端本子')
app = Application(master=root)
app.bind("<Configure>",app.WHup)
app.mainloop()

