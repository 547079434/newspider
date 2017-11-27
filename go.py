import subprocess
import time

while True:
	subprocess.call('cd news && scrapy crawl baidunews && scrapy crawl sinanews', shell=True)
	time.sleep(3600)