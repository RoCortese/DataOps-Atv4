from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "prefab-list-382800",
  "private_key_id": "7d49810a7308148affc29f20edeeff9bcb41d71b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4MxLIIClWEZP7\nBJtapfEAS5MO+SmFzIHnPQ4U/BzTI4mwtcgn8R1ekU1qJGp05lXp3xSkX4nCXXno\nl1MQfpGKTzRYJy6b+rcRAcpR633asJ6HYyGlbQ9lX2Z2VVjaz4+5x+6JkmXMyOu8\nAj9LGFGcVJIk5F+2wJmICZzDMHtSNwf3pB3VYsBS9agS/C6VHvzqBdjH0Z+WIblp\nffyI6iqVbil7bR0qWX7rDXsoiWKk5SWm0DdHhNVyH9nqgYCZ5MvyG2aku4Daa7IL\nJmvL69U9cKNgYrW2IP+8NILQK2bmwQRBYX4xxufE12QLvfiWId9j33CPmS4ouuhp\nPrp/SWcBAgMBAAECggEABkWPaXbeX3DJZ4frb/uD1F8uYHlzfGu3XdesaMKhit8c\nNWMIH9OH7OgQwSkgoo6z7MrQo6zg1nhLMgQigvaTRyi9mxWI8szHYk3rvQyyECHY\nwPp7Kxw2tKx6EzQCWq9r6O8FuEOOwaly7Nes/uYi47o1sGnB+EmQJLOSlcsLHORF\n20GJki+cDzFEAU9CkPKZANYbLHLqhedZPYubDbyUv7WU0U1GUCCpZ+fA5AsMsyeW\nefxbpQ0PBHAF54UL1aLct3sH2QBlGGc6sKghwZpWatEabsPc92JSjU3miFDTOKuF\nrN0aidj6Lbsope39PS2DMNlRVBHQkINkpY8828JNkQKBgQDlAGiPohURCkRAs1o2\nSI9L4QjU8Hej5GGhGlBEGEXxusvjtoftisPPG3psS9xEv3Vx1NtPsR/77QcKQ+ew\nB+h41vk0jq8qW8SxfJlGBnZUCRMQP5tN0W55qthaWUu3HoWU5sijtFxyjjRydD9M\nnscLgmbpbZ71MXO6lwMNs7KvcQKBgQDN6nl9lTFVgZoZar6vzix5m/6y6UnTGkWP\nYju6G3UmpOQFUmPOkhmwAQCXyYgC7yIl61gTcbAB+24rdgypy0ZnNxG5Rx18NkRi\nz0plKldO87OjtNqf0Ie10H0nIJw9JtSJtBB4zsvrl5UypQYQGBvAZpQickoc0iQT\nlzTWN+CIkQKBgQCC/QPSPOUN9TBrTevpJwIIZjU2EEJvFeCeVT3aZYQErFOZ8ju4\nLWqpmc8iCRZ6oIVeUmIMKIXiBYfEYGkzcKKSFG1BmegqM4nD+EB4JJQkp3gnECsW\njRhDMe1FaNR9b1D7hjL4KN/EiwEHAuV+P0gdlj6lgRWurNXEwkJ14PbxkQKBgGAc\n98Q0ZSiiK8l9V7A7req9c28TERBmDN3WXkaKFm6JPJ13TXrYGwFaFmrC+KdV8zx7\n00qQIDVspInIujRu21fGDpHKreqSce0lEHaUAtipS8o32mwKK64juKcQw5yPiVkV\nITMiY3B9+nf/KwtMFXgC6VYCvrEhLRGv3Eu5HSbhAoGAK249Y6yc2ebZCXSpe57J\nTiKy2hjxQHcB6RouirKVUkDbSf9GBc0FSwGecu3vRt6Nzf1VyIDieYR+2qS5osQv\nP3uNzYuQ7T1dtRP92Qg95/BNtxusHOlsSWp37QR08yM5OYyZW2aayFTUR5zWzupn\nMhjIIMZEsEVKWtcXTToenlQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "945217875518-compute@developer.gserviceaccount.com",
  "client_id": "104671523890267223816",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/945217875518-compute%40developer.gserviceaccount.com"
}


try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atv-dataops') ### Nome do seu bucket
  blob = bucket.blob('atv-dataops.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
