import asyncio
import os
from pyppeteer import launch

async def call(address, name):
  domain = 'http://' + address
  try:
    browser = await launch(ignoreHTTPSErrors=True,headless=False, slowMo=0, args=["--no-sandbox","--disable-setuid-sandbox","--disable-gpu","--disable-dev-shm-usage",'--proxy-server="direct://"',"--proxy-bypass-list=*"])
    page = await browser.newPage()
    await page.goto(domain)
    await page.screenshot({'path': name})
    await browser.close()
  except:
    pass


def shot(address, subdomain_resolver):
  new_address = 'researchdns.' + address
  filename = "/home/azureuser/collect/screenshots/" + address + "/"
  os.makedirs(os.path.dirname(filename), exist_ok=True)
#asyncio.ensure_future(main(address))
  name =  "/home/azureuser/collect/screenshots/" + address + "/" + address + '.png'
  asyncio.get_event_loop().run_until_complete(call(address, name))
  if subdomain_resolver:
    name =  "/home/azureuser/collect/screenshots/" + address + "/" + new_address + '.png'
    asyncio.get_event_loop().run_until_complete(call(new_address, name))
#image = Image.open('screen.png')
#image.show()
