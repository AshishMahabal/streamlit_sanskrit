def list2dict(inlist):
	l1 = inlist[0::2]
	l2 = inlist[1::2]
	return dict(zip(l1,l2))
