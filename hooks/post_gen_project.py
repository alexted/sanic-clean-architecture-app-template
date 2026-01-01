import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_directory(directory):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, directory))


def make_directory(directory):
    os.mkdir(os.path.join(PROJECT_DIRECTORY, directory))


def copy_directory(directory, destination):
    shutil.copytree(directory, destination)


use_postgresql = '{{ cookiecutter.use_postgresql }}'.lower()
use_alembic = '{{ cookiecutter.use_alembic }}'.lower()
use_kafka = '{{ cookiecutter.use_kafka }}'.lower()
use_cache = '{{ cookiecutter.use_cache }}'.lower()

if __name__ == '__main__':
    if use_alembic != 'y':
        remove_file('alembic.ini')
        remove_directory(f'src/infrastructure/postgres/migrations')

    if use_postgresql != 'y':
        remove_directory(f'src/infrastructure/postgres')
        remove_directory(f'src/data/items')
        remove_file(f'src/api/items.py')
        remove_directory(f'src/use_cases/items')
        remove_file('tests/data/expected_data.py')
        remove_file('tests/data/mock_data.py')
        remove_file('tests/test_items.py')

    if use_kafka != 'y':
        remove_file('src/infrastructure/kafka.py')

    if use_cache != 'y':
        remove_file(f'src/infrastructure/cache.py')
