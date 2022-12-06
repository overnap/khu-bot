# khu-bot
A Discord notification bot for Kyunghee Univ CE students  
It automatically crawls various information of the university, and alerts via discord when new posts are posted.  

![post](https://user-images.githubusercontent.com/61305403/88489283-6866c680-cfce-11ea-9722-2f51ce9f1612.PNG)
![meal](https://user-images.githubusercontent.com/61305403/88489278-613fb880-cfce-11ea-88a9-623b6276de97.PNG)

Targets:
- Kyunghee University undergraduate announcements
- Kyunghee College of Software announcements
- Kyunghee software business group announcements
- Kyunghee second dormitory (aka J dormitory) announcements
- Kyunghee second dormitory meal

## Requirements
```
pip install -r requirements.txt
```

Need Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases) to get Selenium to work.  
(probably need Firefox 55+ for headless mode.)

Tested in Python 3.8.*.


## Usage
Enter the bot token in config.json.  
```json
{
  "TOKEN": "Enter your own discord bot token",
  "DELAY": 600,
  "PREFIX": "!"
}
```

Then run:  
```
$ python main.py
```

Invite the bot to the server and send ```!start``` message on the desired chat channel.  
This will update the information every 10 minutes and give you a useful alarm.  
You can turn the specific notification on and off with commands ```!dormitory```, ```!undergraduate``` and so on.  

It support Korean commands such as ```!시작```, ```!단과대``` and ```!학식```.  
Command prefix ```!``` and the 10 minutes delay can be modified in config.  
Use ```!help``` to see a list of commands.
