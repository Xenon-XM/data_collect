from Wappalyzer import Wappalyzer, WebPage

def wapp_analyze(domain):
    wappalyzer = Wappalyzer.latest()
    address = 'https://' + domain
    try:
        webpage = WebPage.new_from_url(address)
        result = wappalyzer.analyze_with_categories(webpage)
    except:
        result = 0 
    return result