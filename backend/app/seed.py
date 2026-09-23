"""Initial recipe data. There is no admin UI, so recipes are seeded from here on startup."""

from sqlalchemy import Connection, insert, select

from .models import Recipe

RECIPES = [
    {
        "slug": "nikujaga",
        "title": "ほっこり肉じゃが",
        "description": "甘辛い煮汁がじゃがいもにしみた、定番の家庭料理。",
        "category": "和食",
        "cook_time_minutes": 35,
        "servings": 2,
        "image_path": "/images/nikujaga.svg",
        "ingredients": [
            {"name": "牛薄切り肉", "amount": "150g"},
            {"name": "じゃがいも", "amount": "3個"},
            {"name": "玉ねぎ", "amount": "1個"},
            {"name": "にんじん", "amount": "1/2本"},
            {"name": "しらたき", "amount": "100g"},
            {"name": "だし汁", "amount": "300ml"},
            {"name": "醤油", "amount": "大さじ3"},
            {"name": "みりん", "amount": "大さじ2"},
            {"name": "砂糖", "amount": "大さじ1.5"},
        ],
        "steps": [
            "じゃがいもは一口大に切って水にさらす。玉ねぎはくし切り、にんじんは乱切りにする。",
            "鍋に油を熱し、牛肉を炒める。色が変わったら野菜としらたきを加えて炒め合わせる。",
            "だし汁を加えて煮立て、アクを取る。",
            "砂糖・みりん・醤油を加え、落とし蓋をして中火で15分煮る。",
            "火を止めて10分おき、味をなじませたら完成。",
        ],
    },
    {
        "slug": "oyakodon",
        "title": "とろとろ親子丼",
        "description": "半熟卵でふんわりとじた、10分で作れる丼もの。",
        "category": "和食",
        "cook_time_minutes": 15,
        "servings": 1,
        "image_path": "/images/oyakodon.svg",
        "ingredients": [
            {"name": "鶏もも肉", "amount": "100g"},
            {"name": "玉ねぎ", "amount": "1/4個"},
            {"name": "卵", "amount": "2個"},
            {"name": "ごはん", "amount": "丼1杯"},
            {"name": "めんつゆ(3倍濃縮)", "amount": "大さじ2"},
            {"name": "水", "amount": "80ml"},
            {"name": "三つ葉", "amount": "適量"},
        ],
        "steps": [
            "鶏肉は一口大、玉ねぎは薄切りにする。",
            "小さめのフライパンにめんつゆと水を入れて煮立て、鶏肉と玉ねぎを煮る。",
            "鶏肉に火が通ったら溶き卵の2/3を回し入れ、蓋をして30秒。",
            "残りの卵を加えて火を止め、ごはんにのせて三つ葉を飾る。",
        ],
    },
    {
        "slug": "carbonara",
        "title": "濃厚カルボナーラ",
        "description": "生クリームなし、卵とチーズだけで仕上げる本格派。",
        "category": "洋食",
        "cook_time_minutes": 20,
        "servings": 2,
        "image_path": "/images/carbonara.svg",
        "ingredients": [
            {"name": "スパゲッティ", "amount": "200g"},
            {"name": "ベーコン(ブロック)", "amount": "80g"},
            {"name": "卵黄", "amount": "3個"},
            {"name": "全卵", "amount": "1個"},
            {"name": "パルミジャーノ", "amount": "40g"},
            {"name": "黒こしょう", "amount": "たっぷり"},
        ],
        "steps": [
            "ボウルに卵黄・全卵・すりおろしたチーズを混ぜておく。",
            "塩を入れた湯でスパゲッティを表示時間より1分短くゆでる。",
            "フライパンで拍子木切りにしたベーコンをじっくり炒め、脂を出す。",
            "火を止めてパスタとゆで汁大さじ3を加え、少し冷ましてから卵液を和える。",
            "とろみがついたら皿に盛り、黒こしょうをふる。",
        ],
    },
    {
        "slug": "mapo-tofu",
        "title": "しびれる麻婆豆腐",
        "description": "花椒をきかせた、ごはんが止まらない四川風。",
        "category": "中華",
        "cook_time_minutes": 20,
        "servings": 2,
        "image_path": "/images/mapo-tofu.svg",
        "ingredients": [
            {"name": "木綿豆腐", "amount": "1丁"},
            {"name": "豚ひき肉", "amount": "120g"},
            {"name": "長ねぎ", "amount": "1/2本"},
            {"name": "豆板醤", "amount": "小さじ2"},
            {"name": "甜麺醤", "amount": "大さじ1"},
            {"name": "鶏がらスープ", "amount": "200ml"},
            {"name": "水溶き片栗粉", "amount": "大さじ2"},
            {"name": "花椒", "amount": "小さじ1/2"},
        ],
        "steps": [
            "豆腐は2cm角に切り、塩を入れた湯で2分ゆでて水気を切る。",
            "ひき肉をカリッとするまで炒め、豆板醤・甜麺醤を加えて香りを出す。",
            "スープと豆腐を加えて3分煮る。",
            "水溶き片栗粉で2回に分けてとろみをつけ、ねぎと花椒をちらす。",
        ],
    },
    {
        "slug": "green-curry",
        "title": "タイ風グリーンカレー",
        "description": "ココナッツミルクのコクと青唐辛子の辛さがくせになる。",
        "category": "エスニック",
        "cook_time_minutes": 25,
        "servings": 2,
        "image_path": "/images/green-curry.svg",
        "ingredients": [
            {"name": "鶏むね肉", "amount": "200g"},
            {"name": "なす", "amount": "1本"},
            {"name": "パプリカ(赤)", "amount": "1/2個"},
            {"name": "グリーンカレーペースト", "amount": "30g"},
            {"name": "ココナッツミルク", "amount": "400ml"},
            {"name": "ナンプラー", "amount": "大さじ1"},
            {"name": "砂糖", "amount": "小さじ2"},
            {"name": "バジル", "amount": "1枝"},
        ],
        "steps": [
            "鍋にココナッツミルク100mlとペーストを入れ、油が分離するまで炒める。",
            "そぎ切りにした鶏肉を加えて炒め、残りのココナッツミルクを注ぐ。",
            "なすとパプリカを加えて10分煮る。",
            "ナンプラーと砂糖で味を調え、バジルをのせる。",
        ],
    },
    {
        "slug": "strawberry-panna-cotta",
        "title": "いちごのパンナコッタ",
        "description": "ぷるんとなめらか。いちごソースで見た目も華やかに。",
        "category": "デザート",
        "cook_time_minutes": 20,
        "servings": 4,
        "image_path": "/images/strawberry-panna-cotta.svg",
        "ingredients": [
            {"name": "生クリーム", "amount": "200ml"},
            {"name": "牛乳", "amount": "200ml"},
            {"name": "砂糖", "amount": "40g"},
            {"name": "粉ゼラチン", "amount": "5g"},
            {"name": "いちご", "amount": "150g"},
            {"name": "レモン汁", "amount": "小さじ1"},
        ],
        "steps": [
            "粉ゼラチンを水大さじ2でふやかす。",
            "鍋に生クリーム・牛乳・砂糖30gを入れて温め、火を止めてゼラチンを溶かす。",
            "器に注ぎ、冷蔵庫で3時間以上冷やし固める。",
            "いちごを砂糖10g・レモン汁と電子レンジで2分加熱し、ソースにしてかける。",
        ],
    },
]


def seed_if_empty(conn: Connection) -> None:
    if conn.scalar(select(Recipe.id).limit(1)) is not None:
        return
    conn.execute(insert(Recipe), RECIPES)
