**Customer Support RAG System**

**Objective**

The objective of this project is to build a Customer Support solution that can:

- Answer user questions based on internal company documents using Retrieval-Augmented Generation (RAG)
- Avoid hallucinations by suggesting support ticket creation when answers are not found
- Automatically create support tickets in an issue tracking system using function calling
- Be deployed as a web application on Hugging Face Spaces

**2\. Business Features Implementation**

**2.1 Web Chat Interface**

The system provides a web-based chat interface built with **Streamlit**, where users can:

- Ask questions related to company documents
- Receive answers with document citations
- Create support tickets if an answer is not available
<img width="895" height="423" alt="image" src="https://github.com/user-attachments/assets/cf888401-5e3d-4427-844b-690739d7c0ce" />


**2.2 Answering Questions from Datasources**

The system uses **Retrieval-Augmented Generation (RAG)**:

- User questions are embedded and compared against document embeddings
- Relevant document chunks are retrieved from a vector database
- The AI model generates an answer based only on retrieved content
**2.3 No-Answer Handling & Ticket Suggestion**

If the system cannot find a confident answer:

- It **does not hallucinate**
- It suggests creating a support ticket
- This behavior is controlled by a similarity threshold
**2.4 Support Ticket Creation (Function Calling)**

Users can instruct the system to create a support ticket.

Each ticket contains:

- **User name**
- **User email**
- **Summary (title)**
- **Detailed description**

Tickets are automatically created as **GitHub Issues** using function calling.

**2.5 Issue Tracking System**

- GitHub Issues is used as the issue tracking system
- Tickets are created programmatically using GitHub API
- Each ticket represents a real support request

**2.6 Document Citation**

When an answer is generated from documents, the system provides:

- **Document file name**
- **Page number**

Example:

Source: Toyota-Corolla_2008_EN_\_manual.pdf, page 312

**2.7 Conversation History**

The system maintains conversation history:

- Previous messages are included in the context window
- Follow-up questions are answered correctly based on prior interaction

**2.8 Company Awareness**

The AI system is aware of company information:

- Company Name: **NeoSupport Inc**
- Support Email: **<support@neosupport.example>**
- Phone Number: **+998 71 000 00 00**

This information is displayed in the UI and used in responses.

**3\. Data Sources**

The system uses **three documents** as data sources:

| **Document Name** | **Type** | **Description** |
| --- | --- | --- |
| Toyota-Corolla_2008_EN_\_manual.pdf | PDF | Vehicle manual (400+ pages) |
| Company-Policy-and-Procedure.pdf | PDF | Internal company policy |
| FAQ Document | Text | Support FAQ |

**Data Requirements Compliance**

- At least 3 documents
- At least 2 PDF documents
- At least 1 PDF with more than 400 pages

**4\. Technical Architecture**

**4.1 Programming Language**

- **Python 3.11**
**4.2 Vector Storage**

- **FAISS** is used as the vector database
- Documents are embedded and stored locally
- Vector index files:
  - index.faiss
  - docstore.pkl
**4.3 Function Calling**

Function calling is implemented to:

- Create GitHub Issues as support tickets
- Pass structured parameters (name, email, summary, description)

**4.4 Application Structure**

app.py # Streamlit UI

rag/ # RAG logic (loaders, prompts, tools)

ingest.py # Document ingestion and indexing

requirements.txt # Dependencies

Dockerfile # Deployment configuration

**5\. User Interface**

- Built using **Streamlit**
- Includes:
  - Chat window
  - Ticket information sidebar
  - RAG configuration controls
  - Index status indicator

**6\. Deployment**

**Hosting Platform**

- **Hugging Face Spaces**

**Deployment Method**

- Docker-based deployment
- Publicly accessible URL

Example:

<https://kuchkarovaziz77-rag-support-capstone.hf.space>

**7\. Demonstration Scenarios**

**Example Questions**

- "What engine oil viscosity is recommended for Toyota Corolla 2008?"
- "What precautions should be taken when repairing the SRS airbag?"
- "What are employee responsibilities according to company policy?"
- User asks an out-of-scope question
- System suggests ticket creation
- User confirms → GitHub Issue is created
**8\. Conclusion**

This project successfully demonstrates:

- A production-ready RAG-based customer support system
- Safe AI behavior with hallucination avoidance
- Real-world ticket escalation using function calling
- Deployment on Hugging Face Spaces

All business and technical requirements of the practical task have been fully implemented.

**9\. Links**

- **Hugging Face Space:**  
    <https://kuchkarovaziz77-rag-support-capstone.hf.space>
- **GitHub Repository:** **<https://github.com/azizkuchkarov/cap.stone-pr-1-adv.gen.ai>**
