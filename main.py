import fire
import boto3
import os

remained_lines_idxs = [0,2,3,4,5]

class Translator():
  def __init__(self, profile, region='us-east-1'):
    boto3.setup_default_session(profile_name=profile)
    self.translator = boto3.client(service_name='translate', region_name=region, use_ssl=True)

  def translate(self, base_dir):
    print('translate')
    print(base_dir)
    source_path = os.path.join(base_dir, '_index.ja.md')
    output_path = os.path.join(base_dir, '_index.en.md')

    output_lines = []

    with open(source_path, "r") as source:
      lines = source.readlines()
      idx = 0
      isCode = False
      for line in lines:
        print(line)
        if idx in remained_lines_idxs or line == '' or '{{< figure' in line or '![](' in line or '{{%' in line:
          output_lines.append(line.replace('\n',''))
        elif '```' in line or isCode:
          output_lines.append(line.replace('\n', ''))
          if '```' in line and isCode:
            isCode = False
          else:
            isCode = True
        else:
          result = self.translator.translate_text(
            Text=line,
            SourceLanguageCode="ja", 
            TargetLanguageCode="en"
          )
          output_lines.append(result['TranslatedText'])

        idx += 1

    print('\n'.join(output_lines))

    with open(output_path,'w') as output:
      output.write('\n'.join(output_lines))

  def search_dir(self, base_dir):
    for entry_name in os.listdir(path=base_dir):
      if entry_name == '_index.ja.md':
        self.translate(base_dir)
      if os.path.isdir(os.path.join(base_dir, entry_name)):
        self.search_dir(os.path.join(base_dir, entry_name))

if __name__ == '__main__':
  fire.Fire(Translator)