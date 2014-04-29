(doc) ->
   if doc['type'] isnt 'sample'
      return
   
   for role, hosts of doc['roles']
      for metric, stats of hosts['stats']
         emit([role, metric, doc._id], stats)
