import uuid
import re


def _set_common(r, r_method, names, ttl=30, execute=True):

	id = str(uuid.uuid4())

	pipeline = r.pipeline(True) if execute else r

	names = ['idx:' + name for name in names]

	getattr(pipeline, r_method)('idx:' + id, *names)
	
	pipeline.expire('idx:' + id, ttl)

	if execute:
		pipeline.execute()

	return id




def intersect(r, items, ttl=30, _execute=True):
	return _set_common(r, 'sinterstore', items, ttl, _execute)



def union(r, items, ttl=30, _execute=True):
	return _set_common(r, 'sunionstore', items, ttl, _execute)



def difference(r, items, ttl=30, _execute=True):
	return _set_common(r, 'sdiffstore', items, ttl, _execute)



QUERY_RE = re.compile("[+-]?[a-z']{2,}")
MIN_WORD_LENGTH = 2
title_stop_words = set('''able about across after all almost also am among an and any are as at be because been but by can cannot could dear did do does either else ever every for from get got had has have he her hers him his how however if in into is it its just least let like likely may me might most must my neither no nor not of off often on only or other our own rather said say says she should since so some than that the their them then there these they this tis to too twas us wants was we were what when where which while who whom why will with would yet you your'''.split())


def parse_query(q):
	print "Search for: ", q

	unwanted = set()

	all = []
	
	current = set()

	for match in QUERY_RE.finditer(q.lower()):
		word = match.group()
		prefix = word[:1]

		if prefix in '+-':
			word = word[1:]
		else:
			prefix = None

		word = word.strip("'")
		
		if len(word) < MIN_WORD_LENGTH or word in title_stop_words:
			continue

		if prefix == '-':
			unwanted.add(word)
			continue

		if current and not prefix:
			all.append(list(current))
			current = set()

		current.add(word)

		if current:
			all.append(list(current))

	return all, list(unwanted)





def parse_and_search(r, q, ttl=30):	
	all, unwanted = parse_query(q)
	
	if not all:
		return None

	to_intersect = []

	for syn in all:
		if len(syn) > 1:
			to_intersect.append(union(r, syn, ttl=ttl))
		else:
			to_intersect.append(syn[0])

		if len(to_intersect) > 1:
			intersect_result = intersect(r, to_intersect, ttl=ttl)
		else:
			intersect_result = to_intersect[0]

		if unwanted:
			unwanted.insert(0, intersect_result)
			return difference(r, unwanted, ttl=ttl)

	return intersect_result

