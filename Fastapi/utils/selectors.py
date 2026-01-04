"""
CSS selectors for different news sources.
"""

SELECTORS = {
    "Detik": ["media__title", "title", "h2", "article-title", "list-content__title", "media__link"],
    "Kompas": ["article__list__title", "title", "h3", "article-title", "headline__title", "kcm__title"],
    "CNN Indonesia": ["h2", "title", "article-title", "list__title", "nhd__title", "headline"],
    "Tempo": ["title", "h2", "h3", "article__title", "post-title", "judul"],
    "Tribunnews": ["txt-oev-2", "title", "h2", "article-title", "fbo2", "txt-oev-3"],
    "Liputan6": ["articles--iridescent-list--text-item__title", "title", "h2", "article-title", "headline", "list__title"],
    "Republika": ["h3", "title", "h2", "article-title", "headline", "post__title"],
    "Okezone": ["title", "h2", "h3", "article-title", "list-berita__title", "judul"],
    "Suara": ["inject-title", "title", "h2", "article-title", "headline", "post-title"],
    "Viva": ["title", "h2", "h3", "article-title", "headline", "news-title"],
    "Sindonews": ["title", "h2", "article-title", "headline"],
    "Antara News": ["title", "h2", "article-title", "post-title"],
    "Bisnis.com": ["title", "h2", "article-title", "headline"],
    "Jawa Pos": ["title", "h2", "article-title", "post-title"],
    "BBC Indonesia": ["title", "h2", "article-title", "headline"]
}
