import pickle, os, asyncio, random, tz, datetime, zoneinfo, glob, inspect
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from dotenv import load_dotenv

tz = zoneinfo.ZoneInfo("America/Buenos_Aires")



async def DEBUG_FUNC():
    """Debug Function, just used for knowing what's running currently."""
    
    running_func= inspect.stack()
    print(f"[{await timestamp()}]   RUNNING {running_func[1].function}")



async def cookies_pickle_dumper(page, DEBUG:bool = False):
    """Gets & dumps facebook cookies into a .pkl file named cookies.pkl"""
    
    if DEBUG:
        await DEBUG_FUNC()
    cookies = await page.context.cookies("https://www.facebook.com")

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

    os.remove("cookies.pkl")
    pickle.dump(formatted_cookies, open("cookies.pkl", "wb"))



async def cookies_updater(DEBUG:bool = False):
    """Function used for updating cookies if Facebook anti-automation algorithm ruined the previous ones"""
    
    if DEBUG:
        await DEBUG_FUNC()
    async with Stealth().use_async(async_playwright()) as p:    # Starts a new browser in headless False for user loggin in and saving a new cookies.pkl file
            cookies_browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--log-level=3',
                    '--disable-gpu',
                    '--disable_notifications',
                    '--disable-search-engine-choice-screen',
                    '--disable-blink-features=AutomationControlled'
                ],
            )
            
            cookies_page = await cookies_browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/134.0.0.0 Safari/537.36",
                locale="es-AR",
                timezone_id="America/Argentina/Buenos_Aires",
                        
            )
            await cookies_page.set_viewport_size({"width": 1920, "height": 1080})
            await cookies_page.goto("https://www.facebook.com")
            
            if os.path.exists("credentials.env"):
                await cookies_page.locator("id=email").fill(os.environ.get("EMAIL"))
                await cookies_page.locator("id=pass").fill(os.environ.get("PASSWORD"))
                await cookies_page.locator("id=pass").press("Enter")
                print("Credentials found, auto-login done.")
            
            try:
                facebook_nav = cookies_page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]")
                await facebook_nav.wait_for(timeout=300000)
                await cookies_pickle_dumper(cookies_page, DEBUG)
                await asyncio.sleep(0.5)
                await cookies_page.context.close()
            except Exception as e:
                print(f"{e}\n\nLogin Timeout (5 min), run script again.")
                
            



async def text_loader(DEBUG:bool = False):
    
    if DEBUG:
        await DEBUG_FUNC()
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
            else:
                os.system("clear")
            print('The Text (.txt) file with the message must be named as "mensaje" or "msg""')


async def image_loader(DEBUG:bool = False):
    
    if DEBUG:
        await DEBUG_FUNC()
    file_types = ('*.jpg', '*.png', '*.gif', '*.mp4', '*.wav', '*.webm')
    files = []
    curr = os.getcwd()

    try:
        for i in file_types:
            files.extend(glob.glob(os.path.join(curr, i)))
            
            if files:
                image = files[0]
                return image
            
            else:
                print("Not image was found")

    except:
        print("ERROR LOADING OR LOOKING FOR AN IMAGE")



async def timestamp():
    date = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    return date



async def random_sleeper(min_t:int = 4 ,max_t:int = 16):
    sleeping_time= random.uniform(min_t, max_t)
    await asyncio.sleep(sleeping_time)
    return sleeping_time


async def cookies(page, DEBUG:bool = False):
    """Function used for loading cookies from cookies.pkl file"""
    
    if DEBUG:
        await DEBUG_FUNC()
    if "cookies.pkl" in os.listdir():

        cookies = pickle.load(open("cookies.pkl", "rb"))
        await page.context.clear_cookies()
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

            await page.context.add_cookies([cookie_dict])

        await page.reload()
        
if __name__ == "__main__":
    asyncio.run(cookies_updater())