from imports import *


# WORKING FUNCTIONS

group_error = []
meth1 = 0
meth2 = 0
counter = 1
ok_counter= 0


def webdriver_stealth(driver):
    driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    },)

def scroller(driver):
    driver.execute_script(f"window.scrollTo(0, {random.uniform(23, 732)});")


def randomizer_t():
    randomizer_num = random.uniform(4, 34)
    print(f"T = {randomizer_num}")
    time.sleep(randomizer_num)


def textpaster(driver):
    post2 = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/p")))
    #print("text box found")

    post2.send_keys(text())
    randomizer_t()



def text_past(driver, clean_group):
    randomizer_t()
    try:
        textbox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Foto/vídeo') or contains(text(), 'Photo/video') or contains(text(), 'Write something...')]")))
        textbox.click()
        randomizer_t()
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
        try:
            textbox = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div[1]/span")))
            textbox.click()
            randomizer_t()
        except:
            print("Error trying to post, NO ELEMENT FOUND / PROGRAM TOOK TO MUCH TIME, TRY AGAIN")
            group_error.append(clean_group)
            counter += 1
            randomizer_t()



def picbox(driver):
    global meth2

    try:
        pic_box = driver.find_element(By.XPATH, '//form[@method="POST"]//input[@type="file"]')
        #print("method 1 pic box found")

        pic_box.send_keys(image())
        #print("METHOD1")
        randomizer_t()
    except:
        print("VAR ERROR: pic_box not working.")



def postbutton(driver):
    post_button= WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div/div[3]/div[3]/div/div/div/div[1]/div/span/span")))
    #print("post button found")
        
    post_button.click()
    #print("post button clicked")

    randomizer_t()


# LOADING FUNCTIONS

def opt():
    #print("Options Loaded")
    options = Options() 
    options.add_argument("--log-level=3")
    options.add_argument("--headless=new")      # Se puede desactivar para testing
    options.add_argument("--disable-gpu")       # Se puede desactivar para testing
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    return options


def cookies(driver):
    if "cookies.pkl" in os.listdir():
        #print("Cookies found, no manual login")

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for i in cookies:
            driver.delete_all_cookies()

            for i in cookies:
                cookie_dict = {
                    "domain": i["domain"],
                    "httponly": i["httponly"],
                    "name": i["name"],
                    "path": i["path"],
                    "samesite": i["samesite"],
                    "secure": i["secure"],
                    "value": i["value"]
                }

                driver.add_cookie(cookie_dict)

        driver.refresh()
            

    else:
        try:
            WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div[1]/span")))
            #print(driver.get_cookies())
            cookies = driver.get_cookies()

            formatted_cookies = []
            for i in cookies:
                formatted_cookies.append({
                    'domain': i.get('domain'),
                    'expiry': i.get('expiry'),
                    'httponly': i.get('httponly'),
                    'name': i.get('name'),
                    'path': i.get('path'),
                    'samesite': i.get('samesite'),
                    'secure': i.get('secure'),
                    'value': i.get('value')
            })

            pickle.dump(formatted_cookies, open("cookies.pkl", "wb"))
            #orden cookies: domain, expiry, httponly, name, path, samesite, secure, value

        except selenium.common.exceptions.TimeoutException:
            print("User must have logged in, execute again and login for starting correctly.")


def image():
    print("Looking for images...")

    file_types = ('*.jpg', '*.png', '*.gif', '*.mp4', '*.wav', '*.webm')

    files = []
    curr = os.getcwd()

    try:
        for i in file_types:
            files.extend(glob.glob(os.path.join(curr, i)))
            
            if files:
                image = files[0]
                print("Image found")
                return image
            
            else:
                print("Not image was found")

    except:
        print("ERROR LOADING/SEARCHING AN IMAGE")


def text():

    print("loading message")

    try:
        text_file = open("mensaje.txt", 'r', encoding="utf8")
        text = text_file.read()
        text_file.close()
        return text
    
    except FileNotFoundError:
        try:
            text_file = open("msg.txt", 'r', encoding="utf8")
            text = text_file.read()
            text_file.close()
            return text

        except FileNotFoundError:
            if os.name == "nt":
                os.system("cls")
                print('The Text (.txt) file with the message must be named as "mensaje" or "msg""')


def groups():
    print("loading groups... / Cargando Grupos...")

    try:
        with open("grupos.txt", 'r', encoding="utf8") as groups_file:
            groups = groups_file.readlines()
            print(f"{len(groups)} groups loaded / {len(groups)} grupos cargados")
            
            if not groups: 
                print("No text was found in the text file") 
                return [] 
            
            return groups 
            
    except FileNotFoundError:
        try:
            with open("groups.txt", 'r', encoding="utf8") as groups_file:
                groups = groups_file.readlines() 
            
            if not groups: 
                print("No groups were found in the text file") 
                return [] 
            
            return groups


        except FileNotFoundError:
            if os.name == "nt":
                os.system("cls")
                print('the groups file must be named "grupos" or "groups" for being located') 
            else:
                os.system("clear")
                print('the data file must be named "grupos" or "groups" for being located') 

        except Exception as e: 
            if os.name == "nt":
                os.system("cls")
                print(f"An error occurred: {e}") 
                return []
        else:
            os.system("clear")
            print(f"An error occurred: {e}") 
            return []
    
    except Exception as e: 
        if os.name == "nt":
                os.system("cls")
                print(f"An error occurred: {e}") 
                return []
        else:
            os.system("clear")
            print(f"An error occurred: {e}") 
            return []       


def prof_chooser(driver):
    
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Haz clic en tu foto o añade una cuenta.')]")))
        print("Old login info loaded, need to login again")
        filepath = os.path.join(os.getcwd(), "cookies.pkl")
        os.remove(filepath)
        driver.delete_all_cookies()
        driver.refresh()
        cookies(driver)
    except:
        pass
    
    try:
        main_profile = WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Your profile']")))
        main_profile.click()
    except:
        print("Time Out: Facebook took too long to load, try again.")

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@role='list']")))

        profiles_name = ["Mantener el perfil actual"]
        profiles_list = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Switch to')]")

        profiles_name = ["Keep current profile"]
        profiles_name.extend([i.text for i in profiles_list])

        #print(profiles_name)
        #print(len(profiles_name))

        print("\n\n\n\n\n\nChoose the profile using the number of the profile: ")
        prof_counter = 0
        for i in profiles_name:
            print(f"{prof_counter}- {i}")
            prof_counter +=1


        choice = input(">> ")

        if 0 < int(choice) < prof_counter:
            choice = int(choice) - 1
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((profiles_list[choice]))).click()
        elif int(choice) == 0:
            print(".")
        else:
            print("Please select a valid option number...")
            prof_chooser()

    except:
        print("No extra profiles were found, keeping the current one.")