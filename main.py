from imports import *
from funcs import *
import funcs

# AGREGAR: Tupla de Funciones (Distintas funciones para hacer todo el mismo proceso de "Abrir el postbox, pegar el texto, pegar la foto y publicar" De esta forma el codigo se adapta a cada meotodo anti-bots de facebook)
# AGREGAR: Modificar el texto "Posted X/X" por "Poster X/X | Time Took = X.XX Secs"

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

    webdriver_stealth(driver)
    driver.set_window_size(1980, 935)
    print("Starting Facebook")
    driver.get('https://www.facebook.com')

    #print("Driver Funct")
    cookies(driver)

    #Choose Sub-Profile
    scroller(driver)
    prof_chooser(driver)
    print("...")
    randomizer_t()

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
            text_past(driver, clean_group)

            try:
                textpaster(driver)
                picbox(driver)
                postbutton(driver)

                print(f"posted {counter}/{len(group_list)}")

                funcs.counter += 1
                funcs.ok_counter += 1
            except Exception as exc:
                print("An unexpected error happened while posting, skipping group | Un error inesperado ocurrió mientras se intentó postear, omitiendo grupo")
                print(f"ERROR: {exc}")
                funcs.counter += 1

        except InvalidArgumentException:
            print(f"""
            
            

            Error trying to post in {group} (group number {funcs.counter}), INVALID URL""")
            group_error.append(group)


    # Close driver

    print("End")
    funcs.counter -=1
    print(f"Posted on {funcs.ok_counter} of {funcs.counter}, Method 1 was used {meth1} times and Method 2 {meth2}")

    if funcs.ok_counter != funcs.counter:
        print("Groups that gave error were:")
        for i in group_error:
            print(i)

    driver.close()
    
if __name__ == "__main__":
    main()