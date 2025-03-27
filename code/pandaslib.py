from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    if not isinstance(item, str):
        return float(item)
    cleaned = item.replace('$', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0  # or float('nan') depending on what you're trying to represent

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    try:
        dt = datetime.strptime(timestamp, "%m/%d/%Y")
        return dt.year
    except Exception:
        return None

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    
    if not isinstance(item, str):
        return item
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    if item.strip().lower() in possibilities:
        return 'United States'
    return item


if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

