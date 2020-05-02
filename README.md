# AWS IAM user details 

This is basic Python script to obtain IAM user details

#### Requirements

1. AWS credentials configured in user home directory as ~/.aws/credentials with format:
```
[default]
aws_access_key_id = KEY_ID_HERE
aws_secret_access_key = ACCESS_KEY_HERE
```

2. Python 3
3. The following python libraries :
        1. boto3


#### Details

The script will produce a CSV file with the following columns and related content:

1. User - The name of the IAM user
2. Groups - What groups the user belongs to
3. Access Key Age - The age of the user's access key in days
4. Password Last Used - When the user last logged into the console in days
5. MFA - Whether the user has Multi Factor Authentication enabled on their account
