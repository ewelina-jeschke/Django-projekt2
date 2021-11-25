DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project2',
        'USER': 'postgres',
        'PASSWORD': 'myPassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
