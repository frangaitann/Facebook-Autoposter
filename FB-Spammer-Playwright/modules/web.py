import asyncio, random, csv, re, math, pandas as pd
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
if __name__ != "__main__":
    from modules.misc import *
    
ok_counter= 0
error_counter= 0
groups_q= 0


# Main code, it defines the browser agent and manages the scripts running.
async def web(headless:bool = True, DEBUG:bool = False, AUTOPROF:bool = False):
    """Main code function, it defines the main browser agent and manages the other scripts for posting on every group found in groups list."""
    
    if DEBUG:
        print("\n------DEBUG MODE------")
        await DEBUG_FUNC()
    async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(
                headless=headless,  # MODIFY WITH DEBUG MODE
                args=[
                    '--log-level=3',
                    '--disable-gpu',
                    '--disable_notifications',
                    '--disable-search-engine-choice-screen',
                    '--disable-blink-features=AutomationControlled'
                ],
            )
            
            page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/134.0.0.0 Safari/537.36",
                locale="es-AR",
                timezone_id="America/Argentina/Buenos_Aires",
                        
            )
            
            await page.goto("https://www.facebook.com")
            
            await cookies(page, DEBUG)
            
            await page.mouse.wheel(0, random.uniform(23, 732))
            
            # Check if cookies are useful (No Anti-Automation algorithm interfered)
            try:
                if AUTOPROF:
                    await auto_profile(page, DEBUG)
                else:
                    await profile_chooser(page, DEBUG)
            except Exception as e:
                if DEBUG:
                    raise e
                await cookies_updater(DEBUG)
                await cookies(page, DEBUG)
                if AUTOPROF:
                    await auto_profile(page, DEBUG)
                else:
                    await profile_chooser(page, DEBUG)
                
            await random_sleeper()
            
            await group_loader(page, DEBUG)
            await paster(page, DEBUG)
            
            global ok_counter
            global error_counter
            
            print(f"{ok_counter}/{groups_q} were posted in | {error_counter} groups failed:")
            
            # for error in error counter --> print: group name, group link, Exception, lasted time
            
            
            
async def auto_profile(page, DEBUG:bool = False):
    """Selects the profile by itselfs by looking in credentials.env file for AUTOPROF key."""
    
    if DEBUG:
        await DEBUG_FUNC()
    prof = page.locator("//div[@aria-label='Your profile']")
    await prof.wait_for(timeout=15000)
    await prof.click()
    
    prof_list = page.locator("//html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div[@role='list']")
    await prof_list.wait_for(timeout=15000)
    
    profile = page.locator(f'//div[contains(@aria-label, "Switch to {os.environ.get("AUTOPROF_ELEMENT")}")]')
    await profile.wait_for(timeout=15000)
    await profile.click()



# Scripting for choosing profile    
async def profile_chooser(page, DEBUG:bool = False):
    """Profile Choosing function, it opens profiles list and lists them all for user selection."""
    
    if DEBUG:
        await DEBUG_FUNC()
    prof = page.locator("//div[@aria-label='Your profile']")
    await prof.wait_for(timeout=15000)
    await prof.click()
    
    prof_list = page.locator("//html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div[@role='list']")
    await prof_list.wait_for(timeout=15000)
    
    prof_list = await page.locator("//div[contains(@aria-label, 'Switch to')]").all_text_contents()
    prof_list.insert(0, "Keep current profile")
    
    
    print("\n\n\nChoose the profile using the number of the profile: \n")
    prof_counter = 0
    for i in prof_list:
        print(f"{prof_counter}- {i}")
        prof_counter +=1


    choice = input("\n>> ")

    if 0 < int(choice) < prof_counter:
        choice = int(choice) - 1
        await page.locator("//div[contains(@aria-label, 'Switch to')]").nth(choice).click()
    elif int(choice) == 0:
        print(".")
    else:
        print("Please select a valid option number...")
        profile_chooser(page, DEBUG)          
          


# Loads groups exporting them from facebook/groups directly to a .csv file
async def group_loader(page, DEBUG:bool = False):
    """Group Extract/Import function, it opens www.facebook.com/groups/joins, checks all your groups, appends them to a .csv file and use it for running the entire script"""
    
    if DEBUG:
        await DEBUG_FUNC()
    global groups_q
    
    await page.goto("https://www.facebook.com/groups/joins")
    group_amount_text = await page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/span/div/div[1]/h2/span/span").inner_text()
    group_amount = re.split(r"[\(\)]", group_amount_text)
    groups_q = int(group_amount[1])
    
    group_list = page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div[3]")
    await group_list.wait_for()
    
    
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        current_count = await group_list.locator("//div[@role='listitem']").count()
        if current_count >= int(group_amount[1]):
            break
    
    scroller_amount = lambda x: int(x)*1 /20
    for i in range(math.ceil(scroller_amount(group_amount[1]))+1):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(0.5)
            
    groups_dict= {"NAME": [], "URL": [],}
    counter = 0
    for i in range(int(group_amount[1])):
        groups_dict["NAME"].append(await group_list.locator("//div[@role='listitem']").nth(i).locator("a").nth(1).inner_text())
        groups_dict["URL"].append(await group_list.locator("//div[@role='listitem']").nth(i).locator("a").first.get_attribute("href"))
        counter += 1
        
    df = pd.DataFrame(groups_dict)
    df.to_csv("groups.csv", index=True, mode='w')
            
            

# Reads groups.csv file and iterates over each found group for pasting the message on them.
async def paster(page, DEBUG:bool = False):
    """Posting function, it takes the expected text & picture and post them in each group found in groups.csv"""
    
    if DEBUG:
        await DEBUG_FUNC()
    global ok_counter
    global error_counter
    
    file = open('groups.csv', newline='', encoding="utf-8")
    c_reader = csv.reader(file)
    time_list= []
    
    
    for row in c_reader:
        
        time= []
        for i in range(4):
            t = await random_sleeper(2, 8)
            t = float(f"{t:.2f}")
            time.append(t)
            
        total_time= sum(time)
        try:
            print(f"\n\n[{await timestamp()}] Working with group n°{int(row[0])+1} | {row[2]} ---------- {row[1]}")
            
            await page.goto(row[2])
            text_case= page.locator("//span[contains(text(), 'Foto/vídeo') or contains(text(), 'Photo/video') or contains(text(), 'Write something...')]")
            await text_case.wait_for()
            await text_case.click()
            
            await asyncio.sleep(time[0])
            await page.locator("//html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/p").fill(await text_loader(DEBUG)) # Writing/Pasting text
            
            await asyncio.sleep(time[1])
            await page.locator('//form[@method="POST"]//input[@type="file"]').set_input_files((await image_loader(DEBUG))) # Setting/Pasting the image
            
            await asyncio.sleep(time[2])
            await page.locator("//html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div/div[3]/div[3]/div/div/div/div[1]/div/span/span").click() # Clicking on "Post" button
            
            await asyncio.sleep(time[3])
            print(f"[{await timestamp()}] Completed group n°{int(row[0])+1} in {total_time:.2f}")
            time_list.append(sum(time))
            ok_counter += 1
            
        except Exception as e:
            if row[0] != "":
                print(f"[{await timestamp()}] Group n° {int(row[0])+1}, (Group {row[0]} in .CSV) failed after {total_time:.2f}.\n\n {e}")
                time_list.append(sum(time))
                error_counter += 1
            continue
        
            
if __name__ == "__main__":
    from misc import *
    #asyncio.run(web())
    asyncio.run(web(False, True))