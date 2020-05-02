#!/usr/bin/env python

import boto3
from datetime import date, datetime

iam = boto3.client('iam')

def get_all_users():
    '''
    This function returns a list of all users. This user list will used when getting all other details
    :return:
    '''

    users = []
    paginator = iam.get_paginator('list_users')
    for page in paginator.paginate():
        for user in page['Users']:
            users.append(user['UserName'])
    return users

def get_user_groups(username):
    '''
    This functions returns a list of groups per user
    :param username:
    :return:
    '''

    groups = []

    list_of_groups = iam.list_groups_for_user(UserName=username)
    for group in list_of_groups['Groups']:
        groups.append(group['GroupName'])
    return groups

def get_access_key_age(username):
    '''
    This function returns age, in days, of the user access key
    :param username:
    :return:
    '''

    try:
        res = iam.list_access_keys(UserName=username)
        accesskeydate = res['AccessKeyMetadata'][0]['CreateDate'].date()
        currentdate = date.today()
        active_days = currentdate - accesskeydate
        return str(active_days).strip(', 0:00:00')
    except IndexError:
        return 'None'


def get_password_last_used(username):
    '''
    This function returns the last time, in days, the password was used to login to the console by a user
    :param username:
    :return:
    '''
    try:
        iam = boto3.resource('iam')
        user = iam.User(username)
        passwd_last_use = user.password_last_used.date()
        currentdate = date.today()
        active_days = currentdate - passwd_last_use
        return str(active_days).strip(', 0:00:00')
    except AttributeError:
        return 'None'

def get_mfa(username):
    '''
    This function retuns whether a user has MFA enabled or not
    :param username:
    :return:
    '''

    list_of_mfa_devices = iam.list_mfa_devices(UserName=username)
    for key in list_of_mfa_devices['MFADevices']:
        if key['UserName'] == username:
            return 'MFA enabled'
    if len(list_of_mfa_devices['MFADevices']) == 0:
        return 'No MFA enabled'

def get_user_access_key_id(username):
    data = iam.list_access_keys(UserName=username)
    ak = data['AccessKeyMetadata'][0]['AccessKeyId']
    return ak

def access_key_last_used(username):
    '''
    This function returns ths last time, in days, the access key was used for a user
    :param username:
    :return:
    '''
    try:
        ak = get_user_access_key_id(username)
        last_used = iam.get_access_key_last_used(AccessKeyId=ak)
        lu_date = last_used['AccessKeyLastUsed']['LastUsedDate'].date()
        currentdate = date.today()
        active_days = currentdate - lu_date
        return str(active_days).strip(', 0:00:00')
    except IndexError:
        return 'None'
    except KeyError:
        return 'None'

def main():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M")
    f = open("aws_user_details_{}.csv".format(dt_string), "w+")
    users = get_all_users()
    f.write('User' + ',' + 'Groups' + ',' + 'Access Key Age' + ',' + 'Access Key Last Used' + ',' + 'Password Last Used' + ',' + 'MFA' + '\n')
    for username in users:
        groups = get_user_groups(username)
        if groups == []:
            groups = 'No Groups'
        access_key_age = get_access_key_age(username)
        pass_last_used = get_password_last_used(username)
        if pass_last_used == '':
            pass_last_used = 'Today'
        elif pass_last_used == 'None':
            pass_last_used = 'Never Used'
        mfa = get_mfa(username)
        access_key_last = access_key_last_used(username)
        if access_key_last == '':
            access_key_last = 'Today'
        elif access_key_last == 'None':
            access_key_last = 'Never Used'

        f.write(username + ',' + ' '.join(groups) + ',' + access_key_age + ',' + access_key_last + ',' + pass_last_used
         + ',' + mfa + '\n')

        print(username + ','  + ' '.join(groups) + ',' + access_key_age + ',' + access_key_last + ',' + pass_last_used
              + ',' + mfa)
    f.close()

if __name__ == "__main__":
    main()
