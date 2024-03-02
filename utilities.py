from PIL import Image
import glob
import os
import requests
from sqlalchemy import create_engine
import pandas as pd
import csv
from tqdm import tqdm


def thumbnail(path):
    for i in path:
        print(i)
        newpath = r'E:\Dev\PythonSeries\flaskwatchlist\watchlist\static\images\thumb'
        newpath = os.path.join(newpath, os.path.basename(i).split('.')[0] + '_thumb.jpg')
        im = Image.open(i)
        if im.mode == 'P' or im.mode == 'RGBA':
            im = im.convert('RGB')
        # resize image
        # im.thumbnail((150, 90))
        im = im.resize((500, 300))
        # save image
        im.save(newpath, 'JPEG')
    print('done!')


def getposter():
    engine = create_engine('sqlite:///data.sqlite3')
    df = pd.read_sql_table('movie', engine)
    df.to_csv('movie.csv', index=False)
    s = []
    csv_file_path = 'movie.csv'
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        for i in csvreader:
            s.append(i[3])    
    return s

def getimage():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    path = r'E:/Dev/PythonSeries/flaskwatchlist/watchlist/static/images/poster'
    s = getposter()
    for i in tqdm(s, desc='Downloading images'):
        if i:
            try: 
                r = requests.get(i, headers=headers, stream=True) # 开启流模式
                if r.status_code == 200:
                    file_size = int(r.headers.get('content-length', 0)) # 获取内容总长度
                    file_name = os.path.join(path, i.split('/')[-1].split('.')[0] + '.webp')
                # 进度条
                    progress = tqdm(total=file_size, unit='iB', unit_scale=True,
                                    desc=file_name, initial=0, ascii=True)
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024): # 每次下载1KB
                            if chunk: # 过滤掉keep-alive新块
                                progress.update(len(chunk))
                                f.write(chunk)
                    progress.close()
                    if file_size != 0 and progress.n != file_size:
                        print(f"ERROR, something went wrong with {i}")
                else:
                    print(f'Failed to retrieve {i} with status code: {r.status_code}')
            except requests.RequestException as e:
                print(f'An error occurred: {e}')


        
        

    
if __name__ == '__main__':
    
    path = glob.glob(r'E:\Dev\PythonSeries\flaskwatchlist\watchlist\static\images\*.jpg')
    thumbnail(path)
    
    