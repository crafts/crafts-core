import boto.ec2.cloudwatch
import datetime
import crafts.mal

class CloudWatchMALDriver(crafts.mal.MALDriver):
   def get_metrics(self, start, stop):
      c = boto.ec2.cloudwatch.connect_to_region('us-east-1')
      aws_metrics = c.list_metrics(dimensions={"InstanceId":""})

      end = datetime.datetime.utcnow()
      start = end - datetime.timedelta(hours=1)

      interim_metrics = {} 

      for aws_metric in aws_metrics:
         result = aws_metric.query(start, end, ["Average"], period=300)

         instance = aws_metric.dimensions['InstanceId'][0]
         metric_name = aws_metric.name

         if instance not in interim_metrics:
            interim_metrics[instance] = {}

         for dp in result:
            timestamp = dp['Timestamp']

            if timestamp not in interim_metrics[instance]:
               interim_metrics[instance][timestamp] = {}
            
            interim_metrics[instance][timestamp][metric_name] = dp['Average']

      mal_metrics = []

      for host, metrics in interim_metrics.items():
         mal_metric = {}
         mal_metric['host'] = host
         mal_metric['role'] = "web"

         for timestamp, datapoints in metrics.items():
            mal_metric['timestamp'] = timestamp.isoformat()
            mal_metric['metrics'] = datapoints
            mal_metrics.append(dict(mal_metric))

      crafts.mal.insert_metrics(mal_metrics)
