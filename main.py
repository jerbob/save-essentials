"""Scrape information from every CyberStart Essentials module."""

import re
import os

import requests
from bs4 import BeautifulSoup


video_pattern = re.compile('"(https://[^,]*?mp4[^,]*?)"')

base_url = 'https://essentials.joincyberdiscovery.com{}'
module_url = 'https://essentials.joincyberdiscovery.com/course/module/{}'

input(
    'Copy and Paste the content of your "Cookie" header for '
    'https://essentials.joincyberdiscovery.com in the file cookies.txt.'
    '\nPress enter to continue.\n'
)

# Open and read cookie file
with open('cookies.txt') as file:
    cookies = file.read().strip()

# Create set of section links
section_links = set()


# Create cookie-persistent session
with requests.Session() as session:

    # Add cookies to persistent session
    session.headers.update({'Cookie': cookies})
    # Iterate all modules in essentials
    for module_number in range(1, 47):
        url = module_url.format(module_number)
        soup = BeautifulSoup(
            session.get(url).content, 'html.parser'
        )
        # Find all links for appropriate module sections
        for section_tag in soup.find_all(
            'a', {'class': 'link'}, href=re.compile('.*/section/.*')
        ):
            print('Scraping page {}...'.format(section_tag.attrs['href']))
            # Add links to set
            section_links.add(
                base_url.format(section_tag.attrs['href'])
            )

    for url in section_links:
        # Strip domain from URL, to save file structure
        filename = url.replace(
            'https://essentials.joincyberdiscovery.com/', ''
        ) + '.'
        # Create structure if non-existent
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        content = session.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        video_iframe = soup.find('iframe')
        audio_tag = soup.find('audio')

        if audio_tag:
            # Create HTML element to replace player
            new_player = (
                '<audio controls>'
                '<source src="{}" type="audio/mp3">'
                '</audio>'
            ).format(filename.split('/')[-1] + 'mp3')
            new_player = BeautifulSoup(new_player, 'html.parser')
            # Find player div to replace
            print('Parsing embedded audio {}...'.format(filename))
            player_div = soup.find('div', {'id': 'audio_player'})
            # Get the audio player tag
            audio_src = audio_tag.attrs['src']
            audio_src = base_url.format(audio_src)
            audio = session.get(audio_src).content
            # Write audio content
            print('Writing embedded audio {}...'.format(filename))
            with open(filename + 'mp3', 'wb') as file:
                file.write(audio)
            # Replace the original audio player with the modified tag
            player_div.replace_with(new_player)

        if video_iframe:
            # Create HTML element to replace iframe
            new_video = (
                '<video width="1100" height="619" controls>'
                '<source src="{}" type="video/mp4">'
                '</video>'
            ).format(filename.split('/')[-1] + 'mp4')
            new_video = BeautifulSoup(new_video, 'html.parser')
            # Fake the referer header with the Essentials URL
            session.headers['Referer'] = url
            print('Parsing embedded video {}...'.format(filename))
            video_src = session.get(video_iframe.attrs['src']).content.decode()
            video_src = video_pattern.search(video_src).group(1)
            # Get actual video file content
            video = session.get(video_src).content
            # Write video file with name of section
            print('Writing embedded video {}...'.format(filename))
            with open(filename + 'mp4', 'wb') as file:
                file.write(video)
            # Replace the original iframe with the modified tag
            video_iframe.replace_with(new_video)

        # Open and save the HTML page
        print('Writing section {}...'.format(filename))
        with open(filename + 'html', 'w+') as file:
            file.write(str(soup))
