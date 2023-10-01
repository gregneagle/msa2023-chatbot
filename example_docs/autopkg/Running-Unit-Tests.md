Unit testing helps us ensure that newly added features and major changes to the AutoPkg codebase do not introduce errors or unwanted behavior.

If you're contributing relatively minor changes to AutoPkg, you probably do not need to run unit tests. The steps below are for major contributions and/or future use in continuous integration pipelines.

## Setup

1. Install AutoPkg's (with embedded Python 3) and `git` if you haven't already.

2. Clone the AutoPkg repo to your local computer.

    ```
    git clone https://github.com/autopkg/autopkg.git
    ```

## Testing

1. Change to the __Scripts__ subdirectory within the repo.

    ```
    cd autopkg/Scripts
    ```

2. Run the test script.

    ```
    /usr/local/autopkg/python run_tests.py
    ```

    You should see output that displays the result of each test:

    ```
    test_get_identifier_from_recipe_file_returns_identifier (tests.test_autopkglib.TestAutoPkg)
    get_identifier_from_recipe-file should return identifier. ... ok
    test_get_identifier_from_recipe_file_returns_none (tests.test_autopkglib.TestAutoPkg)
    get_identifier_from_recipe-file should return None if no identifier. ... ok
    ...etc...
    ```

