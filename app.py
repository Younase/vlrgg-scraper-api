from requests.exceptions import RequestException
from contextlib import closing
from requests import get
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, request, send_file

app = Flask(__name__)

# Function to scrape the table from a webpage and convert it to DataFrame
def scrape_tn_stats(link: str) -> pd.DataFrame:
    #get page
    raw_html = None
    try:
        raw_html = simple_get(link)
    except Exception as error:
        print("an error occurred:", error)
    if raw_html is None:
        print("Error getting link")
        return None
    html = BeautifulSoup(raw_html, 'html.parser')
    stats = html.find_all(attrs={'class': 'wf-table'})[0]
    
    # remove team/flag from player name
    for td in stats.find_all('td', class_='mod-player'):
        # Find the <div> with class 'text-of'
        text_of_div = td.find('div', class_='text-of')
        
        if text_of_div:
            # Clear the <td> and keep only the content of the 'text-of' div
            td.clear()
            td.append(text_of_div)

    # change agent images to agent names
    for td in stats.find_all('td', class_='mod-agents'):
        #find all img
        agent_urls = td.find_all('img')
        try:
            plus_x = td.div.div.text
        except:
            plus_x = ''
        #clear the <td> 
        td.clear()
        
        td.append( " ".join(e["src"].split('/')[-1].split('.')[0] for e in agent_urls))
        td.append(' '+plus_x)

    table_html = str(stats)
    table_io = StringIO(table_html)
    df = pd.read_html(table_io)[0]

    return df


def simple_get(url):#retourne le contenu de l'url en argument
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):#verifie la validite de la page web
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


# Flask route to handle the CSV request
@app.route('/get_csv', methods=['GET'])
def get_csv():
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400
    print(url)

    # Get the CSV buffer
    tn_stats = scrape_tn_stats(url)
    
    # Convert the DataFrame to a CSV
    csv_buffer = BytesIO()
    tn_stats.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)  # Move to the start of the buffer
    
    # Send the CSV file as a download
    return send_file(csv_buffer, mimetype='text/csv', as_attachment=True, download_name='data.csv')

# Vercel requires the app to be exposed as 'app'
if __name__ == "__main__":
    app.run(debug=True)
