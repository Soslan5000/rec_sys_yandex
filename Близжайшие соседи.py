import numpy as np
from scipy import sparse as sp
from tqdm import tqdm
import implicit


track_artists_dict = {} # Словарь, в котором хранятся треки в виде ключей и артисты в виде значений
artists_and_songs = {} # Словарь, в котором хранятся артисты в виде ключей и треки в виде значений (list)
with open('track_artists.csv') as f:
    for line in f:
        track, artist = line.split(',')
        if track.isnumeric():
            track_artists_dict[int(track)] = int(artist)
            if artist not in artists_and_songs:
                artists_and_songs[artist] = [track]
            else:
                artists_and_songs[artist].append(track)

# Делаем статистику прослушиваний каждого артиста отдельными пользователями
artists_statistic = [] # список, в котором элементами будут словари, в которых артисты в виде ключей и количество прослушиваний данного артиста для каждого пользователя в виде значений
track_likes = {} # Количество лайков по трекам
with open('test') as f:
    for line in tqdm(f):
        row = {}
        line = [int(i) for i in line.split(' ')]
        for el in line:
            artist = track_artists_dict[el]
            if artist not in row:
                row[artist] = 0
            row[artist] += 1
            if el not in track_likes:
                track_likes[el] = 0
            track_likes[el] += 1
        artists_statistic.append(row)

# Сортируем словарь песен по популярности в порядке убывания
track_likes = sorted(track_likes.items(), key=lambda x: x[1])
track_likes.reverse()
track_likes = dict(track_likes)
popular_tracks = list(track_likes.keys())

# Сортировка песен во всех списках словаря по популярности в порядке убывания
for el in artists_and_songs:
    songs = artists_and_songs[el]
    indexes = [popular_tracks.index(i) for i in songs]
    lenght = len(indexes)
    for i in range(lenght - 1):
        for j in range(lenght - i - 1):
            if indexes[j] < indexes[j + 1]:
                indexes[j], indexes[j + 1] = indexes[j + 1], indexes[j]
                songs[j], songs[j + 1] = songs[j + 1], songs[j]
    artists_and_songs[el] = songs

# Вычисляем количество артистов
num_of_artists = max(track_artists_dict.keys())

# Напишем функцию, которая преобразует информацию пользователя в coo_matrix формат
def to_coo_row(A, lenght):
    ind = []
    val = []
    for i in A:
        ind.append(i)
        val.append(A[i])
    row = np.array([0]*len(ind))
    col = np.array(ind)
    return sp.coo_matrix((np.array(val).astype(np.float32), (row, col)), shape=(1, lenght))

# Создаём таблицу по всем пользователям формата csr
datas = []
for line in tqdm(artists_statistic):
    datas.append(to_coo_row(line, num_of_artists))

X_sparse = sp.vstack(datas).tocsr()

# Обучаем модель
model = implicit.als.AlternatingLeastSquares(factors=100, regularization=0.02, iterations=1)
model.fit(X_sparse.T)

# Записываем соответствующий словарь для тестовой выборки
artists_statistic = []
with open('test') as f:
    for line in tqdm(f):
        row = {}
        line = [int(i) for i in line.split(' ')]
        for el in line:
            artist = track_artists_dict[el]
            if artist not in row:
                row[artist] = 0
            row[artist] += 1
        artists_statistic.append(row)

# Даём рекоммендации
recommendations = []
f = open('rec', 'w')
t = open('test', 'r')
lines = t.readlines()
ind = 0
for a in tqdm(artists_statistic):
    row = to_coo_row(a, num_of_artists).tocsr()
    row_recs_art = model.recommend(0, row, N=100, filter_already_liked_items=False)
    line = lines[ind].split(' ')
    count = 0
    while True:
        for el in row_recs_art[0].tolist():
            for song in artists_and_songs[el]:
                s = str(song)
                if s not in line:
                    f.writelines(s+' ')
                count += 1
                if count == 100:
                    break
            if count == 100:
                break
        if count == 100:
            f.writelines('\n')
            ind += 1
            break