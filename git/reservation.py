import pymysql, datetime, sys

DS = ["01A", "01B", "01C", "01D", "01E", "01F", "01G", "01H", "01I", "01J", "02A", "02B", "02C", "02D", "02E", "02F", "02G", "02H", "02I", "02J",
      "03A", "03B", "03C", "03D", "03E", "03F", "03G", "03H", "03I", "03J", "04A", "04B", "04C", "04D", "04E", "04F", "04G", "04H", "04I", "04J",
      "05A", "05B", "05C", "05D", "05E", "05F", "05G", "05H", "05I", "05J", "06A", "06B", "06C", "06D", "06E", "06F", "06G", "06H", "06I", "06J",
      "07A", "07B", "07C", "07D", "07E", "07F", "07G", "07H", "07I", "07J", "08A", "08B", "08C", "08D", "08E", "08F", "08G", "08H", "08I", "08J",
      "09A", "09B", "09C", "09D", "09E", "09F", "09G", "09H", "09I", "09J", "10A", "10B", "10C", "10D", "10E", "10F", "10G", "10H", "10I", "10J",
      "11A", "11B", "11C", "11D", "11E", "11F", "11G", "11H", "11I", "11J", "12A", "12B", "12C", "12D", "12E", "12F", "12G", "12H", "12I", "12J",
      "13A", "13B", "13C", "13D", "13E", "13F", "13G", "13H", "13I", "13J", "14A", "14B", "14C", "14D", "14E", "14F", "14G", "14H", "14I", "14J"]

MS = ["01A", "01B", "01C", "01D", "01E", "01F", "01G", "01H", "02A", "02B", "02C", "02D", "02E", "02F", "02G", "02H",
      "03A", "03B", "03C", "03D", "03E", "03F", "03G", "03H", "04A", "04B", "04C", "04D", "04E", "04F", "04G", "04H",
      "05A", "05B", "05C", "05D", "05E", "05F", "05G", "05H", "06A", "06B", "06C", "06D", "06E", "06F", "06G", "06H",
      "07A", "07B", "07C", "07D", "07E", "07F", "07G", "07H", "08A", "08B", "08C", "08D", "08E", "08F", "08G", "08H",
      "09A", "09B", "09C", "09D", "09E", "09F", "09G", "09H", "10A", "10B", "10C", "10D", "10E", "10F", "10G", "10H"]


def connection():
    """Połączenie z bazą w pymysql"""
    try:
        mydb = pymysql.connect(user = 'root', password = '', host = '127.0.0.1', db = 'kino', charset='utf8')
        cur = mydb.cursor()
        return cur
    except pymysql.Error:
        print("There was a problem in connecting to the database.  Please ensure that the 'kino' database exists on the local host system.")
        raise pymysql.Error
    except pymysql.Warning:
        pass

def date_form(day):
    """Zmiana nazwenictwa na polskie"""
    new_day = ""
    if day == "Monday":
        new_day = "Poniedziałek"
    elif day == "Tuesday":
        new_day = "Wtorek"
    elif day == "Wednesday":
        new_day = "Środa"
    elif day == "Thursday":
        new_day = "Czwartek"
    elif day == "Friday":
        new_day = "Piątek"
    elif day == "Saturday":
        new_day = "Sobota"
    elif day == "Sunday":
        new_day = "Niedziela"
    return new_day

def movie():
    """Wybór filmu oraz zwrot jego id"""
    day_no = 0
    movie_no = 0
    cursor = connection()
    statement = "SELECT DISTINCT DATE(data), DATE_FORMAT(data, '%W') FROM filmy"
    cursor.execute(statement)
    dates = cursor.fetchall()
    for i in range(0, len(dates)):
        print("%s. %s (%s)" %(i+1, dates[i][0], date_form(dates[i][1])))  #dates[i][1])
    while not 0<day_no<=len(dates):
        day_no = int(input("Wybierz dzień tygodnia (numer): "))
    day = dates[day_no-1][0]
    statement = "SELECT tytul, sala, DATE_FORMAT(data, '%s'), ROUND(TIME_TO_SEC(czas)/60), id_film FROM filmy WHERE data LIKE '%s'" %('%H:%i', "%" + str(day) + "%")
    cursor.execute(statement)
    movies = cursor.fetchall()
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ["Nr", "Film", "Sala", "Początek", "Czas trwania (min)"]
    x.align["Film"] = "l"
    for i in range(0,len(movies)):
        x.add_row([i+1, movies[i][0], movies[i][1], movies[i][2], movies[i][3]])
    print(x.get_string())
    while not 0<movie_no<=len(movies):
        movie_no = int(input("Wybierz film (numer): "))
    return movies[movie_no-1][4]
          
def current_sats(seats_list, sold_seats, reserved_seats):
    """Podmiana miejsc sprzedanych i zarezerwowanych"""
    for i in range(0, len(seats_list)):
        if seats_list[i] in sold_seats:
            seats_list[i] = " X "
        elif seats_list[i] in reserved_seats:
            seats_list[i] = " O "
    return seats_list    
    

def seats():
    """Wydruk dostępnych miejsc na planie całej sali"""
    reserved_seats = []
    sold_seats = []
    seats_list = []
    j = 0
    cursor = connection()
    movie_id = movie()
    statement = "SELECT miejsce, status FROM sprzedaz WHERE id_filmu = '%s'" %(movie_id)
    cursor.execute(statement)
    seats= cursor.fetchall()
    for i in range(0, len(seats)):
        if seats[i][1] == "S":
            sold_seats.append(seats[i][0])
        elif seats[i][1] == "R":
            reserved_seats.append(seats[i][0])
    statement = "SELECT sala FROM filmy WHERE id_film = %s" %(movie_id)
    cursor.execute(statement)
    cinema_hall = cursor.fetchall()
    if cinema_hall[0][0] == "mała":
        seats_list = MS[:]
        current_sats(seats_list, sold_seats, reserved_seats)
        while j < len(seats_list):
            print(seats_list[j], seats_list[j+1], seats_list[j+2], seats_list[j+3], seats_list[j+4], seats_list[j+5], seats_list[j+6], seats_list[j+7])
            j = j + 8
        print("\nX - miejsce sprzedane     O - miejsce zarezerwowane")
    elif cinema_hall[0][0] == "duża":
        seats_list = DS[:]
        current_sats(seats_list, sold_seats, reserved_seats)
        while j < len(seats_list):
            print(seats_list[j], seats_list[j+1], seats_list[j+2], seats_list[j+3], seats_list[j+4], seats_list[j+5], seats_list[j+6], seats_list[j+7], seats_list[j+8], seats_list[j+9])             
            j = j + 10
        print("\nX - miejsce sprzedane     O - miejsce zarezerwowane")
    return seats_list, movie_id
     
def available_place(seats_list):
    """Sprawdzenie dostępności miejsca"""
    place = ""
    while place not in seats_list:
        place = input("Podaj miejsce: ").upper()
    return place

def reservation():
    """Rezerwacja lub sprzedaż miejsca"""
    status = ""
    ticket = ""
    cursor = connection()
    print("Wybierz datę i film: \n")
    seats_list, movie_id = seats()
    i = int(input("\nPodaj ilość miejsc (max 8): "))
    statement = "SELECT nr_rezerwacji FROM sprzedaz ORDER BY nr_rezerwacji DESC LIMIT 1"
    cursor.execute(statement)
    reservation_no = cursor.fetchall()
    reservation_no = reservation_no[0][0] + 1   #numer rezerwacji wspólny dla wszystkich jednorazowo zakupionych biletów
    reservation_date = datetime.datetime.now()
    while status != "R" and status != "S":
        status = input("Rezerwacja czy sprzedaż (R/S): ").upper()
    cursor = connection()
    f = open("bilet" + str(reservation_no)+".txt","w")  #utworzenie pliku zewnętrznego z tranzakcją
    f.write("Nr rezerwacji: %s" %reservation_no)
    f.write("\tStatus sprzedaży: %s" %status)
    for j in range(0,i):
        place = available_place(seats_list)
        ticket = ""
        while ticket != "N" and ticket != "U":
            ticket = input("Bilet normalny czy uglowy (N/U): ").upper()
            f.write("\nMiejsce: %s" %place)
            f.write("\tRodzaj biletu: %s" %ticket)        
        mydb = pymysql.connect(user = 'root', password = '', host = '127.0.0.1', db = 'kino', charset='utf8')
        cursor = mydb.cursor()
        statement = "INSERT INTO sprzedaz VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s')" %(reservation_no, place, movie_id, status, reservation_date, ticket)
        cursor.execute(statement)
        mydb.commit()
        mydb.close()
    print("Dokonano tranzakcji nr: " + str(reservation_no))
    f.close()

def status_change():
    """Zmiana statusu z rezerwacji na sprzedaż"""
    reservation_no = ""
    choice = ""
    reservation_list = []
    cursor = connection()  
    statement = "SELECT DISTINCT nr_rezerwacji FROM sprzedaz"
    cursor.execute(statement)
    reservations = cursor.fetchall()
    for i in range(0, len(reservations)):
        reservation_list.append(reservations[i][0])
    while reservation_no not in reservation_list:
        reservation_no = int(input("Podaj numer rezerwacji: "))
    mydb = pymysql.connect(user = 'root', password = '', host = '127.0.0.1', db = 'kino', charset='utf8')
    cursor = mydb.cursor()
    statement = "UPDATE sprzedaz SET status = 'S' WHERE nr_rezerwacji = %s" %(reservation_no)
    cursor.execute(statement)
    mydb.commit()
    mydb.close()
    print("Status rezerwacji nr %s został zmieniony na SPRZEDANE" %(reservation_no))

def show_details():
    """Umożliwia podejrzenie rezerwacji po numerze"""
    cursor = connection()
    reservation_no = int(input("Podaj numer rezerwacji: "))
    statement = "SELECT s.nr_rezerwacji, s.id_biletu, s.miejsce, s.id_filmu, s.rodzaj_biletu, s.status, f.id_film, f.tytul, f.data FROM sprzedaz AS s, filmy AS f WHERE s.id_filmu = f.id_film AND nr_rezerwacji = %s" %(reservation_no)
    cursor.execute(statement)
    reservation_details = cursor.fetchall()
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ["Numer rezerwacji", "Numer biletu", "Miejsce", "Rodzaj biletu", "Status", "Film", "Projekcja"]
    for i in range(0, len(reservation_details)):
        x.add_row([reservation_details[i][0], reservation_details[i][1], reservation_details[i][2], reservation_details[i][4], reservation_details[i][5], reservation_details[i][7], reservation_details[i][8]])
    print(x.get_string())    
  
def show_dates():
    """Możliwość podejrzenia dat wyświetlenia konkretnego filmu"""
    cursor = connection()
    title = input("Podaj tytuł filmu: ").upper()
    statement = "SELECT data, sala, tytul FROM filmy WHERE tytul LIKE '%s'" %("%" + str(title) + "%")
    cursor.execute(statement)
    date_list = cursor.fetchall()
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ["Tytuł", "Data", "SALA"]
    for i in range(0, len(date_list)):
        x.add_row([date_list[i][2], date_list[i][0], date_list[i][1]])
    print(x.get_string())    
    
def menu():
    print("""
    Menu:\n
    1 - sprawdź terminy seansów dla wybranego filmu
    2 - sprawdź szczegoły wybranej rezerwacji/sprzedaży
    3 - zmien status z rezerwacja na sprzedaż 
    4 - dokonaj sprzedaży/rezerwacji 
    5 - zakończ
    
    """)

    menu_choice = int(input("Wprowadź interesującą Cię opcje: "))
    return menu_choice

def main():
    menu_choice = 0
    while menu_choice != 5:
        menu_choice = menu()   
        if menu_choice == 1:
            show_dates()         
        elif menu_choice == 2:
            show_details()
        elif menu_choice == 3:
            status_change()
        elif menu_choice == 4:
            reservation() 
        else:
            print("Koniec")

main()





