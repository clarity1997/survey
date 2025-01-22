
import openai

class AzureOpenAIChat:
    def __init__(self, api_key, azure_endpoint):
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint

    def create_chat_completion(self, model, input_message_list):
        """
        Creates a chat completion using Azure OpenAI.

        Args:
            model (str): The model name or deployment name.
            input_message_list (list): List of messages for chat completion.

        Returns:
            dict: Response from the chat completion API. 
        """
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2023-12-01-preview",
            azure_endpoint=self.azure_endpoint
        )

        response = client.chat.completions.create(
            model=model,
            messages=input_message_list
        )

        return response
    


def call_ai(data_list):
    api_key = '2d62018330f247b49c1db9482646a0f4'
    azure_endpoint = 'https://oai-hkpctdu-prd-eastus-project-1.openai.azure.com/'

    chat_client = AzureOpenAIChat(api_key, azure_endpoint)

    # user cut in
    input_messages = data_list

    model_name = "ryan_gpt_4o"
    response = chat_client.create_chat_completion(model_name, input_messages)
    print(response.choices[0].message.content)

    return response









def call_magic_function_1(input_string):
    # Get the request data
    input_list = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": input_string},

    ]
    user_input_api_key = '2d62018330f247b49c1db9482646a0f4'
    azure_endpoint = 'https://oai-hkpctdu-prd-eastus-project-1.openai.azure.com/'
    chat_client = AzureOpenAIChat(api_key=user_input_api_key, azure_endpoint=azure_endpoint)

    model_name = "ryan_gpt_4o"
    response = chat_client.create_chat_completion(model_name, input_list)
    string_result = response.choices[0].message.content

    return string_result
# print(call_magic_function_1("how are you today?"))


# 
    # input_list = [
    # {"role": "system", "content": "You are a helpful assistant help me to write code"},
    # {"role": "user", "content": input_string},

    # ]
def call_magic_function_2(input_list_of_string):
    # Get the request data
    input_list = input_list_of_string

    user_input_api_key = '2d62018330f247b49c1db9482646a0f4'
    azure_endpoint = 'https://oai-hkpctdu-prd-eastus-project-1.openai.azure.com/'
    chat_client = AzureOpenAIChat(api_key=user_input_api_key, azure_endpoint=azure_endpoint)

    model_name = "ryan_gpt_4o"
    response = chat_client.create_chat_completion(model_name, input_list)
    string_result = response.choices[0].message.content

    return string_result