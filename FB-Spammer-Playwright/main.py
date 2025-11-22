from modules.web import *
from dotenv import load_dotenv


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv("credentials.env")
if os.environ.get("DEBUG") == "True":
    DEBUG= True
else:
    DEBUG= False
    
if os.environ.get("AUTOPROF") == "True":
    AUTOPROF= True
else:
    AUTOPROF= False
    

print(""" __    __      _       _     _   __                                           
/ / /\ \ \_ __(_) __ _| |__ | |_/ _\_ __   __ _ _ __ ___  _ __ ___   ___ _ __ 
\ \/  \/ / '__| |/ _` | '_ \| __\ \| '_ \ / _` | '_ ` _ \| '_ ` _ \ / _ \ '__|
 \  /\  /| |  | | (_| | | | | |__\ \ |_) | (_| | | | | | | | | | | |  __/ |   
  \/  \/ |_|  |_|\__, |_| |_|\__\__/ .__/ \__,_|_| |_| |_|_| |_| |_|\___|_|   
                 |___/             |_|                                        """)

asyncio.run(web(DEBUG=DEBUG, AUTOPROF=AUTOPROF))


# Add:
# Exceptions
# Clean Code
# Others
# Change DEBUG System
# Logs
# Many copys & Images
