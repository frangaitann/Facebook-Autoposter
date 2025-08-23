from imports import *
from funcs import *
import funcs

# ADD: Be able to use more than 1 pic and select randomly between those pictures per post (for avoiding anti-bots system)
# ADD: Same of above but with text, being able to put many copys on the .txt file OR making changes to one text by AI
# ADD: Linux support
# AUTOMATE: This code can be reworked for automatic profile selection and auto-executing with .bat file (for avoiding manual execution)

#V 1.4.6


def main():
    #loading chrome & facebook

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print("Starting script")

    options = opt()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    webdriver_stealth(driver)
    driver.set_window_size(1980, 935)
    #print("Starting web")
    
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
    driver.get('https://www.facebook.com')
    
    print("""  ______    _        _____                                           
 |  ____|  | |      / ____|                                          
 | |__ __ _| |__   | (___  _ __   __ _ _ __ ___  _ __ ___   ___ _ __ 
 |  __/ _` | '_ \   \___ \| '_ \ / _` | '_ ` _ \| '_ ` _ \ / _ \ '__|
 | | | (_| | |_) |  ____) | |_) | (_| | | | | | | | | | | |  __/ |   
 |_|  \__,_|_.__/  |_____/| .__/ \__,_|_| |_| |_|_| |_| |_|\___|_|   
                          | |                                        
                          |_|                                           V 1.4.0""")

    #print("Driver Funct")
    cookies(driver)

    #Choose Sub-Profile
    scroller(driver)
    prof_chooser(driver)
    print("...")
    time.sleep(randomizer_t())

    # Post on each group
    group_list_raw = groups()
    group_list = [g.strip() for g in group_list_raw if g.strip() and "facebook.com/groups/" in g]

    for group in group_list:
        try:
            remove = "https://www.facebook.com/groups/"
            group_name_clean = group.replace(remove, "")
            clean_group = group_name_clean

            print(f"""
        
        
            Working with {group_name_clean} group number {funcs.counter}""")
            driver.get(group)

            scroller(driver)
            t1 = text_past(driver, clean_group) #this has randomizer()

            try:
                t2 = textpaster(driver) #this has randomizer()
                t3 = picbox(driver) #this has randomizer()
                t4 = postbutton(driver) #this has randomizer()
                
                t = t1 + t2 + t3 + t4
                t = round(t, 2)

                print(f"posted {funcs.counter}/{len(group_list)} in {t} seconds")

                funcs.counter += 1
                funcs.ok_counter += 1
                funcs.total_t += t
            except Exception as exc:
                print(f"An unexpected error happened while posting, skipping group.")
                print(f"ERROR: {exc}")
                funcs.counter += 1

        except:
            print(f"""
            
            

            Error trying to post in {group} (group number {funcs.counter}), INVALID URL.""")
            group_error.append(group)


    # Close driver
    
    driver.close()

    print("End")
    funcs.counter -=1
    print(f"Posted on {funcs.ok_counter} of {funcs.counter}, lasted {round(funcs.total_t)}s")

    if funcs.ok_counter != funcs.counter:
        print("Groups that gave error were:")
        for i in group_error:
            print(i)
    
    getpass.getpass("<< Hit Enter for closing script window >>")
    
if __name__ == "__main__":
    main()