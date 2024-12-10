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
            "If prompt is not in English, translate it to English. "
            "You are part of a project which is creating a search engine for Tartu University researchers using embedding vectors. "
            "You should analyze user input and extract from it the specific data for searching and give it to us. "
            "If needed, you should translate input to English. "
            "Also you can ignore institute/University/type of research and delete them from the output. "
            "Output must only contain the filtered data."
        )

        return self.request(system_prompt, input_text)

    def create_output(self, user_input, unprocessed_output):
        """
        Create output for the user input.
        """
        system_prompt = (
            "You are part of a project which is creating a search engine for Tartu University researchers using embedding vectors. "
            "You should analyze user_input and unprocessed_output and answer for the user_input, using the unprocessed_output."
            "Answer should be in same language as user_input, language of unprocessed_output doesnt matter. "
            "Do not translate titles. If needed fix names of the authors."
            "Do not add any additional information. Add that you can help to find more researchers if needed. - in your words"
            "Add also text formatting to the output."
        )
        return self.request(system_prompt, f"user_input:{user_input} unprocessed_output:{unprocessed_output}")

    def request(self, system_prompt, user_input):
        chat_completion = self.client.chat.completions.create(
            model="IDS2024_MATETSKI_gpt_4o_mini",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return chat_completion.choices[0].message.content
