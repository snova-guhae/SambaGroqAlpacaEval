import numpy as np 
import random
import Groq
import requests
import argparse
random.seed(0)
np.random.seed(0)

def run_model(args):
    eval_set = datasets.load_dataset("tatsu-lab/alpaca_eval", "alpaca_eval")["eval"]
    model = args.model
    outputs = []

        for example in tqdm(eval_set):
            instruction = example['instruction']
            instance = {}
            instance['instruction'] = instruction
            instance['generator'] = model
            instance['dataset'] = example['dataset']
            instance['datasplit'] = "eval"
            messages = ['role': 'user', "content": 'instruction']
            if model == "groq":
                client = Groq(
                    api_key=os.environ['GROQ_API_KEY'],
                )
                while True:
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model="llama3-8b-8192",
                            temperature=0
                        )
                        response_text = chat_completion.choices[0].message.content
                    except:
                        time.sleep(5)
                        continue
                    break
            elif model == "samba":
                payload = {
                    "inputs": messages,
                    "params": {
                        "max_tokens_allowed_in_completion": {"type": "int", "value": 500},
                        "min_token_capacity_for_completion": {"type": "int", "value": 2},
                        "skip_special_token": {"type": "bool", "value": True},
                        "stop_sequences": {"type": "list", "value": ["[INST]", "[INST]", "[/INST]", "[/INST]"]}
                    },
                    "expert": "llama3-8b"
                }
                url = os.environ.get("SAMBA_URL")
                key = os.environ.get("SAMBA_KEY")

                headers = {
                    "Authorization": f"Basic {key}",
                    "Content-Type": "application/json"
                }
                post_response = requests.post(url, json=payload, headers=headers, stream=True)

                response_text = ""
                for line in post_response.iter_lines():
                    if line.startswith(b"data: "):
                        data_str = line.decode('utf-8')[6:]
                        try:
                            line_json = json.loads(data_str)
                            content = line_json.get("stream_token", "")
                            if content:
                                response_text += content
                        except json.JSONDecodeError as e:
                            pass
        
            instance['output'] = response_text
            outputs.append(instance)

            with open(args.out_json, 'w') as f:
                json.dump(outputs, f, indent = 4)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", default = None)
    parser.add_argument("--out_json", default = None)
    
    args = parser.parse_args()
    run_model(args)
    
if __name__ == "__main__":
    main()