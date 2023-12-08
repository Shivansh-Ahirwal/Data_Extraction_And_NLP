import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests

def main():
    urls = pd.read_csv("C:\\Users\\Sachi\\Downloads\\Input.xlsx - Sheet1.csv")
    
    def article_scraper(urls,i):
        url = urls['URL'][i]  # Replace with the target website URL
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text from all <p> tags
            all_p_text = [p.get_text(strip=True) for p in soup.find_all('p')]

            # creating txt file with url_id
            filename = 'C:\\Users\\Sachi\\sunny projects\\blackcoffee_project\\output_files\\' + str(urls['URL_ID'][i])
            file = open(filename,'w',encoding = "utf-8")
            final_output = []

            final_output.append(all_p_text[1])
            
            for text in all_p_text[16:]:
                final_output.append(text)
            for items in final_output:
                file.write(items)
            file.close()
        else:
            print(f'Failed to retrieve the page. Status code: {response.status_code}')
    
    for i in range(0,113):
        article_scraper(urls,i)
       
if "__name__"=="__main__":
    
    main()