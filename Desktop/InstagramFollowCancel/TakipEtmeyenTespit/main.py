import json

# JSON dosyalarından verileri oku
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSON verilerini oku
followers_data = load_json('./followers_1.json')  # Seni takip edenler
following_data = load_json('./following.json')  # Senin takip ettiklerin

# JSON içeriğine göre kullanıcı adlarını çıkar
followers = {item["string_list_data"][0]["value"] for item in followers_data}
following = {item["string_list_data"][0]["value"] for item in following_data["relationships_following"]}

# Seni takip etmeyenleri bul
not_following_back = following - followers

# Sonucu ekrana yazdır
print("Seni takip etmeyen hesaplar:")
for user in sorted(not_following_back):
    print(user)

# Sonucu bir dosyaya kaydetmek için (isteğe bağlı)
with open("not_following_back.json", "w", encoding="utf-8") as output_file:
    json.dump(list(not_following_back), output_file, indent=4, ensure_ascii=False)
