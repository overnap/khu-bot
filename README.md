# khu-bot
A Discord notification bot for Kyunghee Univ CE students  
It automatically crawls various information of the university, and alerts via discord when new posts are posted.  

경희대학교 컴퓨터공학과 학생을 위한 디스코드 알림 봇  
대학생활을 하면서 필요한 여러 정보를 크롤링하고 디스코드를 통해 알림해줍니다.  
2020년 1학기 웹파이썬 과목에서 진행한 텀프로젝트입니다.

![post](https://user-images.githubusercontent.com/61305403/88489283-6866c680-cfce-11ea-9722-2f51ce9f1612.PNG)
![meal](https://user-images.githubusercontent.com/61305403/88489278-613fb880-cfce-11ea-88a9-623b6276de97.PNG)

Target:
- Kyunghee University undergraduate announcements (especially common and international campus post)
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

Tested in Python 3.7.*.


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
You can turn the j dormitory diet notification on and off with the command ```!meal```.  
Send ```!stop``` when you want to stop working.  

Command prefix ```!``` and the 10 minutes delay can be modified in config.
