import re

title_stop_words = set('''able about across after all almost also am among an and any are as at be because been but by can cannot could dear did do does either else ever every for from get got had has have he her hers him his how however if in into is it its just least let like likely may me might most must my neither no nor not of off often on only or other our own rather said say says she should since so some than that the their them then there these they this tis to too twas us wants was we were what when where which while who whom why will with would yet you your'''.split())


def title(body):
	MIN_WORD_LENGTH = 2

	words = set()
	
	WORDS_RE = re.compile("[a-z']{2,}")

	for match in WORDS_RE.finditer(body.lower()):
		word = match.group().strip("'")

		if len(word) > MIN_WORD_LENGTH:
			words.add(word)

	return words - title_stop_words



def abstract(body):
	pass