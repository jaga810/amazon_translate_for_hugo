import fire
import boto3
import os

remained_lines_idx = [0,2,3,4,5]

class Translator():
  def __init__(self, profile, region='us-east-1'):
    boto3.setup_default_session(profile_name=profile)
    self.translator = boto3.client(service_name='translate', region_name=region, use_ssl=True)

  def translate(self, base_dir):
    print('translate')
    print(base_dir)
    source_path = os.path.join(base_dir, 'index.ja.md')
    output_path = os.path.join(base_dir, 'index.en.md')

    with open(source_path, "r") as source:
      txt = source.read()
      lines = txt.split('\n')

      result = self.translator.translate_text(
        Text=txt,
        SourceLanguageCode="ja", 
        TargetLanguageCode="en"
      )

      print(result['TranslatedText'])

      result_lines = result['TranslatedText'].split('\n')
      for idx in remained_lines_idx:
        result_lines[idx] = lines[idx]

      with open(output_path,'w') as output:
        output.write('\n'.join(result_lines))

  def search_dir(self, base_dir):
    for entry_name in os.listdir(path=base_dir):
      if entry_name == 'index.ja.md':
        self.translate(base_dir)
      if os.path.isdir(os.path.join(base_dir, entry_name)):
        self.search_dir(os.path.join(base_dir, entry_name))

if __name__ == '__main__':
  fire.Fire(Translator)