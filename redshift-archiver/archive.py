"""
    Archives data and table structure of Redshift tables

"""

import boto3
import settings
from datetime import datetime

from redash import RedashPoller

def update_create_table_sql(redash):
    r = redash.get_fresh_query_result(6395,{})
    """
        query 6395 is copied from 
        https://github.com/awslabs/amazon-redshift-utils/blob/master/src/AdminViews/v_generate_tbl_ddl.sql
    """

    return r

def get_create_table_sql(schema, table, redash, s3):
    """
        Writes a create table statement for this table
        in the s3 bucket folder bucketname/<schemaname>
    """
    params = {'p_schema': schema, 'p_table': table}
    res = redash.get_fresh_query_result(5927, params)
    """
        query 5927

        -- first, run https://redash.moveon.casa/queries/6395/source 
        -- to update admin.v_generate_tbl_ddl

        select ddl::text
        from admin.v_generate_tbl_ddl
        where schemaname = '{{schema}}'
        and tablename = '{{table}}';
    """
    sql = res.text.replace('ddl\r\n','')
    key = '{0}/{0}.{1}.sql'.format(schema, table)
    print(key)
    s3.Bucket(settings.S3_BUCKET).put_object(Key=key, Body=sql)
    print('wrote table create sql to s3://{}/{}'.format(settings.S3_BUCKET, key))
    return sql

def export_table(schema, table, redash):
    """
        Maybe this will also drop the table after successful export.
        If so, need to be very careful to catch all the errors here.
        Nope, let's do that manually in a separate step.
    """
    params = {
        'p_schema': schema,
        'p_table': table,
        'p_aki': settings.AWS_ACCESS_KEY_ID,
        'p_sak': settings.AWS_SECRET_ACCESS_KEY
    }
    res = redash.get_fresh_query_result(5928, params)
    """ 
        query 5928:

        unload ('select * from {{schema}}.{{table}}')
        to 's3://redshift-archive.moveon.org/{{schema}}.{{table}}/'
        access_key_id '{{aki}}' secret_access_key '{{sak}}'
        manifest gzip csv header allowoverwrite;

        select random();
    """
    # confirm that table data have indeed been exported without errors
    print('exported table data to s3://{}/{}.{}/'.format(settings.S3_BUCKET, schema, table))
    return res

if __name__ == '__main__':
    redash = RedashPoller(settings.REDASH_BASE_URL, settings.REDASH_USER_API_KEY)
    s3 = boto3.resource('s3')
    if settings.refresh_table_create_sql:
        r = update_create_table_sql(redash)
    print("Started archiving at {}".format(datetime.now()))
    for tablename in settings.tables_to_archive:
        schema, table = tablename.split('.')
        sql = get_create_table_sql(schema, table, redash, s3)
        print(sql)
        res = export_table(schema, table, redash)
        print(res)
    print("Finished archiving at {}".format(datetime.now()))

