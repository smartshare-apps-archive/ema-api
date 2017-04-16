
def index_article(r, pmid, tokens):
	pipeline = r.pipeline(True)

	for token in tokens:
		pipeline.sadd('idx:' + token, pmid)

	return len(pipeline.execute())