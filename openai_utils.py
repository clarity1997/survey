from openai import AzureOpenAI
# Azure OpenAI setup
def gpt_4o_openai_functon(input_messages_list):
    key1 = '2d62018330f247b49c1db9482646a0f4'
    key2 = '5d44e0f490eb4acc937aec6baa729781'

    MY_AZURE_OPENAI_ENDPOINT = 'https://oai-hkpctdu-prd-eastus-project-1.openai.azure.com/'

    client = AzureOpenAI(
        api_key=key1,  # or use key2
        api_version="2023-12-01-preview",
        azure_endpoint=MY_AZURE_OPENAI_ENDPOINT
    )

    response = client.chat.completions.create(
        model="ryan_gpt_4o",  # model = "deployment_name".
        messages=input_messages_list
    )

    return response.choices[0].message.content


def text_mode_message_list_example(a, b):
    return [
        {"role": "system", "content": f"{a}"},
        {"role": "user", "content": f"{b}"}
    ]

def read_markdown_file(file_path):
    """
    Reads the content of a markdown file.

    Parameters:
    file_path (str): The path to the markdown file.

    Returns:
    str: The content of the markdown file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except Exception as e:
        return f"Error: An error occurred while reading the file. Details: {str(e)}"

def save_to_markdown(message, md_path):
    """
    Saves the given message to a markdown file.

    Parameters:
    message (str): The markdown formatted message to be saved.
    md_path (str): The path where the markdown file will be saved.

    Returns:
    None
    """
    try:
        with open(md_path, 'w', encoding='utf-8') as file:
            file.write(message)
        print(f"Message successfully saved to {md_path}")
    except Exception as e:
        print(f"Error: An error occurred while writing to the file. Details: {str(e)}")
