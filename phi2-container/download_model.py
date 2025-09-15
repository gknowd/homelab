from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/phi-2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained("/app/model")
tokenizer.save_pretrained("/app/model")
