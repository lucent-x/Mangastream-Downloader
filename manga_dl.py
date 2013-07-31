from os       import makedirs
from bs4      import BeautifulSoup
from urllib   import urlretrieve
from urllib2  import urlopen
from os.path  import exists, isfile
import mechanize
import cookielib

class Crawler:

  def __init__(self, url):
    self.url = url
    self.main_html = urlopen(url)
    self.main_soup = BeautifulSoup(self.main_html.read())

  def getManga(self):
    if self.main_html.code == 200:
      self.getFreshMangaList()

  def getFreshMangaList(self):
    for lists in self.main_soup.find_all('ul', {'class' : 'new-list'}):
      self.mangaList = lists.find_all('li', {'class' : 'active'})
      self.getFreshMangaListUrl(self.mangaList)
    
  def getFreshMangaListUrl(self, lists):
    for link in lists:
      mangaUrl = link.find('a').get('href')
      d = ImageDownloader(mangaUrl)
      d.download()

  def go(self):
    self.getManga()

class ImageDownloader:

  def __init__(self, url):
    self.url = url
    self.home_url = 'http://mangastream.com'

  def download(self):
    url_split = self.url.split('/')

    while url_split[-1] != 'end':

      print self.url
      
      dir_name = url_split[-4] + '_' + url_split[-3]

      self.downloadImage(self.url, dir_name, url_split[-1])

      html = urlopen(self.url)
      html_soup = BeautifulSoup(html.read())

      for next_html in html_soup.find('li', {'class' : 'next'}):
        next_link = next_html.get('href')

      self.url = next_link
      url_split = self.url.split('/')

  def downloadImage(self, url, dir_name, cnt):
    dir_path = 'downloads/' + dir_name
    manga_html = urlopen(url)
    manga_soup = BeautifulSoup(manga_html.read())

    img = manga_soup.find('img', id='manga-page')
    img_src = img.get('src')

    file_extension = img_src.split('/')[-1].split('.')[-1]
    file_name = dir_name + '_' + cnt + '.' + file_extension

    if not exists(dir_path):
      makedirs(dir_path)

    if not isfile(dir_path + '/' + file_name):
      try: 
        br = mechanize.Browser()

        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        image_response = br.open_novisit(img_src)

        with open(dir_path + '/' + file_name, 'wb') as f:
          f.write(image_response.read())
          print('Downloading ' + file_name + '...')
      except:
        print('Download error!')
    else:
      print('Image already exists.')

def main():
  url = 'http://mangastream.com'
  c = Crawler(url)
  c.go()

if __name__ == '__main__':
  main()