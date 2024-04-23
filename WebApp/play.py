from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_music(music = "DefaultMusicBlblbl") :
	
	request_url = 'http://example.com'
	music_data = requests.get(request_url).json()
	
	return music_data
	
if __name__ != "__main__" :
	print('\n*** Get Current Music: ')
	music = input("\nEnter music name : ")
	music_data = get_current_music(music)
	print("\n")
	pprint(music_data)
