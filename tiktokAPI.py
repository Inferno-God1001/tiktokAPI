import re, requests
from flask import Flask, jsonify


app = Flask(__name__)


def get_response(username_root):
    display_name = None
    username = None
    status = "not found"
    id_ = 0
    followers = 0
    following = 0
    likes = 0
    videos = 0
    bio = None


    if username_root:
        html = requests.get(f"https://tiktok.com/@{username_root}").text

        if '"statusCode":0' in html:
            status = "found"
            id_ = int(re.search(r'"id":"(\d+)"', html).group(1))
            display_name = re.search(r'"nickname":"(.*?)"', html).group(1)
            username = re.search(r'"uniqueId":"(.*?)"', html).group(1)
            followers = int(re.search(r'"followerCount":(\d+)', html).group(1))
            following = int(re.search(r'"followingCount":(\d+)', html).group(1))
            likes = int(re.search(r'"heartCount":(\d+)', html).group(1))
            videos = int(re.search(r'"videoCount":(\d+)', html).group(1))
            bio = re.search(r'"signature":"(.*?)"', html).group(1)



        return {
            "status": status,
            "id": id_,
            "displayName": display_name,
            "username": username,
            "followers": followers,
            "following": following,
            "likes": likes,
            "videos": videos,
            "bio": bio
        }


@app.route("/json/@<username>")
def API_json(username):
    return jsonify(get_response(username))
app.run(host="0.0.0.0", port=5000)
