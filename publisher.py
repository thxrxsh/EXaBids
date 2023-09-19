import os
import socket
import pickle
import threading
import time
import datetime
import subprocess
import importlib.util


colorama_module = importlib.util.find_spec("colorama")
pandas_module = importlib.util.find_spec("pandas")


if colorama_module == None:
    while True:
        os.system("cls")
        print("\n Could'n find the 'colorama' module in you computer.\n Please connect your computer to internet and type 'ok' to proceed or 'no' to exit.")
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
                input(f"Somthing went wrong. ")
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
USERNAME = None
COLS = 96
LINES = 48
LINES_S = 35
WINDOW = 1
os.system(f'mode CON: cols={COLS} lines={LINES_S}')

def show_banner():
    os.system("cls")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

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
    print( " EXaBids Publisher v2.0 ".center(COLS,"░"))
    print()
    print(f"    {current_date}"+ " "*(COLS-26) + f"{current_time}")
    print()


def send_msg(msg):
    msg = msg.encode(FORMAT)
    msg_len = str( len(msg) ).encode(FORMAT)
    msg_len += b' ' * (HEADER - len(msg_len))
    client.send(msg_len)
    client.send(msg)

def recv_msg():
    msg_len = int(client.recv(HEADER).decode(FORMAT))
    msg = client.recv(msg_len).decode(FORMAT)
    # print("Response from server > "+msg)
    return msg

def recv_data():
    data_len = int(client.recv(HEADER).decode(FORMAT))
    data = pickle.loads(client.recv(data_len))
    # print("Response from server > "+data)
    return data


def authenticate():
    global USERNAME
    global start_datetime
    global end_datetime
    print("\n")
    print("\t\t\t ",Fore.BLACK+Back.WHITE+" 1 | SIGN IN "+Fore.RESET+Back.RESET,"               ",Fore.BLACK+Back.WHITE+ " 2 | SIGN UP "+Fore.RESET+Back.RESET)

    authentication_status = None

    while authentication_status == None:

        option = input("\n\n [EXa Bids]> ")
        if option == '1':
            send_msg("sign-in")
            response = recv_msg()

            if response == "request-username":
                os.system('cls')
                show_banner()
                print(Fore.BLACK+Back.WHITE+" SIGN IN ".center(COLS) +Fore.RESET+Back.RESET)
                user = input("\n\n Enter Username > ")
                send_msg(user)

                response = recv_msg()
                while True:
                    if response == "invalid-username":
                        os.system('cls')
                        show_banner()
                        print(Fore.BLACK+Back.WHITE+" SIGN IN ".center(COLS) +Fore.RESET+Back.RESET)
                        print("\n\n")
                        err_msg = " Username Not Found "
                        print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                        user = input("\n\n Enter Username > ")
                        send_msg(user)
                        response = recv_msg()
                    else:
                        break

            if response == "request-password":
                os.system("cls")
                show_banner()
                print(Fore.BLACK+Back.WHITE+" SIGN IN ".center(COLS) +Fore.RESET+Back.RESET)
                print("\n\n")
                print(" ",Fore.BLACK+Back.WHITE+f" User  |  {user} " +Fore.RESET+Back.RESET)
                print("\n")
                passwd = input(f" Enter the password for '{user}' > ")
                send_msg(passwd)

                response = recv_msg()
                while True:
                    if response == "invalid-password":
                        os.system("cls")
                        show_banner()
                        print(Fore.BLACK+Back.WHITE+" SIGN IN ".center(COLS) +Fore.RESET+Back.RESET)
                        print("\n\n")
                        print(" ",Fore.BLACK+Back.WHITE+f" User  |  {user} " +Fore.RESET+Back.RESET)
                        print("\n")
                        err_msg = " Password Incorrect "
                        print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                        passwd = input(f"\n\n Enter the password for '{user}' > ")
                        send_msg(passwd)
                        response = recv_msg()
                    elif response == "sign-in-successful":

                        start_datetime = datetime.datetime.strptime(recv_msg(), "%Y-%m-%d %H:%M:%S")
                        end_datetime = datetime.datetime.strptime(recv_msg(), "%Y-%m-%d %H:%M:%S")
                        USERNAME = user
                        authentication_status = "OK"
                        os.system(f'mode CON: cols={COLS} lines={LINES}')
                        break


        elif option == '2':
            send_msg("sign-up")
            response = recv_msg()

            if response == "request-username":
                os.system('cls')
                show_banner()
                print("\n")
                print(Fore.BLACK+Back.WHITE+" SIGN UP ".center(COLS) +Fore.RESET+Back.RESET)
                user = input("\n\n Enter Username > ")
                
                while True:
                    if len(user) > 2:
                        send_msg(user)
                        break
                    else:
                        os.system('cls')
                        show_banner()
                        print(Fore.BLACK+Back.WHITE+" SIGN UP ".center(COLS) +Fore.RESET+Back.RESET)
                        print("\n\n")
                        err_msg = " Username length must be greater than 2 "
                        print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                        user = input("\n\n Enter Username > ")
                response = recv_msg()
                while True:
                    if response == "username-exist":
                        os.system('cls')
                        show_banner()
                        print(Fore.BLACK+Back.WHITE+" SIGN UP ".center(COLS) +Fore.RESET+Back.RESET)
                        print("\n\n")
                        err_msg = " Username already exist "
                        print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                        user = input("\n\n Enter Username > ")
                        send_msg(user)
                        response = recv_msg()
                    else:
                        break
 
            if response == "request-password":
                os.system("cls")
                show_banner()
                print(Fore.BLACK+Back.WHITE+" SIGN UP ".center(COLS) +Fore.RESET+Back.RESET)
                print("\n\n")
                print(" ",Fore.BLACK+Back.WHITE+f" User  |  {user} " +Fore.RESET+Back.RESET)
                print("\n")
                passwd = input(f" Enter a password  > ")
                passwd_conf = input(f" Confirm password  > ")

                while True:
                    os.system("cls")
                    show_banner()
                    print(Fore.BLACK+Back.WHITE+" SIGN UP ".center(COLS) +Fore.RESET+Back.RESET)
                    print("\n\n")
                    print(" ",Fore.BLACK+Back.WHITE+f" User  |  {user} " +Fore.RESET+Back.RESET)
                    print("\n")
                        
                    if passwd != passwd_conf:
                        err_msg = " Confirm password doesn't match "
                        print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                        passwd = input(f"\n\n Enter a password  > ")
                        passwd_conf = input(f" Confirm password  > ")

                    elif len(passwd) < 8: # Check whether the password length is greater than 8
                        err_msg = " Password length must be greater than 8  "
                        print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
                        passwd = input(f"\n\n Enter a password  > ")
                        passwd_conf = input(f" Confirm password  > ")
                    else:
                        send_msg(passwd)

                        response = recv_msg()
                        if response == "sign-up-successful":
                            start_datetime = datetime.datetime.strptime(recv_msg(), "%Y-%m-%d %H:%M:%S")
                            end_datetime = datetime.datetime.strptime(recv_msg(), "%Y-%m-%d %H:%M:%S")
                            USERNAME = user
                            authentication_status = "OK"
                            ok_msg = " Registration Successful "
                            print(Fore.RESET+Back.RESET+" "*((COLS-len(ok_msg))//2) +Fore.BLACK+Back.LIGHTGREEN_EX+ok_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(ok_msg))//2))
                            input("\n\n Press any key to continue ...")
                            os.system("cls")
                            os.system(f'mode CON: cols={COLS} lines={LINES}')
                            show_banner()
                            break

        else:
            os.system('cls')
            show_banner()
            print("\n")
            print("\t\t ",Fore.BLACK+Back.WHITE+" 1 | SIGN IN "+Fore.RESET+Back.RESET,"               ",Fore.BLACK+Back.WHITE+ " 2 | SIGN UP "+Fore.RESET+Back.RESET)
            print("\n\n")
            err_msg = " Enter the number of your option "
            print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))

    return authentication_status






def print_data():
    global data
    global data_time
    global WINDOW
    global user_alerts
    global start_datetime
    global end_datetime
    
    help_menu = '''
help        - For this help menu

~ INFORMATION
    info        - Get informations about the stoks
        Syntax:
                info <SYMBOL>
                    - Get information about selected stocks
                    - EX: info ABC , info ABC XYZ AAL
                    (Maximum stocks count is 5)
                
                info [highest/lowest] [price/profit]
                    highest - Get the highest values to the top
                    lowest  - Get the lowest values to the top
                    price   - Make the order according to the price
                    profit  - Make the order according to the profit
                        - EX: info highest profit , info lowest price
                (This will return only 5 rows)

~ PUBLISH
    PUB <SYMBOL> <information> <SECURITY>
        - EX: PUB ABCD "Open Day on 3.4.2022" 74904
        - EX: PUB XYZ "Close Day on 5.4.2022" 64950
'''    

    while True :
        with lock:

            current_datetime = datetime.datetime.now()
          
            show_banner()
            

            if current_datetime < start_datetime:
                time_difference = start_datetime - current_datetime
                if time_difference.seconds < 60:
                    print(Fore.BLACK+Back.LIGHTGREEN_EX+" Time To Start ".center(COLS) +Fore.RESET+Back.RESET)
                else:
                    print(Fore.BLACK+Back.WHITE+" Time To Start ".center(COLS) +Fore.RESET+Back.RESET)
                print("\n\t\t\t", time_difference.days, "days  :: ", time_difference.seconds//3600, "hours  :: ", (time_difference.seconds//60)%60, "minutes  :: ", time_difference.seconds%60, "seconds")

            elif (current_datetime >= start_datetime) and (current_datetime <= end_datetime):
                time_difference = end_datetime - current_datetime
                if time_difference.seconds < 60:
                    print(Fore.WHITE+Back.RED+" Time To End ".center(COLS) +Fore.RESET+Back.RESET)
                else:
                    print(Fore.BLACK+Back.WHITE+" Time To End ".center(COLS) +Fore.RESET+Back.RESET)
                print("\n\t\t\t", time_difference.days, "days  :: ", time_difference.seconds//3600, "hours  :: ", (time_difference.seconds//60)%60, "minutes  :: ", time_difference.seconds%60, "seconds")

            elif current_datetime > end_datetime:
                time_difference = current_datetime - end_datetime
                print(Fore.BLACK+Back.WHITE+" Ended ".center(COLS) +Fore.RESET+Back.RESET)
                print("\n\t\t\t", time_difference.days, "days  :: ", time_difference.seconds//3600, "hours  :: ", (time_difference.seconds//60)%60, "minutes  :: ", time_difference.seconds%60, "seconds")


            if (WINDOW == 1) or (WINDOW == 2):

                print("\n  ",end='')
                for i in range(len(data['columns'])):
                    if data['columns'][i] == 'Symbol':
                        print(Back.WHITE+Fore.BLACK+"   SYMBOL   ",end=Fore.RESET+Back.RESET+"   ")
                    elif data['columns'][i] == 'Name':
                        print(Back.WHITE+Fore.BLACK+"     NAME     ",end=Fore.RESET+Back.RESET+"   ")
                    elif data['columns'][i] == 'Price':
                        print(Back.WHITE+Fore.BLACK+"    PRICE   ",end=Fore.RESET+Back.RESET+"   ")
                    elif data['columns'][i] == 'Security':
                        print(Back.WHITE+Fore.BLACK+"   SECURITY   ",end=Fore.RESET+Back.RESET+"   ")
                    elif data['columns'][i] == 'Profit':
                        print(Back.WHITE+Fore.BLACK+"   PROFIT   ",end=Fore.RESET+Back.RESET+"   ")
                    elif data['columns'][i] == 'END TIME':
                        print(Back.WHITE+Fore.BLACK+"    END IN   ",end=Fore.RESET+Back.RESET+" ")
                    
                print(Fore.RESET+Back.RESET+"\n")

                for i in range(len(data['data'])):
                    print('',end='')
                    for j in range(len(data['data'][i])):

                        if j == 5:
                            stock_time_difference = data['data'][i][j] - datetime.datetime.now()
                            if stock_time_difference.days >= 0:
                                data['data'][i][j] = f"{stock_time_difference.days}d {stock_time_difference.seconds//3600}h {(stock_time_difference.seconds//60)%60}m {stock_time_difference.seconds%60}s"
                            else:
                                data['data'][i][j] = "END"

                        if str(data['data'][i][j])[:8] == "0d 0h 0m":
                            print(Fore.LIGHTRED_EX+f"{data['data'][i][j] }".center(15),end=Fore.RESET+"\t")

                        else:
                            print(f"{data['data'][i][j]}".center(15),end="\t")
                    print("\n")

                print("")
                print(Back.LIGHTBLACK_EX + Fore.BLACK + Style.DIM +" NOTIFICATIONS ".center(COLS,"░")  + Style.RESET_ALL+Back.RESET+Fore.RESET )
                print("")

                if WINDOW == 1:
                    alert_rows = 6
                
                elif WINDOW == 2:
                    alert_rows = 16 - len(data['data'])*2
        
                if not len(user_alerts) > alert_rows:
                    for alert in user_alerts:
                        print("\t"+alert)
                    for i in range(alert_rows-len(user_alerts)):
                        print("")
                else:
                    for i in range(alert_rows):
                        print("\t"+user_alerts[i])

                print()
                print(f" Data sent at : {data_time} ".center(COLS))
                print()


            elif WINDOW == 3:
                print("")
                print(Back.LIGHTBLACK_EX + Fore.BLACK + Style.DIM +" HELP MENU ".center(COLS,"░")  + Style.RESET_ALL+Back.RESET+Fore.RESET )
                print(help_menu)
                

            
            print(Back.LIGHTBLACK_EX + Fore.BLACK + Style.DIM +" CONSOLE ".center(COLS,"░")  + Style.RESET_ALL+Back.RESET+Fore.RESET )


        time.sleep(1)



def get_realtime_data():
    global data
    global data_time
    global WINDOW
    global user_alerts
    global start_datetime
    global end_datetime
    while True:
        received_data = recv_data()
        data = received_data[0]
        start_datetime = received_data[1][0]
        end_datetime = received_data[1][1]    
        data_time = received_data[1][2]
        WINDOW = received_data[2]
        user_alerts = received_data[3]
        time.sleep(1)
        

            
# print("Press ENTER to open console. Type HELP in console to get help menu.")

def console():
    global USERNAME
    while True:
        input()
        with lock:
            command = input(f" [{USERNAME}@EXaBids] >> ")
        send_msg(command+","+USERNAME )







if __name__ == "__main__":

    while True:
        show_banner()
        IP = input("\n\n Enter the ip address of EXaBids server : ")
        try:
            SERVER = (IP,2022)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(SERVER)
            break
        except:
            show_banner()
            err_msg = " Couldn't connect to the server "
            print(Fore.RESET+Back.RESET+" "*((COLS-len(err_msg))//2) +Fore.WHITE+Back.RED+err_msg+Fore.RESET+Back.RESET+ " "*((COLS-len(err_msg))//2))
            op = input("\n\n Enter any key to Retry or 'e' to Exit : ")
            if op == 'e': os.sys.exit()





    data = {}
    data_time = ""
    user_alerts = []
    start_datetime = ""
    end_datetime = ""
    show_banner()
    
    response = recv_msg()

    if response == "authentication-Required":
        authentication_status = authenticate()

        if authentication_status == "OK":
            lock = threading.Lock()

            realtime_data_thread = threading.Thread(target=get_realtime_data)
            realtime_data_thread.start()

            print_data_thread = threading.Thread(target=print_data)
            print_data_thread.start()
            
            console()
        

        
        else:
            print("\t: Authentication Fail")
