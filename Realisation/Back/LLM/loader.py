from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from gigachat import GigaChat
from config import GIGA_API_KEY

def loadKnownBase(directory_path):
    """загрузка всех файлов из директории
        """
    
    all_docs = []
    
    # txt
    txt_loader = DirectoryLoader(
    directory_path,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},  
    show_progress=True,  
    use_multithreading=True,     
)
    all_docs.extend(txt_loader.load())


    # docx
    word_loader = DirectoryLoader(
    directory_path,
    glob="**/*.docx",
    loader_cls=UnstructuredWordDocumentLoader,
    show_progress=True,  
    use_multithreading=True,
    exclude=["**/~$*.docx"]
)

    all_docs.extend(word_loader.load())    

    # doc
    doc_loader = DirectoryLoader(
        directory_path,
        glob="**/*.doc",
        loader_cls=UnstructuredWordDocumentLoader,
        show_progress=True,
        use_multithreading=True,
        exclude=["**/~$*.doc"]
    )
    all_docs.extend(doc_loader.load())

    # Количество документов
    print(f"Загружено документов: {len(all_docs)}")

      # Разбиение для LLM на чанки 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(all_docs)

    for i, chunk in enumerate(chunks[:5]):
        print(f"\n--- Чанк {i} ---")
        print(chunk.page_content)

    return chunks      



def gen_questions(chunks, n, m, k):
    """генерация вопросов
    """
    
    document_text = "\n\n".join(chunk.page_content for chunk in chunks)

    prompt = f"""
    
    Ты — ассистент по созданию образовательных тестов. 
    Ты получаешь текст документа и генерируешь тестовые вопросы строго по его содержанию. 
    Отвечай ТОЛЬКО валидным JSON без пояснений, комментариев и markdown-блоков.

    На основе следующего текста {document_text} сгенерируй {n} тестовых вопросов.

    Для каждого сгенерированного вопроса дай ровно {m} ответов, из них {k} ответов должны быть правильными ответами.

    Формат ответа — строго JSON:
    
    {{
        "msg_type": "questions_list",
        "questions": [
            {{
                "question_num": 1,
                "question_txt": "текст вопроса",
                "correct_answs": [
                    {{"answ_txt": "текст правильного ответа"}}
                ],
                "not_correct_answs": [
                    {{"answ_txt": "текст неправильного ответа"}}
                ]
            }}
        ]
    }}
           
    """
    
    with GigaChat(
        credentials=GIGA_API_KEY,
        verify_ssl_certs=False
    ) as giga:
        response = giga.chat(prompt)

    return response.choices[0].message.content
