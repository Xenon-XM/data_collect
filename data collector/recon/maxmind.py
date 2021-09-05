from geoip2_tools.manager import Geoip2DataBaseManager
geoip2_manager = Geoip2DataBaseManager('MAXMIND KEY')

def maxmind_info(address):
  maxmind={}
  try:
    maxmind['country'] = geoip2_manager['country'].reader.country(address).country.name
  except:
    maxmind['country'] = 0
  try:
    maxmind['city'] = geoip2_manager['city'].reader.city(address).city.name
  except:
    maxmind['city'] = 0
  try:
    maxmind['asn'] = geoip2_manager['asn'].reader.asn(address).autonomous_system_organization
  except:
    maxmind['asn'] = 0
  return maxmind
