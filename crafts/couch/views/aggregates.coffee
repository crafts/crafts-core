(doc) ->
   if doc.type isnt "sample"
      return

   aggregate = {}

   for host, metrics of doc.hosts
      for metric, value of metrics
         if metric not of aggregate
            aggregate[metric] = {
               count: 0,
               sum: 0,
               min: value,
               max: 0,
               avg: 0
            }
            measure = aggregate[metric]

         measure.count += 1
         measure.sum += value
         measure.min = if value < measure.min then value else measure.min
         measure.max = if value > measure.max then value else measure.max
         measure.avg = measure.sum / measure.count

   emit([doc.role, doc.timestamp], aggregate)
