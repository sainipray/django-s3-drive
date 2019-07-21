import os
import posixpath

from storages.backends.s3boto3 import S3Boto3Storage


class PrivateS3Storage(S3Boto3Storage):

    file_overwrite = False
    custom_domain = False

    def listdir(self, name):
        path = self._normalize_name(self._clean_name(name))
        if path and not path.endswith('/'):
            path += '/'
        directories = []
        files = []
        paginator = self.connection.meta.client.get_paginator('list_objects')
        pages = paginator.paginate(Bucket=self.bucket_name, Delimiter='/', Prefix=path)
        for page in pages:
            for entry in page.get('CommonPrefixes', ()):
                directories.append(posixpath.relpath(entry['Prefix'], path))
            for entry in page.get('Contents', ()):
                files.append({'Key': posixpath.relpath(entry['Key'], path),
                              'LastModified': entry['LastModified'],
                              'Size': entry['Size']})
        return directories, files
