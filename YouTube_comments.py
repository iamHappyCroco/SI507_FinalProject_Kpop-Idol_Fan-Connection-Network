import pandas as pd
import requests
import time

API_KEY = 'AIzaSyAo2nWMHernd1W1MOQ9X7bOdTmhQEaSVeQ'

video_ids = {
    # BLACKPINK
    "BLACKPINK - Pink Venom": "gQlMMD8auMs",
    "BLACKPINK - Shut Down": "POe9SOEKotk",
    "BLACKPINK - How You Like That": "ioNng23DkIM",
    "BLACKPINK - DDU-DU DDU-DU": "IHNzOHi8sJs",
    "BLACKPINK - Kill This Love": "2S24-y0Ij3Y",
    # BTS
    "BTS - Dynamite": "gdZLi9oWNZg",
    "BTS - Butter": "WMweEpGlu_U",
    "BTS - Boy With Luv": "XsX3ATc3FbA",
    "BTS - FAKE LOVE": "7C2z4GqqS5E",
    "BTS - MIC Drop": "kTlv5_Bs8aw",
    # TWICE
    "TWICE - Fancy": "kOHB85vDuow",
    "TWICE - Feel Special": "3ymwOvzhwHs",
    "TWICE - I CAN'T STOP ME": "CM4CkVFmTds",
    "TWICE - CHEER UP": "c7rCyll5AeY",
    "TWICE - What is Love?": "i0p1bmr0EmE",
    # SEVENTEEN
    "SEVENTEEN - HOT": "gRnuFC4Ualw",
    "SEVENTEEN - Rock with you": "dG4x6ohAQAs",
    "SEVENTEEN - Very Nice": "Qmmdn0LJ-u8",
    "SEVENTEEN - Super": "UBURTj20HXI",
    # EXO
    "EXO - Love Shot": "pSudEWBAYRE",
    "EXO - Tempo": "iwd8N6K-sLk",
    "EXO - Monster": "KSH-FVVtTf0",
    "EXO - Ko Ko Bop": "IdssuxDdqKk",
    # Red Velvet
    "Red Velvet - Psycho": "U7mPqycQ0tQ",
    "Red Velvet - Feel My Rhythm": "WyiIGEHQP8o",
    "Red Velvet - Bad Boy": "J_CFBjAyPWE",
    "Red Velvet - Russian Roulette": "QslJYDX3o8s",
    # ITZY
    "ITZY - WANNABE": "fE2h3lGlOsk",
    "ITZY - DALLA DALLA": "pNfTK39k55U",
    "ITZY - LOCO": "68u3wq0_UhA",
    "ITZY - Not Shy": "wTowEKjDGkU",
    # Stray Kids
    "Stray Kids - God's Menu": "TQTlCHxyuu8",
    "Stray Kids - Thunderous": "EaswWiwMVs8",
    "Stray Kids - MANIAC": "OvioeS1ZZ7o",
    "Stray Kids - Back Door": "X-uJtV8ScYk",
    # (G)I-DLE
    "(G)I-DLE - TOMBOY": "Jh4QFaPmdss",
    "(G)I-DLE - HWAA": "XEOCbFJjRw0",
    "(G)I-DLE - LION": "6oanIo_2Z4Q",
    # IVE
    "IVE - LOVE DIVE": "Y8JFxS1HlDo",
    "IVE - After LIKE": "F0B7HDiY-10",
    "IVE - ELEVEN": "Y8JFxS1HlDo",
    # ENHYPEN
    "ENHYPEN - FEVER": "nQ6wLuYvGd8",
    "ENHYPEN - Drunk-Dazed": "6OY4sMpT4uE",
    "ENHYPEN - Blessed-Cursed": "GjnfXQbXH9Y",
    # TXT
    "TXT - Blue Hour": "Vd9QkWsd5p4",
    "TXT - LO$ER=LO♡ER": "AwV3rmvDXuc",
    "TXT - Good Boy Gone Bad": "JzODFhH0V2g",
    # LE SSERAFIM
    "LE SSERAFIM - FEARLESS": "4vbDFu0PUew",
    "LE SSERAFIM - ANTIFRAGILE": "pyf8cbqyfPs",
    # NewJeans
    "NewJeans - Attention": "js1CtxSY38I",
    "NewJeans - Hype Boy": "Rg84ulH0Q6k",
    "NewJeans - Ditto": "V8vU5bW10KY",
    "NewJeans - OMG": "2QWQVm9J5DM",
    # NMIXX
    "NMIXX - O.O": "3GWscde8rM8",
    "NMIXX - DICE": "p1bjnyDqI9k",
    # ATEEZ
    "ATEEZ - Guerrilla": "8dJyRm2jJ-U",
    "ATEEZ - Wonderland": "Z_BhMhZpAug",
    # TREASURE
    "TREASURE - JIKJIN": "PvhW9-4dW9k",
    "TREASURE - BOY": "JSAfPh1A25E",
    # MAMAMOO
    "MAMAMOO - HIP": "KhTeiaCezwM",
    "MAMAMOO - Starry Night": "8OwKiSKidsQ",
    # MONSTA X
    "MONSTA X - Love Killa": "JSOWnSjiA8s",
    "MONSTA X - Gambler": "taViG6-w2uM",
    # GOT7
    "GOT7 - NOT BY THE MOON": "gHYhRACwnmM",
    "GOT7 - Lullaby": "9RUeTYbSOoY",
    # ASTRO
    "ASTRO - ONE": "zdHvj7id4Mk",
    "ASTRO - Candy Sugar Pop": "KZCfhgS2sDg",
    # VICTON
    "VICTON - Mayday": "h3sjXbVbqPY",
    "VICTON - Chronograph": "4W4z0O8v1oM",
    # SF9
    "SF9 - Good Guy": "qqeij8J1RIc",
    "SF9 - Trauma": "a5LfN1asNw8",
    # PENTAGON
    "PENTAGON - Shine": "MVdJ2lN_5Uo",
    "PENTAGON - DO or NOT": "Eomc8DPSBRM",
    # Golden Child
    "Golden Child - ONE(Lucid Dream)": "Oyd01QAdLko",
    "Golden Child - Ra Pam Pam": "2bZzUDSBgSY",
    # Dreamcatcher
    "Dreamcatcher - Scream": "Pq_mbTSR-a0",
    "Dreamcatcher - BOCA": "1QD0FeZyDtg",
    # LOONA
    "LOONA - Butterfly": "XEOCbFJjRw0",
    "LOONA - PTT(Paint The Town)": "TE3sMZD9m8U",
    # EVERGLOW
    "EVERGLOW - DUN DUN": "2N4tXf3Ensw",
    "EVERGLOW - LA DI DA": "jeqdYqsrsA0",
    # AB6IX
    "AB6IX - BREATHE": "9wUKhE2F6c0",
    "AB6IX - STAY YOUNG": "JxUFrpD-Gxw",
    # VERIVERY
    "VERIVERY - G.B.T.B": "DeKNNtS7KpA",
    "VERIVERY - Get Away": "1UgP6mS3hTA",
    # CRAVITY
    "CRAVITY - Break all the Rules": "gukn5y4N13E",
    "CRAVITY - Gas Pedal": "DeG2OdDZ0KY",
    # WEi
    "WEi - TWILIGHT": "H4m5SY2u7do",
    "WEi - Too Bad": "tHZ3_t1nFcE",
    # Weki Meki
    "Weki Meki - Picky Picky": "k6vqVR9K5xg",
    "Weki Meki - Oopsy": "D8VEhcPeSlc",
    # Cherry Bullet
    "Cherry Bullet - Hands Up": "0I5cY9c2JZk",
    "Cherry Bullet - Love So Sweet": "mfJxj1j3Kz0",
    # Kep1er
    "Kep1er - WA DA DA": "tNet5M-rSLE",
    "Kep1er - Up!": "x8eUGJp_0NI",
    # CLC
    "CLC - HELICOPTER": "0FB2EoKTK_Q",
    "CLC - NO": "ytMJ4bTQGDM"
}


def get_video_comments(video_id, max_comments=100):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'maxResults': 100,
        'textFormat': 'plainText',
        'key': API_KEY
    }
    count = 0
    while url and count < max_comments:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch comments for video ID: {video_id}")
            break
        data = response.json()

        for item in data.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "video_id": video_id,
                "author": snippet["authorDisplayName"],
                "text": snippet["textDisplay"],
                "likes": snippet["likeCount"],
                "published_at": snippet["publishedAt"]
            })
            count += 1
            if count >= max_comments:
                break

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break
        time.sleep(1)  # avoid rate limits

    return comments

# Gather comments for all videos
all_comments = []
for title, vid_id in video_ids.items():
    print(f"Collecting comments for: {title}")
    comments = get_video_comments(vid_id, max_comments=100)
    for c in comments:
        c["video_title"] = title
    all_comments.extend(comments)

# Convert to DataFrame
comments_df = pd.DataFrame(all_comments)
comments_df.to_csv("kpop_youtube_comments.csv", index=False)
print("Saved expanded YouTube comments to 'kpop_youtube_comments.csv'")
print(comments_df.head())