from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto


model_name_LLM_hugging = "Qwen/Qwen2.5-7B-Instruct"#Qwen/Qwen2.5-1.5B-Instruct
tokenizer = AutoTokenizer.from_pretrained(model_name_LLM_hugging)
model = AutoModelForCausalLM.from_pretrained(model_name_LLM_hugging).to("cuda")
# model = AutoModelForCausalLM.from_pretrained(
#     "Qwen/Qwen2.5-3B-Instruct",
#     torch_dtype="auto",
#     device_map="auto"
# )
# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")

prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
print(response)