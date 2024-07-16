.. _setup_install:

Python and Poetry Setup
===========================================

- Athena requires Python 3.11. You can install it from the `Python website <https://www.python.org/downloads/>`_.
- Athena uses `Poetry <https://python-poetry.org/>`_ instead of pip to manage dependencies. You can find installation instructions on the `Poetry website <https://python-poetry.org/docs/>`_.

You can install all dependencies of a poetry project using

    .. code-block:: bash

        poetry install

You'll have to do this once in the following folders to set up the project:

- ``assessment_module_manager``
- ``athena``
- ``module_*`` (for each module)

.. note::
    | The ``psycopg2`` module needs PostgreSQL to be installed on your system. You can find installation instructions on the `PostgreSQL website <https://www.postgresql.org/download/>`_.
    | Example to install it on MacOS: ``brew install postgresql``

You can find more information about Poetry in the `Poetry documentation <https://python-poetry.org/docs/>`_.