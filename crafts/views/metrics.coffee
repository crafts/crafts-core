(doc) ->
   if doc['type'] isnt 'sample'
      return
   
   emit(doc._id, doc['roles'])
