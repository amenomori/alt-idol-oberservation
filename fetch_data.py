from dotenv import load_dotenv
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

load_dotenv(verbose=True)

refresh: bool = True

sp: spotipy.Spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    )
)

artists: str = "artists"

limit: int = 50
offset: int = 0

df_name_genre: pd.DataFrame = pd.DataFrame(columns=["id", "name", "genre"])
df_name_related_name: pd.DataFrame = pd.DataFrame(
    columns=["id", "name", "related_id", "related_name"]
)

while refresh:
    searched: dict = sp.search(
        q="genre:alt-idol",
        limit=limit,
        offset=offset,
        type="artist",
        market="JP",
    )

    for _, item in enumerate(tqdm(searched[artists]["items"])):
        id: str = item["id"]
        name: str = item["name"]
        for _, g in enumerate(item["genres"]):
            df_name_genre.loc[len(df_name_genre)] = [id, name, g]

        related: dict = sp.artist_related_artists(id)
        for _, r in enumerate(related["artists"]):
            df_name_related_name.loc[len(df_name_related_name)] = [
                id,
                name,
                r["id"],
                r["name"],
            ]

    if searched[artists]["next"] is not None:
        offset += limit
    else:
        break

if refresh:
    df_name_genre.to_csv("name_genre.csv", index=False)
    df_name_related_name.to_csv("name_related_name.csv", index=False)
