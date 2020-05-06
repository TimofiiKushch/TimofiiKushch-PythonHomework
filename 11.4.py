class Goods:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self):
        pass
    def getInfo(self):
        pass

class FoodProduct(Goods):
    def __init__(self, name, price, mass, expireIn):
        Goods.__init__(self, name, price)
        self.mass = mass
        self.expireIn = expireIn
    def __str__(self):
        return "FoodProduct " + str(self.name) + " " + str(self.price) + " " + str(self.mass) + " " + str(self.expireIn)
    def getInfo(self):
        return "{} за ціною {} ({}г), строк придатності {} день(-я, -ів) (FoodProduct)".format(self.name, self.price, self.mass, self.expireIn)

class Clothes(Goods):
    def __init__(self, name, price, brand, size):
        Goods.__init__(self, name, price)
        self.brand = brand
        self.size = size
    def __str__(self):
        return "Clothes " + str(self.name) + " " + str(self.price) + " " + str(self.brand) + " " + str(self.size)
    def getInfo(self):
        return "{} розміру {} від {} за ціною {} (Clothes)".format(self.name, self.size, self.brand, self.price)

class Book(Goods):
    def __init__(self, name, price, author):
        Goods.__init__(self, name, price)
        self.author = author
    def __str__(self):
        return "Book " + str(self.name) + " " + str(self.price) + " " + str(self.author)
    def getInfo(self):
        return "{} від {} за ціною {} (Book)".format(self.name, self.author, self.price)

class Store:
    def __init__(self):
        self.products = {}
    def addProduct(self, descStr):
        lst = descStr.split()
        allGood = False
        try:
            if lst[0] in self.products:
                if lst[0] == "FoodProduct":
                    self.products[lst[0]].append(FoodProduct(lst[1], lst[2], lst[3], lst[4]))
                    allGood = True
                elif lst[0] == "Clothes":
                    self.products[lst[0]].append(Clothes(lst[1], lst[2], lst[3], lst[4]))
                    allGood = True
                elif lst[0] == "Book":
                    self.products[lst[0]].append(Book(lst[1], lst[2], lst[3]))
                    allGood = True
            else:
                if lst[0] == "FoodProduct":
                    self.products[lst[0]] = [FoodProduct(lst[1], lst[2], lst[3], lst[4])]
                    allGood = True
                elif lst[0] == "Clothes":
                    self.products[lst[0]] = [Clothes(lst[1], lst[2], lst[3], lst[4])]
                    allGood = True
                elif lst[0] == "Book":
                    self.products[lst[0]] = [Book(lst[1], lst[2], lst[3])]
                    allGood = True
        except IndexError:
            pass
        return allGood
    def eraseProduct(self, descStr):
        lst = descStr.split()
        allGood = False
        try:
            if lst[0] in self.products:
                if lst[0] == "FoodProduct":
                    for i, product in enumerate(self.products[lst[0]]):
                        if product.name == lst[1] and product.price == lst[2] and product.mass == lst[3] and product.expireIn == lst[4]:
                            del self.products[lst[0]][i]
                            allGood = True
                elif lst[0] == "Clothes":
                    for i, product in enumerate(self.products[lst[0]]):
                        if product.name == lst[1] and product.price == lst[2] and product.brand == lst[3] and product.size == lst[4]:
                            del self.products[lst[0]][i]
                            allGood = True
                elif lst[0] == "Book":
                    for i, product in enumerate(self.products[lst[0]]):
                        if product.name == lst[1] and product.price == lst[2] and product.author == lst[3]:
                            del self.products[lst[0]][i]
                            allGood = True
        except IndexError:
            pass
        if allGood:
            if len(self.products[lst[0]]) == 0:
                self.products.pop(lst[0])
            return True
        else:
            return False

######################################################################################################
import tkinter as tki
class Programm:
    def __init__(self, store):
        self.store = store
        self.root = tki.Tk()
        self.root.geometry('1400x800+100+100')

        def getProductText(filter = "all"):
            productText = ""
            if filter == "all":
                for key in sorted(store.products.keys()):
                    for product in store.products[key]:
                        productText += product.getInfo() + "\n"
            elif filter == "FoodProduct":
                for product in store.products["FoodProduct"]:
                    productText += product.getInfo() + "\n"
            elif filter == "Clothes":
                for product in store.products["Clothes"]:
                    productText += product.getInfo() + "\n"
            elif filter == "Book":
                for product in store.products["Book"]:
                    productText += product.getInfo() + "\n"
            return productText

        self.filter = "all"

        self.logList = [("> Вітаємо! Для купівлі або повернення товару необхідно ввести відповідний\nхарактеристичний рядок.\n" +
        "Для FoodProduct: FoodProduct -назва- -ціна- -маса- -строк придатності-\n" +
        "Для Clothes: Clothes -назва- -ціна- -бренд- -розмір-\n" +
        "Для Book: Book -назва- -ціна- -автор-\n" +
        "Приклад: Book \"Книга\" 100 Автор\n")]
        logText = self.logList[0]
        def updateLog(string):
            self.logList.append(string)
            if (len(self.logList) > 20):
                del self.logList[0]
            logText = ""
            for s in self.logList:
                logText += s + "\n"
            return logText

        #####################

        productFrame = tki.Frame(self.root, highlightbackground = "grey", highlightthickness = 2)

        productListFrame = tki.Canvas(productFrame, width = 600, height = 300)
        scrollbar1 = tki.Scrollbar(productFrame, orient = "vertical", command = productListFrame.yview)

        self.productList = tki.Label(productListFrame, text = getProductText(), font = "TimesNewRoman 11", justify = "left")
        productListFrame.create_window(0, 0, anchor = 'nw', window = self.productList)

        productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)

        productListFrame.pack(anchor = "nw", side = "left")
        scrollbar1.pack(side = "right", fill  = "y", expand = True)
        productFrame.place(x = 750, y = 20)

        #####################

        logFrame = tki.Frame(self.root, highlightbackground = "grey", highlightthickness = 2)

        logListFrame = tki.Canvas(logFrame, width = 600, height = 300)
        scrollbar2 = tki.Scrollbar(logFrame, orient = "vertical", command = logListFrame.yview)

        self.logLabel = tki.Label(logListFrame, text = logText, font = "TimesNewRoman 13", justify = "left")
        logListFrame.create_window(0, 0, anchor = 'nw', window = self.logLabel)

        logListFrame.configure(scrollregion = logListFrame.bbox("all"), yscrollcommand = scrollbar2.set)

        logListFrame.pack(anchor = "nw", side = "left")
        scrollbar2.pack(side = "right", fill  = "y", expand = True)
        logFrame.place(x = 750, y = 400)
        
        #####################

        add1 = tki.Button(self.root, text = "Показати усі товари", font = "Arial 15", width = 30, height = 1, bg = "yellow")
        def add1_pressed():
            self.productList["text"] = getProductText()
            productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)
            self.filter = "all"
        add1["command"] = add1_pressed
        add2 = tki.Button(self.root, text = "Показати лише FoodProduct товари", font = "Arial 15", width = 30, height = 1, bg = "yellow")
        def add2_pressed():
            self.productList["text"] = getProductText("FoodProduct")
            productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)
            self.filter = "FoodProduct"
        add2["command"] = add2_pressed
        add3 = tki.Button(self.root, text = "Показати лише Clothes товари", font = "Arial 15", width = 30, height = 1, bg = "yellow")
        def add3_pressed():
            self.productList["text"] = getProductText("Clothes")
            productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)
            self.filter = "Clothes"
        add3["command"] = add3_pressed
        add4 = tki.Button(self.root, text = "Показати лише Book товари", font = "Arial 15", width = 30, height = 1, bg = "yellow")
        def add4_pressed():
            self.productList["text"] = getProductText("Book")
            productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)
            self.filter = "Book"
        add4["command"] = add4_pressed

        self.addButtonsVisible = False

        entry1 = tki.Entry(self.root, font = "Arial 12", width = 35)
        confirm1 = tki.Button(self.root, text = "✓", font = "Arial 15", height = 1, width = 3, bg = "green1")
        def confirm1_pressed():
            if self.store.eraseProduct(entry1.get()):
                self.logLabel["text"] = updateLog("> Дякуємо за покупку!")
                self.productList["text"] = getProductText(self.filter)
                productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)
            else:
                self.logLabel["text"] = updateLog("> Спробуйте ще раз.")
            logListFrame.configure(scrollregion = logListFrame.bbox("all"), yscrollcommand = scrollbar2.set)
        confirm1["command"] = confirm1_pressed
        self.entry1Visible = False

        entry2 = tki.Entry(self.root, font = "Arial 12", width = 35)
        confirm2 = tki.Button(self.root, text = "✓", font = "Arial 15", height = 1, width = 3, bg = "green1")
        def confirm2_pressed():
            if self.store.addProduct(entry2.get()):
                self.logLabel["text"] = updateLog("> Товар повернуто.")
                self.productList["text"] = getProductText(self.filter)
                productListFrame.configure(scrollregion = productListFrame.bbox("all"), yscrollcommand = scrollbar1.set)
            else:
                self.logLabel["text"] = updateLog("> Спробуйте ще раз.")
            logListFrame.configure(scrollregion = logListFrame.bbox("all"), yscrollcommand = scrollbar2.set)
        confirm2["command"] = confirm2_pressed
        self.entry2Visible = False
        
        button1 = tki.Button(self.root, text = "Показати товари►", font = "Arial 15", width = 30, height = 1, bg = "cyan")
        def button1_pressed():
            if self.addButtonsVisible == False:
                entry1.place_forget()
                confirm1.place_forget()
                entry2.place_forget()
                confirm2.place_forget()
                add1.place(x = 370, y = 20)
                add2.place(x = 370, y = 65)
                add3.place(x = 370, y = 110)
                add4.place(x = 370, y = 155)
                self.entry1Visible = False
                self.entry2Visible = False
                self.addButtonsVisible = True
            else:
                add1.place_forget()
                add2.place_forget()
                add3.place_forget()
                add4.place_forget()
                self.addButtonsVisible = False
        button1["command"] = button1_pressed
        button1.place(x = 20, y = 20)

        button2 = tki.Button(self.root, text = "Купити товар►", font = "Arial 15", width = 30, height = 1, bg = "cyan")
        def button2_pressed():
            if self.entry1Visible == False:
                entry1.place(x = 370, y = 72)
                confirm1.place(x = 700, y = 65)
                entry2.place_forget()
                confirm2.place_forget()
                add1.place_forget()
                add2.place_forget()
                add3.place_forget()
                add4.place_forget()
                self.entry1Visible = True
                self.entry2Visible = False
                self.addButtonsVisible = False
            else:
                entry1.place_forget()
                confirm1.place_forget()
                self.entry1Visible = False
        button2["command"] = button2_pressed
        button2.place(x = 20, y = 65)

        button3 = tki.Button(self.root, text = "Повернути товар►", font = "Arial 15", width = 30, height = 1, bg = "cyan")
        def button3_pressed():
            if self.entry2Visible == False:
                entry1.place_forget()
                confirm1.place_forget()
                entry2.place(x = 370, y = 117)
                confirm2.place(x = 700, y = 110)
                add1.place_forget()
                add2.place_forget()
                add3.place_forget()
                add4.place_forget()
                self.entry1Visible = False
                self.entry2Visible = True
                self.addButtonsVisible = False
            else:
                entry2.place_forget()
                confirm2.place_forget()
                self.entry2Visible = False
        button3["command"] = button3_pressed
        button3.place(x = 20, y = 110)

        button4 = tki.Button(self.root, text = "Вийти", font = "Arial 15", width = 30, height = 1, bg = "cyan")
        def button4_pressed():
            self.root.destroy()
        button4["command"] = button4_pressed
        button4.place(x = 20, y = 155)
    def run(self):
        self.root.mainloop()

#####################################################################################################
store = Store()
f = open("StoreData.txt")
for line in f.readlines():
    if line:
        store.addProduct(line)
p = Programm(store)
p.run()