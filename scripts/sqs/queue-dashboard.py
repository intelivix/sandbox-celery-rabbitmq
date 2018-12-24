from decouple import config
import boto3
from jinja2 import Template

QUEUE_NAME = config('QUEUE_NAME', default='queue-example')
cloudwatch = boto3.client('cloudwatch')


def context_(template_name='aws/dashboard.json.jinja2'):
    with open(template_name, 'r') as file_:
        template = Template(file_.read())
    return template.render(queue_name=QUEUE_NAME)


if __name__ == '__main__':
    dashboard_body_json = context_()
    response = cloudwatch.put_dashboard(
        DashboardName=f'{QUEUE_NAME}-dashboard',
        DashboardBody=dashboard_body_json
    )

    if not response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        Exception('Problems during the dashboard creation.')
