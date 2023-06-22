from text_generation import InferenceAPIClient
from huggingface_hub import login


class chat_model():
    def __init__(self, hf_token, mname: str = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"):
        login(token=hf_token, add_to_git_credential=True, write_permission=True)
        self.chat_model = InferenceAPIClient(mname, timeout=90)
        self.context = ""
        self.number = 0

    def query_bot(self, text: str, BOT_SYSTEM_INSTRUCTION: str = '', SYSTEM_REFRESH: str = ''):
        MAX_CONTEXT_LENGTH = 1000
        MAX_TOTAL_LENGTH = 1512
        print("Usuario: " + text)
        # Agregar el promptText al contexto y truncar si es necesario
        prompt_text = '''<|prompter|>{}<|endoftext|>
        <|assistant|>'''.format(f"{SYSTEM_REFRESH} {text}")
        system = '''<|prompter|>{}<|endoftext|>
        <|assistant|>Yes, I got.<|endoftext|>
        '''.format(BOT_SYSTEM_INSTRUCTION)
        context = (
            f"{self.context}{system}{prompt_text}")[-MAX_CONTEXT_LENGTH:]
        # Asegurarse de que la longitud del texto generado no exceda MAX_TOTAL_LENGTH
        max_new_tokens = min(MAX_TOTAL_LENGTH - len(context), 1200)
        print(max_new_tokens)
        try:
            inputs = self.chat_model.generate(
                context, max_new_tokens=max_new_tokens, 
                temperature=0.8, truncate=1000, 
                do_sample=True, 
                repetition_penalty=1.2, 
                top_p=0.9).generated_text
        except Exception as err:
            print(err)
            context = prompt_text  # Resetear el contexto
            inputs = self.chat_model.generate(
                context, max_new_tokens=max_new_tokens, 
                temperature=0.8, truncate=1000, 
                do_sample=True, 
                repetition_penalty=1.2, 
                top_p=0.9).generated_text
        finally:
            self.context = (f"{context} {inputs}")[-MAX_CONTEXT_LENGTH:]
            self.number += 1
            return inputs
