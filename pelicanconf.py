AUTHOR = 'Tim Lehr'
SITENAME = 'Tim Lehr'
BIO_TEXT = 'Software Engineer <a href="https://disneyanimation.com" target="_blank" rel="noopener noreferrer">@disneyanimation</a>'
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com" target="_blank" rel="noopener noreferrer">Pelican</a> and <a href="http://pages.github.com">GitHub&nbsp;Pages</a>.'
INDEX_DESCRIPTION = 'Website of Tim Lehr, Software Engineer working at Walt Disney Animation Studios.'

PATH = 'content'

TIMEZONE = 'America/Vancouver'
DEFAULT_DATE_FORMAT = '%B %-d, %Y'
DEFAULT_PAGINATION = False
DEFAULT_LANG = 'en'
SUMMARY_MAX_LENGTH = 42

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Url generation
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'

ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Disable authors, categories, tags, and category pages
DIRECT_TEMPLATES = ['index', 'archives']
CATEGORY_SAVE_AS = ''

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

# PLUGINS
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["sitemap", "assets", "neighbors", "pelican_redirect"]

SITEMAP = {'format': "xml"}

ASSET_SOURCE_PATHS = ['static']
ASSET_CONFIG = [
    ('cache', False),
    ('manifest', False),
    ('url_expire', False),
    ('versions', False),
]

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {'linenums': None},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# *** THEME ***
THEME = 'pneumatic'
THEME_COLOR = '#FFFFFF'
STATIC_PATHS = ['res', "extra", 'articles', 'wp-posts', '.well-known', "extra/CNAME"]

extras = ['CNAME', 'favicon.ico']
EXTRA_PATH_METADATA = {'extra/%s' % file: {'path': file} for file in extras}

ICONS_PATH = 'res/icons'
TYPOGRIFY = True

# Social
SOCIAL_ICONS = [
    ('https://www.linkedin.com/in/lehrtim/', 'LinkedIn', 'fa-linkedin'),
    #('https://twitter.com/PunSolo', 'Twitter', 'fa-twitter'),
    ('https://github.com/timlehr', 'GitHub', 'fa-github'),
    ('https://www.imdb.com/name/nm11461846/', 'IMDb', 'fa-imdb'),
    ('mailto:03.must_gimlets@icloud.com', 'Email', 'fa-envelope'),
]

SIDEBAR_LINKS = [
    '<a href="/about/">About</a>',
    '<a href="/archive/">Archive</a>',
]