from imports import *
from funcs import *

# AGREGAR: Tupla de Funciones (Distintas funciones para hacer todo el mismo proceso de "Abrir el postbox, pegar el texto, pegar la foto y publicar" De esta forma el codigo se adapta a cada meotodo anti-bots de facebook)

# FUNCIONA

def main():
    #loading chrome & facebook

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print("Starting Chrome")

    options = opt()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    print("Starting Facebook")
    driver.get('https://www.facebook.com')

    #print("Driver Funct")
    cookies(driver)

    #Choose Sub-Profile
    prof_chooser(driver)
    print("...")
    time.sleep(2)

    # Post on each group
    counter = 1
    ok_counter= 0
    group_list_raw = groups()
    group_list = [g.strip() for g in group_list_raw if g.strip() and "facebook.com/groups/" in g]
    group_error = []
    meth1 = 0
    meth2 = 0

    for group in group_list:
        try:
            remove = "https://www.facebook.com/groups/"
            group_name_clean = group.replace(remove, "")
            clean_group = group_name_clean

            print(f"""
        
        
            Working with {group_name_clean} group number {counter}""")
            driver.get(group)

            try:
                text1(driver)

            except (NoSuchElementException, TimeoutException):
                try:
                    text2(driver)

                except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                    print(f"""
            
            

                    Error trying to post in {group_name_clean} (group number {counter}), NO ELEMENT FOUND / PROGRAM TOOK TO MUCH TIME, TRY AGAIN | Error al intentar postear en {group_name_clean} (grupo numero {counter}), ELEMENTO NO ENCONTRADO""")
                    group_error.append(clean_group)
                    counter += 1

            try:
                textpaster(driver)

                try:
                    picbox1(driver)
                    meth1+=1

                except (NoSuchElementException, TimeoutException):
                    picbox2(driver)
                    meth2+=1

                postbutton(driver)

                print(f"posted {counter}/{len(group_list)}")

                counter += 1
                ok_counter += 1
            except Exception as exc:
                print("An unexpected error happened while posting, skipping group | Un error inesperado ocurrió mientras se intentó postear, omitiendo grupo")
                print(f"ERROR: {exc}")
                counter += 1

        except InvalidArgumentException:
            print(f"""
            
            

            Error trying to post in {group} (group number {counter}), INVALID URL""")
            group_error.append(group)


    # Close driver

    print("End")
    counter -=1
    print(f"Posted on {ok_counter} of {counter}, Method 1 was used {meth1} times and Method 2 {meth2}")

    if ok_counter != counter:
        print("Groups that gave error were:")
        for i in group_error:
            print(i)

    driver.close()
    
if __name__ == "__main__":
    main()