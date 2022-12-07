track_stats = {}

with open('train') as f:
    lines = f.readlines()
    for line in lines:
        tracks = line.strip().split(' ')
        for track in tracks:
            if track not in track_stats:
                track_stats[track] = 0
            track_stats[track] += 1

with open('test') as f:
    test = f.readlines()

popular_tracks = sorted(track_stats.items(), key=lambda item: item[1], reverse=True)[:100]
popular_tracks_list = [x[0] for x in popular_tracks]

top_tracks = sorted(track_stats.items(), key=lambda item: item[1], reverse=True)[:1000]
top_tracks_set = set([x[0] for x in top_tracks])

global_track_score = {}
for track in top_tracks:
    global_track_score[track[0]] = track_stats[track[0]] ** 0.5

track_count = {}
with open('train') as f:
    lines = f.readlines()
    for (i, line) in enumerate(lines):
        tracks = line.strip().split(' ')
        filtered_tracks = []
        for track in tracks:
            if track in top_tracks_set:
                filtered_tracks.append(track)
        for i in range(len(filtered_tracks)):
            track1 = filtered_tracks[i]
            for j in range(len(filtered_tracks)):
                if i != j:
                    track2 = filtered_tracks[j]
                    if track1 not in track_count:
                        track_count[track1] = {}
                    current_count = track_count[track1]
                    if track2 not in current_count:
                        current_count[track2] = 0
                    current_count[track2] += 1

result = []
empty_track_score = 0
for query in test:
    test_tracks = query.strip().split(' ')
    track_score = {}
    for track in test_tracks:
        if track in track_count:
            for track_id in track_count[track]:
                score = track_count[track][track_id]
                if track_id not in track_score:
                    track_score[track_id] = 0
                track_score[track_id] += score / global_track_score[track] / global_track_score[track_id]
    if len(track_score) == 0:
        result.append(' '.join(popular_tracks_list) + '\n')
        empty_track_score += 1
    else:
        best_tracks = sorted(track_score.items(), key=lambda item: item[1], reverse=True)[:100]
        result.append(' '.join([x[0] for x in best_tracks]) + '\n')

with open('result.txt', 'w') as f:
    f.writelines(result)
