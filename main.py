import tkinter
import customtkinter as ct
import sqlite3
import time
from datetime import datetime

con = sqlite3.connect("database.db") 
cur = con.cursor() # Veritabanı ve cursor bağlantısı.

global currentDay           #Sık kullanılacak verilerin global yapılması.
global currentMonth
global currentYear

currentDay = datetime.now().day
currentMonth = datetime.now().month #Takvime yazmak için güncel tarihler.
currentYear = datetime.now().year

exceptions = [4, 6, 9, 11] #30 gün olan aylar.
months=["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
dayOfWeek = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}
numbers=["0","1","2","3","4","5","6","7","8","9"]

calendarButtons = []

root = ct.CTk()

root.geometry("1100x650") 
root.title("Takvim")
root.resizable(False, False)
ct.set_appearance_mode("light")  #Ekran boyutu ve renk ayarları

def login(usr, psw):   # Girilen kullanıcı adı ve şifrenin veritabanında kontrol edilmesi.
    cur.execute("""SELECT password FROM userdata WHERE username = (?)""", (usr,))
    dbPsw = cur.fetchone()
    try:
        if dbPsw[0] == psw:    
            global loggedInUser
            loggedInUser = usr
            succesfulLogin()
        else:
            errorBox("login")
    except:
        errorBox("login")

def openLoginPanel(): # Giriş yapma ekranı.
    
    def showPassWordEvent(): # Şifreyi göster butonunun çalışması
        if buttonVariable.get() == "on":
            passwordEntry.configure(show = "")
        elif buttonVariable.get() == "off":
            passwordEntry.configure(show = "*")

    def innerFunction():
        givenUserName = usernameEntry.get()
        givenPassword = passwordEntry.get()
        login(givenUserName, givenPassword) # Girilen k. adı ve şifrenin kontrol fonksiyonuna gitmesi.
    
    global loginPanel
    loginPanel = ct.CTkFrame(master = root, width = 300, height = 400)
    loginPanel.place(relx= 0.4, rely = 0.5, anchor = "w")

    usernameLabel = ct.CTkLabel(master = loginPanel, text = "Kullanıcı Adı", width = 3, height = 3)
    usernameEntry = ct.CTkEntry(master=loginPanel, width = 200, height = 40, placeholder_text="Kullanıcı Adını Gir")
    usernameLabel.grid(row = 0, column = 0, sticky = "w", pady = 2, padx = 5)
    usernameEntry.grid(row = 1, column = 0, pady = 2, padx = 5)

    passwordEntry = ct.CTkEntry(master=loginPanel, width = 200, height = 40, placeholder_text="Şifreni Gir", show = "*")
    passwordLabel = ct.CTkLabel(master = loginPanel, text = "Şifre", width = 10, height = 10)
    passwordLabel.grid(row = 2, column = 0, sticky = "w", pady = 2, padx = 5)
    passwordEntry.grid(row = 3, column = 0, sticky = "w", pady = 2, padx = 5)

    loginButton = ct.CTkButton(master=loginPanel, text="Giriş Yap", width=95, command = innerFunction)
    registerButton = ct.CTkButton(master=loginPanel, text="Kayıt Ol", width=95, command = openRegisterPanel)
    loginButton.grid(row = 5, column = 0, sticky = "w", pady = 10, padx = 5)
    registerButton.grid(row = 5, column = 0, sticky = "e", pady = 10, padx = 5)
    root.bind('<Return>', lambda event:innerFunction())

    buttonVariable = ct.StringVar(value="off")
    hidePasswordButton = ct.CTkCheckBox(master = loginPanel, width = 100, height = 5, text = "Şifreyi Göster", variable = buttonVariable, onvalue="on", offvalue="off", command=showPassWordEvent)
    hidePasswordButton.grid(row = 4, column = 0, sticky = "w",pady = 10, padx = 5)

def checkErrors(passwordError,tcnError,phoneError,nameError,surnameError,usernameError):
    errors=[] #Girilen bilgilerin boş olmaması, TCN ve telefon numalaralarının sayısal değer olması vb. gibi girdilerin kontrolü.
    if tcnError == 1:
        pass
    else:
        errors.append(tcnError)
    if phoneError == 1:
        pass
    else:
        errors.append(phoneError)
    if passwordError == "password":
        errors.append(passwordError)
    if nameError == "name":
        errors.append(nameError)
    if surnameError == "name":
        errors.append("srn")
    if usernameError == "name":
        errors.append("usr")
    if len(errors)>0:
        errorBox(errors)
    else:
        return 1

def errorBox(errors): #Girdilerde sorun olması durumunda açılan hata penceresi.
    def innerFunc():
        errorFrame.destroy()

    errorTexts= {
    "TCN":"Girilen TC Kimlik Numarasında bir hata var.", #Hatanın tipine göre gönderilen mesajlar:
    "phone":"Girilen telefon numarasında bir hata var.",
    "password":"Şifrende boşluk olamaz.",
    "name":"Adında boşluk olamaz.",
    "srn":"Soyadında boşluk olamaz.",
    "usr":"Kullanıcı adında boşluk olamaz.",
    "mail":"E-mail adresinde boşluk olamaz.",
    "time":"Girilen saatte bir hata var.",
    "time2":"Bitiş saati başlangıç saatinden erken olamaz.",
    "rmndr":"Hatırlatma saati 0'dan büyük olmalı.",
    "rmndr2":"Hatırlatma saati sadece sayılardan oluşmalı.",
    "rmndr3":"Hatırlatma saati boş bırakılamaz."
    }

    errorFrame = ct.CTkFrame(master = root, width=300, height=200)
    errorFrame.place(relx=0.36,rely=0.4)

    errorLabel = ct.CTkLabel(master=errorFrame, text = "UYARI!").place(x=129, y = 5)

    acceptButton = ct.CTkButton(master = errorFrame, text="Tamam", width= 290, command=innerFunc)
    acceptButton.place(x=5, y=165)

    counter = 0
    if errors == "bos":
        ct.CTkLabel(master=errorFrame, text =" Yanında (*) olan bölümler boş bırakılamaz.").place(x=10, y = 30+(counter*20))
    elif errors == "login":
        ct.CTkLabel(master=errorFrame, text =" Kullanıcı adı ya da şifre yanlış.").place(x=10, y = 30+(counter*20))
    else:
        for i in errors:
            ct.CTkLabel(master=errorFrame, text = errorTexts[i]).place(x=10, y = 30+(counter*20))
            counter = counter + 1

def checkEntry(name, entry): #Girdilerin tekrar kontrolü.
    if name == "TCN":
        if len(entry)==11:
            for num in entry:
                if num in numbers:
                    return 1
                else:
                    return "TCN"
        else:
            return "TCN"
    elif name == "phone":
        if len(entry)==11:
            for num in entry:
                if num in numbers:
                    return 1
                else:
                    return "phone"
        else:
            return "phone"
    elif name == "password":
        for letter in entry:
            if letter == " ":
                return "password"
    elif name == "name":
        for letter in entry:
            if letter == " ":
                return "name"
    
def openRegisterPanel(): #Kayıt olma ekranı.
    def innerFunction(): #Girilen girdilerin alındığı ve hata kontrol fonksiyonuna gönderildiği fonksiyon.
        errors = []
        givenName = nameEntry.get() or -1
        givenSurname = surnameEntry.get() or -1
        givenUsername = usernameEntry.get() or -1
        givenPassword = passwordEntry.get() or -1
        givenTCN = TCNEntry.get() or -1
        givenPhoneNum = phoneNumEntry.get() or -1
        givenMail = mailEntry.get() or "nil"
        givenAdress = adressEntry.get() or "nil"
        givenUserType = userTypeCombobox.get()
        if givenName == -1 or givenSurname == -1 or givenUsername == -1 or givenPassword == -1 or givenTCN == -1 or givenPhoneNum == -1:
            errorBox("bos")
            return

        passwordError = checkEntry("password", givenPassword)
        tcnError = checkEntry("TCN", givenTCN)
        phoneError = checkEntry("phone", givenPhoneNum)
        nameError = checkEntry("name", givenName)
        surnameError = checkEntry("name", givenSurname)
        usernameError = checkEntry("name", givenUsername)

        if checkErrors(passwordError,tcnError,phoneError,nameError,surnameError,usernameError)== 1:
            registerPanel.destroy() #Hata yoksa veritabanına yeni kullanıcı bilgilerinin eklendiği if bloğu.
            cur.execute("""INSERT INTO userdata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (givenUsername, givenName, givenSurname, givenPassword, givenTCN, givenPhoneNum, givenMail, givenAdress, givenUserType))
            con.commit()
            global loggedInUser
            loggedInUser = givenUsername
            succesfulLogin() #Giriş yapmayı sağlayan ve kayıt/giriş ekranını kapatan fonksiyonun çalışması.

    loginPanel.destroy()

    global registerPanel
    registerPanel = ct.CTkFrame(master = root, width = 300, height = 400)
    registerPanel.place(relx= 0.4, rely = 0.5, anchor = "w")

    nameLabel = ct.CTkLabel(master = registerPanel, text = "Ad (*)", width = 3, height = 3)
    nameEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Adını Gir")
    nameLabel.grid(row = 0, column = 0, sticky = "w", pady = 2, padx = 5)
    nameEntry.grid(row = 1, column = 0, pady = 2, padx = 5)
    
    surnameLabel = ct.CTkLabel(master = registerPanel, text = "Soyad (*)", width = 10, height = 10)
    surnameEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Soyadını Gir")
    surnameLabel.grid(row = 2, column = 0, sticky = "w", pady = 2, padx = 5)
    surnameEntry.grid(row = 3, column = 0, sticky = "w", pady = 2, padx = 5)

    usernameLabel = ct.CTkLabel(master = registerPanel, text = "Kullanıcı Adı (*)", width = 10, height = 10)
    usernameEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Kullanıcı Adını Gir")
    usernameLabel.grid(row = 4, column = 0, sticky = "w", pady = 2, padx = 5)
    usernameEntry.grid(row = 5, column = 0, sticky = "w", pady = 2, padx = 5)

    passwordLabel = ct.CTkLabel(master = registerPanel, text = "Şifre (*)", width = 10, height = 10)
    passwordEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Şifreni Gir", show = "*")
    passwordLabel.grid(row = 6, column = 0, sticky = "w", pady = 2, padx = 5)
    passwordEntry.grid(row = 7, column = 0, sticky = "w", pady = 2, padx = 5)

    TCNLabel = ct.CTkLabel(master = registerPanel, text = "TC Kimlik Numarası (*)", width = 10, height = 10)
    TCNEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="TC Kimlik Numaranı Gir")
    TCNLabel.grid(row = 8, column = 0, sticky = "w", pady = 2, padx = 5)
    TCNEntry.grid(row = 9, column = 0, sticky = "w", pady = 2, padx = 5)

    phoneNumLabel = ct.CTkLabel(master = registerPanel, text = "Telefon Numarası (*)", width = 10, height = 10)
    phoneNumEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Telefon Numaranı Gir")
    phoneNumLabel.grid(row = 10, column = 0, sticky = "w", pady = 2, padx = 5)
    phoneNumEntry.grid(row = 11, column = 0, sticky = "w", pady = 2, padx = 5)

    mailLabel = ct.CTkLabel(master = registerPanel, text = "Email", width = 10, height = 10)
    mailEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Email Adresini Gir")
    mailLabel.grid(row = 12, column = 0, sticky = "w", pady = 2, padx = 5)
    mailEntry.grid(row = 13, column = 0, sticky = "w", pady = 2, padx = 5)

    adressLabel = ct.CTkLabel(master = registerPanel, text = "Adres", width = 10, height = 10)
    adressEntry = ct.CTkEntry(master=registerPanel, width = 200, height = 40, placeholder_text="Adres Gir")
    adressLabel.grid(row = 14, column = 0, sticky = "w", pady = 2, padx = 5)
    adressEntry.grid(row = 15, column = 0, sticky = "w", pady = 2, padx = 5)

    userTypeLabel = ct.CTkLabel(master = registerPanel, text = "Kullanıcı Tipi", width = 10, height = 10)
    userTypeCombobox = ct.CTkComboBox(master=registerPanel, width = 200, height = 40, values=["Kullanıcı", "Admin"])
    userTypeLabel.grid(row = 16, column = 0, sticky = "w", pady = 2, padx = 5)
    userTypeCombobox.grid(row = 17, column = 0, sticky = "e", pady = 2, padx = 5)

    backButton = ct.CTkButton(master=registerPanel, text="Geri", width=95, command = backButtonFunc)
    registerButton = ct.CTkButton(master=registerPanel, text="Kayıt Ol", width=95, command = innerFunction)
    backButton.grid(row = 18, column = 0, sticky = "w", pady = 10, padx = 5)
    registerButton.grid(row = 18, column = 0, sticky = "e", pady = 10, padx = 5)

def backButtonFunc():
    registerPanel.destroy()
    openLoginPanel()

def openMainPanel(): # Giriş yapıldığında ekranın sağında oluşan büyük takvimin oluşturulması.
    mainPanel = ct.CTkFrame(master = root, width = 810, height = 630)
    mainPanel.place(x= 290, y = 10)
    mondayLabel = ct.CTkLabel(master = mainPanel, text = "Pazartesi").grid(row = 0, column = 1, pady = 2, padx = 35)
    tuesdayLabel = ct.CTkLabel(master = mainPanel, text = "Salı").grid(row = 0, column = 2, pady = 2, padx = 35)
    wednesdayLabel = ct.CTkLabel(master = mainPanel, text = "Çarşamba").grid(row = 0, column = 3, pady = 2, padx = 35)
    thursdayLabel = ct.CTkLabel(master = mainPanel, text = "Perşembe").grid(row = 0, column = 4, pady = 2, padx = 35)
    fridayLabel = ct.CTkLabel(master = mainPanel, text = "Cuma").grid(row = 0, column = 5, pady = 2, padx = 35)
    saturdayLabel = ct.CTkLabel(master = mainPanel, text = "Cumartesi").grid(row = 0, column = 6, pady = 2, padx = 35)
    sundayLabel = ct.CTkLabel(master = mainPanel, text = "Pazar").grid(row = 0, column = 7, pady = 2, padx = 35)

def openMonthPanel(): # Seçili olan ayın gösterildiği ve değiştirilebildiği ekranın oluşturulması.
    global monthPanel
    monthPanel = ct.CTkFrame(master= root, width = 275, height = 50)
    monthPanel.place(x = 10, y = 10)
    
    previousButton = ct.CTkButton(master = root, text ="<", width = 5, command=lambda:printDate("p")).place(x = 15, y = 20)
    nextButton = ct.CTkButton(master = root, text = ">",  width = 5, command=lambda:printDate("n")).place(x = 260, y = 20)
    monthLabel = ct.CTkLabel(master = monthPanel, text = months[currentMonth-1] + "  " + str(currentYear)).place(x = 95, y = 12)

def openCalendarPanel(): # Seçili olan aydaki gün bilgilerinin oluşturulduğu ve takvim olarak 7 satır, 6 sütun şeklinde ekrana
    global calendarPanel # yazıldığı fonksiyon.
    calendarPanel = ct.CTkFrame(master= root, width = 802, height = 592, corner_radius= 0)
    calendarPanel.place(x = 290, y = 50)

    dateNow = datetime(currentYear,currentMonth,1,1,1,1)
    tS = dateNow.timestamp()
    dateTime = datetime.fromtimestamp(tS)
    fD = dayOfWeek[dateTime.strftime('%A')]

    sayac = 1
    limit1 = 500
    limit2 = 500
  
    if (currentMonth-1) == 2:  #Ayların gün sayısına göre sorunsuz şekilde takvime eklenmesi için kullanılan if else bloğu.
        if (currentYear%4)==0:
            sayac = 29-fD+2
            limit1 = 29
        else:
            sayac = 28-fD+2
            limit1 = 28
    elif (currentMonth-1) in exceptions:
        sayac = 30-fD+2
        limit1 = 30
    else:
        sayac = 31-fD+2
        limit1 = 31

    if (currentMonth) == 2:
        if (currentYear%4)==0:
            limit2 = 29
        else:
            limit2 = 28
    elif (currentMonth) in exceptions:
        limit2 = 30
    else:
        limit2 = 31

    sayac2 = 2
    yazi = []
    id = 0
    esik = False

    for x in range (1, 7, 1): #6x7 şeklinde günlerin takvime eklenmesi.
        yPos = 4 + ((x-1) * 98)
        for i in range (1, 8, 1):
            if sayac == limit1+1:
                sayac = 1
                sayac2 = sayac2 - 1
                limit1 = 100
                esik = True
            if esik:
                if sayac == limit2+1:
                    sayac = 1
                    sayac2 = sayac2 - 1
                    limit2 = 100
            xPos = 4 + ((i-1) * 114)
            yazi.append(str(sayac) +" "+ months[currentMonth-sayac2] +" "+ str(currentYear))
            calendarButtons.append(ct.CTkButton(master = calendarPanel, fg_color= ("#eeefff", "blue"), hover_color= "#fffeff",text = yazi[id], text_color="#555555", anchor="nw" ,corner_radius= 0, width = 110, height = 94, command=lambda c=id: openCreateEventPanel(calendarButtons[c].cget("text"), calendarButtons[c])))
            calendarButtons[id].place(x=xPos, y=yPos)
            sayac = sayac + 1
            id = id + 1 
        
def openUpcomingEventsPanel(): #Ekranın sol tarafında kalan yaklaşan etkinliklerin gösterildiği panel.
    upcomingEventsLabel = ct.CTkLabel(master = root, text = "1 ay içindeki etkinlikleriniz:").place(x = 70, y = 360)
    global selectedMonthEventsLabel
    selectedMonthEventsLabel = ct.CTkLabel(master= root, text = str(currentYear) +" yılı "+ months[currentMonth-1] + " ayındaki etkinlikleriniz:" )
    selectedMonthEventsLabel.place(x = 40, y = 80)

def textToNumeric(dateText):  # Tarih bilgilerinin üzerinde kontrollerin yapılabilmesi için sayısal değere döndürülmesi fonksiyonu.
    sayac = 0
    day = 0
    year = dateText[-4:]
    dateText=dateText[:-5]
    for letter in dateText:
        if letter == " ":
            day = dateText[:sayac]
            dateText = dateText[sayac+1:]
        sayac = sayac + 1
    month = dateText
    month = (months.index(month))+1
    return int(day), int(month), int(year)

eventButtons = []  #Butonların ve ID'lerinin kaydedildiği list'ler.
eventBIDs = []
eventTMButtons = []
eventIDs = []

def clearEvent(which): # Panellerin güncellenebilmesi için list'lerin sıfırlandığı fonksiyon.
    if which == "tm":
        if len(eventTMButtons)>0:
            for button in eventTMButtons:
                button.destroy()
        eventTMButtons.clear()
        eventIDs.clear()
    elif which == "upc":
        if len(eventButtons)>0:
            for button in eventButtons:
                button.destroy()
        eventButtons.clear()
        eventBIDs.clear()

def eventsThisMonth(): # Seçili olan aydaki etkinlikler paneline, etkinlikleri ekleme fonksiyonu.
    clearEvent("tm")
    tmID = 0
    cur.execute("""SELECT * FROM events WHERE user = (?) AND visible = 1""", (loggedInUser,))
    userEvents = cur.fetchall()
    for event in userEvents:
        day, month, year = textToNumeric(event[5])
        yPos = 110 + len(eventTMButtons)*30
        time = str(event[2])
        time = time[:2]+":"+time[2:]
        if month == currentMonth and year == currentYear: # Etkinlikler seçili olan aydaysa panele eklenmesi.
            eventTMButtons.append(ct.CTkFrame(master= root, width=275, height=25))
            eventTMButtons[tmID].place(x = 10, y= yPos)
            eventName = event[0]
            if len(event[0])>4:
                eventName = str(event[0])[:4]+"..."
            ct.CTkLabel(master= eventTMButtons[tmID], text = event[5] + "-" +time + "-" + eventName).place(x = 5, y=0)
            eventIDs.append(ct.CTkLabel(master= eventTMButtons[tmID], text = event[7]))
            ct.CTkButton(master= eventTMButtons[tmID], text = "Sil", command=lambda c=tmID:deleteEventPanel(eventIDs[c].cget("text"),eventName,event[5]), height=20,width=20).place(x=180, y=2.25)
            ct.CTkButton(master= eventTMButtons[tmID], text = "Düzenle", command=lambda c=tmID:editEvent(eventIDs[c].cget("text")), height=20,width=40).place(x=210, y=2.25)
            tmID = tmID + 1

def deleteEventPanel(eventID, eventName, eventDate):  # Etkinlikleri silmek için oluşturulan panel.
    def deleteEvent(eventID):
        cur.execute("""UPDATE events SET visible = 0 WHERE user = (?) AND eventID = (?)""", (loggedInUser, eventID))
        con.commit()
        eventsThisMonth()
        upcomingEvents()
    def innerFunc(conf):
        if conf != -1:
            deleteEvent(conf)
        deleteEventFrame.destroy()

    deleteEventFrame = ct.CTkFrame(master = root, width=300, height = 200)
    deleteEventFrame.place(relx= 0.4, rely=0.3)
    deleteEventLabel = ct.CTkLabel(master = deleteEventFrame, text = eventDate +" tarihindeki " + eventName + " isimli etkinliği\nsilmek istediğine emin misin?").place(x=20, y=15)
    confirmButton = ct.CTkButton(master = deleteEventFrame, text="Evet, sil.", command=lambda:innerFunc(eventID)).place(x=8,y=165)
    backButton = ct.CTkButton(master = deleteEventFrame, text="Hayır, silme.", command=lambda:innerFunc(-1)).place(x=153, y=165)

def updateEvent(args, eventID): #Etkinliklerin veritabanında güncellenmesi.
    cur.execute("""UPDATE events SET eventName = (?), eventDetails =(?), startingTime = (?), endingTime = (?), reminderDay = (?) WHERE user = (?) AND eventID = (?)""", (args[0],args[1],args[2],args[3],args[5],loggedInUser, eventID))
    con.commit()
    eventsThisMonth() #Güncellenen etkinliklerin panellerde de güncellenmesi.
    upcomingEvents()

def editEvent(eventID): # Etkinlikleri güncellemek için açılan ekran.
    def dest():
        createEventPanel.destroy()
    def innerFunc(date, evntNm):  # Kullanıcının girdiği verileri kontrol eden ve hata yoksa güncelleme fonksiyonuna gönderen fonksiyon.
        givenEventName = eventNameEntry.get()
        givenEventsDetail = eventDetailsEntry.get("0.0", "end") or "Detay yok."
        givenStartingTime = str((startingTimeHoursEntry.get() or "12")) + str((startingTimeMinsEntry.get() or "00"))
        givenEndingTime = str((endingTimeHoursEntry.get() or "14")) + str((endingTimeMinsEntry.get() or "00"))
        reminderState = switchVariable.get()
        givenReminder = eventReminderEntry.get()
        
        if givenEventName == '':
            givenEventName = evntNm
        for letter in givenStartingTime:
            if letter not in numbers:
                errorBox(["time"])
                return
        for letter in givenEndingTime:
            if letter not in numbers:
                errorBox(["time"])
                return
        if int(givenStartingTime) > 2359 or int(givenStartingTime) < 0:
            errorBox(["time"])
            return     
        elif int(givenEndingTime) > 2359 or int(givenEndingTime) < 0:
            errorBox(["time"])
            return     
        if int(givenStartingTime) >= int(givenEndingTime):
            errorBox(["time2"])
            return
        if reminderState == "on":
            if givenReminder == '':
                errorBox(["rmndr3"])
                return 
            for letter in givenReminder:
                if letter not in numbers:
                    errorBox(["rmndr2"])
                    return
            if int(givenReminder) < 0:
                errorBox(["rmndr"])
                return
        else:
            givenReminder = -1
        args = [givenEventName, givenEventsDetail, givenStartingTime, givenEndingTime, reminderState, givenReminder]
        updateEvent(args, eventID)
        uploadEvents()
        dest()

    def switch_event(): #Hatırlatıcının kurulup kurulmayacağını kontrol eden ve ona göre girdi alımını açıp kapatan fonksiyon
        if switchVariable.get() == "on":
            eventReminderEntry.configure(state = "normal")
        elif switchVariable.get() == "off":
            eventReminderEntry.configure(state = "disabled")

    global createEventPanel
    createEventPanel = ct.CTkFrame(master = root, width = 300, height = 420)
    createEventPanel.place(relx= 0.4, rely = 0.5, anchor = "w")

    cur.execute("""SELECT * FROM events WHERE user = (?) AND eventID=(?)""", (loggedInUser,eventID))
    userEvents = cur.fetchall() 

    chosenDateLabel = ct.CTkLabel(master = createEventPanel, text = str(userEvents[0][0])).place(x = 100, y = 5)

    eventNameLabel = ct.CTkLabel(master = createEventPanel, text = "Etkinlik Adı", width = 3, height = 3).place(x = 10, y = 35)
    eventNameEntry = ct.CTkEntry(master= createEventPanel, placeholder_text=userEvents[0][0] ,width = 280, height = 40)
    eventNameEntry.place (x = 10, y = 55)

    eventDetailsLabel = ct.CTkLabel(master = createEventPanel, text = "Detayları Gir", width = 10, height = 10).place(x = 10, y = 105)
    eventDetailsEntry = ct.CTkTextbox(master= createEventPanel, width = 280, height = 120)
    eventDetailsEntry.place(x = 10, y = 125)
    eventDetailsEntry.insert("0.0", userEvents[0][1])

    stTime = str(userEvents[0][2])
    stTime2 = stTime[2:]
    stTime = stTime[:2]
    stratingTimeLabel = ct.CTkLabel(master = createEventPanel, text = "Başlangıç Saati", width = 10, height = 10).place(x = 40, y = 250)
    startingTimeHoursEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= int(stTime), width=30, height = 30)
    startingTimeMinsEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= int(stTime2), width=30, height = 30)
    startingTimeDotsLabel = ct.CTkLabel(master = createEventPanel, text = ":", width = 10, height = 10).place(x = 75, y = 276)
    startingTimeHoursEntry.place(x=45, y = 270)
    startingTimeMinsEntry.place(x=85, y = 270)

    endTime = str(userEvents[0][3])
    endTime2 = endTime[2:]
    endTime = endTime[:2]
    endingTimeLabel  = ct.CTkLabel(master = createEventPanel, text = "Bitiş Saati", width = 10, height = 10).place(x = 190, y = 250)
    endingTimeHoursEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= int(endTime), width=30, height = 30)
    endingTimeMinsEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= int(endTime2), width=30, height = 30)
    endingTimeDotsLabel = ct.CTkLabel(master = createEventPanel, text = ":", width = 10, height = 10).place(x = 215, y = 276)
    endingTimeHoursEntry.place(x=185, y = 270)
    endingTimeMinsEntry.place(x=225, y = 270)

    switchVariable = ct.StringVar(value="off")
    eventReminderSwitch = ct.CTkSwitch(master = createEventPanel, text="Hatırlatıcı Kur", command=switch_event, variable=switchVariable, onvalue="on", offvalue="off")
    eventReminderSwitch.place(x = 10, y = 300)

    eventReminderLabel = ct.CTkLabel(master = createEventPanel, text = "Kaç gün önceye hatırlatıcı kurmak istersin?").place(x=10, y = 330)
    eventReminderEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= "1", width=30, height = 30, state = "disabled")
    eventReminderEntry.place(x=260, y = 328)

    backButton = ct.CTkButton(master= createEventPanel, text="Geri", width=135, height=40, command = dest).place(x = 13, y = 370)
    createEventButton = ct.CTkButton(master= createEventPanel, text="Kaydet", width=135, height=40, command=lambda:innerFunc(userEvents[0][5],userEvents[0][0])).place(x = 153, y= 370)

def upcomingEvents(): # 1 ay içindeki etkinliklerin tespit edilip panele eklendiği fonksiyon.
    clearEvent("upc")
    cur.execute("""SELECT * FROM events WHERE user = (?) AND visible = 1""", (loggedInUser,))
    userEvents = cur.fetchall()
    eventUPC = 0
    dayNow = datetime.now().day
    monthNow = datetime.now().month
    yearNow = datetime.now().year
    eventButtons.clear()
    for event in userEvents: # Etkinliklerin sayısal olarak tarihlerinin alınması.
        day, month, year = textToNumeric(event[5])
        yPos = 390 + len(eventButtons)*30
        time = str(event[2])
        time = time[:2]+":"+time[2:]
        if year == yearNow: # Etkinliklerin 1 ay içinde olup olmadığının kontrolü ve 1 ay içindeyse ekrana yazdırılmaları.
            if ((month == monthNow) and (day >= dayNow)) or ((month == monthNow-1) and (day>= dayNow)) or ((month == monthNow+1) and (day<= dayNow)):
                eventButtons.append(ct.CTkFrame(master= root, width=275, height=25))
                eventButtons[eventUPC].place(x = 10, y= yPos)
                eventName = event[0]
                if len(event[0])>4:
                    eventName = str(event[0])[:4]+"..."
                ct.CTkLabel(master= eventButtons[eventUPC], text = event[5] + "-" +time + "-" + eventName).place(x = 5, y=0)
                eventBIDs.append(ct.CTkLabel(master= eventButtons[eventUPC], text = event[7]))
                ct.CTkButton(master= eventButtons[eventUPC], text = "Sil", command=lambda c=eventUPC:deleteEventPanel(eventBIDs[c].cget("text"),eventName,event[5]), height=20,width=20).place(x=180, y=2.25)
                ct.CTkButton(master= eventButtons[eventUPC], text = "Düzenle", command=lambda c=eventUPC:editEvent(eventBIDs[c].cget("text")), height=20,width=40).place(x=210, y=2.25)
                eventUPC = eventUPC + 1

def uploadEvents(): # Oluşturulan yeni etkinliklerin sapdaki büyük takvimde günlerine eklenmesi için veritabanından bilgilerin alınması.
    cur.execute("""SELECT * FROM events WHERE user = (?) AND visible = 1""", (loggedInUser,))
    userEvents = cur.fetchall()
    for event in userEvents:
        for button in calendarButtons:
            bttnDate = button.cget("text")
            if event[5] == bttnDate:
                eventCreated(event[0], event[2], button) # Günlere etkinlikleri ekleyen fonksiyonun çağırılması.

def eventCreated(name, time, bttn): # Etkinlikleri ekleyen fonksiyon.
    eventShowFrame = ct.CTkFrame(master=bttn, width=110, height = 25, fg_color="#ff4040", corner_radius=0)
    eventShowFrame.place(x=0, y=25)
    time = str(time)
    time = time[:2]+":"+time[2:]
    eventTimeLabel = ct.CTkLabel(master=eventShowFrame, text = time,height=5).place(x=5, y=4)
    eventNameLabel = ct.CTkLabel(master=eventShowFrame, text = " - "+name,height=5).place(x=40, y=4)

def succesfullyCreateEvent(args, bttn): #Hatasız şekilde oluşturulan etkinliklerin veritabanına eklenmesi işlevini sağlayan fonksiyon.
    eventName = args[0]
    eventDetails = args[1] 
    startingTime = int(args[2])
    endingTime = int(args[3] )
    reminderState = args[4] 
    reminderTime = args[5]
    eventDate = args[6]

    if reminderState == "off":
        givenReminder = -1
    if reminderTime == '':
        reminderTime = -1
    cur.execute("""SELECT * FROM events WHERE user = (?)""", (loggedInUser,)) #Giriş yapan kullanıcının verilerinin alınması.
    userEvents = cur.fetchall()
    currentID = len(userEvents)
    cur.execute("""INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (eventName, eventDetails, startingTime, endingTime, reminderTime, eventDate, loggedInUser, currentID+1, 1))
    con.commit()
    eventCreated(eventName, startingTime, bttn)
    upcomingEvents()
    eventsThisMonth()

def openCreateEventPanel(date, button): #Etkinlik oluşturma ekranı.
    def innerFunc(): #Hataların son kez kontrol edildiği ve hata olmadığı sürece etkinliğin veritabanına ekleneceği fonksiyona gönderilmesi.
        givenEventName = eventNameEntry.get() or -1
        givenEventsDetail = eventDetailsEntry.get("0.0", "end") or "Detay yok."
        givenStartingTime = str((startingTimeHoursEntry.get() or "12")) + str((startingTimeMinsEntry.get() or "00"))
        givenEndingTime = str((endingTimeHoursEntry.get() or "14")) + str((endingTimeMinsEntry.get() or "00"))
        reminderState = switchVariable.get()
        givenReminder = eventReminderEntry.get()
            
        for letter in givenStartingTime:
            if letter not in numbers:
                errorBox(["time"])
                return
        for letter in givenEndingTime:
            if letter not in numbers:
                errorBox(["time"])
                return
        if int(givenStartingTime) > 2359 or int(givenStartingTime) < 0:
            errorBox(["time"])
            return     
        elif int(givenEndingTime) > 2359 or int(givenEndingTime) < 0:
            errorBox(["time"])
            return     
        if int(givenStartingTime) >= int(givenEndingTime):
            errorBox(["time2"])
            return
        if reminderState == "on":
            if givenReminder == '':
                errorBox(["rmndr3"])
                return 
            for letter in givenReminder:
                if letter not in numbers:
                    errorBox(["rmndr2"])
                    return
            if int(givenReminder) < 0:
                errorBox(["rmndr"])
                return
        args = [givenEventName, givenEventsDetail, givenStartingTime, givenEndingTime, reminderState, givenReminder, date]
        succesfullyCreateEvent(args, button) 
        eventCreateBack()

    for bttn in calendarButtons: #Arkaplandaki butonların tıklanmaya kapatılması.
        bttn.configure(state = "disabled")

    def switch_event(): # Hatırlatıcı kurulup kurulmayacağını kontrol eden fonksiyon. 
        if switchVariable.get() == "on":
            eventReminderEntry.configure(state = "normal")
        elif switchVariable.get() == "off":
            eventReminderEntry.configure(state = "disabled")

    global createEventPanel
    createEventPanel = ct.CTkFrame(master = root, width = 300, height = 420)
    createEventPanel.place(relx= 0.4, rely = 0.5, anchor = "w")

    chosenDateLabel = ct.CTkLabel(master = createEventPanel, text = str(date)).place(x = 100, y = 5)

    eventNameLabel = ct.CTkLabel(master = createEventPanel, text = "Etkinlik Adı", width = 3, height = 3).place(x = 10, y = 35)
    eventNameEntry = ct.CTkEntry(master= createEventPanel, width = 280, height = 40)
    eventNameEntry.place (x = 10, y = 55)

    eventDetailsLabel = ct.CTkLabel(master = createEventPanel, text = "Detayları Gir", width = 10, height = 10).place(x = 10, y = 105)
    eventDetailsEntry = ct.CTkTextbox(master= createEventPanel, width = 280, height = 120)
    eventDetailsEntry.place(x = 10, y = 125)

    stratingTimeLabel = ct.CTkLabel(master = createEventPanel, text = "Başlangıç Saati", width = 10, height = 10).place(x = 40, y = 250)
    startingTimeHoursEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= "12", width=30, height = 30)
    startingTimeMinsEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= "00", width=30, height = 30)
    startingTimeDotsLabel = ct.CTkLabel(master = createEventPanel, text = ":", width = 10, height = 10).place(x = 75, y = 276)
    startingTimeHoursEntry.place(x=45, y = 270)
    startingTimeMinsEntry.place(x=85, y = 270)

    endingTimeLabel  = ct.CTkLabel(master = createEventPanel, text = "Bitiş Saati", width = 10, height = 10).place(x = 190, y = 250)
    endingTimeHoursEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= "14", width=30, height = 30)
    endingTimeMinsEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= "00", width=30, height = 30)
    endingTimeDotsLabel = ct.CTkLabel(master = createEventPanel, text = ":", width = 10, height = 10).place(x = 215, y = 276)
    endingTimeHoursEntry.place(x=185, y = 270)
    endingTimeMinsEntry.place(x=225, y = 270)

    switchVariable = ct.StringVar(value="off")
    eventReminderSwitch = ct.CTkSwitch(master = createEventPanel, text="Hatırlatıcı Kur", command=switch_event, variable=switchVariable, onvalue="on", offvalue="off")
    eventReminderSwitch.place(x = 10, y = 300)

    eventReminderLabel = ct.CTkLabel(master = createEventPanel, text = "Kaç gün önceye hatırlatıcı kurmak istersin?").place(x=10, y = 330)
    eventReminderEntry = ct.CTkEntry(master = createEventPanel, placeholder_text= "1", width=30, height = 30, state = "disabled")
    eventReminderEntry.place(x=260, y = 328)

    backButton = ct.CTkButton(master= createEventPanel, text="Geri", width=135, height=40, command = eventCreateBack).place(x = 13, y = 370)
    createEventButton = ct.CTkButton(master= createEventPanel, text="Oluştur", width=135, height=40, command=innerFunc).place(x = 153, y= 370)
    
def eventCreateBack(): #Etkinliklerin sorunsuz şekilde oluşturulmasından sonra butonların kullanıma açılması.
    createEventPanel.destroy()
    for bttn in calendarButtons:
        bttn.configure(state = "normal")

def printDate(bttn): #Seçili olan ayın değiştirildiği fonksiyon.

    if bttn == "p":
        if currentMonth > 1:                    #Kullanıcının bastığı butona göre bir önceki veya sonraki aya gitmesi ve ocak/aralık
            currentMonth = currentMonth - 1     #aylarında oluşabilecek sorunların çözümü.
        elif currentMonth == 1:
            currentMonth = 12
            currentYear = currentYear - 1
    elif bttn == "n":
        if currentMonth < 12:
            currentMonth = currentMonth + 1
        elif currentMonth == 12:
            currentMonth = 1
            currentYear = currentYear + 1

    monthPanel.destroy()                #Kullanıcı seçili ayı değiştirdiğinde panellerin yeniden yüklenebilmesi için
    openMonthPanel()                    #gerekli fonksiyonların çağırılması ve açık olan panellerin kapatılması.
    calendarButtons.clear()
    calendarPanel.destroy()
    openCalendarPanel()
    selectedMonthEventsLabel.destroy()
    openUpcomingEventsPanel()
    uploadEvents()
    eventsThisMonth()

def succesfulLogin():                   #Kullanıcı başarılı şekilde giriş yaptığında takvim ekranının açılması.
    openCalendarPanel()
    openUpcomingEventsPanel()
    openMainPanel()
    openMonthPanel()
    uploadEvents()
    upcomingEvents()
    eventsThisMonth()

openLoginPanel()

root.mainloop()
