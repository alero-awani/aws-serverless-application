# Build Serverless Production Application

## Reference

### User Service

  ![user-service-diagram](assets/user-service.png)

1. Use the cookiecutter file to initialize the project structure.

    ```sh
    sam init --name "ws-serverless-patterns" --location "https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/76bc5278-3f38-46e8-b306-f0bfda551f5a/module2/sam-python/sam-cookiecutter-2023-11-03.zip"

    cd ws-serverless-patterns

    rm samconfig.toml

    cd ./users
    ```

1. Sam Template Description
    ![sam-template-description](assets/sam-template.png)

1. Build the Project

    ```sh
    cd ~/environment/ws-serverless-patterns/users
    sam build
    ```

    - The sam build command processes your `AWS SAM template file`, `application code`, and any applicable `language-specific files` and `dependencies`. 
    - The command also copies build artifacts in the format and location expected for subsequent steps in your workflow. 
    - You specify dependencies in a manifest file that you include in your application, such as requirements.txt for Python functions, or package.json for Node.js functions.

1. Deploy the Project

    ```sh
    sam deploy --guided --stack-name ws-serverless-patterns-users
    ```
