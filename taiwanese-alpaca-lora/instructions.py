import pandas as pd
import json

def gen_train_instructions(read_fname, write_fname):
    df = pd.read_excel(read_fname,header=None, engine="openpyxl")
    data = df.iloc[:,1:8].values
    instruction,input,output=[],[],[]
    for i in range(1,len(data)):
        instruction.append("Answer the given multiple choice question.")
        input.append(data[i][0]+"\n" + str(data[i][1])+"\n1. "+ str(data[i][2])+"\n2. "+str(data[i][3])+"\n3. "+str(data[i][4])+"\n4. "+str(data[i][5]))
        output.append(str(data[i][6]))
    new_data = []
    for i in range(len(instruction)):
         item = { 'instruction': instruction[i], 'input': input[i], 'output': output[i] }
         new_data.append(item)
    with open(write_fname, 'w') as f:
        json.dump(new_data, f, indent=4,ensure_ascii=False)

def gen_test_instructions(read_fname, write_fname):
    df = pd.read_excel(read_fname, header=None)
    data = df.iloc[:, 0:7].values
    id, instruction, input = [], [], []
    for i in range(1, len(data)):
        id.append(data[i][0])
        instruction.append("Answer the given multiple choice question.")
        input.append(data[i][1] + "\n\n問題:" + str(data[i][2]) + "\n1. " + str(
            data[i][3]) + "\n2. " + str(data[i][4]) + "\n3. " + str(data[i][5]) + "\n4. " + str(data[i][6]))
    new_data = []
    for i in range(len(instruction)):
        item = {'id': id[i], 'instruction': instruction[i], 'input': input[i]}
        new_data.append(item)
    with open(write_fname, 'w') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # gen_train_instructions("raw_data/AI.xlsx","data/data_AI.json")
    gen_test_instructions("raw_data/AI1000.xlsx", "data/answer.json")

