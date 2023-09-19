import socket
import os
import threading
import time
import datetime
import pickle
import importlib.util
import subprocess
import ctypes


colorama_module = importlib.util.find_spec("colorama")
pandas_module = importlib.util.find_spec("pandas")

if colorama_module == None:
    while True:
        os.system("cls")
        print("\n Could'n find the 'colorama' module in your computer.\n Please connect your computer to internet and type 'ok' to proceed or 'no' to exit.")
        choice = input("\n > ")
        if choice == "ok":
            try:
               subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', 'colorama']) 
            except:
                input("Couldn't install the colorama module. check your connection.")
                continue
            
            try:
                colorama_module = importlib.util.find_spec("colorama")

                from colorama import Fore
                from colorama import Back
                from colorama import Style
                
                break

            except:
                print(f"Somthing went wrong. ")
                continue
        elif choice == "no":
            os.sys.exit()

else:
    from colorama import Fore
    from colorama import Back
    from colorama import Style



if pandas_module == None:
    while True:
        os.system("cls")
        print("\n Could'n find the 'pandas' module in your computer.\n Please connect your computer to internet and type 'ok' to proceed or 'no' to exit.")
        choice = input("\n > ")
        if choice == "ok":
            try:
                subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', 'pandas'])
            except:
                input("Couldn't install the pandas module. check your connection.")
                continue
            
            try:
                pandas_module = importlib.util.find_spec("pandas")
                import pandas
                break

            except:
                input(f"Somthing went wrong. ")
                continue

        elif choice == "no":
            os.sys.exit()


else:
    import pandas


HEADER = 64
FORMAT = "utf-8"

COLS = 90
LINES = 47
LINES_S = 35
os.system(f'mode CON: cols={COLS} lines={LINES_S}')


DATE = datetime.date.today()

def show_banner():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    os.system("cls")


    banner = '''
        
         ██████████ █████ █████              ███████████   ███      █████        
        ░░███░░░░░█░░███ ░░███              ░░███░░░░░███          ░░███         
         ░███  █ ░  ░░███ ███    ██████      ░███    ░███ ████   ███████  ███████ 
         ░██████     ░░█████    ░░░░░███     ░██████████ ░░███  ███░░███  ███░░  
         ░███░░█      ███░███    ███████     ░███░░░░░███ ░███ ░███ ░███    ███ 
         ░███ ░   █  ███ ░░███  ███░░███     ░███    ░███ ░███ ░███ ░███    ░░███
         ██████████ █████ █████░░██████      ███████████  █████░░████████ ███████ 
     
    '''
    print(Fore.LIGHTCYAN_EX+banner+Fore.RESET)
    print(" EXaBids Server v2.0 ".center(COLS,"░"))
    print()
    print(f"    {current_date}"+ " "*(COLS-26) + f"{current_time}")
    print("")



# Send messages to the client applications
def send_msg(con, msg):
    global file_name
    try:
        msg = msg.encode(FORMAT)
        msg_len = str( len(msg) ).encode(FORMAT) # Get the length of message and encode it in utf-8
        msg_len += b' ' * (HEADER - len(msg_len)) # Add spaces(' ') to msg_len untill it gets HEADER size
        con.send(msg_len)
        con.send(msg)
    except:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}]  Message sending error\n")


# Recieve messages from the client applications
def recv_msg(con):
    global file_name
    try:
        msg_len = int(con.recv(HEADER).decode(FORMAT))
        msg = con.recv(msg_len).decode(FORMAT)
        # print("Response from client > "+msg)
        return msg
    except:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] A user refused the connection  \n")
        exit()


def send_data(con, data):
    global file_name
    try:
        data = pickle.dumps(data)
        data_len = str( len(data) ).encode(FORMAT)
        data_len += b' ' * (HEADER - len(data_len))
        con.send(data_len)
        con.send(data)
    except:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Connection Refused ({user})\n")
        exit()



def print_data():
    global start_datetime
    global end_datetime
    global end_datetime_int
    global file_name
    global current_datetime
    global current_datetime_int
    

    while True:
        current_datetime = datetime.datetime.now()
        current_datetime_int = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        end_datetime_int = int(datetime.datetime.strftime(end_datetime, "%Y%m%d%H%M%S"))
        
        
        show_banner()
        if current_datetime < start_datetime:
            time_difference = start_datetime - current_datetime
            if time_difference.seconds < 60:
                print(Fore.BLACK+Back.LIGHTGREEN_EX+" Time To Start ".center(COLS) +Fore.RESET+Back.RESET)
            else:
                print(Fore.BLACK+Back.WHITE+" Time To Start ".center(COLS) +Fore.RESET+Back.RESET)
            print("\n\t\t", time_difference.days, "days  :: ", time_difference.seconds//3600, "hours  :: ", (time_difference.seconds//60)%60, "minutes  :: ", time_difference.seconds%60, "seconds")

        elif (current_datetime >= start_datetime) and (current_datetime <= end_datetime):
            time_difference = end_datetime - current_datetime
            if time_difference.seconds < 60:
                print(Fore.WHITE+Back.RED+" Time To End ".center(COLS) +Fore.RESET+Back.RESET)
            else:
                print(Fore.BLACK+Back.WHITE+" Time To End ".center(COLS) +Fore.RESET+Back.RESET)
            print("\n\t\t", time_difference.days, "days  :: ", time_difference.seconds//3600, "hours  :: ", (time_difference.seconds//60)%60, "minutes  :: ", time_difference.seconds%60, "seconds")

        elif current_datetime > end_datetime:
            time_difference = current_datetime - end_datetime
            print(Fore.BLACK+Back.WHITE+" Ended ".center(COLS) +Fore.RESET+Back.RESET)
            print("\n\t\t", time_difference.days, "days  :: ", time_difference.seconds//3600, "hours  :: ", (time_difference.seconds//60)%60, "minutes  :: ", time_difference.seconds%60, "seconds")

        print()
        print(Back.LIGHTBLACK_EX + Fore.BLACK + Style.DIM +" LOG ".center(COLS,"░")  + Style.RESET_ALL+Back.RESET+Fore.RESET )

        with open(file_name, "r+" ) as alert_file:
            alerts = alert_file.read().split("\n")
        
        for alert in alerts[:-26:-1]:
            print(" "+alert)
        
        time.sleep(1)




##############################################################  CLIENT  #############################################################


def start_client():
    global file_name
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    try:
        HOST = socket.gethostbyname(socket.gethostname()) # Get the IP address of computer
        PORT = 2021
    
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating the socket
        server.bind((HOST,PORT)) # Binding the connection
        with lock:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Server is strating as {HOST}\n")

    except socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Binding error \n"+ str(err_msg) + "\n\nRetrying binding...\n")
        server.bind((HOST,PORT))

    try:
        server.listen() # Listening for new connections
        with lock:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Server is listening for clients on PORT {PORT}\n")

    except socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Listening error {str(err_msg)}\n")

    try:
        while True:
            con, addr = server.accept()
            client_ctrl_thread = threading.Thread(target=handle_clients, args=(con, addr))
            # Create new thread and call to the handle_clients function
            client_ctrl_thread.start()

    except  socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Can't accept the connections\n")



def authenticate_clients(con, addr):
    global client_user_pass_data
    global file_name
    global start_datetime
    global end_datetime

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    with open("client_userpass.pickle","rb") as user_data_file:
        client_user_pass_data = pickle.load(user_data_file)

    send_msg(con, "authentication-Required")
    response = recv_msg(con)
    print(response)

    if response == "sign-in": 
        try:
            send_msg(con, "request-username")
            user = recv_msg(con)

            while True:
                if user not in client_user_pass_data.keys(): # Check whether the username is a true one
                    send_msg(con, "invalid-username")
                    user = recv_msg(con)
            
                else:
                    send_msg(con, "request-password")
                    while True:
                        passwd = recv_msg(con)
                        if passwd != client_user_pass_data[user]: # Check whether the password is correct acording to the username
                            send_msg(con, "invalid-password")
                        else:
                            send_msg(con, "sign-in-successful")
                            send_msg(con, start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                            send_msg(con, end_datetime.strftime("%Y-%m-%d %H:%M:%S"))

                            with open(file_name, "a+") as alert_file:
                                alert_file.write(f"\t[{current_time}] Client connected :: {user}\n")
                            return ['sign-in', user, passwd]
                            
        except:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}]  Sign-in error\n")


    elif response == "sign-up":
        try:

            send_msg(con, "request-username")
            while True:
                user = recv_msg(con)
                if user in client_user_pass_data.keys():
                    send_msg(con, "username-exist")

                else:
                    send_msg(con, "request-password")
                    passwd = recv_msg(con)

                    if (user and passwd):
                        client_user_pass_data[user] = passwd
                        with open("client_userpass.pickle","wb") as user_data_file:
                            pickle.dump(client_user_pass_data, user_data_file)
                        
                        send_msg(con, "sign-up-successful")
                        send_msg(con, start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        send_msg(con, end_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        with open(file_name, "a+") as alert_file:
                            alert_file.write(f"\t[{current_time}] New client joined ({user})\n")

                        return ['sign-up', user, passwd]
                    
        except:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}]  Sign-up error\n")



def client_realtime_data(con, addr, user, window, ctrl_data, client_alerts):
    global stocks
    global kill
    global start_datetime
    global start_datetime_int
    global end_datetime
    global end_datetime_int
    global current_datetime
    global current_datetime_int
    global file_name
    global stock_subscribers
    global stock_updates

    

    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        # for i in range(len(stocks['END TIME'][:])) :
        #     stock_time_difference = stocks['END TIME'][i] - datetime.datetime.now()
        #     stocks['END TIME'][i] =    


        if current_datetime_int == start_datetime_int:
            client_alerts.append(f"[{current_time}] Auction started !")
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Auction started !\n")

        elif current_datetime_int == end_datetime_int:
            client_alerts.append(f"[{current_time}] Auction ended !")
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Auction ended !\n")

        for symbol in stock_subscribers.keys():
            if user in stock_subscribers[symbol]:
                for stock_update_msg in stock_updates[symbol]:
                    if stock_update_msg not in client_alerts:
                        client_alerts.append(stock_update_msg)
        
        if kill[addr] == 0:

            if window == 1:
                temp_stocks = stocks.sort_values(ctrl_data[0], ascending=ctrl_data[1]).head(5).to_dict("tight")
                temp_client_alerts = client_alerts[:-6:-1]


            elif window == 2:
                temp_stocks = []
                for sym in ctrl_data:
                    temp_stocks.append(stocks.loc[stocks["Symbol"] == sym])
                temp_stocks = pandas.concat(temp_stocks).head(5).to_dict("tight")
                temp_client_alerts = client_alerts[:-14:-1]

            elif window == 3:
                temp_client_alerts = []
                temp_stocks = []

            st_en_cur_time = [start_datetime, end_datetime, current_time]
            data = [temp_stocks, st_en_cur_time, window, temp_client_alerts]
            send_data(con, data)
            time.sleep(1)

        elif kill[addr] == 1:
            return



def handle_clients(con, addr):
    global kill
    global stocks
    global file_name
    global current_datetime
    global current_datetime_int
    global end_datetime
    global end_datetime_int
    client_alerts = []
    session = authenticate_clients(con, addr)
    user = session[1]
    kill[addr] = 0
    
    
    if session:

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        client_alerts.append(f"[{current_time}] Auction start time : {start_datetime}")
        client_alerts.append(f"[{current_time}] Auction end time : {end_datetime}")


        ctrl_data = ["Profit", False]
        window = 1
        client_realtime_data_thread = threading.Thread(target=client_realtime_data, args=(con, addr, user, window, ctrl_data, client_alerts))
        client_realtime_data_thread.start()


        while True:
            msg = recv_msg(con)
            msg = msg.split(",")
            command = msg[0]
            user = msg[1]
            command = command.split()

            if len(command) > 0:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                if command[0] == "info":

                    if command[1] == "highest":
                        window = 1
                        if command[2] == "price":
                            ctrl_data = ["Price",False]
                        elif command[2] == "profit":
                            ctrl_data = ["Profit", False]
                        else:
                            client_alerts.append(f'[{current_time}] Invalid Command! <{command[2]}>. Type "help" to get help menu.')

                    elif command[1] == "lowest":
                        window = 1
                        if command[2] == "price":
                            ctrl_data = ["Price",True]
                        elif command[2] == "profit":
                            ctrl_data = ["Profit", True]
                        else:
                            client_alerts.append(f'[{current_time}] Invalid Command! <{command[2]}>. Type "help" to get help menu.')


                    elif command[1] == "stock":
                        if len(command) > 2:
                            ctrl_data = command[2:]
                            window = 2
                    else:
                        client_alerts.append(f'[{current_time}] Invalid Command! <{command[1]}>. Type "help" to get help menu.')                                            
                
                elif command[0] == "help":
                    window = 3

                elif command[0] == "SUB":
                    for symbol in command[1:]:
                        if symbol in list(stocks["Symbol"]):
                            stock_subscribers[symbol].append(user)
                            client_alerts.append(f'[{current_time}] Successfully Subscribed! {symbol}')
                        else:
                            client_alerts.append(f'[{current_time}] Invalid Code {symbol}')




                elif command[0] in list(stocks["Symbol"]):
                    current_datetime = datetime.datetime.now()
                    current_datetime_int = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    
                    if (current_datetime_int >= start_datetime_int ) and (current_datetime_int <= end_datetime_int):
                        
                        if len(command) > 1:

                            stock_time = stocks.loc[stocks["Symbol"] == command[0], "END TIME"].to_string().split('   ')[1]
                            stock_time = datetime.datetime.strptime(stock_time, "%Y-%m-%d %H:%M:%S")
                            stock_time_difference = stock_time - datetime.datetime.now()

                            if  stock_time_difference.days >= 0 :
                                if (float(command[1]) > stocks.loc[stocks["Symbol"] == command[0], "Price"]).bool():

                                    stocks.loc[stocks["Symbol"] == command[0], "Price"] = float(command[1])
                                    
                                    client_alerts.append(f'[{current_time}] Successfully Bided! {command[0]} {command[1]}')
                                    
                                    with open(file_name,"a+") as alert_file:
                                        alert_file.write(f'\t[{current_time}] {user} Successfully Bided! {command[0]} {command[1]}\n')

                                    stock_updates[command[0]].append(f'[{current_time}] {command[0]} BID {command[1]}')



                                    if stock_time_difference.seconds <= 60:
                                        stocks.loc[stocks["Symbol"] == command[0], "END TIME"] = end_datetime + datetime.timedelta(seconds=60)
                                        client_alerts.append(f"[{current_time}] {command[0]} stock time extended in 60sec. Endtime : {end_datetime}")

                                        with open(file_name, "a+") as alert_file:
                                            alert_file.write(f"\t[{current_time}] {command[0]} stock time extended in 60sec. Endtime : {end_datetime}\n")


                                        end_datetime = end_datetime + datetime.timedelta(seconds=60)
                                        client_alerts.append(f"[{current_time}] Auction time extended in 60sec. Endtime : {end_datetime}")

                                        with open(file_name, "a+") as alert_file:
                                            alert_file.write(f"\t[{current_time}] Auction time extended in 60sec. Endtime : {end_datetime}\n")


                                else:
                                    client_alerts.append(f'[{current_time}] Invalid Bid {command[0]} {command[1]}')

                            else:
                                client_alerts.append(f'[{current_time}] Blocked! Bidding ended for "{command[0]}" at {end_datetime} ')
                        else:
                            client_alerts.append(f'[{current_time}] Invalid Bid {command[0]} ')
                    
                    elif current_datetime_int < start_datetime_int :
                        client_alerts.append(f'[{current_time}] Bloked! Auction will start at {start_datetime} ')

                    elif current_datetime_int > end_datetime_int :
                        client_alerts.append(f'[{current_time}] Blocked! Auction ended at {end_datetime} ')


                elif command[0].isupper() :
                    t = time.localtime()
                    client_alerts.append(f'[{current_time}] Invalid Stock Code {command[0]} ')
                
                else:
                    t = time.localtime()
                    client_alerts.append(f'[{current_time}] Invalid Command! <{command[0]}>. Type "help" to get help menu.')                    

            kill[addr] = 1
            client_realtime_data_thread.join()

            kill[addr] = 0
            client_realtime_data_thread = threading.Thread(target=client_realtime_data, args=(con, addr, user, window, ctrl_data, client_alerts))
            client_realtime_data_thread.start()







############################################################# Publishers ##########################################################

def start_publisher():
    global file_name
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    try:
        HOST = socket.gethostbyname(socket.gethostname()) # Get the IP address of computer
        PORT = 2022
        # with open(file_name, "a+") as alert_file:
        #     alert_file.write(f"\t[{current_time}] Server is strating as {HOST}\n")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating the socket
        server.bind((HOST,PORT)) # Binding the connection

    except socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Binding error \n"+ str(err_msg) + "\n\nRetrying binding...\n")
        server.bind((HOST,PORT))

    try:
        server.listen() # Listening for new connections
        with lock:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Server is listening for publishers on PORT {PORT}\n")

    except socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Listening error {str(err_msg)}\n")

    try:
        while True:
            con, addr = server.accept()
            publisher_ctrl_thread = threading.Thread(target=handle_publishers, args=(con, addr))
            # Create new thread and call to the handle_clients function
            publisher_ctrl_thread.start()

    except  socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Can't accept the connections\n")



def authenticate_publishers(con, addr):
    global publisher_user_pass_data
    global file_name
    global start_datetime
    global end_datetime

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    with open("publisher_userpass.pickle","rb") as user_data_file:
        publisher_user_pass_data = pickle.load(user_data_file)

    send_msg(con, "authentication-Required")
    response = recv_msg(con)
    print(response)

    if response == "sign-in": 
        try:
            send_msg(con, "request-username")
            user = recv_msg(con)

            while True:
                if user not in publisher_user_pass_data.keys(): # Check whether the username is a true one
                    send_msg(con, "invalid-username")
                    user = recv_msg(con)
            
                else:
                    send_msg(con, "request-password")
                    while True:
                        passwd = recv_msg(con)
                        if passwd != publisher_user_pass_data[user]: # Check whether the password is correct acording to the username
                            send_msg(con, "invalid-password")
                        else:
                            send_msg(con, "sign-in-successful")
                            send_msg(con, start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                            send_msg(con, end_datetime.strftime("%Y-%m-%d %H:%M:%S"))

                            with open(file_name, "a+") as alert_file:
                                alert_file.write(f"\t[{current_time}] Publisher connected :: {user}\n")
                            return ['sign-in', user, passwd]
                            
        except:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}]  Sign-in error\n")


    elif response == "sign-up":
        try:

            send_msg(con, "request-username")
            while True:
                user = recv_msg(con)
                if user in publisher_user_pass_data.keys():
                    send_msg(con, "username-exist")

                else:
                    send_msg(con, "request-password")
                    passwd = recv_msg(con)

                    if (user and passwd):
                        publisher_user_pass_data[user] = passwd
                        with open("publisher_userpass.pickle","wb") as user_data_file:
                            pickle.dump(publisher_user_pass_data, user_data_file)
                        
                        send_msg(con, "sign-up-successful")
                        send_msg(con, start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        send_msg(con, end_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        with open(file_name, "a+") as alert_file:
                            alert_file.write(f"\t[{current_time}] New publisher joined ({user})\n")

                        return ['sign-up', user, passwd]
                    
        except:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}]  Sign-up error\n")



def publisher_realtime_data(con, addr, user, window, ctrl_data, publisher_alerts):
    global stocks
    global kill
    global start_datetime
    global start_datetime_int
    global end_datetime
    global end_datetime_int
    global current_datetime
    global current_datetime_int
    global file_name
    global stock_subscribers
    global stock_updates
    

    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        # for i in range(len(stocks['END TIME'][:])) :
        #     stock_time_difference = stocks['END TIME'][i] - datetime.datetime.now()
        #     stocks['END TIME'][i] =    


        if current_datetime_int == start_datetime_int:
            publisher_alerts.append(f"[{current_time}] Auction started !")
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Auction started !\n")

        elif current_datetime_int == end_datetime_int:
            publisher_alerts.append(f"[{current_time}] Auction ended !")
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Auction ended !\n")
        
        if kill[addr] == 0:

            if window == 1:
                temp_stocks = stocks.sort_values(ctrl_data[0], ascending=ctrl_data[1]).head(5).to_dict("tight")
                temp_publisher_alerts = publisher_alerts[:-6:-1]


            elif window == 2:
                temp_stocks = []
                for sym in ctrl_data:
                    temp_stocks.append(stocks.loc[stocks["Symbol"] == sym])
                temp_stocks = pandas.concat(temp_stocks).head(5).to_dict("tight")
                temp_publisher_alerts = publisher_alerts[:-14:-1]

            elif window == 3:
                temp_publisher_alerts = []
                temp_stocks = []

            st_en_cur_time = [start_datetime, end_datetime, current_time]
            data = [temp_stocks, st_en_cur_time, window, temp_publisher_alerts]
            send_data(con, data)
            time.sleep(1)

        elif kill[addr] == 1:
            return



def handle_publishers(con, addr):
    global kill
    global stocks
    global file_name
    global current_datetime
    global current_datetime_int
    global end_datetime
    global end_datetime_int
    publisher_alerts = []


    session = authenticate_publishers(con, addr)
    user = session[1]

    kill[addr] = 0
    
    if session:

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        publisher_alerts.append(f"[{current_time}] Auction start time : {start_datetime}")
        publisher_alerts.append(f"[{current_time}] Auction end time : {end_datetime}")

        ctrl_data = ["Profit", False]
        window = 1
        publisher_realtime_data_thread = threading.Thread(target=publisher_realtime_data, args=(con, addr, user, window, ctrl_data, publisher_alerts))
        publisher_realtime_data_thread.start()


        while True:
            msg = recv_msg(con)
            msg = msg.split(",")
            command = msg[0]
            user = msg[1]

            if '"' not in command:
                command = command.split()

            elif command.count('"') == 2:
                command = command.split('"')
                stock_update_msg = command[1]
                security_code = command[2].strip()
                command = command[0].strip().split()

            else:
                publisher_alerts.append(f"[{current_time}] Invalied Syntax!. Use double quotes correctly")


            if len(command) > 0:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                if command[0] == "info":

                    if command[1] == "highest":
                        window = 1
                        if command[2] == "price":
                            ctrl_data = ["Price",False]
                        elif command[2] == "profit":
                            ctrl_data = ["Profit", False]
                        else:
                            publisher_alerts.append(f'[{current_time}] Invalid Command! <{command[2]}>. Type "help" to get help menu.')

                    elif command[1] == "lowest":
                        window = 1
                        if command[2] == "price":
                            ctrl_data = ["Price",True]
                        elif command[2] == "profit":
                            ctrl_data = ["Profit", True]
                        else:
                            publisher_alerts.append(f'[{current_time}] Invalid Command! <{command[2]}>. Type "help" to get help menu.')


                    elif command[1] == "stock":
                        if len(command) > 2:
                            ctrl_data = command[2:]
                            window = 2
                    else:
                        publisher_alerts.append(f'[{current_time}] Invalid Command! <{command[1]}>. Type "help" to get help menu.')                                            
                
                elif command[0] == "help":
                    window = 3


                elif command[0] == "PUB":

                    if command[1] in list(stocks["Symbol"]):
                        current_datetime = datetime.datetime.now()
                        current_datetime_int = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)

                        if (security_code == str(stocks.loc[stocks["Symbol"] == command[1], "Security"]).split()[1].strip() ):
                            stock_updates[command[1]].append(f'[{current_time}] {command[1]} "{stock_update_msg}"')
                            publisher_alerts.append(f'[{current_time}] Successfully Published! {command[1]} "{stock_update_msg}" ')

                        else:
                            publisher_alerts.append(f'[{current_time}] Invalid Security Code {command[1]} ')


                    elif command[1].isupper() :
                        t = time.localtime()
                        publisher_alerts.append(f'[{current_time}] Invalid Stock Code {command[1]} ')
                    
                else:
                    t = time.localtime()
                    publisher_alerts.append(f'[{current_time}] Invalid Command! <{command[0]}>. Type "help" to get help menu.')                    

            kill[addr] = 1
            publisher_realtime_data_thread.join()

            kill[addr] = 0
            publisher_realtime_data_thread = threading.Thread(target=publisher_realtime_data, args=(con, addr, user, window, ctrl_data, publisher_alerts))
            publisher_realtime_data_thread.start()






if __name__ == "__main__":
    show_banner()
    client_user_pass_data = {}
    publisher_user_pass_data = {}
    kill = {}
    stock_updates = {}
    stock_subscribers = {}

    stocks = pandas.read_csv("stocks.csv")

    for symbol in list(stocks["Symbol"]):
        stock_updates[symbol] = []
        stock_subscribers[symbol] = []


    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    start_datetime = str(input(' Start date and time (yyyy-mm-dd hh:mm:ss): '))
    
    
    while True:
        show_banner()
        current_datetime_int = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

        try:
            start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
            start_datetime_int = int(datetime.datetime.strftime(start_datetime, "%Y%m%d%H%M%S"))
        except:
            print("\n\n")
            err_msg = " Enter valied date and time "
            print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
            start_datetime = str(input('\n\n Start date and time (yyyy-mm-dd hh:mm:ss): '))
            continue

        if start_datetime_int <= current_datetime_int:
            print("\n\n")
            err_msg = " Enter valied date and time "
            print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
            start_datetime = str(input('\n\n Start date and time (yyyy-mm-dd hh:mm:ss): '))
            continue
        
        else:

            print(f" Start time\t: {start_datetime}\n\n")

            end_datetime = str(input(' End date and time (yyyy-mm-dd hh:mm:ss): '))
            while True:
                try:
                    end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")
                    end_datetime_int = int(datetime.datetime.strftime(end_datetime, "%Y%m%d%H%M%S"))
                except:
                    print("\n\n")
                    err_msg = " Enter valied date and time "
                    print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                    end_datetime = str(input('\n\n End date and time (yyyy-mm-dd hh:mm:ss): '))
                    continue

                if end_datetime_int <= start_datetime_int :
                    print("\n\n")
                    err_msg = " Enter valied date and time "
                    print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                    end_datetime = str(input('\n\nEnd date and time (yyyy-mm-dd hh:mm:ss): '))
                    continue

                else:
                    break
            
            break

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    file_name = f'Log/{DATE}__{time.strftime("%H-%M-%S", t)}__SYS.txt'
    
    alert_file = open(file_name,"w+")
    alert_file.close()
    
    with open(file_name, "a+") as alert_file:
        alert_file.write(f"\t[{current_time}] Auction start time : {start_datetime}\n")
        alert_file.write(f"\t[{current_time}] Auction end time : {end_datetime}\n")


    stocks['END TIME'] = end_datetime

    os.system(f'mode CON: cols={COLS} lines={LINES}')
    



    print_data_thread = threading.Thread(target=print_data)
    print_data_thread.start()

    lock = threading.Lock()

    start_publisher_thread = threading.Thread(target=start_publisher)
    start_publisher_thread.start()

    start_client()
