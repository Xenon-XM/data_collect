import urllib.request, ssl
import re, sqlite3, time, sys, socket

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
request_timeout = 5
error_retry = 3

def http_get(hyperlink):

  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE

  for i in range(error_retry):
    try:
      req = urllib.request.Request(hyperlink, headers={'User-Agent': user_agent}, data=None)
      response = urllib.request.urlopen(req, context=ctx, timeout=request_timeout)
      return response.read().decode('utf-8')

    except Exception as e:
      sys.stderr.write('error: http_get()\n')
      time.sleep(2)
  return 0


# params: {'key1':'val1','key2':'val2'}
def http_post(hyperlink, params):

  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  for i in range(error_retry):
    try:
      req = urllib.request.Request(hyperlink, headers={'User-Agent': user_agent}, data=urllib.parse.urlencode(params).encode() )
      response = urllib.request.urlopen(req, context=ctx, timeout=request_timeout)
      return response.read().decode('utf-8')

    except Exception as e:
      sys.stderr.write('error: http_post()\n')
      time.sleep(2)




def alexa_rank(website):
  text_res = http_get('https://www.alexa.com/siteinfo/' + website)

# find global rank
  m1 = re.search(r'"global": ([\d,]+?),', text_res, re.MULTILINE | re.IGNORECASE | re.DOTALL)
  if m1:
    global_rank = m1.group(1)
   # print(website, 'Global rank:', global_rank, sep=' ')
    return global_rank


# if not ranked by alexa
  if not m1:
    return -1


