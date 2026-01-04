"""
News sources configuration.
Contains all news sources and their category URLs.
"""

NEWS_SOURCES = {
    "Detik": {
        "Terpopuler": "https://www.detik.com/terpopuler",
        "Otomotif": "https://oto.detik.com/",
        "Politik": "https://news.detik.com/politik",
        "Ekonomi": "https://finance.detik.com/",
        "Olahraga": "https://sport.detik.com/",
        "Teknologi": "https://inet.detik.com/",
        "Hiburan": "https://20.detik.com/"
    },
    "Kompas": {
        "Tren": "https://www.kompas.com/tren",
        "Otomotif": "https://otomotif.kompas.com/",
        "Politik": "https://nasional.kompas.com/politik",
        "Ekonomi": "https://money.kompas.com/",
        "Olahraga": "https://bola.kompas.com/",
        "Teknologi": "https://tekno.kompas.com/",
        "Hiburan": "https://www.kompas.com/hype"
    },
    "CNN Indonesia": {
        "Nasional": "https://www.cnnindonesia.com/nasional",
        "Otomotif": "https://www.cnnindonesia.com/otomotif",
        "Politik": "https://www.cnnindonesia.com/politik",
        "Ekonomi": "https://www.cnnindonesia.com/ekonomi",
        "Olahraga": "https://www.cnnindonesia.com/olahraga",
        "Teknologi": "https://www.cnnindonesia.com/teknologi",
        "Hiburan": "https://www.cnnindonesia.com/hiburan"
    },
    "Tempo": {
        "Terpopuler": "https://www.tempo.co/terpopuler",
        "Otomotif": "https://otomotif.tempo.co/",
        "Politik": "https://nasional.tempo.co/politik",
        "Ekonomi": "https://bisnis.tempo.co/",
        "Olahraga": "https://sport.tempo.co/",
        "Teknologi": "https://tekno.tempo.co/",
        "Hiburan": "https://cantik.tempo.co/"
    },
    "Tribunnews": {
        "Populer": "https://www.tribunnews.com/populer",
        "Otomotif": "https://www.tribunnews.com/otomotif",
        "Politik": "https://www.tribunnews.com/politik",
        "Ekonomi": "https://www.tribunnews.com/bisnis",
        "Olahraga": "https://www.tribunnews.com/sport",
        "Teknologi": "https://www.tribunnews.com/techno",
        "Hiburan": "https://www.tribunnews.com/seleb"
    },
    "Liputan6": {
        "News": "https://www.liputan6.com/news",
        "Otomotif": "https://www.liputan6.com/otomotif",
        "Politik": "https://www.liputan6.com/news/politik",
        "Ekonomi": "https://www.liputan6.com/bisnis",
        "Olahraga": "https://www.liputan6.com/bola",
        "Teknologi": "https://www.liputan6.com/tekno",
        "Hiburan": "https://www.liputan6.com/showbiz"
    },
    "Republika": {
        "Terpopuler": "https://www.republika.co.id/terpopuler",
        "Otomotif": "https://otomotif.republika.co.id/",
        "Politik": "https://nasional.republika.co.id/politik",
        "Ekonomi": "https://ekonomi.republika.co.id/",
        "Olahraga": "https://olahraga.republika.co.id/",
        "Teknologi": "https://tekno.republika.co.id/",
        "Islam": "https://islam.republika.co.id/"
    },
    "Okezone": {
        "Beranda": "https://www.okezone.com/",
        "Otomotif": "https://otomotif.okezone.com/",
        "Politik": "https://nasional.okezone.com/politik",
        "Ekonomi": "https://economy.okezone.com/",
        "Olahraga": "https://sports.okezone.com/",
        "Teknologi": "https://techno.okezone.com/",
        "Hiburan": "https://celebrity.okezone.com/"
    },
    "Suara": {
        "Terpopuler": "https://www.suara.com/terpopuler",
        "Otomotif": "https://www.suara.com/otomotif",
        "Politik": "https://www.suara.com/politik",
        "Ekonomi": "https://www.suara.com/bisnis",
        "Olahraga": "https://www.suara.com/sport",
        "Teknologi": "https://www.suara.com/tekno",
        "Hiburan": "https://www.suara.com/entertainment"
    },
    "Viva": {
        "Berita": "https://www.viva.co.id/berita",
        "Otomotif": "https://www.viva.co.id/otomotif",
        "Politik": "https://www.viva.co.id/berita/politik",
        "Ekonomi": "https://www.viva.co.id/berita/bisnis",
        "Olahraga": "https://www.viva.co.id/sport",
        "Teknologi": "https://www.viva.co.id/digital",
        "Hiburan": "https://www.viva.co.id/showbiz"
    },
    "Sindonews": {
        "Nasional": "https://nasional.sindonews.com/",
        "Otomotif": "https://otomotif.sindonews.com/",
        "Ekonomi": "https://ekonomi.sindonews.com/",
        "Olahraga": "https://sports.sindonews.com/",
        "Teknologi": "https://tekno.sindonews.com/",
        "Hiburan": "https://lifestyle.sindonews.com/"
    },
    "Antara News": {
        "Nasional": "https://www.antaranews.com/nasional",
        "Ekonomi": "https://www.antaranews.com/ekonomi",
        "Olahraga": "https://www.antaranews.com/olahraga",
        "Teknologi": "https://www.antaranews.com/teknologi",
        "Hiburan": "https://www.antaranews.com/hiburan"
    },
    "Bisnis.com": {
        "Ekonomi": "https://ekonomi.bisnis.com/",
        "Otomotif": "https://otomotif.bisnis.com/",
        "Teknologi": "https://teknologi.bisnis.com/",
        "Hiburan": "https://lifestyle.bisnis.com/"
    },
    "Jawa Pos": {
        "Nasional": "https://www.jawapos.com/nasional",
        "Ekonomi": "https://www.jawapos.com/ekonomi",
        "Olahraga": "https://www.jawapos.com/olahraga",
        "Teknologi": "https://www.jawapos.com/tekno",
        "Hiburan": "https://www.jawapos.com/entertainment"
    },
    "BBC Indonesia": {
        "Berita": "https://www.bbc.com/indonesia",
        "Internasional": "https://www.bbc.com/indonesia/internasional",
        "Teknologi": "https://www.bbc.com/indonesia/majalah"
    }
}
