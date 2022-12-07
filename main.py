import numpy as np
from scipy import sparse as sp
from tqdm import tqdm
import implicit

def to_coo_row(A, lenght):
    ind = []
    val = []
    for i in A:
        ind.append(i)
        val.append(1)
    row = np.array([0]*len(ind))
    col = np.array(ind)
    return sp.coo_matrix((np.array(val), (row, col)), shape=(1, lenght+1))

def num_of_songs(name):
    print('Парсим файл', name)
    number_of_songs = 0
    with open(name) as f:
        lines = f.readlines()
        for line in tqdm(lines):
            song = line.split(',')[0]
            if song.isnumeric():
                number_of_songs = max(number_of_songs, int(song))
    return number_of_songs

def train_datas_csr(name, number_of_songs):
    datas = []
    print('Парсим файл', name)
    with open(name) as f:
        lines = f.readlines()
        for line in tqdm(lines):
            row = []
            tracks = line.strip().split(' ')
            for track in tracks:
                row.append(int(track))
            datas.append(to_coo_row(row, number_of_songs))
    print('Объединяем строки')
    X_sparse = sp.vstack(datas).tocsr()
    return X_sparse

def learn(X_sparse, itters):
    print('Обучаем модель')
    model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=itters)
    model.fit(X_sparse.T)
    return model

def reccomendation(name, model, number_of_songs):
    print('Парсим файл test')
    with open('test') as f:
        with open(name, 'w') as p:
            lines = f.readlines()
            for line in tqdm(lines):
                row = []
                tracks = line.strip().split(' ')
                for track in tracks:
                    row.append(int(track))
                row = to_coo_row(row, number_of_songs).tocsr()
                raw_recs = model.recommend(userid=0, user_items=row, N=100, filter_already_liked_items=True, recalculate_user=True)
                for el in raw_recs[0]:
                    p.writelines(str(el) + ' ')
                p.writelines('\n')


n_songs = num_of_songs('track_artists.csv')
X_sparse = train_datas_csr('train', n_songs)
for i in range(1, 10, 2):
    name = str(i) + ' itter' + '.txt'
    print('Обучаем модель. Количество иттераций:', i)
    model = learn(X_sparse, i)
    print('Заполняем файл', name)
    reccomendation(name, model, n_songs)
