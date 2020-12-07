import requests
import time
from twilio.rest import Client
from bs4 import BeautifulSoup

account_sid = 'AC5a7504e19c21e199ccb005f6c8211266' 
auth_token = '212d3bdfe0a84d182d522b117086890e' 
client = Client(account_sid, auth_token) 

URL = 'https://moredrops.cl/Drops/c/dropsCategories?sort=creationtime&q=%3Arelevance#'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

if __name__ == "__main__":
    
    while True:
        
        try:
            
            response = requests.get(URL, headers=HEADERS)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            content = soup.find('div', attrs={'class' : 'details'})
            
            time.sleep(30)
            
            new_response = requests.get(URL, headers=HEADERS)
            
            new_soup = BeautifulSoup(new_response.text, 'html.parser')
            
            new_content = new_soup.find('div', attrs={'class' : 'details'})
            
            if content == new_content:
                print("La pag sigue igual.")
                continue
            
            else:
                
                for wrapper in soup.find_all('div', attrs={'class' : 'main__inner-wrapper'}):
                    details = wrapper.find('div', attrs={'class' : 'details'})
                    
                    find_attrs = details.find_all("a")[0].attrs
                    
                    sneaker_href = find_attrs.get('href')
                    sneaker_prelink = "https://moredrops.cl"
                    
                    sneaker_link = sneaker_prelink + sneaker_href
                    sneaker_name = details.find('a', attrs={'class' : 'name'}).get_text(separator='').rstrip().strip()
                    
                    message = client.messages.create( 
                        from_='whatsapp:+14155238886',  
                        body='NUEVAS ZAPATILLAS: {a}\nLINK: {b}'.format(a=sneaker_name,b=sneaker_link),      
                        to='whatsapp:+56948594296',
                    )   
                    print(message.sid)
                    print(sneaker_name)
                    continue

        except:
            print("Algo ha fallado")
            continue



