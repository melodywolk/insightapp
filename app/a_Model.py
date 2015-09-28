def ModelIt(fromUser  = 'Default', name =''):
  print 'The Name is %s' % name
  result = name+'_Pouet'
  if fromUser != 'Default':
    return result
  else:
    return 'check your input'
