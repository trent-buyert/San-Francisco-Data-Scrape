from bs4 import BeautifulSoup
import requests as rq
import os

url = "https://www.sandiego.gov/planning-commission/documents/agenda"

archiveUrl = "https://www.sandiego.gov/planning-commission/documents/agenda/archive"
baseSite = "https://www.sandiego.gov"
SDDatascrapePath = rf"C:\Users\Trent\coding\python projects\San Diego Data Scrape"
years = ['2022', '2023', '2024']
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# creating file structure
for year in years:
    for month in months:
        if not os.path.exists(rf"{SDDatascrapePath}\{year}\{month}"):
            os.makedirs(rf"{SDDatascrapePath}\{year}\{month}")

#2024 data scrape
agendaHtml = rq.get(url + "/archive").text
soup = BeautifulSoup(agendaHtml, "html.parser")
table = soup.find(class_="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item")
anchors = table.find_all("a")
for anchor in anchors:
    if 'agenda' in anchor['href'] or 'Agenda' in anchor['href']:
        if 'Public' not in anchor.text:
            agendaPath = f"{baseSite}{anchor['href']}"
            date = anchor.text.split("2024")[0] + "2024"
            if 'Adjourned' not in anchor.text:
                meetingType = 'Regular'
            else:
                meetingType = "Adjourned"
            filename = f"{date}_Meeting {meetingType} Agenda_Planning Commission"
            agenda = rq.get(agendaPath)
            if agenda.status_code == 200:
                for month in months:
                    if month in date:
                        currentMonth = month
                        break
                outputAgendaPath = rf"{SDDatascrapePath}\2024\{currentMonth}\{filename}.pdf"
                with open(outputAgendaPath, "wb") as file:
                    print(f"{filename} written.")
                    file.write(agenda.content)


#2023 and 2022 data scrape

agendaHtml = rq.get(url + "/archive").text
soup = BeautifulSoup(agendaHtml, "html.parser")
# table = soup.find(class_="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item")
unorderedLists = soup.find_all("ul")
for ul in unorderedLists[39:62]:
    listItems = ul.find_all("li")
    for li in listItems:
        anchors = li.find_all("a")
        for anchor in anchors:
            if 'Comment' not in anchor.text and 'comment' not in anchor.text:
                agendaUrl = anchor['href']
                if agendaUrl[2] == 'w':
                    agendaPath = f"https:{agendaUrl}"
                    print(agendaPath)
                else:
                    agendaPath = f"{baseSite}{agendaUrl}"
                    print(agendaPath)
                if 'Adjourned' in anchor.text:
                    meetingType = "Adjourned"
                else:
                    meetingType = "Regular"
                if '2023' in anchor.text:
                    year = '2023'
                else:
                    year = '2022'
                date = f"{anchor.text.split("202")[0]}{year}"
                filename = f"{date}_Meeting {meetingType} Agenda_Planning Commission"
                agenda = rq.get(agendaPath)
                if agenda.status_code == 200:
                    for month in months:
                        if month in date:
                            currentMonth = month
                            break
                    outputAgendaPath = rf"{SDDatascrapePath}\{year}\{currentMonth}\{filename}.pdf"
                    with open(outputAgendaPath, "wb") as file:
                        print(f"{filename} written.")
                        file.write(agenda.content)


