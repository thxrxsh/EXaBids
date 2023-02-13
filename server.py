import socket
import os
import threading
import time
import datetime
import pickle
import importlib
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
                print("Couldn't install the colorama module. check your connection.")
                continue
            
            try:
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
HOST = socket.gethostbyname(socket.gethostname()) # Get the IP address of computer
PORT = 2021

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
    print(" EXaBids Server v1.1 ".center(COLS,"░"))
    print()
    print(f"    {current_date}"+ " "*(COLS-26) + f"{current_time}")
    print("")


def start_server():
    global file_name
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    try:
        global HOST
        global PORT
    
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating the socket
        server.bind((HOST,PORT)) # Binding the connection
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Server is strating as {HOST}\n")

    except socket.error as err_msg:
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Binding error \n"+ str(err_msg) + "\n\nRetrying binding...\n")
        server.bind((HOST,PORT))

    try:
        server.listen() # Listening for new connections
        with open(file_name, "a+") as alert_file:
            alert_file.write(f"\t[{current_time}] Server is listening on PORT {PORT}\n")

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
            alert_file.write(f"\t[{current_time}] A client Refused the connection  \n")
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


# Authenticate the clients
def authenticate(con, addr):
    global user_pass_data
    global file_name
    global start_datetime
    global end_datetime

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    with open("userpass.pickle","rb") as user_data_file:
        user_pass_data = pickle.load(user_data_file)

    send_msg(con, "authentication-Required")
    response = recv_msg(con)
    print(response)

    if response == "sign-in": 
        try:
            send_msg(con, "request-username")
            user = recv_msg(con)

            while True:
                if user not in user_pass_data.keys(): # Check whether the username is a true one
                    send_msg(con, "invalid-username")
                    user = recv_msg(con)
            
                else:
                    send_msg(con, "request-password")
                    while True:
                        passwd = recv_msg(con)
                        if passwd != user_pass_data[user]: # Check whether the password is correct acording to the username
                            send_msg(con, "invalid-password")
                        else:
                            send_msg(con, "sign-in-successful")
                            send_msg(con, start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                            send_msg(con, end_datetime.strftime("%Y-%m-%d %H:%M:%S"))

                            with open(file_name, "a+") as alert_file:
                                alert_file.write(f"\t[{current_time}] New client connected :: {user}\n")
                            return ['sign-in', user, passwd]
                            
        except:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}]  Sign-in error\n")


    elif response == "sign-up":
        try:

            send_msg(con, "request-username")
            while True:
                user = recv_msg(con)
                if user in user_pass_data.keys():
                    send_msg(con, "username-exist")

                else:
                    send_msg(con, "request-password")
                    passwd = recv_msg(con)

                    if (user and passwd):
                        user_pass_data[user] = passwd
                        with open("userpass.pickle","wb") as user_data_file:
                            pickle.dump(user_pass_data, user_data_file)
                        
                        send_msg(con, "sign-up-successful")
                        send_msg(con, start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        send_msg(con, end_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        with open(file_name, "a+") as alert_file:
                            alert_file.write(f"\t[{current_time}] New client joined ({user})\n")

                        return ['sign-up', user, passwd]
                    
        except:
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}]  Sign-up error\n")



def realtime_data(con, addr, window, ctrl_data, user_alerts):
    global stocks
    global kill
    global start_datetime
    global start_datetime_int
    global end_datetime
    global end_datetime_int
    global current_datetime
    global current_datetime_int
    global file_name

    

    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        # for i in range(len(stocks['END TIME'][:])) :
        #     stock_time_difference = stocks['END TIME'][i] - datetime.datetime.now()
        #     stocks['END TIME'][i] =    


        if current_datetime_int == start_datetime_int:
            user_alerts.append(f"[{current_time}] Auction started !")
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Auction started !\n")

        elif current_datetime_int == end_datetime_int:
            user_alerts.append(f"[{current_time}] Auction ended !")
            with open(file_name, "a+") as alert_file:
                alert_file.write(f"\t[{current_time}] Auction ended !\n")
        
        if kill[addr] == 0:

            if window == 1:
                temp_stocks = stocks.sort_values(ctrl_data[0], ascending=ctrl_data[1]).head(5).to_dict("tight")
                temp_user_alerts = user_alerts[:-6:-1]


            elif window == 2:
                temp_stocks = []
                for sym in ctrl_data:
                    temp_stocks.append(stocks.loc[stocks["Symbol"] == sym])
                temp_stocks = pandas.concat(temp_stocks).head(5).to_dict("tight")
                temp_user_alerts = user_alerts[:-14:-1]

            elif window == 3:
                temp_user_alerts = []
                temp_stocks = []

            st_en_cur_time = [start_datetime, end_datetime, current_time]
            data = [temp_stocks, st_en_cur_time, window, temp_user_alerts]
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
    user_alerts = []
    session = authenticate(con, addr)
    kill[addr] = 0
    
    
    if session:

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        user_alerts.append(f"[{current_time}] Auction start time : {start_datetime}")
        user_alerts.append(f"[{current_time}] Auction end time : {end_datetime}")

        ctrl_data = ["Profit", False]
        window = 1
        realtime_data_thread = threading.Thread(target=realtime_data, args=(con, addr, window, ctrl_data, user_alerts))
        realtime_data_thread.start()


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
                            user_alerts.append(f'[{current_time}] Invalid Command! <{command[2]}>. Type "help" to get help menu.')

                    elif command[1] == "lowest":
                        window = 1
                        if command[2] == "price":
                            ctrl_data = ["Price",True]
                        elif command[2] == "profit":
                            ctrl_data = ["Profit", True]
                        else:
                            user_alerts.append(f'[{current_time}] Invalid Command! <{command[2]}>. Type "help" to get help menu.')


                    elif command[1] == "stock":
                        if len(command) > 2:
                            ctrl_data = command[2:]
                            window = 2
                    else:
                        user_alerts.append(f'[{current_time}] Invalid Command! <{command[1]}>. Type "help" to get help menu.')                                            
                
                elif command[0] == "help":
                    window = 3




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
                                    
                                    user_alerts.append(f'[{current_time}] Successfully Bided! {command[0]} {command[1]}')
                                    
                                    with open(file_name,"a+") as alert_file:
                                        alert_file.write(f'\t[{current_time}] {user} Successfully Bided! {command[0]} {command[1]}\n')



                                    if stock_time_difference.seconds <= 60:
                                        stocks.loc[stocks["Symbol"] == command[0], "END TIME"] = end_datetime + datetime.timedelta(seconds=60)
                                        user_alerts.append(f"[{current_time}] {command[0]} stock time extended in 60sec. Endtime : {end_datetime}")

                                        with open(file_name, "a+") as alert_file:
                                            alert_file.write(f"\t[{current_time}] {command[0]} stock time extended in 60sec. Endtime : {end_datetime}\n")


                                        end_datetime = end_datetime + datetime.timedelta(seconds=60)
                                        user_alerts.append(f"[{current_time}] Auction time extended in 60sec. Endtime : {end_datetime}")

                                        with open(file_name, "a+") as alert_file:
                                            alert_file.write(f"\t[{current_time}] Auction time extended in 60sec. Endtime : {end_datetime}\n")


                                else:
                                    user_alerts.append(f'[{current_time}] Invalid Bid {command[0]} {command[1]}')

                            else:
                                user_alerts.append(f'[{current_time}] Blocked! Bidding ended for "{command[0]}" at {end_datetime} ')
                        else:
                            user_alerts.append(f'[{current_time}] Invalid Bid {command[0]} ')
                    
                    elif current_datetime_int < start_datetime_int :
                        user_alerts.append(f'[{current_time}] Bloked! Auction will start at {start_datetime} ')

                    elif current_datetime_int > end_datetime_int :
                        user_alerts.append(f'[{current_time}] Blocked! Auction ended at {end_datetime} ')


                elif command[0].isupper() :
                    t = time.localtime()
                    user_alerts.append(f'[{current_time}] Invalid Stock Code {command[0]} ')
                
                else:
                    t = time.localtime()
                    user_alerts.append(f'[{current_time}] Invalid Command! <{command[0]}>. Type "help" to get help menu.')                    

            kill[addr] = 1
            realtime_data_thread.join()

            kill[addr] = 0
            realtime_data_thread = threading.Thread(target=realtime_data, args=(con, addr, window, ctrl_data, user_alerts))
            realtime_data_thread.start()




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










if __name__ == "__main__":
    show_banner()
    user_pass_data = {}
    kill = {}

    stocks = pandas.read_csv("stocks.csv")

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


    start_server()


    
    # print("Run1")

    # user_pass_data = {"Tharusha": "password"}

    # user_data_file = open("userpass.pickle","wb")

    # pickle.dump(user_pass_data, user_data_file)

    # user_data_file.close()
    # print("Run2")

