# Sunbiz Parse Project for Campbell Property Management
Parses the sunbiz page to look for annual reports for Campbell Property Associations based on Associations' Tax IDs

## Steps To Run File
1. Download zip file under the green code button on Github.
2. Extract the zip file and open it as a folder.
3. Open up the command prompt and navigate to the folder using the "cd" command.
4. Once inside, paste this "venv\Scripts\activate" and press enter to activate the virtual environment.
5. Now run the scrape_web file by typing "python scrape_web.py" and pressing enter.
6. The file will ask for the excel file used to extract Tax IDs and save annual report data to.
7. Paste the file location like the example is shown.
8. The file will automatically go through each tax ID and mark if the 2026 annual report is there.
9. The file will then finish and you can open up the excel sheet to see the results.

## For Future Uses
Change the scraper API key in the code after paying for the ScraperAPI service here: https://www.scraperapi.com/. The key is in the .env file.<br>
Make sure the Tax Ids are in column E in the Association excel sheet.<br>
Update the code to 2027 or a different year if needed. 

## To update code
Open up the scrape_web.py file and you can change the code in any IDE (including Notepad).

