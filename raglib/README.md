# Raglib

A simple ***library*** for performing **multi-source** RAG for the ***LeetLLaMA*** project.

## Architecture

```bash
.
├── common
│   ├── chunker
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── vanilla_chunker.py
│   ├── embedder
│   │   ├── base.py
│   │   ├── bge_embedder.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── vstore_connector
│       ├── base.py
│       ├── __init__.py
│       └── milvus_connector.py
├── doc_rag
│   ├── crawler.py
│   └── __init__.py
├── __init__.py
└── leet_rag
    ├── df_processor.py
    └── __init__.py
```

### ~/common

Houses the **common** functionality to ***both*** RAGs, which are:

- Chunking
- Embedding
- Vectore Store Connector

### ~/doc_rag

Has the ***web crawler*** head for the processing of the ***Python documentation***, but can be extended for any other official documentation

### ~/leet_rag

Has the ***df processor*** head for the ***.jsonl*** dataset with problem-solution pairs in *Python* 

---

@ By [TheComputerScientist](https://www.linkedin.com/in/andrew-darnall-a978171ab/)

---