(doc) ->
   if doc['type'] isnt 'sample'
      return

   for role, hosts of doc['roles']
      emit([role, doc._id], hosts)
