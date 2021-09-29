from posixpath import split
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import os

driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.youtube.com/playlist?list=PLDoPjvoNmBAxzNO8ixW83Sf8FnLy_MkUT")
content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, "lxml")
links = soup.find_all('span',class_='style-scope ytd-thumbnail-overlay-time-status-renderer')
number_of_videos = soup.find_all('span',class_='style-scope yt-formatted-string')
PlaylistTitle = soup.find('a',class_='yt-simple-endpoint style-scope yt-formatted-string')


minutes = []
seconds = []
Indexs=[]
hours=[]
for i in range(len(links)):
    duration=links[i].text
    duration_no_tap=duration[3:-1]
    spliting_for_loop =[]
    for n in range(len(duration_no_tap)):
        if duration_no_tap[n]==":":
            spliting_for_loop.append(n)

    if len(spliting_for_loop)==2:
        hours.append(duration_no_tap[:spliting_for_loop[0]])
        minutes.append(duration_no_tap[spliting_for_loop[0]:spliting_for_loop[1]])
        seconds.append(duration_no_tap[spliting_for_loop[1]:])

    else:
        minutes.append(duration_no_tap[:spliting_for_loop[0]])
        seconds.append(duration_no_tap[spliting_for_loop[0]+1:])
            


driver.quit()

seconds_without_zero=[]
for i in range(len(seconds)):
    with_zero = seconds[i]
    without_zero=''
    if with_zero[0]=="0":
        without_zero=with_zero[1:]
        seconds_without_zero.append(without_zero)

    else:
        seconds_without_zero.append(with_zero)

    
#print(seconds_without_zero)



all_seconds=0
for i in range(len(seconds_without_zero)):
    if ":" in seconds_without_zero[i]:
        withoutPoints=seconds_without_zero[i]
        all_seconds=all_seconds+int(withoutPoints[1:])
    else:
        all_seconds=all_seconds+int(seconds_without_zero[i])




all_minutes = 0
for i in range(len(minutes)):
    if ':' in minutes[i]:
        minute_wtihout_points=minutes[i]
        all_minutes=all_minutes+int(minute_wtihout_points[1:])

    else:
        all_minutes=all_minutes+int(minutes[i])





all_hours=0
for i in range (len(hours)):
    if ':' in hours[i]:
        hours_wtihout_points=hours[i]
        all_hours=all_hours+int(hours_wtihout_points[1:])

    else:
        all_hours=all_hours+int(hours[i])


full_playlist_duration=all_hours+all_minutes/60+all_seconds/3600
string_full_playlist_duration=str(full_playlist_duration)


for i in range(len(string_full_playlist_duration)):
    if string_full_playlist_duration[i]=='.':
        if len(string_full_playlist_duration)>i+3:
            specified_string_full_playlist_duration = string_full_playlist_duration[:i+3]
            break
        else:
            specified_string_full_playlist_duration = string_full_playlist_duration 
            break
        
        

updates=''
for i in range(1,len(number_of_videos)):
    updates=updates+number_of_videos[i].text


os.chdir('D:\\python scripts\\keyword code')
file= open(PlaylistTitle.text+'.txt','w')



file.write('playlist duration is  ' + specified_string_full_playlist_duration +'  hours\n' )
file.write( 'number of videos =  ' + number_of_videos[0].text + '\n')
file.write( 'status of latest update('+  updates  + ' )')


file.close()
