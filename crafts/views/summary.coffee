(doc) ->
   if doc['type'] isnt 'sample'
      return
   
   res = {}
   for role, hosts of doc['roles']
      res[role] = hosts['stats']

   emit(doc._id, res)
