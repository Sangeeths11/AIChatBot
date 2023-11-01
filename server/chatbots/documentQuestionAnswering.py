
import os
import openai


import api.appconfig as config

os.environ["OPENAI_API_KEY"] =  config.OPENAI_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    pass


if __name__ == "__main__":
    main()