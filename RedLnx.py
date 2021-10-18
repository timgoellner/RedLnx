# RedLnx Version 0.5 -> BETA by SirRoti(#2788)
try:
    import os
    import time
    import sys
    import json
    from configparser import ConfigParser
    from colorama import Fore, Style, Back

    def ErrorHandeling(func):
        while True:
            os.system("cls")
            print("""
            
            
            
                             RedLnx ErrorHandeling
                         An Error occurred in """ + func + """


                
       
            """)
            input()

    def PermissionCheck():
        file = "RedLnx.ini"
        config = ConfigParser()
        config.read(file)
        devmode = config["DEVMODE"]["~"]
        if devmode == "True":
            print(f"-devmode: permission check: {str(usr)}")
        try:
            _ = config["USER"]["*" + str(usr)]
            return
        except:
            users = config.options("USER")
            admin_password = ""
            for user in users:
                if user.startswith("*"):
                    admin_password = config["USER"][user]
                    break
            if input("sudo password: ") == str(admin_password):
                return
            else:
                print("user: incorrect password")
                main()

    def help(comd):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: help")
            try:
                RedLnxCMDFILE = open("RedLNXCMD.json", "r")
                RedLnxCMD = json.load(RedLnxCMDFILE)
                print(f"""RedLnx 0.5 (BETA) LTS (GNU/Linux 5.4.78-2-pve x86_64)
GNU bash, version 0.5(1)-release

Usage: {RedLnxCMD[str(comd)]["usage"]}
Description: {RedLnxCMD[str(comd)]["descr"]}
Informations: {RedLnxCMD[str(comd)]["infos"]}""")
            except:
                print("""RedLnx 0.5 (BETA) LTS (GNU/Linux 5.4.78-2-pve x86_64)
GNU bash, version 0.5(1)-release
These shell commands are defined internally.

help [cmd]
exit
clear
ls
cd [dir]
python
echo [arg]
mkdir [dir] [ext]
rmdir [dir] [ext]
mk [file] [ext]
rm [file] [ext]
user [cmd] [name] [psswd]
cat [file]""")
            main()
        except:
            ErrorHandeling("help")

    def echo(str_):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: echo: " + str(str_))
            str_.remove("echo")
            echo_ = ""
            for strA in str_:
                echo = echo_
                if echo == "":
                    spacing = ""
                else:
                    spacing = " "
                echo_ =(echo + spacing + strA)
            print(echo_)
            main()
        except:
            ErrorHandeling("echo")

    def mkdir(dir, extra):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: mkdir: " + dir + ": " + extra)
            if dir == "/":
                if extra == "--no-root-warn":
                    pass
                else:
                    print("mkdir: cannot create directory ‘/’: File is not makeable")
                    print("mkdir: if you still want the directory ‘/’: add --no-root-warn but be sure that this could break the file system")
                    main()
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            names = config.options(loc)
            count = str(names).count("~")
            if count >= 1023:
                print("mkdir: can not create " + dir + ": the maximal directory/file size in this directory is reached")
                main()
            name = ""
            if count == 0:
                name = "~"
            else:
                while count > -1:
                    name = name + "~"
                    count -= 1
            config.set(loc, name, dir)
            if loc == "/":
                slash = ""
            else:
                slash = "/"
            config.add_section(loc + slash + dir)
            with open(file, "w") as configfile:
                config.write(configfile)
            main()
        except:
            ErrorHandeling("mkdir")

    def rmdir(dir, extra):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: rmdir: " + dir + ": " + extra)
            if dir == "/":
                if extra == "--no-root-warn":
                    pass
                else:
                    print("rmdir: cannot delete directory ‘/’: File is not deleteable")
                    print("rmdir: if you still want the directory ‘/’ deleted: add --no-root-warn but be sure that this could break the file system")
                    main()
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            options = config.options(loc)
            name_ = ""
            for name in options:
                value = config[loc][name]
                if value == dir:
                    name_ = name
            if dir == "/":
                config.remove_section("/")
                with open(file, "w") as configfile:
                    config.write(configfile)
                main()
            if name_ == "":
                print("rmdir: cannot remove '" + loc + dir + "': No such file or directory")
                main()
            config.remove_option(loc, name_)
            with open(file, "w") as configfile:
                config.write(configfile)
            config.remove_section(loc + "/" + dir)
            with open(file, "w") as configfile:
                config.write(configfile)
            main()  
        except:
            ErrorHandeling("rmdir")

    def mk(dat, extra):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            if dat == "":
                print("mk: missing operand")
                main()
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                if extra == "":
                    dot = ""
                else:
                    dot = ": "
                print("-devmode: mk: " + str(dat) + dot + str(extra))
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            dot = dat.count(".")
            if dot == 0:
                print("mk: the File must have an ending")
                main()
            if str(dat).startswith("/"):
                if extra == "--no-root-warn":
                    pass
                else:
                    print("mk: cannot create file ‘" + dat + "’: File is not makeable")
                    print("mk: if you still want the file ‘" + dat + "’ created: add --no-root-warn but be sure that this could break the file system")
                    main()
            ending = dat.split(".")[1]
            endings = ["txt","py"]
            if ending in endings:
                pass
            else:
                supported = ""
                for ending_ in endings:
                    supported = (supported + " " + ending_)
                print("mk: this ending is not supported, use:" + supported)
                main()
            names = config.options(loc)
            count = str(names).count("~")
            if count >= 1023:
                print("mk: can not create " + dat + ": the maximal directory/file size in this directory is reached")
                main()
            name = ""
            if count == 0:
                name = "~"
            else:
                while count > -1:
                    name = name + "~"
                    count -= 1
            config.set(loc, name, dat)
            with open(file, "w") as configfile:
                config.write(configfile)
            loc = loc.replace("/","-")
            dok = open("Dokuments/" + loc + "~" + dat, "w+")
            dok.close()
            main()
        except:
            ErrorHandeling("mk")

    def rm(dat, extra):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            if dat == "":
                print("rm: missing operand")
                main()
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                if extra == "":
                    dot = ""
                else:
                    dot = ": "
                print("-devmode: rm: " + str(dat) + dot + str(extra))
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            loc = loc.replace("/","-")
            dok = ("Dokuments/" + loc + "~" + dat)
            try:
                loc = loc.replace("-","/")
                options = config.options(loc)
                name_ = ""
                for name in options:
                    value = config[loc][name]
                    if value == dat:
                        name_ = name
                if name_ == "":
                    if loc == "/":
                        loc = ""
                    print("rm: cannot remove " + loc + "/" + dat + ": noch such file")
                    main()
                config.remove_option(loc, name_)
                with open(file, "w") as configfile:
                    config.write(configfile)
                os.remove(dok)
            except:
                loc = loc.replace("-","/")
                if loc == "/":
                    loc = ""
                print("rm: cannot remove " + loc + "/" + dat + ": noch such file")
            main()
        except:
            ErrorHandeling("rm")

    def nano(dok):
        # Command is not finished
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            if dok == "":
                print("nano: missing operand")
                main()
            devmode = config["DEVMODE"]["~"]
            if devmode == "true":
                print("-devmode: rm: " + str(dok))
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            loc = loc.replace("/","-")
            try:
                dok = ("Dokuments/" + loc + "~" + dok)
                dok_ = open(dok,"r+")
                in_ = dok_.read()
                print(in_)
            except:
                print("nano: " + dok + ": no such file")
                main()
            main()
        except:
            ErrorHandeling("nano")

    def cat(file_name):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: cat: " + str(file_name))
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            dot = file_name.count(".")
            if dot == 0:
                print("cat: the File must have an ending")
                main()
            ending = file_name.split(".")[1]
            endings = ["txt","py"]
            if ending in endings:
                pass
            else:
                supported = ""
                for ending_ in endings:
                    supported = (supported + " " + ending_)
                print("cat: this ending is not supported, use:" + supported)
                main()
            loc = loc.replace("/","-")
            try:
                cat_file = open("Dokuments/" + loc + "~" + file_name, "r")
            except:
                print(f"cat: file does not exists: {file_name}")
                main()
            file_lines = cat_file.readlines()
            out_lines = []
            for line in file_lines:
                out_lines.append(line.replace("\n", ""))
            for line in out_lines:
                print(line)
            cat_file.close()
            main()
        except:
            ErrorHandeling("cat")

    def user(comd,user_,pswd):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: user: " + str(comd) + ": " + str(user_) + ": " + str(pswd))
            PermissionCheck()
            if user_.startswith("*"):
                print("user: forbidden letter in user name: *")
                main()
            if comd.lower() == "create":
                try:
                    test_var = config["USER"][str(user_)]
                    print(f"user: user already exists: {str(user_)}")
                    main()
                except:
                    pass
                config.set("USER", str(user_), str(pswd))
                with open(file, "w") as configfile:
                    config.write(configfile)
            elif comd.lower() == "remove":
                try:
                    test_var = config["USER"][str(user_)]
                except:
                    try:
                        test_var = config["USER"]["*" + str(user_)]
                        print(f"user: cant remove admin account: {str(user_)}")
                        main()
                    except:
                        print(f"user: user not exists: {str(user_)}")
                        main()
                if str(user_) == str(usr):
                    print("user: cannot remove current used user")
                    main()
                config.remove_option("USER", str(user_))
                with open(file, "w") as configfile:
                    config.write(configfile)
            elif comd.lower() == "edit":
                try:
                    test_var = config["USER"][str(user_)]
                except:
                    try:
                        test_var = config["USER"]["*" + str(user_)]
                    except:
                        print(f"user: user not exists: {str(user_)}")
                        main()
                try:
                    test_user = config["USER"]["*" + user_]
                    user_ = "*" + user_
                except:
                    pass
                config.set("USER", str(user_), str(pswd))
                with open(file, "w") as configfile:
                    config.write(configfile)
            elif comd.lower() == "list":
                users = config.options("USER")
                for cur_user in users:
                    cur_pswd = config["USER"][str(cur_user)]
                    print(f"{str(cur_user)}  {str(cur_pswd)}")
            else:
                print(f"user: no such instruction: {str(comd)}")
            main()
        except:
            ErrorHandeling("user")

    def ls():
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: ls")
            loc = config["LOCATION"]["~"]
            if loc == "":
                loc = "/"
            else:
                pass 
            keys = config.options(loc)
            in_ = ""
            for key in keys:
                value = config[loc][key]
                in_ = (in_ + "  " + value)
            print(in_)
            main()
        except:
            ErrorHandeling("ls")

    def cd(dir):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: cd: " + dir)
            loc = config["LOCATION"]["~"]
            dir = str(dir)
            if dir.startswith("/"):
                new_path = dir
                try:
                    config.set(new_path, "-", "-bash Testlink")
                    config.remove_option(new_path, "-")
                except:
                    print(new_path + ": no such directory")
                    main()
                config.set("LOCATION", "~", new_path)
                with open(file, "w") as configfile:
                    config.write(configfile)
                main()
            if "/" in dir:
                try:
                    config.set((loc + "/" + dir), "-", "-bash Testlink")
                    config.remove_option((loc + "/" + dir), "-")
                except:
                    print(loc + "/" + dir + ": no such directory")
                    main()
                config.set("LOCATION", "~", (loc + "/" + dir))
                with open(file, "w") as configfile:
                    config.write(configfile)
                main()
            if loc == "":
                loc = "/"
            keys = config.options(loc)
            in_ = []
            for key in keys:
                value = config[loc][key]
                in_.append(value)
            if dir in in_:
                if loc == "/":
                    loc = ""
                config.set("LOCATION", "~", (loc + "/" + dir))
                with open(file, "w") as configfile:
                    config.write(configfile)
                main()
            else:
                if loc == "/":
                    loc = ""
                print(loc + "/" + dir + ": no such directory")
                main()
        except:
            ErrorHandeling("cd")


    def get_math(cmd):
        if "+" in cmd:
            math_sym = "+"
        elif "-" in cmd:
            math_sym = "-"
        elif "/" in cmd:
            math_sym = "/"
        elif "*" in cmd:
            math_sym = "*"
        else:
            return
        math_nums = cmd.split(math_sym)
        if not len(math_nums) == 2:
            print(len(math_nums))
            return
        if math_sym == "+":
            result = int(math_nums[0]) + int(math_nums[1])
        elif math_sym == "-":
            result = int(math_nums[0]) - int(math_nums[1])
        elif math_sym == "/":
            result = int(math_nums[0]) / int(math_nums[1])
        elif math_sym == "*":
            result = int(math_nums[0]) * int(math_nums[1])
        else:
            result = ""
        print(result)
        main()
        

    def main():
        global exit
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            if devmode == "True":
                print("-devmode: cmd")
            loc = config["LOCATION"]["~"]
            cmd = input(f"{Fore.GREEN}{usr}@RedLnx{Fore.WHITE}:{Fore.BLUE}~" + loc + f"# {Fore.WHITE}")

            if cmd.startswith("exit"):
                exit = True

            elif cmd.startswith("ls"):
                ls()

            elif cmd.startswith("clear"):
                os.system("cls")
                main()

            elif cmd.startswith("python"):
                print("python: use \"exit()\" to come back to the console")
                print()
                os.system("python")
                main()

            elif cmd.startswith("echo"):
                str_ = cmd.split(" ")
                echo(str_)

            elif cmd.startswith("mkdir"):
                try:
                    dir = cmd.split(" ")[1]
                except:
                    dir = ""
                    print("mkdir: missing operand")
                    main()
                try:
                    extra = cmd.split(" ")[2]
                except:
                    extra = ""
                mkdir(dir, extra)

            elif cmd.startswith("rmdir"):
                try:
                    dir = cmd.split(" ")[1]
                except:
                    dir = ""
                    print("rmdir: missing operand")
                    main()
                try:
                    extra = cmd.split(" ")[2]
                except:
                    extra = ""
                rmdir(dir, extra)

            elif cmd.startswith("mk"):
                try:
                    dat = cmd.split(" ")[1]
                except:
                    dat = ""
                    print("mk: missing operand")
                    main()
                try:
                    extra = cmd.split(" ")[2]
                except:
                    extra = ""
                mk(dat, extra)

            elif cmd.startswith("rm"):
                try:
                    dat = cmd.split(" ")[1]
                except:
                    dat = ""
                    print("mk: missing operand")
                    main()
                try:
                    extra = cmd.split(" ")[2]
                except:
                    extra = ""
                rm(dat, extra)

            elif cmd.startswith("user"):
                vars = cmd.split(" ")
                vars.remove("user")
                try:
                    if str(vars[0].lower()) == "list":
                        user_ = "False"
                        pass
                    else:
                        user_ = vars[1]
                except:
                    user_ = ""
                    print("user: missing operand")
                    main()
                comd = vars[0]
                try:
                    pswd = vars[2]
                except:
                    pswd = ""
                user(comd,user_,pswd)

            # elif cmd.startswith("nano"):
            #     try:
            #         dok = cmd.split(" ")[1]
            #     except:
            #         print("nano: missing operand")
            #         main()
            #     nano(dok)

            elif cmd.startswith("cat"):
                try:
                    file_name = cmd.split(" ")[1]
                except:
                    print("cat: missing operand")
                    main()
                cat(file_name)

            elif cmd.startswith("cd"):
                try:
                    dir = cmd.split(" ")[1]
                except:
                    dir = ""
                    config.set("LOCATION", "~", "")
                    with open(file, "w") as configfile:
                        config.write(configfile)
                    main()
                cd(dir)

            elif cmd.startswith("help"):
                try:
                    comd = cmd.split(" ")[1]
                except:
                    comd = "None"
                help(comd)

            elif cmd == "":
                main()

            else:
                get_math(cmd)
                print(cmd + ": command not found")
                main()
        except:
            if exit == True:
                sys.exit()
            ErrorHandeling("cmd-input")

    def passin(usr):
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]
            can_passin = True
            global admin
            if usr.startswith("*"):
                password = False
                can_passin = False
            else:
                try:
                    password = config["USER"][str(usr)]
                    admin = "False"
                except:
                    try:
                        password = config["USER"]["*" + str(usr)]
                        admin = "True"
                    except:
                        password = False
                        can_passin = False
            if devmode == "True":
                print("-devmode: passin: " + usr + ": " + str(can_passin))
            if input(f"{Style.BRIGHT}[{Fore.GREEN}+{Fore.WHITE}]{Style.NORMAL} " + usr + "@45.146.252.250's password: ") == str(password) and can_passin == True:
                time.sleep(1)
                print("""Welcome to RedLnx 0.5 (BETA) LTS (GNU/Linux 5.4.78-2-pve x86_64)

      ___           ___          _____                          ___           ___
     /  /\         /  /\        /  /::\     ___                /__/\         /__/|
    /  /::\       /  /:/_      /  /:/\:\   /__/\               \  \:\       |  |:|
   /  /:/\:\     /  /:/ /\    /  /:/  \:\  \  \:\     ___       \  \:\      |  |:|
  /  /:/~/:/    /  /:/ /:/_  /__/:/ \__\:|  \  \:\   /  /\  _____\__\:\   __|__|:|
 /__/:/ /:/___ /__/:/ /:/ /\ \  \:\ /  /:/   \  \:\ /  /:/ /__/::::::::\ /__/::::\____
 \  \:\/:::::/ \  \:\/:/ /:/  \  \:\  /:/     \  \:\  /:/  \  \:\~~\~~\/    ~\~~\::::/
  \  \::/~~~~   \  \::/ /:/    \  \:\/:/       \  \:\/:/    \  \:\  ~~~      |~~|:|~~
   \  \:\        \  \:\/:/      \  \::/         \  \::/      \  \:\          |  |:|
    \  \:\        \  \::/        \__\/           \__\/        \  \:\         |  |:|
     \__\/         \__\/                                       \__\/         |__|/

                """)
                if devmode == "True":
                    print("-devmode: startup")
                config.set("LOCATION", "~", "")
                with open(file, "w") as configfile:
                    config.write(configfile)
                main()
            else:
                time.sleep(1)
                print(f"{Style.BRIGHT}[{Fore.RED}-{Fore.WHITE}]{Style.NORMAL} Access denied")
                passin(usr)
        except:
            ErrorHandeling("passin")

    
    def setup():
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            print("""Welcome to RedLnx 0.5 (BETA) LTS (GNU/Linux 5.4.78-2-pve x86_64)
The RedLnx 0.5 (BETA) Setup is Starting. Have fun using RedLnx

      ___           ___          _____                          ___           ___
     /  /\         /  /\        /  /::\     ___                /__/\         /__/|
    /  /::\       /  /:/_      /  /:/\:\   /__/\               \  \:\       |  |:|
   /  /:/\:\     /  /:/ /\    /  /:/  \:\  \  \:\     ___       \  \:\      |  |:|
  /  /:/~/:/    /  /:/ /:/_  /__/:/ \__\:|  \  \:\   /  /\  _____\__\:\   __|__|:|
 /__/:/ /:/___ /__/:/ /:/ /\ \  \:\ /  /:/   \  \:\ /  /:/ /__/::::::::\ /__/::::\____
 \  \:\/:::::/ \  \:\/:/ /:/  \  \:\  /:/     \  \:\  /:/  \  \:\~~\~~\/    ~\~~\::::/
  \  \::/~~~~   \  \::/ /:/    \  \:\/:/       \  \:\/:/    \  \:\  ~~~      |~~|:|~~
   \  \:\        \  \:\/:/      \  \::/         \  \::/      \  \:\          |  |:|
    \  \:\        \  \::/        \__\/           \__\/        \  \:\         |  |:|
     \__\/         \__\/                                       \__\/         |__|/

                """)
            global usr
            usr = input(f"{Style.BRIGHT}[{Fore.YELLOW}-{Fore.WHITE}]{Style.NORMAL} Please enter a username: ")
            passwd = input(f"{Style.BRIGHT}[{Fore.YELLOW}-{Fore.WHITE}]{Style.NORMAL} Please enter a password: ")
            config.set("USER", "*" + usr, passwd)
            with open(file, "w") as configfile:
                config.write(configfile)
            config.set("SETUP", "~", "True")
            with open(file, "w") as configfile:
                config.write(configfile)
            exit = False
            main()
        except:
            ErrorHandeling("setup")


    def login():
        try:
            file = "RedLnx.ini"
            config = ConfigParser()
            config.read(file)
            devmode = config["DEVMODE"]["~"]

            if devmode == "True":
                print("-devmode: login")
            global usr
            usr = input(f"{Style.BRIGHT}[{Fore.GREEN}+{Fore.WHITE}]{Style.NORMAL} login as: ")
            exit = False
            passin(usr)
        except:
            ErrorHandeling("login")


    if __name__ == "__main__":
        os.system("cls")

        file = "RedLnx.ini"
        config = ConfigParser()
        config.read(file)

        setup_cnt = config["SETUP"]["~"]
        if setup_cnt == "False":
            setup()
        else:
            login()

except Exception as exep:
    print(f"""
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                               An unexpectet Error occurred that RedLnx couldn't handle
                                          Try Restart or Reinstall RedLnx                                                                                                                                                                                                                                                                                   
                    """ + str(exep.with_traceback) + "\n                                               " + str(exep) + """                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                 """) 
    input()
