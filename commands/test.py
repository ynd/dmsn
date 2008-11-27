def test(dMsn, args):
 s = ''
 for i in range(0,700):
  s += str(i) + '.'
 
 dMsn.Terminal.writeline('bob said: ' + s + ':)')
