import re
import sys

APP_NAME_RE = re.compile(r'^[a-zA-Z0-9-]+$')

use_postgresql = '{{ cookiecutter.use_postgresql }}'.lower()
use_alembic = '{{ cookiecutter.use_alembic }}'.lower()
use_kafka = '{{ cookiecutter.use_kafka }}'.lower()
use_cache = '{{ cookiecutter.use_cache }}'.lower()

if __name__ == '__main__':
    exit_code = 0

    if use_alembic == 'y' and use_postgresql != 'y':
        print('ERROR: inconsistent configuration, you can\'t use alembic without gino')

        exit_code = 1

    sys.exit(exit_code)
