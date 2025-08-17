from imports import *
from funcs import *
import funcs

# AGREGAR: Tupla de Funciones (Distintas funciones para hacer todo el mismo proceso de "Abrir el postbox, pegar el texto, pegar la foto y publicar" De esta forma el codigo se adapta a cada meotodo anti-bots de facebook)
# AGREGAR: Modificar el texto "Posted X/X" por "Poster X/X | Time Took = X.XX Secs"
# AGREGAR: Darle varías fotos, poder elegir si postear todas o que sean opción a intercambiar (que elija una random entre esas), que el script detecte la cantidad EJ: 4 y saque un numero del 1 al 4 para elegir que foto usar y asi evitar detectar la automatización
# AGREGAR: Lo mismo que arriba pero con el texto, dentro del mismo .txt poner varios copys separados por "" u otro simbolo el cual sea el separador Y/O hacer cambios en un unico texto para evitar la detección, podria hacerse agregando tildes donde no van (queda poco profesional), cambiando los espacios, borrando algunas palabras o incluso integrando ChatGPT para darle como prompt el copy y pedirle que lo cambie
# QUITAR:  Información sensible MIA para poder publicar el repositorio debidamente
# AUTOMATIZAR: Se puede hacer lo mismo que este codigo pero que elija el perfil automaticamente y asi iniciar el script a traves de un .bat diariamente
# AGREGAR: Utilidad para Linux (Parcial)

#V 1.4.0


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

                print(f"posted {funcs.counter}/{len(group_list)}")

                funcs.counter += 1
                funcs.ok_counter += 1
            except Exception as exc:
                print("An unexpected error happened while posting, skipping group | Un error inesperado ocurrió mientras se intentó postear, omitiendo grupo")
                print(f"ERROR: {exc}")
                funcs.counter += 1

        except:
            print(f"""
            
            

            Error trying to post in {group} (group number {funcs.counter}), INVALID URL""")
            group_error.append(group)


    # Close driver

    print("End")
    funcs.counter -=1
    print(f"Posted on {funcs.ok_counter} of {funcs.counter}")

    if funcs.ok_counter != funcs.counter:
        print("Groups that gave error were:")
        for i in group_error:
            print(i)

    driver.close()
    
if __name__ == "__main__":
    main()