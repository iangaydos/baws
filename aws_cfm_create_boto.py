import boto3, time

# disclaimers
print ' ***** '
print 'This is program is for demostration purposes only and not production worthy code.'
print 'You should have prereqs installed as listed at http://iangaydos.com'
print 'Please note that AWS will charge you for any resources created by CloudFormation.'
print 'You can delete this stack following execution but you will incur charges after executing.'
print ' ***** '

# hardcode sample elb cloudformation template from amazon
# noinspection PyPep8
template_url = "https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2/ELBWithLockedDownAutoScaledInstances.template"
print 'For this demo we will use the AWS template from: ' + template_url
print ' ***** '

# gather inputs from the user before deploying the stack
ec2_instance_type = raw_input('Please input EC2 instance class (t1.micro, t2.micro, or t2.small): ')
print 'For demo purposes, keep instance class small to minimize cost.'
pem_key_name = raw_input('Please enter the key pair name to use for SSH into EC2 instances: ')
stack_name = raw_input('Please enter your stack name with no spaces or special characters (e.g., MyCFMtestStack): ')

# establish low-level client to cloudformation
client = boto3.client('cloudformation')


# call the create_stack method using the user inputs as parameters
response = client.create_stack(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=[
            {
                'ParameterKey': 'InstanceType',
                'ParameterValue': ec2_instance_type
            },
            {
                'ParameterKey': 'KeyName',
                'ParameterValue': pem_key_name
            }
        ],
        TimeoutInMinutes=10,
        ResourceTypes=[
            'AWS::*'
        ],
        OnFailure='ROLLBACK',
        Tags=[
            {
                'Key': 'description',
                'Value': 'This is a test stack created using boto3 from Python'
            },
        ]
)

# checking status of creation before gathering outputs
cloudformation = boto3.resource('cloudformation')
stack = cloudformation.Stack(name=stack_name)

current_stack_status = stack.stack_status
print 'Your stack is being created. Status will update every 1 min'

while stack.stack_status == 'CREATE_IN_PROGRESS':
    time.sleep(60)
    stack.reload()  # reload the status after waiting 60 secs
    current_stack_status = stack.stack_status
    print 'Checking again after 1 min. Current stack status is: ' + current_stack_status

# get the url of the elastic load balancer created by CloudFormation
output = stack.outputs[0]
elb_url = output['OutputValue']
print ' **** '
print 'You can now test your deployed stack at: ' + elb_url

print 'Do not forget to delete your stack in the console to avoid additional charges.'


