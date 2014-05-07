(doc) ->
   if doc.type isnt "sample"
      return

   emit([doc.role, doc.timestamp], doc.hosts)
