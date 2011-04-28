SETUP = {
	"blog-title": "Refaktor Labs Blog",
	"title-separator": "::",
	"template": "basic"
}

MEMO = {} #we memoize templates

from BeautifulSoup import BeautifulSoup
import unicodedata, pickle, datetime, re, os, errno

def process_inbox():
	posts = []
	for file in get_inbox_files():
		f = open(file[0])
		posts.insert(0, make_blogpost(f.read()))
		f.close()
		os.rename(file[0], file[1])
	if len(posts):
		print "found new posts"
		posts.extend(pickle.load(open("posts.pickled")))
		update_index(posts)
		pickle.dump(posts, open("posts.pickled", "w"))

def get_inbox_files():
	return [ ("../inbox/"+file, "../inbox/zzz__"+file,) for file in os.listdir("../inbox") if not file.startswith("zaazz__") ]

#post

def make_blogpost(post):
	title = get_title(post)
	time = datetime.datetime.now()
	r = { "title": title, "slug": get_slug(title), "year": time.year, 'month': time.month }
	dir = "../%(year)s/%(month)s/" % r;
	assure_dir(dir);
	open(dir+r["slug"]+'.html', 'w').write(gen_post_page(post, title))
	return r

def gen_post_page(post, title):
	return templatize("header", dict(SETUP, **{"title": title})) + \
		"<!--content-->" + post + "<!--/content-->" + \
		templatize("footer", SETUP)

def get_title(data):
	return BeautifulSoup(data).find('h2').renderContents()

def assure_dir(dir):
	try:
		os.makedirs(dir)
	except OSError, e:
		if e.errno != errno.EEXIST:
			raise

#index

def update_index(posts):
	open("../index.html", "w").write(gen_index(posts))

def gen_index(posts):
	return templatize("index-header", SETUP) + \
		gen_index_list(posts) + \
		templatize("index-footer", SETUP)

def gen_index_list(posts):
	return reduce(lambda acc, post: acc + templatize("index-posts", post), posts, "")

#tpl

def templatize(tpl, data):
	return get_tpl(tpl) % data

def get_tpl(name):
	return MEMO['tpl'+name] if name in MEMO else load_tpl(name)

def load_tpl(name):
	MEMO['tpl'+name] = r = open("../templates/%(template)s/%(tplname)s.html" % dict(SETUP, **{"tplname": name })).read()
	return r

#util

def get_slug(value):
	_slugify_strip_re = re.compile(r'[^\w\s-]')
	_slugify_hyphenate_re = re.compile(r'[-\s]+')
	if not isinstance(value, unicode):
		value = unicode(value)
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(_slugify_strip_re.sub('', value).strip().lower())
	return _slugify_hyphenate_re.sub('-', value)

if __name__ == '__main__':
	process_inbox()
