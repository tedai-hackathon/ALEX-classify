# Contributing 

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

## 🤝 How to submit a contribution

To make a contribution, follow the following steps:

1. Clone this repository
2. Create a new branch (feat, fix, test)
3. Do the changes on your branch
4. If you modified the code (new feature or bug-fix), please add tests for it
5. Check the linting [see below](https://github.com/gventuri/pandas-ai/blob/main/CONTRIBUTING.md#-linting)
6. Ensure that all tests pass [see below](https://github.com/gventuri/pandas-ai/blob/main/CONTRIBUTING.md#-testing)
7. Submit a pull request

For more details about pull requests, please read [GitHub's guides](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).


### 📦 Package manager

We use `poetry` as our package manager. You can install poetry by following the instructions [here](https://python-poetry.org/docs/#installation).

Please DO NOT use pip or conda to install the dependencies. Instead, use poetry:

```bash
poetry install --all-extras
```

### 📌 Pre-commit

To ensure our standards, make sure to install pre-commit before starting to contribute.

```bash
pre-commit install
```

### 🧹 Linting

We use `ruff` to lint our code. You can run the linter by running the following command:

```bash
ruff pandasai examples
```

Make sure that the linter does not report any errors or warnings before submitting a pull request.

### Code Format with `black`

We use `black` to reformat the code by running the following command:

```bash
black pandasai 
```

### 🧪 Testing

We use `pytest` to test our code. You can run the tests by running the following command:

```bash
poetry run pytest
```

Make sure that all tests pass before submitting a pull request.
