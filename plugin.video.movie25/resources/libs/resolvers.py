# -*- coding: cp1252 -*-
import urllib,urllib2,re,cookielib,string,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.net import Net as net

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')

class ResolverError(Exception):
    def __init__(self, value, value2):
        value = value
        value2 = value2
    def __str__(self):
        return repr(value,value2)

def resolve_url(url, filename = False):
    stream_url = False
    if(url):
        try:
            url = url.split('"')[0]
            match = re.search('xoxv(.+?)xoxe(.+?)xoxc',url)
            print "host "+url
            if(match):
                import urlresolver
                source = urlresolver.HostedMediaFile(host=match.group(1), media_id=match.group(2))
                if source:
                    stream_url = source.resolve()
            elif re.search('billionuploads',url,re.I):
                stream_url=resolve_billionuploads(url, filename)
            elif re.search('180upload',url,re.I):
                stream_url=resolve_180upload(url)
            elif re.search('veehd',url,re.I):
                stream_url=resolve_veehd(url)
            elif re.search('vidto',url,re.I):
                stream_url=resolve_vidto(url)
            elif re.search('epicshare',url,re.I):
                stream_url=resolve_epicshare(url)
            elif re.search('lemuploads',url,re.I):
                stream_url=resolve_lemupload(url)
            elif re.search('mightyupload',url,re.I):
                stream_url=resolve_mightyupload(url)               
            elif re.search('hugefiles',url,re.I):
                stream_url=resolve_hugefiles(url)
            elif re.search('megarelease',url,re.I):
                stream_url=resolve_megarelease(url)
            elif re.search('movreel',url,re.I):
                stream_url=resolve_movreel(url)
            elif re.search('bayfiles',url,re.I):
                stream_url=resolve_bayfiles(url)
            elif re.search('nowvideo',url,re.I):
                stream_url=resolve_nowvideo(url)
            elif re.search('novamov',url,re.I):
                stream_url=resolve_novamov(url)
            elif re.search('vidspot',url,re.I):
                stream_url=resolve_vidspot(url)
            elif re.search('videomega',url,re.I):
                stream_url=resolve_videomega(url)
            elif re.search('youwatch',url,re.I):
                stream_url=resolve_youwatch(url)
            elif re.search('youtube',url,re.I):
                try:url=url.split('watch?v=')[1]
                except:
                    try:url=url.split('com/v/')[1]
                    except:url=url.split('com/embed/')[1]
                stream_url='plugin://plugin.video.youtube/?action=play_video&videoid=' +url
            else:
                import urlresolver
                print "host "+url
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                    if isinstance(stream_url,urlresolver.UrlResolver.unresolvable):
                        showUrlResoverError(stream_url)
                        stream_url = False
                else:
                    stream_url=url
            try:
                stream_url=stream_url.split('referer')[0]
                stream_url=stream_url.replace('|','')
            except:
                pass
        except ResolverError as e:
            #logerror(str(e))
            #showpopup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR] ' + e.value2,'[B][COLOR red]'+e.value+'[/COLOR][/B]',5000, elogo)
            try:
                import urlresolver
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                    if isinstance(stream_url,urlresolver.UrlResolver.unresolvable):
                        showUrlResoverError(stream_url)
                        stream_url = False
            except Exception as e:
                logerror(str(e))
                showpopup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
        except Exception as e:
            logerror(str(e))
            showpopup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
    else:
        logerror("video url not valid")
        showpopup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]video url not valid[/COLOR][/B]',5000, elogo)
    if stream_url and re.search('\.(zip|rar|7zip)$',stream_url,re.I):
        logerror("video url found is an archive")
        showpopup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]video url found is an archive[/COLOR][/B]',5000, elogo)
        return False
    return stream_url

def showUrlResoverError(unresolvable):
    logerror(str(unresolvable.msg))
    showpopup('[B]UrlResolver Error[/B]','[COLOR red]'+str(unresolvable.msg)+'[/COLOR]',10000, elogo)
def logerror(log):
    xbmc.log(log, xbmc.LOGERROR)
def showpopup(title='', msg='', delay=5000, image=''):
    xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % (title, msg, delay, image))
    
def grab_cloudflare(url):

    class NoRedirection(urllib2.HTTPErrorProcessor):
        # Stop Urllib2 from bypassing the 503 page.    
        def http_response(self, request, response):
            code, msg, hdrs = response.code, response.msg, response.info()

            return response
        https_response = http_response

    cj = cookielib.CookieJar()
    
    opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
    response = opener.open(url).read()
        
    jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
    if jschl:
        import time
        jschl = jschl[0]    
    
        maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

        domain_url = re.compile('(https?://.+?/)').findall(url)[0]
        domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
        
        time.sleep(5)
        
        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
        final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
        
        response = normal.open(url).read()

    return response

def millis():
      import time as time_
      return int(round(time_.time() * 1000))
    
def load_json(data):
      def to_utf8(dct):
            rdct = {}
            for k, v in dct.items() :
                  if isinstance(v, (str, unicode)) :
                        rdct[k] = v.encode('utf8', 'ignore')
                  else :
                        rdct[k] = v
            return rdct
      try :        
            from lib import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
      except:
            try:
                  import json
                  json_data = json.loads(data, object_hook=to_utf8)
                  return json_data
            except:
                  import sys
                  for line in sys.exc_info():
                        print "%s" % line
      return None
    
def resolve_bayfiles(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp Bayfiles Link...')       
        dialog.update(0)
        print 'MashUp Bayfiles - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        try: vfid = re.compile('var vfid = ([^;]+);').findall(html)[0]
        except:pass
        try:urlpremium='http://'+ re.compile('<a class="highlighted-btn" href="http://(.+?)">Premium Download</a>').findall(html)[0]
        except:urlpremium=[]
        if urlpremium:
                return urlpremium
        else:
                try:
                    delay = re.compile('var delay = ([^;]+);').findall(html)[0]
                    delay = int(delay)
                except: delay = 300
                t = millis()
                html2 = net().http_GET("http://bayfiles.net/ajax_download?_=%s&action=startTimer&vfid=%s"%(t,vfid)).content
                datajson=load_json(html2)
                if datajson['set']==True:
                    token=datajson['token']
                    url_ajax = 'http://bayfiles.net/ajax_download'
                    post = "action=getLink&vfid=%s&token=%s" %(vfid,token)
                    finaldata=net().http_GET(url_ajax + '?' + post).content
                    patron = 'onclick="javascript:window.location.href = \'(.+?)\''
                    matches = re.compile(patron,re.DOTALL).findall(finaldata)
                    return matches[0] #final url mp4
    except:
        html = net().http_GET(url).content
        try:
                match2=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) has recently downloaded a file. Upgrade to premium or wait (.+?) min.</strong>').findall(html)[0]
                raise ResolverError('You recently downloaded a file. Upgrade to premium or wait',"Bayfiles")
                return
        except:
                match3=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) is already downloading. Upgrade to premium or wait.</strong>').findall(html)
                raise ResolverError('You are already downloading. Upgrade to premium or wait.',"Bayfiles")
                return

def resolve_youwatch(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp Youwatch Link...')       
        dialog.update(0)
        print 'MashUp Youwatch - Requesting GET URL: %s' % url
        if 'embed' not in url:
            mediaID = re.findall('http://youwatch.org/([^<]+)', url)[0]
            url='http://youwatch.org/embed-'+mediaID+'.html'
        else:url=url
        html = net().http_GET(url).content
        try:
                html=html.replace('|','/')
                stream=re.compile('/mp4/video/(.+?)/(.+?)/(.+?)/setup').findall(html)
                for id,socket,server in stream:
                    continue
        except:
                raise ResolverError('This file is not available on',"Youwatch")
        stream_url='http://'+server+'.youwatch.org:'+socket+'/'+id+'/video.mp4?start=0'
        return stream_url
    except Exception, e:
        logerror('**** Youwatch Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Youwatch[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_videomega(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp Videomega Link...')       
        dialog.update(0)
        print 'MashUp Videomega - Requesting GET URL: %s' % url
        try:
            mediaID = re.findall('http://videomega.tv/.?ref=([^<]+)', url)[0]
            url='http://videomega.tv/iframe.php?ref='+mediaID
        except:url=url
        html = net().http_GET(url).content
        try:
                encodedurl=re.compile('unescape.+?"(.+?)"').findall(html)
        except:
                raise ResolverError('This file is not available on',"VideoMega")
        url2=urllib.unquote(encodedurl[0])
        stream_url=re.compile('file: "(.+?)"').findall(url2)[0]
        return stream_url
    except Exception, e:
        logerror('**** Videomega Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Videomega[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

    
def resolve_vidspot(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp Vidspot Link...')       
        dialog.update(0)
        print 'MashUp Vidspot - Requesting GET URL: %s' % url
        mediaID=re.findall('http://vidspot.net/([^<]+)',url)[0]
        url='http://vidspot.net/embed-'+mediaID+'.html'
        print url
        html = net().http_GET(url).content
        r = re.search('"file" : "(.+?)",', html)
        if r:
            stream_url = urllib.unquote(r.group(1))

        return stream_url

    except Exception, e:
        logerror('**** Vidspot Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Vidspot[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

    
def resolve_novamov(url):
        try:
            import unwise
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving MashUp Novamov Link...')       
            dialog.update(0)
            print 'MashUp Novamov - Requesting GET URL: %s' % url
            html = net().http_GET(url).content
            html = unwise.unwise_process(html)
            
            filekey = unwise.resolve_var(html, "flashvars.filekey")
            media_id=re.findall('.+?/video/([^<]+)',url)
            #get stream url from api
            api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
            html = net().http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise ResolverError('File Not Found or removed',"Novamov")
                raise ResolverError('Failed to parse url',"Novamov")
                
            return stream_url
        except urllib2.URLError, e:
            logerror('Novamov: got http error %d fetching %s' %
                                    (e.code, web_url))
            return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Novamov Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Novamov[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)

def resolve_nowvideo(url):
        try:
            import unwise
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving MashUp Nowvideo Link...')       
            dialog.update(0)
            print 'MashUp Nowvideo - Requesting GET URL: %s' % url
            html = net().http_GET(url).content
            html = unwise.unwise_process(html)
            
            filekey = unwise.resolve_var(html, "flashvars.filekey")
            try:media_id=re.findall('.+?/video/([^<]+)',url)[0]
            except:media_id=re.findall('http://embed.nowvideo.+?/embed.php.?v=([^<]+)',url)[0]
            #get stream url from api
            api = 'http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
            html = net().http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise ResolverError('File Not Found or removed',"Nowvideo")
                raise ResolverError('Failed to parse url',"Nowvideo")
                
            return stream_url
        except urllib2.URLError, e:
            logerror('Nowvideo: got http error %d fetching %s' %
                                    (e.code, web_url))
            return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Nowvideo Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Nowvideo[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)

def resolve_movreel(url):

    try:


        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp Movreel Link...')       
        dialog.update(0)
        
        print 'MashUp Movreel - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** MashUp Movreel - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable on the host,Movreel in maintenance,2000)")

        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="(submit|hidden)" name="method_free" (style=".*?" )*value="(.*?)">', html).group(3)
        method_premium = re.search('<input type="(hidden|submit)" name="method_premium" (style=".*?" )*value="(.*?)">', html).group(3)
        

        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        data = {'op': op, 'id': postid, 'referer': url, 'rand': rand, 'method_premium': method_premium}
        
        print 'MashUp Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net().http_POST(url, data).content

        #Only do next post if Free account, skip to last page for download link if Premium
        if method_free:
            #Check for download limit error msg
            if re.search('<p class="err">.+?</p>', html):
                logerror('***** Download limit reached')
                errortxt = re.search('<p class="err">(.+?)</p>', html).group(1)
                xbmc.executebuiltin("XBMC.Notification("+errortxt+",Movreel,2000)")
    
            dialog.update(66)
            
            #Set POST data values
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
    
            if r:
                for name, value in r:
                    data[name] = value
            else:
                logerror('***** MashUp Movreel - Cannot find data values')
                xbmc.executebuiltin("XBMC.Notification(Unable to resolve Movreel Link,Movreel,2000)") 

            print 'MashUp Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
            html = net().http_POST(url, data).content

        #Get download link
        dialog.update(100)
        link = re.search('<a href="(.+)">Download Link</a>', html)
        if link:
            return link.group(1)
        else:
            xbmc.executebuiltin("XBMC.Notification(Unable to find final link,Movreel,2000)")

    except Exception, e:
        logerror('**** Mash Up Movreel Error occured: %s' % e)
        raise ResolverError(str(e),"Movreel")
    finally:
        dialog.close()

def resolve_megarelease(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp MegaRelease Link...')
        dialog.update(0)
        
        print 'MegaRelease MashUp - Requesting GET URL: %s' % url
        html = net().http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** MegaRelease - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,MegaRelease in maintenance,2000)")                                
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('Mash Up: Resolve MegaRelease - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MegaRelease,2000)")
            return False

        filename = re.search('You have requested <font color="red">(.+?)</font>', html).group(1)
        filename = filename.split('/')[-1]
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://megarelease.org/(.+)$', url).group(1)
        
        vid_embed_url = 'http://megarelease.org/vidembed-%s%s' % (guid, extension)
        UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', UserAgent)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename
        
        dialog.update(100)

        return download_link
        
    except Exception, e:
        logerror('**** Mash Up MegaRelease Error occured: %s' % e)
        raise ResolverError(str(e),"MegaRelease")
    finally:
        dialog.close()

def resolve_veehd(url):
    name = "veeHD"
    cookie_file = os.path.join(datapath, '%s.cookies' % name)
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from random import choice
    userName = ['mashup1', 'mashup3', 'mashup4', 'mashup5', 'mashup6', 'mashup7']
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Mash Up VeeHD Link...')       
        dialog.update(0)
        loginurl = 'http://veehd.com/login'
        ref = 'http://veehd.com/'
        submit = 'Login'
        terms = 'on'
        remember_me = 'on'
        data = {'ref': ref, 'uname': choice(userName), 'pword': 'xbmcisk00l', 'submit': submit, 'terms': terms, 'remember_me': remember_me}
        html = net(user_agent).http_POST(loginurl, data).content
        if dialog.iscanceled(): return False
        dialog.update(33)
        net().save_cookies(cookie_file)
        headers = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'}
        net().set_cookies(cookie_file)
        print 'Mash Up VeeHD - Requesting GET URL: %s' % url
        html = net().http_GET(url, headers).content
        if dialog.iscanceled(): return False
        dialog.update(66)
        fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
        frag = 'http://%s%s'%('veehd.com',fragment[1])
        net().set_cookies(cookie_file)
        html = net().http_GET(frag, headers).content
        r = re.search('"video/divx" src="(.+?)"', html)
        if r:
            stream_url = r.group(1)
        if not r:
            print name + '- 1st attempt at finding the stream_url failed probably an Mp4, finding Mp4'
            a = re.search('"url":"(.+?)"', html)
            if a:
                r=urllib.unquote(a.group(1))
                if r:
                    stream_url = r
                else:
                    logerror('***** VeeHD - File Not Found')
                    xbmc.executebuiltin("XBMC.Notification(File Not Found,VeeHD,2000)")
                    return False
            if not a:
                a = re.findall('href="(.+?)">', html)
                stream_url = a[1]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return stream_url
    except Exception, e:
        logerror('**** Mash Up VeeHD Error occured: %s' % e)
        raise ResolverError(str(e),"VeeHD")

def resolve_billionuploads(url, filename):
    try:
 
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Mash Up BillionUploads Link...')  
        dialog.update(0)
            
        print 'Mash Up BillionUploads - Requesting GET URL: %s' % url
        import requests
        response = requests.get(url)
        html =response.text
        html = html.encode("ascii", "ignore")
        dialog.update(50)
        
        if re.search('This server is in maintenance mode', html):
                logerror('***** BillionUploads - Site reported maintenance mode')
                xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,BillionUploads in maintenance,2000)")                                
                return None
        if re.search('File Not Found', html, re.I):
                logerror('***** BillionUploads - File Not Found')
                xbmc.executebuiltin("XBMC.Notification(File Not Found,BillionUploads,2000)")
                return False
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        for name, value in r:
            data[name] = value
            
        captchaimg = re.search('<img src="(http://BillionUploads.com/captchas/.+?)"', html)

        data.update({'submit_btn':'', 'referer': '', 'method_free': '', 'method_premium':''})

        r = re.search('document.createElement\(\'input\'\)\)\.attr\(\'type\',\'hidden\'\)\.attr\(\'name\',\'(.+?)\'\)\.val\(\$\(\'textarea\[source="(.+?)"\]\'\)\.val', html)
        if r:
            ra = re.search('<textarea source="%s" style="display: none;visibility: hidden">(.+?)</textarea>' % r.group(2), html)
            if ra:
                data.update({r.group(1):ra.group(1)})
            
        r = re.search('document\.getElementById\(\'.+\'\)\.innerHTML=decodeURIComponent\(\"(.+?)\"\);', html)
        if r:
            r = re.findall('type="hidden" name="(.+?)" value="(.+?)">', urllib.unquote(r.group(1)).decode('utf8') )
            for name, value in r:
                data.update({name:value})

        r = re.findall('\(\'input\[name=\"(.+?)\"\]\'\)\.remove\(\);', html)
        for keyval in r:
            del data[keyval]
        
        dialog.update(50)
        
        html = net().http_POST(url, data).content
        dialog.update(100)
        
        def custom_range(start, end, step):
            while start <= end:
                yield start
                start += step

        def checkwmv(e):
            s = ""
            
            # Create an array containing A-Z,a-z,0-9,+,/
            i=[]
            u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
            for z in range(0, len(u)):
                for n in range(u[z][0],u[z][1]):
                    i.append(chr(n))
            #print i

            # Create a dict with A=0, B=1, ...
            t = {}
            for n in range(0, 64):
                t[i[n]]=n
            #print t

            for n in custom_range(0, len(e), 72):

                a=0
                h=e[n:n+72]
                c=0

                #print h
                for l in range(0, len(h)):            
                    f = t.get(h[l], 'undefined')
                    if f == 'undefined':
                        continue
                    a= (a<<6) + f
                    c = c + 6

                    while c >= 8:
                        c = c - 8
                        s = s + chr( (a >> c) % 256 )
            return s

        dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)[0]
        dl = dll.split('GvaZu')[1]
        dl = checkwmv(dl)
        dl = checkwmv(dl)
        print 'Link Found: %s' % dl                

        return dl
    except Exception, e:
            logerror('BillionUploads - Exception occured: %s' % e)
            raise ResolverError(str(e),"BillionUploads")
            return None
    finally:
            dialog.close()


def resolve_180upload(url):

    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Mash Up 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        
        print 'Mash Up 180Upload - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if ">File Not Found" in html:
            logerror('Mash Up: Resolve 180Upload - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,180Upload,2000)")
            return False
        if re.search('\.(rar|zip)</b>', html, re.I):
            logerror('Mash Up: Resolve 180Upload - No Video File Found')
            xbmc.executebuiltin("XBMC.Notification(No Video File Found,180Upload,2000)")
            return False
        if dialog.iscanceled(): return False
        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()

           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   xbmc.executebuiltin("XBMC.Notification(You must enter text in the image to access video,2000)")
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving Mash Up 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'Mash Up 180Upload - Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(100)
        
        link = re.search('id="lnk_download" href="([^"]+)"', html)
        if link:
            print 'Mash Up 180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        logerror('**** Mash Up 180Upload Error occured: %s' % e)
        raise ResolverError(str(e),"180Upload") 
    finally:
        dialog.close()
        
def resolve_vidto(url):
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from resources.libs import jsunpack
    import time
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Mash Up Vidto Link...')
        dialog.update(0)
        html = net(user_agent).http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(11)
        logerror('Mash Up: Resolve Vidto - Requesting GET URL: '+url)
        r = re.findall(r'<font class="err">File was removed</font>',html,re.I)
        if r:
            logerror('Mash Up: Resolve Vidto - File Was Removed')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Vidto,2000)")
            return False
        if not r:
            r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                           ,html,re.M|re.DOTALL)
            if r:
                unpacked = jsunpack.unpack(r[0])#this is where it will error, not sure if resources,libs added to os path
                r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
            if not r:
                r = re.findall('type="hidden" name="(.+?)" value="(.+?)">',html)
                post_data = {}
                for name, value in r:
                    post_data[name] = value
                post_data['usr_login'] = ''
                post_data['referer'] = url
                for i in range(7):
                    time.sleep(1)
                    if dialog.iscanceled(): return False
                    dialog.update(22+i*11.3)
                html = net(user_agent).http_POST(url,post_data).content
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                               ,html,re.M|re.DOTALL)
                if r:
                    unpacked = jsunpack.unpack(r[0])
                    r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
                if not r:
                    r = re.findall(r"var file_link = '(.+?)';",html)
        if dialog.iscanceled(): return False
        dialog.update(100)
        return r[0]
    except Exception, e:
        logerror('Mash Up: Resolve Vidto Error - '+str(e))
        raise ResolverError(str(e),"Vidto") 
    finally:
        dialog.close()

def resolve_epicshare(url):
    try:
        puzzle_img = os.path.join(datapath, "epicshare_puzzle.png")
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp EpicShare Link...')
        dialog.update(0)
        
        print 'EpicShare - MashUp Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** EpicShare - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,EpicShare in maintenance,2000)")  
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('***** EpicShare - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,EpicShare,2000)")
            return False

        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            logerror('***** EpicShare - Cannot find data values')
            raise Exception('Unable to resolve EpicShare Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving MashUp EpicShare Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'EpicShare - MashUp Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(100)
        
        link = re.search('<a id="lnk_download"  href=".+?product_download_url=(.+?)">', html)
        if link:
            print 'MashUp EpicShare Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            logerror('***** EpicShare - Cannot find final link')
            raise Exception('Unable to resolve EpicShare Link')
        
    except Exception, e:
        logerror('**** EpicShare MashUp Error occured: %s' % e)
        raise ResolverError(str(e),"EpicShare") 
    finally:
        dialog.close()

def resolve_lemupload(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp LemUpload Link...')       
        dialog.update(0)
#         
        print 'LemUpload - MashUp Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            print '***** LemUpload - File Not Found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,LemUpload,2000)")
            return False
        
        if re.search('This server is in maintenance mode', html):
            print '***** LemUpload - Server is in maintenance mode'
            xbmc.executebuiltin("XBMC.Notification(Site In Maintenance,LemUpload,2000)")
            return False

        filename = re.search('<h2>(.+?)</h2>', html).group(1)
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://lemuploads.com/(.+)$', url).group(1)
        vid_embed_url = 'http://lemuploads.com/vidembed-%s%s' % (guid, extension)
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        if dialog.iscanceled(): return False
        dialog.update(100)
        link = response.geturl()
        if link:
            redirect_url = re.search('(http://.+?)video', link)
            if redirect_url:
                link = redirect_url.group(1) + filename
            print 'MashUp LemUpload Link Found: %s' % link
            return  link
        else:
            logerror('***** LemUpload - Cannot find final link')
            raise Exception('Unable to resolve LemUpload Link')

    except Exception, e:
        logerror('**** LemUpload Error occured: %s' % e)
        raise ResolverError(str(e),"LemUpload") 
    finally:
        dialog.close()
        
def resolve_mightyupload(url):
    from resources.libs import jsunpack
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MightyUpload Link...')       
        dialog.update(0)
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        logerror('Mash Up: Resolve MightyUpload - Requesting GET URL: '+url)
        r = re.findall(r'name="(.+?)" value="?(.+?)"', html, re.I|re.M)
        if r:
            post_data = {}
            for name, value in r:
                post_data[name] = value
            post_data['referer'] = url
            html = net().http_POST(url, post_data).content
            if dialog.iscanceled(): return False
            dialog.update(100)
            r = re.findall(r'<a href=\"(.+?)(?=\">Download the file</a>)', html)
            return r[0]
        else:
            logerror('***** MightyUpload - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MightyUpload,2000,"+elogo+")")
            return False
    except Exception, e:
        logerror('Mash Up: Resolve MightyUpload Error - '+str(e))
        raise ResolverError(str(e),"MightyUpload") 

def resolve_hugefiles(url):
    from resources.libs import jsunpack
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving HugeFiles Link...')       
        dialog.update(0)
        html = net().http_GET(url).content
        r = re.findall('File Not Found',html)
        if r:
            xbmc.log('Mash Up: Resolve HugeFiles - File Not Found or Removed', xbmc.LOGERROR)
            xbmc.executebuiltin("XBMC.Notification(File Not Found or Removed,HugeFiles,2000)")
            return False
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)">', html)
        for name, value in r:
            data[name] = value
            data.update({'method_free':'Free Download'})
        if data['fname'] and re.search('\.(rar|zip)$', data['fname'], re.I):
            dialog.update(100)
            logerror('Mash Up: Resolve HugeFiles - No Video File Found')
            xbmc.executebuiltin("XBMC.Notification(No Video File Found,HugeFiles,2000)")
            return False
        if dialog.iscanceled(): return False
        dialog.update(33)
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(66)
        if 'reached the download-limit' in html:
            logerror('Mash Up: Resolve HugeFiles - Daily Limit Reached, Cannot Get The File\'s Url')
            xbmc.executebuiltin("XBMC.Notification(Daily Limit Reached,HugeFiles,2000)")
            return False
        embed = re.search('<h2>Embed code</h2>.+?<IFRAME SRC="(.+?)"', html, re.DOTALL + re.IGNORECASE)
        html = net().http_GET(embed.group(1)).content
        sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
        r = re.findall(sPattern, html, re.DOTALL|re.I)
        if r:
            sUnpacked = jsunpack.unpack(r[0])
            sUnpacked = sUnpacked.replace("\\'","")
            r = re.findall('file,(.+?)\)\;s1',sUnpacked)
            if not r:
               r = re.findall('"src"value="(.+?)"/><embed',sUnpacked)
            if dialog.iscanceled(): return False
            dialog.update(100)
            dialog.close()
            return r[0]
        if not r:
            logerror('***** HugeFiles - Cannot find final link')
            raise Exception('Unable to resolve HugeFiles Link')
    except Exception, e:
        logerror('Mash Up: Resolve HugeFiles Error - '+str(e))
        raise ResolverError(str(e),"HugeFiles") 
