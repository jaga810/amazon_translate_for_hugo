# Amazon Translate for Hugo
This tool allows you to translate Hugo markdown templates from Japanese to English with Amazon Translate.
Specify root directory of md files then tools scan children dir recursively and translate each md files into English.

## Usage
1. clone this repo to your project
2. `pip install -r requirements.txt`
3. `python main.py --profile ${your_aws_profile_name} search_dir ${path to root of md files}`