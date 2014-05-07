(doc, req) ->
   provides("json", () ->

      res = []
      while row = getRow()
         time = Date.parse(row.key[1])
         res = res.concat([[time, row.value["requests"]["sum"]]])

      return JSON.stringify(res)
   )
