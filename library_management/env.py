import json
import os


def get_credentials():
    creds = {}
    if "env" in os.environ:
        creds['debug'] = os.environ['debug']
        creds['allowed_hosts'] = os.environ['allowed_hosts']
        creds['django_secret_key'] = os.environ['django_secret_key']
        # creds['db_name'] = os.environ['db_name']
        # creds['db_user'] = os.environ['db_user']
        # creds['db_host'] = os.environ['db_host']
        # creds['cors_origin_whitelist'] = os.environ['cors_origin_whitelist']
        # creds['aws_access_key'] = os.environ['aws_access_key']
        # creds['aws_secret_key'] = os.environ['aws_secret_key']
        # creds['email_via'] = os.environ['email_via']
        # creds['email_host'] = os.environ['email_host']
        # creds['email_user'] = os.environ['email_user']
        # creds['email_password'] = os.environ['email_password']
        # creds['s3_bucket'] = os.environ['s3_bucket']
    else:
        env_file_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(env_file_dir, '.env'), 'r') as f:
            creds = json.loads(f.read())
    return creds


credentials = get_credentials()
