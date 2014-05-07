(doc) ->
   if doc.type isnt "prediction"
      return

   emit([doc.role, doc.timestamp], doc.predictions)
