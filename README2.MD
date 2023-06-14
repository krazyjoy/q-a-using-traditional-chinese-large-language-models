[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/u6vAXDAo)
## Installation
1. conda create --name llama python=3.9
2. conda activate llama
3. git clone https://github.com/tloen/alpaca-lora
4. cd alpaca-lora
5. pip install -r requirements.txt
6. conda install cudatoolkit

關於installation的部分，當時我一直無法安裝正確的(11.8版本)cudatoolkit，
加上網路上又沒有此解。後來才知道我用的是2020年的anaconda所以他沒有這麼新的cudatoolkit，到官網下載2023年的才有。

## Edit `finetune.py`
1.  我前幾次訓練都會跑出亂碼，且只有2%的正確率，debug之後才發現如果
    沒有註解掉:
    ```
        # old_state_dict = model.state_dict
        # model.state_dict = (
        #     lambda self, *_, **__: get_peft_model_state_dict(
        #         self, old_state_dict()
        #     )
        # ).__get__(model, type(model))
    ```
    模型不會更新，自然也就不會儲存weight和bias，表現自然相當於只有用老師的模型去回答問題。
2. 假如使用雙卡，需在 `adapters_weights = torch.load(checkpoint_name)`
小括號內加逗號補`map_location="cuda:0"`。假如指定兩張卡`map_location={}"cuda:0, cuda:1}"`

3. `--fp16 False`

4. `resume_from_checkpoint`我都是使用整個大資料夾，包含`adapter_model.bin, adapter_config.json`這樣即便是放不同資料或設定參數不同，也不易出錯


執行時加上WORLD_SIZE=2 ...那段
```
WORLD_SIZE=2 CUDA_VISIBLE_DEVICES=0,1 torchrun --nproc_per_node=2 --master_port=1234 finetune.py \
python finetune.py --base_model 'decapoda-research/llama-7b-hf' --data_path 'taiwanese-alpaca-lora/data/merge.json' --output_dir 'taiwanese-alpaca-lora/pretrain5' --batch_size 200 --micro_batch_size 2 --num_epochs 3 --val_set_size 100 --learning_rate 3e-4 --cutoff_len 1600 --lora_r 8 --lora_alpha 16 --lora_dropout 0.05 --lora_target_modules '[q_proj,v_proj,k_proj,o_proj]' --add_eos_token --train_on_inputs --group_by_length --resume_from_checkpoint taiwanese-alpaca-lora/teacher-pretrain
```

## Data Preparation
- run `instruction.py`
    - 將raw_data/AI.xlsx轉換成data_AI.json
    - instruction: "Answer the given multiple choice question.",
    - input: 短文\n問題\n選項1\n選項2\n選項3\n選項4
    - output: 正確答案


- combine `data_AI.json` 和NTU的 `alpaca-tw_en-align.json`
    `alpaca-tw_en-align.json`: https://github.com/ntunlplab/traditional-chinese-alpaca/blob/main/data/alpaca-tw_en-align.json 
    產生 `merge.json`下去訓練

- `answer.json`同樣是由AI1000.xlsx經`instructions.py`生成。

## RUN COMMAND

```
conda activate llama
cd alpaca-lora
```
1. use teacher's pretrain model + merged data
```
python finetune.py --base_model 'decapoda-research/llama-7b-hf' --data_path 'taiwanese-alpaca-lora/data/merge.json' --output_dir 'taiwanese-alpaca-lora/pretrain5' --batch_size 200 --micro_batch_size 2 --num_epochs 3 --val_set_size 100 --learning_rate 3e-4 --cutoff_len 1600 --lora_r 8 --lora_alpha 16 --lora_dropout 0.05 --lora_target_modules '[q_proj,v_proj,k_proj,o_proj]' --add_eos_token --train_on_inputs --group_by_length --resume_from_checkpoint taiwanese-alpaca-lora/teacher-pretrain
```
- 1 epoch: 20% accuracy
- 2 epoch: 26% accuracy
- 3 epoch: 27% accuracy

2. use 1.'s pretrain model + merged data
```
python finetune.py --base_model 'decapoda-research/llama-7b-hf' --data_path 'taiwanese-alpaca-lora/data/merge.json' --output_dir 'taiwanese-alpaca-lora/pretrain6' --batch_size 200 --micro_batch_size 2 --num_epochs 3 --val_set_size 100 --learning_rate 3e-4 --cutoff_len 1600 --lora_r 8 --lora_alpha 16 --lora_dropout 0.05 --lora_target_modules '[q_proj,v_proj,k_proj,o_proj]' --add_eos_token --train_on_inputs --group_by_length --resume_from_checkpoint taiwanese-alpaca-lora/pretrain5
```

train-loss:0.83
## 訓練經驗
1. data_AI.json v.s. merge.json
- 效果來說，data_AI.json 雖然他的訓練時長
較短，但表現非常不好，試過一次(1 epoch, loss: 1.7) 之後就沒再嘗試。
|  n_epochs    | train_loss  | accuracy |
|--------------|------------ | ---------|
|  2           |   1.83      |      |

2. teacher pretrain 3 epochs
|  n_epochs    | train_loss  | accuracy |
|--------------|------------ | ---------|
|  1           |   1.01      |   0.20   |
|  2           |   0.94      |   0.26   |
|  3           |   0.87      |   0.276  |

3. teacher_pretrain 3 epochs + pretrain5 3 epochs:
|train_loss  | accuracy |
|----------- | ---------|
|   0.83     |    0.19  |

## Generate
```
 python generate-teacher.py --load_8bit --base_model 'decapoda-research/llama-7b-hf' --lora_weights 'taiwanese-alpaca-lora/pretrain4/'
```

- 
# upload
```
git init
git add ./folder_name
git commit -m "message1"
git branch -M main
git remote add origin https://github.com/MachineLearningNTUT/q-a-using-traditional-chinese-large-language-models-0812509.git
git push -u origin main
```

-------continue uploading--------------
```
git add ./folder_name2
git commit -m "message2"
git push -u origin main
```