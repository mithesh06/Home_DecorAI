from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.schema.output_parser import StrOutputParser

class LLM_Interface:
    def __init__(self) -> None:
        self.configure()
        self.llm = ChatOpenAI()
        
        # inputs: obj_res (results from the object detection), height, width
        self.description_prompt = ChatPromptTemplate.from_template("\n{obj_res}The above text are x1, y1, x2, y2 coordinates of every object in an image of Image dimensions: {width}x{height}\nGenerate a description of the room as a paragraph, for an image caption. Use relative positions of objects to each other and the room. use terms like to the left of, to the right of the room, above, below, etc.., and do not mention coordinates of the objects")
        self.description_chain = LLMChain(
                llm=self.llm,
                prompt=self.description_prompt,
                verbose=True,    
                output_parser = StrOutputParser()
            )
        # inputs: style,
        self.suggestion_prompt = ChatPromptTemplate.from_template("{description}\nYou are an interior decorator. give an instructional paragraph to make the room fit the style \" {style}\".  make changes that aren't too drastic. The structure of the actual room must be the same, the home decor items must be changed, or shifted in positions. give a paragraph of 100 words.  begin and use terms like '1. change xys..., ' ")
        self.suggestion_chain = LLMChain(
                llm=self.llm,
                prompt=self.suggestion_prompt,
                verbose=True,
                output_parser = StrOutputParser()
            )   
        
    def configure(self):
        load_dotenv()
    
    def suggest(self,OBJ_RES,height,width,STYLE): 
        description = self.description_chain.predict(obj_res = OBJ_RES, height = height, width = width)
        suggestion = self.suggestion_chain.predict(description = description, style =STYLE)
        print(suggestion)
        return suggestion
