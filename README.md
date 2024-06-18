# How to run Alpaca-Eval

First, we create the generations

```bash
    export SAMBA_URL=<INSERT SAMBA URL>
    export SAMBA_KEY=<INSERT SAMBA KEY>
    export GROQ_API_KEY=<INSERT GROQ KEY>

    python alpaca_generate.py --model groq --out_json groq.json
    python alpaca_generate.py --model samba --out_json samba.json
```


Then, following https://github.com/tatsu-lab/alpaca_eval, we can evaluate the scores

```bash
    alpaca_eval --model_outputs groq.json
    alpaca_eval --model_outputs samba.json
```