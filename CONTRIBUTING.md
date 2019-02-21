# Contribution Guide

Here are some contribution guide if you want to contribute to `AFS-SDK` but without any idea how to getting start.

## Setup Develop Environment

To develop `AFS-SDK`, you have to install some develop dependencies and make sure your `AFS-SDK` is under edit mode:

```shell
pip install -e .['dev']
```

## Run tests

To run tests, use `tox` is recommended, use following command to use `tox`:

```shell
tox
```

When using `tox`, it require `python3.5`, `python3.6`, and `python3.7` runtime environments.

Think it is too complicated? You can use other simple ways to run tests like:

```shell
python setup.py test
# Or
pytest tests/
```

After all tests are done, `AFS-SDK` will generate test reports automatically under `test_reports/`.

## Documentation

`AFS-SDK` provide documents at [Readthedocs](http://afs-docs.readthedocs.io/en/latest/sdk/). If you want to help us to improve the document, you might want to check the result before open a pull request. Use following command to build document at local:

```shell
cd docs/
make html
```

And you can check the result by open `docs/_build/html/index.html`.

## Pull Request

Wants to submit a pull request? Here is a checklist to make sure you are ready for pull request:

- [ ] All changes are commited.
- [ ] Pass all unit tests.
- [ ] All document are updated.

After sending pull request, your PR must review by **one** preson.