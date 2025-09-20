from datasets import load_dataset
from datasets import DatasetDict
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model
from trl import SFTConfig, SFTTrainer


model_name = 'TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T'
template_tokenizer = AutoTokenizer.from_pretrained('TinyLlama/TinyLlama-1.1B-Chat-v1.0')

def format_prompt(example):
    chat =  example['messages']
    prompt = template_tokenizer.apply_chat_template(chat, tokenize=False)
    return {
        'text': prompt
    }

dataset = load_dataset('HuggingFaceH4/ultrachat_200k', trust_remote_code=True)
dataset_train = dataset['train_sft']
dataset_test = dataset['test_sft']
dataset = DatasetDict({
    'train': dataset_train.shuffle(seed=42).take(100_000),
    'test': dataset_test
})
dataset = dataset.map(format_prompt, remove_columns=dataset['train'].column_names)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    llm_int8_enable_fp32_cpu_offload=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = '<PAD>'
tokenizer.padding_size = 'left'
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map='auto',
    quantization_config=bnb_config
)
model.config.use_cache=False
model.config.pretraining_tp=1
peft_config = LoraConfig(
    lora_alpha=32,
    lora_dropout=0.1,
    r=64,
    bias='none',
    task_type='CAUSAL_LM',
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj']
)
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)

output_dir = 'train_dir'

config = SFTConfig(
    output_dir=output_dir,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=1,
    gradient_accumulation_steps=4,
    optim="paged_adamw_8bit",
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    logging_steps=100,
    eval_steps=100,
    do_eval=True,
    fp16=True,
    gradient_checkpointing=True,
    packing=True,
    max_length=512,
    dataset_text_field="text",
    completion_only_loss=False,
)

trainer = SFTTrainer(
    model=model,
    args=config,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test'],
    peft_config=peft_config,
    processing_class=tokenizer
)
trainer.train()
trainer.model.save_pretrained("TinyLlama-1.1B-Chat-v1.1")