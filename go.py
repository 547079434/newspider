import subprocess
import time

while True:
	subprocess.call('cd d://project/newspider/news && scrapy crawl baidunews && scrapy crawl sinanews', shell=True)
	time.sleep(3600)