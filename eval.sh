export SAMBA_URL=<INSERT SAMBA URL>
export SAMBA_KEY=<INSERT SAMBA KEY>
export GROQ_API_KEY=<INSERT GROQ KEY>

python alpaca_generate.py --model groq --out_json groq.json
python alpaca_generate.py --model samba --out_json samba.json