import requests as rq
from bs4 import BeautifulSoup
def download_videos(url, outputPath):
    mp4Content = rq.get(url, stream=True)
    if mp4Content.status_code == 200:
        with open(outputPath, "wb") as file:
            file.write(mp4Content.content)
            print("Download success!")
    else:
        print("Failed to download a file!")


SDDatascrapePath = rf"C:\Users\Trent\coding\python projects\San Diego Data Scrape"
siteUrl = "https://sandiego.granicus.com/ViewPublisher.php?view_id=8"
site = rq.get(siteUrl).text
soup = BeautifulSoup(site, "html.parser")
table = soup.find("tbody")
trs = table.find_all("tr")
for tr in trs[77:89]:
    td = tr.find_all("td")
    date = td[1].text
    print(date)
    anchor = tr.find_all("a")
    mp4Url = anchor[1]['href']
    download_videos(mp4Url, rf"{SDDatascrapePath}\{date}.mp4")
