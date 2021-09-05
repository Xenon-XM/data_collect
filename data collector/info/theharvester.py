#!/usr/bin/env python3

from info.theHarvester.theHarvester.discovery import *
from info.theHarvester.theHarvester.discovery import dnssearch, takeover, shodansearch
from info.theHarvester.theHarvester.discovery.constants import *
from info.theHarvester.theHarvester.lib import hostchecker
from info.theHarvester.theHarvester.lib import reportgraph
from info.theHarvester.theHarvester.lib import stash
from info.theHarvester.theHarvester.lib import statichtmlgenerator
from info.theHarvester.theHarvester.lib.core import *
import argparse
import asyncio
import datetime
import netaddr
import re
import sys
from platform import python_version

all_emails: list = []
all_hosts: list = []
all_ip: list = []
all_people: list = []
async def start(domain):
   
    try:
        db = stash.StashManager()
        await db.do_init()
    except Exception:
        pass

   
    full: list = []
    ips: list = []
    google_dorking = False
    host_ip: list = []
    limit = 200
    shodan = False
    start = 0
    all_urls: list = []
    
    word=str(domain)
    
    use_proxy = False

    async def store(search_engine: Any, source: str, process_param: Any = None, store_host: bool = False,
                    store_emails: bool = False, store_ip: bool = False, store_people: bool = False,
                    store_links: bool = False, store_results: bool = False) -> None:
        """
        Persist details into the database.
        The details to be stored is controlled by the parameters passed to the method.

        :param search_engine: search engine to fetch details from
        :param source: source against which the details (corresponding to the search engine) need to be persisted
        :param process_param: any parameters to be passed to the search engine eg: Google needs google_dorking
        :param store_host: whether to store hosts
        :param store_emails: whether to store emails
        :param store_ip: whether to store IP address
        :param store_people: whether to store user details
        :param store_links: whether to store links
        :param store_results: whether to fetch details from get_results() and persist
        """
        await search_engine.process(use_proxy) if process_param is None else await \
            search_engine.process(process_param, use_proxy)
        db_stash = stash.StashManager()
        if source == 'suip':
            print(f'\033[94m[*] Searching {source[0].upper() + source[1:]} this module can take 10+ min but is worth '
                  f'it. \033[0m')
        else:
            print(f'\033[94m[*] Searching {source[0].upper() + source[1:]}. \033[0m')
        if store_host:
            host_names = [host for host in filter(await search_engine.get_hostnames()) if f'.{word}' in host]
            if source != 'hackertarget' and source != 'pentesttools' and source != 'rapiddns':
                # If source is inside this conditional it means the hosts returned must be resolved to obtain ip
                full_hosts_checker = hostchecker.Checker(host_names)
                temp_hosts, temp_ips = await full_hosts_checker.check()
                ips.extend(temp_ips)
                full.extend(temp_hosts)
            else:
                full.extend(host_names)
            all_hosts.extend(host_names)
            await db_stash.store_all(word, all_hosts, 'host', source)
        if store_emails:
            email_list = filter(await search_engine.get_emails())
            all_emails.extend(email_list)
            await db_stash.store_all(word, email_list, 'email', source)
        if store_ip:
            ips_list = await search_engine.get_ips()
            all_ip.extend(ips_list)
            await db_stash.store_all(word, all_ip, 'ip', source)
        if store_results:
            email_list, host_names, urls = await search_engine.get_results()
            all_emails.extend(email_list)
            host_names = [host for host in filter(host_names) if f'.{word}' in host]
            all_urls.extend(filter(urls))
            all_hosts.extend(host_names)
            await db.store_all(word, all_hosts, 'host', source)
            await db.store_all(word, all_emails, 'email', source)
        if store_people:
            people_list = await search_engine.get_people()
            await db_stash.store_all(word, people_list, 'people', source)
            all_people.extend(people_list)
            if len(people_list) == 0:
                print('\n[*] No users found.\n\n')
           # else:
           #     print('\n[*] Users found: ' + str(len(people_list)))
            #    print('---------------------')
            #    for usr in sorted(list(set(people_list))):
            #        print(usr)
            
        if store_links:
            links = await search_engine.get_links()
            await db.store_all(word, links, 'name', engineitem)

    stor_lst = []

    input="baidu,bing,bufferoverun,certspotter,crtsh,dnsdumpster,duckduckgo,exalead,google,hackertarget,linkedin,linkedin_links,netcraft,omnisint,otx,qwant,rapiddns,sublist3r,threatcrowd,threatminer,twitter,urlscan,virustotal,yahoo"
    engines = engines = sorted(set(map(str.strip, input.split(','))))
    if set(engines).issubset(Core.get_supportedengines()):
        print(f'\033[94m[*] Target: {word} \n \033[0m')

        for engineitem in engines:
            if engineitem == 'baidu':
                from info.theHarvester.theHarvester.discovery import baidusearch
                try:
                    baidu_search = baidusearch.SearchBaidu(word, limit)
                    stor_lst.append(store(baidu_search, engineitem, store_host=True, store_emails=True))
                except Exception:
                    pass

            elif engineitem == 'bing' or engineitem == 'bingapi':
                from info.theHarvester.theHarvester.discovery import bingsearch
                try:
                    bing_search = bingsearch.SearchBing(word, limit, 0)
                    bingapi = ''
                    if engineitem == 'bingapi':
                        bingapi += 'yes'
                    else:
                        bingapi += 'no'
                    stor_lst.append(
                        store(bing_search, 'bing', process_param=bingapi, store_host=True, store_emails=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)
                    else:
                        print(e)

            elif engineitem == 'bufferoverun':
                from info.theHarvester.theHarvester.discovery import bufferoverun
                try:
                    bufferoverun_search = bufferoverun.SearchBufferover(word)
                    stor_lst.append(store(bufferoverun_search, engineitem, store_host=True, store_ip=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'censys':
                from info.theHarvester.theHarvester.discovery import censys
                try:
                    censys_search = censys.SearchCensys(word)
                    stor_lst.append(store(censys_search, engineitem, store_host=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)

            elif engineitem == 'certspotter':
                from info.theHarvester.theHarvester.discovery import certspottersearch
                try:
                    certspotter_search = certspottersearch.SearchCertspoter(word)
                    stor_lst.append(store(certspotter_search, engineitem, None, store_host=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'crtsh':
                try:
                    from info.theHarvester.theHarvester.discovery import crtsh
                    crtsh_search = crtsh.SearchCrtsh(word)
                    stor_lst.append(store(crtsh_search, 'CRTsh', store_host=True))
                except Exception as e:
                    print(f'\033[93m[!] A timeout occurred with crtsh, cannot find {args.domain}\n {e}\033[0m')

            elif engineitem == 'dnsdumpster':
                try:
                    from info.theHarvester.theHarvester.discovery import dnsdumpster
                    dns_dumpster_search = dnsdumpster.SearchDnsDumpster(word)
                    stor_lst.append(store(dns_dumpster_search, engineitem, store_host=True))
                except Exception as e:
                    print(f'\033[93m[!] An error occurred with dnsdumpster: {e} \033[0m')

            elif engineitem == 'duckduckgo':
                from info.theHarvester.theHarvester.discovery import duckduckgosearch
                duckduckgo_search = duckduckgosearch.SearchDuckDuckGo(word, limit)
                stor_lst.append(store(duckduckgo_search, engineitem, store_host=True, store_emails=True))

            elif engineitem == 'exalead':
                from info.theHarvester.theHarvester.discovery import exaleadsearch
                exalead_search = exaleadsearch.SearchExalead(word, limit, 0)
                stor_lst.append(store(exalead_search, engineitem, store_host=True, store_emails=True))

            elif engineitem == 'github-code':
                try:
                    from info.theHarvester.theHarvester.discovery import githubcode
                    github_search = githubcode.SearchGithubCode(word, limit)
                    stor_lst.append(store(github_search, engineitem, store_host=True, store_emails=True))
                except MissingKey as ex:
                    print(ex)
                else:
                    pass

            elif engineitem == 'google':
                from info.theHarvester.theHarvester.discovery import googlesearch
                google_search = googlesearch.SearchGoogle(word, limit, 0)
                stor_lst.append(store(google_search, engineitem, process_param=google_dorking, store_host=True,
                                        store_emails=True))

            elif engineitem == 'hackertarget':
                from info.theHarvester.theHarvester.discovery import hackertarget
                hackertarget_search = hackertarget.SearchHackerTarget(word)
                stor_lst.append(store(hackertarget_search, engineitem, store_host=True))

            elif engineitem == 'hunter':
                from info.theHarvester.theHarvester.discovery import huntersearch
                # Import locally or won't work.
                try:
                    hunter_search = huntersearch.SearchHunter(word, limit, 0)
                    stor_lst.append(store(hunter_search, engineitem, store_host=True, store_emails=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)
                    else:
                        pass

            elif engineitem == 'intelx':
                from info.theHarvester.theHarvester.discovery import intelxsearch
                # Import locally or won't work.
                try:
                    intelx_search = intelxsearch.SearchIntelx(word)
                    stor_lst.append(store(intelx_search, engineitem, store_host=True, store_emails=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)
                    else:
                        print(f'An exception has occurred in Intelx search: {e}')

            elif engineitem == 'linkedin':
                from info.theHarvester.theHarvester.discovery import linkedinsearch
                linkedin_search = linkedinsearch.SearchLinkedin(word, limit)
                stor_lst.append(store(linkedin_search, engineitem, store_people=True))

            elif engineitem == 'linkedin_links':
                from info.theHarvester.theHarvester.discovery import linkedinsearch
                linkedin_links_search = linkedinsearch.SearchLinkedin(word, limit)
                stor_lst.append(store(linkedin_links_search, 'linkedin', store_links=True))

            elif engineitem == 'netcraft':
                from info.theHarvester.theHarvester.discovery import netcraft
                netcraft_search = netcraft.SearchNetcraft(word)
                stor_lst.append(store(netcraft_search, engineitem, store_host=True))

            elif engineitem == 'omnisint':
                from info.theHarvester.theHarvester.discovery import omnisint
                try:
                    omnisint_search = omnisint.SearchOmnisint(word, limit)
                    stor_lst.append(store(omnisint_search, engineitem, store_host=True, store_ip=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'otx':
                from info.theHarvester.theHarvester.discovery import otxsearch
                try:
                    otxsearch_search = otxsearch.SearchOtx(word)
                    stor_lst.append(store(otxsearch_search, engineitem, store_host=True, store_ip=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'pentesttools':
                from info.theHarvester.theHarvester.discovery import pentesttools
                try:
                    pentesttools_search = pentesttools.SearchPentestTools(word)
                    stor_lst.append(store(pentesttools_search, engineitem, store_host=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)
                    else:
                        print(f'An exception has occurred in PentestTools search: {e}')

            elif engineitem == 'projectdiscovery':
                from info.theHarvester.theHarvester.discovery import projectdiscovery
                try:
                    projectdiscovery_search = projectdiscovery.SearchDiscovery(word)
                    stor_lst.append(store(projectdiscovery_search, engineitem, store_host=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)
                    else:
                        print('An exception has occurred in ProjectDiscovery')

            elif engineitem == 'qwant':
                from info.theHarvester.theHarvester.discovery import qwantsearch
                qwant_search = qwantsearch.SearchQwant(word, 0, limit)
                stor_lst.append(store(qwant_search, engineitem, store_host=True, store_emails=True))

            elif engineitem == 'rapiddns':
                from info.theHarvester.theHarvester.discovery import rapiddns
                try:
                    rapiddns_search = rapiddns.SearchRapidDns(word)
                    stor_lst.append(store(rapiddns_search, engineitem, store_host=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'securityTrails':
                from info.theHarvester.theHarvester.discovery import securitytrailssearch
                try:
                    securitytrails_search = securitytrailssearch.SearchSecuritytrail(word)
                    stor_lst.append(store(securitytrails_search, engineitem, store_host=True, store_ip=True))
                except Exception as e:
                    if isinstance(e, MissingKey):
                        print(e)
                    else:
                        pass

            elif engineitem == 'sublist3r':
                from info.theHarvester.theHarvester.discovery import sublist3r
                try:
                    sublist3r_search = sublist3r.SearchSublist3r(word)
                    stor_lst.append(store(sublist3r_search, engineitem, store_host=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'spyse':
                from info.theHarvester.theHarvester.discovery import spyse
                try:
                    spyse_search = spyse.SearchSpyse(word)
                    stor_lst.append(store(spyse_search, engineitem, store_host=True, store_ip=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'threatcrowd':
                from info.theHarvester.theHarvester.discovery import threatcrowd
                try:
                    threatcrowd_search = threatcrowd.SearchThreatcrowd(word)
                    stor_lst.append(store(threatcrowd_search, engineitem, store_host=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'threatminer':
                from info.theHarvester.theHarvester.discovery import threatminer
                try:
                    threatminer_search = threatminer.SearchThreatminer(word)
                    stor_lst.append(store(threatminer_search, engineitem, store_host=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'trello':
                from info.theHarvester.theHarvester.discovery import trello
                # Import locally or won't work.
                trello_search = trello.SearchTrello(word)
                stor_lst.append(store(trello_search, engineitem, store_results=True))

            elif engineitem == 'twitter':
                from info.theHarvester.theHarvester.discovery import twittersearch
                twitter_search = twittersearch.SearchTwitter(word, limit)
                stor_lst.append(store(twitter_search, engineitem, store_people=True))

            elif engineitem == 'urlscan':
                from info.theHarvester.theHarvester.discovery import urlscan
                try:
                    urlscan_search = urlscan.SearchUrlscan(word)
                    stor_lst.append(store(urlscan_search, engineitem, store_host=True, store_ip=True))
                except Exception as e:
                    print(e)

            elif engineitem == 'virustotal':
                from info.theHarvester.theHarvester.discovery import virustotal
                virustotal_search = virustotal.SearchVirustotal(word)
                stor_lst.append(store(virustotal_search, engineitem, store_host=True))

            elif engineitem == 'yahoo':

                from info.theHarvester.theHarvester.discovery import yahoosearch
                yahoo_search = yahoosearch.SearchYahoo(word, limit)
                stor_lst.append(store(yahoo_search, engineitem, store_host=True, store_emails=True))
    else:
        print('\033[93m[!] Invalid source.\n\n \033[0m')
        sys.exit(1)
    
    async def worker(queue):
        while True:
            # Get a "work item" out of the queue.
            stor = await queue.get()
            try:
                await stor
                queue.task_done()
                # Notify the queue that the "work item" has been processed.
            except Exception:
                queue.task_done()

    async def handler(lst):
        queue = asyncio.Queue()

        for stor_method in lst:
            # enqueue the coroutines
            queue.put_nowait(stor_method)
        # Create five worker tasks to process the queue concurrently.
        tasks = []
        for i in range(5):
            task = asyncio.create_task(worker(queue))
            tasks.append(task)

        # Wait until the queue is fully processed.
        await queue.join()

        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are cancelled.
        await asyncio.gather(*tasks, return_exceptions=True)

    await handler(lst=stor_lst)
    # Sanity check to see if all_emails and all_hosts are defined.
    try:
        all_emails
    except NameError:
        print('\n\n\033[93m[!] No emails found because all_emails is not defined.\n\n \033[0m')
        sys.exit(1)
    try:
        all_hosts
    except NameError:
        print('\n\n\033[93m[!] No hosts found because all_hosts is not defined.\n\n \033[0m')
        sys.exit(1)




async def entry_point(domain):
    try:
        Core.banner()
        await start(domain)
    except KeyboardInterrupt:
        print('\n\n\033[93m[!] ctrl+c detected from user, quitting.\n\n \033[0m')
    except Exception as error_entry_point:
        print(error_entry_point)
        sys.exit(1)

if python_version()[0:3] < '3.7':
    print('\033[93m[!] Make sure you have Python 3.7+ installed, quitting.\n\n \033[0m')
    sys.exit(1)


def harvest_emails():
    if len(all_emails) == 0:
        return 0
    else:
        return sorted(list(set(all_emails)))
def harvest_hosts():
    if len(all_hosts) == 0:
        return 0
    else:
        return sorted(list(set(all_hosts)))
        
def harvest_ips():
    if len(all_ip) == 0:
        return 0
    else:
        ip_list = sorted([str(netaddr.IPAddress(ip.strip())) for ip in set(all_ip)])
        return ip_list
def harvest_people():
    if len(all_people) == 0:
        return 0
    else:
        return sorted(list(set(all_people)))

async def harvest(target):
    global all_emails 
    all_emails = []
    global all_hosts
    all_hosts = []
    global all_ip
    all_ip = []
    global all_people 
    all_people = []
    domain=str(target)
    platform = sys.platform
    if platform == 'win32':
    # Required or things will break if trying to take screenshots
        import multiprocessing
        multiprocessing.freeze_support()
        asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy
    else:
        if python_version()[0:3] < '3.9':
            import uvloop
            uvloop.install()

        if "linux" in platform:
            import aiomultiprocess
        # As we are not using Windows we can change the spawn method to fork for greater performance
            aiomultiprocess.set_context("fork")
    await entry_point(domain)

