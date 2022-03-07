from lambda_function import lambda_handler

if __name__ == "__main__":
    lambda_handler(
        event={
            'testSuffix': '-local-test'
        },
        context=None
    )
