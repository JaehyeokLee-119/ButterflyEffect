from openai import OpenAI

import re
from utils import normalize_answer
from search import (
    EmbeddingFaiss
)
from prompt import (
    SYSTEM_MESSAGE, 
    INSIGHTS,
    FEWSHOTS
)

client = OpenAI()

def make_message(role, content):
    return {"role": role, "content": content}

def gpt_agent(messages, message, model):
    messages.append(message)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            stop = ["\n", "\n\n"])
        return response.choices[0].message.content.strip().replace(message['content'], "")
    except Exception as e:
        return str(e)

def log_message(messages):
    print(messages[-1]['content'])
    return messages[-1]['content']

class ReactAgent():
    def __init__(self, dataset, df, wiki_index, explorer, model, max_step):
        self.dataset = dataset
        self.df = df
        self.wiki_index = wiki_index
        self.search_engine = EmbeddingFaiss(explorer, wiki_index)
        self.model = model
        self.max_step = max_step
    
    def check_finish(self, search_documents, question, answer):
        check = False
        if answer in ['yes', 'no']:
            check = True
        if answer in question:
            check = True
        for document in search_documents:
            if answer in self.search_engine.get_search(document):
                check = True
            if answer in document:
                check = True
        return check
    
    def eval_hotpotqa(self, index):
        thought_id = 1
        messages = []
        message_logs = []
        search_documents = []
        data = self.dataset.iloc[index]

        # System prompt
        messages.append(make_message("system", SYSTEM_MESSAGE))

        # User Prompt
        fewshots_content = "\n\n".join(FEWSHOTS)
        user_message = f'You must take maximum of {self.max_step} steps\nHere are some examples:\n\n{fewshots_content}\n\n(END OF EXAMPLES)\n\n'
        user_message += f'The following are some experience you gather on a similar task of question answering using Wikipedia. Use these as references to help you perform this task:\n{INSIGHTS}\n\n'
        user_message += f"Now it's your turn!\nQuestion: {data.question}\n"
        messages.append(make_message("user", user_message))

        message_logs.append(f"Question: {data.question}")

        print(f"Question: {data.question}")

        while(thought_id <= self.max_step):
            thought_message = make_message("assistant", f"Thought {thought_id}: ")
            thought_content = gpt_agent(messages, thought_message, self.model)
            messages.append(make_message("assistant", f"Thought {thought_id}: {thought_content}\n"))
            message_logs.append(log_message(messages))
            action_message = make_message("assistant", f"Action {thought_id}: ")
            action_content = gpt_agent(messages, action_message, self.model)
            match_search = re.findall(r"Search\[(.*?)\]", action_content)
            match_finish = re.findall(r"Finish\[(.*?)\]", action_content)
                
            if len(match_search)>0:
                matches = match_search[0]
                if thought_id == self.max_step:
                    messages.append(make_message("user", f"This time you must use Finish[answer] at Action 10.\nIf you cannot find the answer in the document, use generally known knowledge to respond.\n"))
                    message_logs.append(log_message(messages))
                    action_message = make_message("assistant", f"Action {thought_id}: ")
                    action_content = gpt_agent(messages, action_message, self.model)
                    match_finish = re.findall(r"Finish\[(.*?)\]", action_content)
                    if len(match_finish)>0:    
                        predict = match_finish[0]
                    self.df.iloc[index]['search_documents'] = search_documents
                    self.df.iloc[index]['predict'] = predict
                    messages.append(make_message("assistant", f"Action {thought_id}: Finish[{predict}]\n"))
                    message_logs.append(log_message(messages))
                    if normalize_answer(predict) == normalize_answer(data.answer):
                        messages.append(make_message("assistant", f"Observation {thought_id}: Answer is CORRECT\n"))
                        message_logs.append(log_message(messages))
                        return (message_logs, self.df)
                    else:
                        messages.append(make_message("assistant", f"Observation {thought_id}: Answer is INCORRECT, the Answer was {data.answer}\n"))
                        message_logs.append(log_message(messages))
                        return (message_logs, self.df)
                else:
                    messages.append(make_message("assistant", f"Action {thought_id}: Search[{matches}]\n"))
                    message_logs.append(log_message(messages))
                    documents = self.search_engine.get_topk(matches)
                    if matches.lower() == documents[0].lower():
                        search_documents.append(documents[0])
                        messages.append(make_message("assistant", f"Observation {thought_id}: {self.search_engine.get_search(documents[0])}\n"))
                        message_logs.append(log_message(messages))
                    else:
                        similar_documents = [f"[{document}]" for document in documents]
                        similar = ", ".join(similar_documents)
                        messages.append(make_message("assistant", f"Observation {thought_id}: Could not find [{matches}]. Similar: {similar}\n"))
                        message_logs.append(log_message(messages))
                thought_id+=1
            elif len(match_finish)>0:
                if thought_id <= 2:
                    messages.append(make_message("user", f"This time you must use Search[entity].\n"))
                    message_logs.append(log_message(messages))
                    action_message = make_message("assistant", f"Action {thought_id}: ")
                    action_content = gpt_agent(messages, action_message, self.model)
                    match_search = re.findall(r"Search\[(.*?)\]", action_content)
                    if len(match_search)>0:    
                        matches = match_search[0]
                        messages.append(make_message("assistant", f"Action {thought_id}: Search[{matches}]\n"))
                        message_logs.append(log_message(messages))
                        documents = self.search_engine.get_topk(matches)
                        if matches.lower() == documents[0].lower():
                            search_documents.append(documents[0])
                            messages.append(make_message("assistant", f"Observation {thought_id}: {self.search_engine.get_search(documents[0])}\n"))
                            message_logs.append(log_message(messages))
                        else:
                            similar_documents = [f"[{document}]" for document in documents]
                            similar = ", ".join(similar_documents)
                            messages.append(make_message("assistant", f"Observation {thought_id}: Could not find [{matches}]. Similar: {similar}\n"))
                            message_logs.append(log_message(messages))
                    thought_id+=1
                    continue
                predict = match_finish[0]
                check = self.check_finish(search_documents, data.question, predict)
                if thought_id > self.max_step:
                    messages.append(make_message("user", f"This time you must use Finish[answer] at Action 10.\nIf you cannot find the answer in the document, use generally known knowledge to respond.\n"))
                    message_logs.append(log_message(messages))
                    action_message = make_message("assistant", f"Action {thought_id}: ")
                    action_content = gpt_agent(messages, action_message, self.model)
                    match_finish = re.findall(r"Finish\[(.*?)\]", action_content)
                    if len(match_finish)>0:    
                        predict = match_finish[0]
                    check = True
                if check==False:
                    messages.append(make_message("assistant", f"Action {thought_id}: Finish[{predict}]\n"))
                    message_logs.append(log_message(messages))
                    messages.append(make_message("user", "Your answer does not exactly match anything from the observation or question. The answer must be taken exactly from the observation or question without changing a single letter. Pay attention to singular and plural forms. Rewrite the answer."))
                    message_logs.append(log_message(messages))
                    action_message = make_message("assistant", f"Action {thought_id+1}: ")
                    action_content = gpt_agent(messages, action_message, self.model)
                    match_finish = re.findall(r"Finish\[(.*?)\]", action_content)
                    if len(match_finish)>0:    
                        predict = match_finish[0]
                self.df.iloc[index]['search_documents'] = search_documents
                self.df.iloc[index]['predict'] = predict
                messages.append(make_message("assistant", f"Action {thought_id}: Finish[{predict}]\n"))
                message_logs.append(log_message(messages))
                if normalize_answer(predict) == normalize_answer(data.answer):
                    messages.append(make_message("assistant", f"Observation {thought_id}: Answer is CORRECT\n"))
                    message_logs.append(log_message(messages))
                    return (message_logs, self.df)
                else:
                    messages.append(make_message("assistant", f"Observation {thought_id}: Answer is INCORRECT, the Answer was {data.answer}\n"))
                    message_logs.append(log_message(messages))
                    return (message_logs, self.df)
            else:
                messages.append(make_message("assistant", f"Action {thought_id}: {action_content}\n"))
                message_logs.append(log_message(messages))
                messages.append(make_message("user", f"You used the wrong action."))
                message_logs.append(log_message(messages))
                thought_id+=1

        return (message_logs, self.df)



