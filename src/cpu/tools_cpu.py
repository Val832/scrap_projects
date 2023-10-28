from src.cpu import Crawler

def missing_cpu_table (url): 

        res = Crawler.extract_html(url)
        table = Crawler.find(res, tag='table', method=1,
                             attrs_key='id', attrs_value='test-suite-results')

        missing_table = {}
        for row in table.findAll('tr'):
            header = row.find('th').text
            missing_table[header] = "NA"
        
        return missing_table

def fetch_cpu_data(url, missing_table, session):
    try :
        res = Crawler.extract_html(url)
        table = Crawler.find(res, tag='table', element_id='test-suite-results')
        data = {}
        for row in table.findAll('tr'):
            header = row.find('th').text
            value = row.find('td').text
            data[header] = value
        return data 
    except: 
        data = missing_table
        return data 