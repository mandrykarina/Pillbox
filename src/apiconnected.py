from yandex_music import Client

token = 'y0_AgAAAAA2DZGJAAG8XgAAAAD4hlk7I8DRDKyCS7Sj-76dHMBPd9IUD1Q'
client = Client(token).init()

track_name = 'Starboy'
search_results = client.search(track_name)

# Проверяем результаты поиска
if search_results and search_results.tracks:
    found_track = search_results.tracks
    print(found_track)

    # навание трека и автор
    title = found_track.results[0].title
    author = found_track.results[0].artists[0].name

    print(title, '-', author)

    # Получаем ID найденного трека
    track_id = found_track.results[0].id
    print("ID трека:", track_id)
else:
    print("Трек не найден")










