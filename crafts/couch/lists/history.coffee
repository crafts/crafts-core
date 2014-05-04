(doc, req) ->
   provides("json", () ->

      res = []
      while row = getRow()
         time = Date.parse(row.key)
         for key, value of row.value
            res = res.concat([[time, value["requests"]["sum"]]])

      return JSON.stringify(res)
   )
