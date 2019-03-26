from winreg import *
import sys
import io

global dic_value
global ProfileList
global AutoRun

dic_value = {'사용중인 운영체제' : '' , '사용자 이름' : '', '시스템 경로' : '', '컴퓨터 이름' : '', '방화벽' : ''}

def main() :

    global dic_value
    global ProfileList
    global AutoRun

    read_reg()
    for title, value in dic_value.items():
        print(title, ":", value)
        if(title == "시스템 경로") :
            show_user(ProfileList)
        if(title == "방화벽") :
            print("시스템 부팅 후 자동 시작 프로그램 :")
            get_value(AutoRun,"many")

        print()

def read_reg() :

    global dic_value
    global ProfileList
    global AutoRun

    software_subkey = "SOFTWARE\Microsoft"
    windowsnt = software_subkey + "\\Windows NT\CurrentVersion"

    dic_value['사용중인 운영체제'] = get_value(windowsnt,"ProductName")
    dic_value['사용자 이름'] = get_value(windowsnt,"RegisteredOwner")
    dic_value['시스템 경로'] = get_value(windowsnt,"SystemRoot")

    ProfileList = windowsnt + "\\ProfileList"
    AutoRun = software_subkey + "\\Windows\CurrentVersion\Run"

    system_subkey = "SYSTEM\CurrentControlSet"
    dic_value['컴퓨터 이름'] = get_value(system_subkey+"\\Control\ComputerName\ComputerName","ComputerName")
    
    if(get_value(system_subkey+"\\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile","EnableFirewall") == 1) :
        dic_value['방화벽'] = "허용"
    
    else :
        dic_value['방화벽'] = "설정 안함"

def get_value(subkey, keyname) :

    reg_handle = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg_handle,subkey)

    i = 0

    for i in range(0, 100) :

        try :
            name, value, reg_type = EnumValue(key,i)

            if(keyname == "many") :
                print("\t프로그램 이름 :",name,"    \t경로 :",value)

            if(keyname in name) :
                CloseKey(key)
                CloseKey(reg_handle)
                return value
                break
        
        except WindowsError as e :
            pass

def show_user(subkey) :
    
    reg_handle = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    key = OpenKey(reg_handle,subkey)
    print("사용자 계정 목록 :")

    for i in range(0, 100) :

        try :
            keyname = EnumKey(key, i)
            subkey_profile = "%s\\%s" % (subkey, keyname)
            key_profile = OpenKey(reg_handle, subkey_profile)

            try :

                for j in range(0, 100) :
                    name, value, reg_type = EnumValue(key_profile, j)

                    if("ProfileImagePath" in name and "Users" in value) :
                        print("\t",value)
            
            except WindowsError as e :
                pass
            
            CloseKey(key_profile)
            
        
        except WindowsError as e :
            break
    
    CloseKey(key)
    CloseKey(reg_handle)
                
main()