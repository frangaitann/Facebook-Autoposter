from modules.web import *
from dotenv import load_dotenv


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv("credentials.env")
if os.environ.get("DEBUG") == "True":
    DEBUG = True
else:
    DEBUG = False
    

print("""___________     ___.     _________                                               ___  __      __        .__       .__     __    ___    
\_   _____/____ \_ |__  /   _____/__________    _____   _____   ___________     /  / /  \    /  \_______|__| ____ |  |___/  |_  \  \   
 |    __) \__  \ | __ \ \_____  \\____ \__  \  /     \ /     \_/ __ \_  __ \   /  /  \   \/\/   /\_  __ \  |/ ___\|  |  \   __\  \  \  
 |     \   / __ \| \_\ \/        \  |_> > __ \|  Y Y  \  Y Y  \  ___/|  | \/  (  (    \        /  |  | \/  / /_/  >   Y  \  |     )  ) 
 \___  /  (____  /___  /_______  /   __(____  /__|_|  /__|_|  /\___  >__|      \  \    \__/\  /   |__|  |__\___  /|___|  /__|    /  /  
     \/        \/    \/        \/|__|       \/      \/      \/     \/           \__\        \/            /_____/      \/       /__/ """)

asyncio.run(web(DEBUG=DEBUG))


# Add:
# Exceptions
# Clean Code
# Others
# Change DEBUG System
# Logs
# Many copys & Images
