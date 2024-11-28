from openai import AzureOpenAI


class AILib:
    def __init__(self, api_key, api_version, azure_endpoint):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

    def extract(self, input_text):
        """
        Extract searching data from user input.
        If needed - translate the text to English.
        """
        system_prompt = (
            "You are part of a project which is creating a search engine for Tartu University researchers using embedding vectors. "
            "You should analyze user input and extract from it the specific data for searching and give it to us. "
            "If needed, you should translate input to English. "
            "Also you can ignore institute/University/type of research and delete them from the output. "
            "Output must only contain the filtered data."
        )

        chat_completion = self.client.chat.completions.create(
            model="IDS2024_MATETSKI_gpt_4o_mini",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ]
        )
        return chat_completion.choices[0].message.content
