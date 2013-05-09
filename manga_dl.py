from os       import makedirs
from bs4      import BeautifulSoup
from urllib   import urlretrieve
from urllib2  import urlopen
from os.path  import exists, isfile

class Crawler:

  def __init__(self, url):
    self.url = url
    self.main_html = urlopen(url)
    self.main_soup = BeautifulSoup(self.main_html.read())

  def getManga(self):
    if self.main_html.code == 200:
      self.getFreshMangaList()

  def getFreshMangaList(self):
    for lists in self.main_soup.find_all('ul', {'class' : 'freshmanga'}):
      self.mangaList = lists.find_all('li', {'class' : 'new'})
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
      
      dir_name = url_split[-3] + '_' + url_split[-2]

      self.downloadImage(self.url, dir_name, url_split[-1])

      html = urlopen(self.url)
      html_soup = BeautifulSoup(html.read())

      for next_html in html_soup.find_all(id="controls"):
        next_link = next_html.find('a', {'class' : 'active'}).find_next_sibling('a')

      self.url = self.home_url + next_link.get('href')
      url_split = self.url.split('/')

  def downloadImage(self, url, dir_name, cnt):
    dir_path = 'downloads/' + dir_name
    manga_html = urlopen(url)
    manga_soup = BeautifulSoup(manga_html.read())

    img = manga_soup.find('img', id='p')
    img_src = img.get('src')

    file_extension = img_src.split('/')[-1].split('.')[-1]
    file_name = dir_name + '_' + cnt + '.' + file_extension

    if not exists(dir_path):
      makedirs(dir_path)

    if not isfile(dir_path + '/' + file_name):
      try: 
        urlretrieve(img_src, dir_path + '/' + file_name)
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