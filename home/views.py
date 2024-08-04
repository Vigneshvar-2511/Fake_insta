from django.shortcuts import render
from instagrapi import Client
import json
import httpx
import urllib.request
from PIL import Image

def home(request):
    if(request.method=='POST'):
        try:
            client = httpx.Client(
            headers={
            # this is internal ID of an instegram backend app. It doesn't change often.
            "x-ig-app-id": "936619743392459",
            # use browser-like features
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",})


            def scrape_user(username: str):
                """Scrape Instagram user's data"""
                result = client.get(
                f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
                )
                data = json.loads(result.content)
                return data["data"]["user"]

            k=scrape_user(request.POST["insta_id"])
            l=[]
            d={}
            d['insta_id']=request.POST['insta_id']
            d['followers']=k['edge_followed_by']['count']
            print(d['followers'])
            d['following']=k['edge_follow']['count']
            d['full_name']=k['full_name']
            d['profile_pic_url']=k['profile_pic_url']
            d['bio']=k['biography']
            d['posts']=k['edge_owner_to_timeline_media']['count']
            urllib.request.urlretrieve(d['profile_pic_url'],'x')
            return render(request,'home/result.html',d)
        except:
            return render(request,'home/home.html',{'error':'invalid insta_id'})
    return render(request,'home/home.html',{'error':'insta_id'})
# Create your views here.
