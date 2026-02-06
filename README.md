Customer Support RAG System
Objective
The objective of this project is to build a Customer Support solution that can:
•	Answer user questions based on internal company documents using Retrieval-Augmented Generation (RAG)
•	Avoid hallucinations by suggesting support ticket creation when answers are not found
•	Automatically create support tickets in an issue tracking system using function calling
•	Be deployed as a web application on Hugging Face Spaces
________________________________________
2. Business Features Implementation
2.1 Web Chat Interface
The system provides a web-based chat interface built with Streamlit, where users can:
•	Ask questions related to company documents
•	Receive answers with document citations
•	Create support tickets if an answer is not available
<img width="895" height="423" alt="image" src="https://github.com/user-attachments/assets/25d5e927-7931-4dad-af14-fd00641fccfd" />

2.2 Answering Questions from Datasources
The system uses Retrieval-Augmented Generation (RAG):
•	User questions are embedded and compared against document embeddings
•	Relevant document chunks are retrieved from a vector database
•	The AI model generates an answer based only on retrieved content
<img width="873" height="413" alt="image" src="https://github.com/user-attachments/assets/8a137c4e-1f77-4a72-be03-a08a4ba61e5a" />

2.3 No-Answer Handling & Ticket Suggestion
If the system cannot find a confident answer:
•	It does not hallucinate
•	It suggests creating a support ticket
•	This behavior is controlled by a similarity threshold
<img width="974" height="454" alt="image" src="https://github.com/user-attachments/assets/e3aaba2b-ae96-4109-ba3e-47b1b55cff36" />

2.4 Support Ticket Creation (Function Calling)
Users can instruct the system to create a support ticket.
Each ticket contains:
•	User name
•	User email
•	Summary (title)
•	Detailed description
Tickets are automatically created as GitHub Issues using function calling.
<img width="974" height="520" alt="image" src="https://github.com/user-attachments/assets/b1150eef-fe52-405f-8103-169c11ad12b0" />

2.5 Issue Tracking System
•	GitHub Issues is used as the issue tracking system
•	Tickets are created programmatically using GitHub API
•	Each ticket represents a real support request
________________________________________
2.6 Document Citation
When an answer is generated from documents, the system provides:
•	Document file name
•	Page number
Example:
Source: Toyota-Corolla_2008_EN__manual.pdf, page 312
<img width="974" height="390" alt="image" src="https://github.com/user-attachments/assets/d747b3f6-3a43-4fd9-b4aa-b6b9512bd752" />

2.7 Conversation History
The system maintains conversation history:
•	Previous messages are included in the context window
•	Follow-up questions are answered correctly based on prior interaction
________________________________________
2.8 Company Awareness
The AI system is aware of company information:
•	Company Name: NeoSupport Inc
•	Support Email: support@neosupport.example
•	Phone Number: +998 71 000 00 00
This information is displayed in the UI and used in responses.

<img width="974" height="146" alt="image" src="https://github.com/user-attachments/assets/b544126b-3439-457a-b698-bed507a31fa9" />

3. Data Sources
The system uses three documents as data sources:
Document Name	Type	Description
Toyota-Corolla_2008_EN__manual.pdf	PDF	Vehicle manual (400+ pages)
Company-Policy-and-Procedure.pdf	PDF	Internal company policy
FAQ Document	Text	Support FAQ
Data Requirements Compliance
•	At least 3 documents
•	At least 2 PDF documents
•	At least 1 PDF with more than 400 pages

<img width="913" height="267" alt="image" src="https://github.com/user-attachments/assets/3859b743-f767-4284-bac9-86c3cf89d8e7" />

4. Technical Architecture
4.1 Programming Language
•	Python 3.11

<img width="767" height="401" alt="image" src="https://github.com/user-attachments/assets/ff2f7de4-da93-4c34-8417-e8f8c33a246a" />
4.2 Vector Storage
•	FAISS is used as the vector database
•	Documents are embedded and stored locally
•	Vector index files:
o	index.faiss
o	docstore.pkl

<img width="974" height="416" alt="image" src="https://github.com/user-attachments/assets/4d8dd2c7-c41b-46c5-9956-7b4e9eeaf5a9" />
4.3 Function Calling
Function calling is implemented to:
•	Create GitHub Issues as support tickets
•	Pass structured parameters (name, email, summary, description)
________________________________________
4.4 Application Structure
app.py                	# Streamlit UI
rag/                 	 	# RAG logic (loaders, prompts, tools)
ingest.py             	# Document ingestion and indexing
requirements.txt      	# Dependencies
Dockerfile            	# Deployment configuration
________________________________________
5. User Interface
•	Built using Streamlit
•	Includes:
o	Chat window
o	Ticket information sidebar
o	RAG configuration controls
o	Index status indicator
________________________________________
6. Deployment
Hosting Platform
•	Hugging Face Spaces
Deployment Method
•	Docker-based deployment
•	Publicly accessible URL
Example:
https://kuchkarovaziz77-rag-support-capstone.hf.space


<img width="974" height="265" alt="image" src="https://github.com/user-attachments/assets/483c261b-af27-4a49-94e5-9dea998993d1" />

7. Demonstration Scenarios
Example Questions
•	“What engine oil viscosity is recommended for Toyota Corolla 2008?”
•	“What precautions should be taken when repairing the SRS airbag?”
•	“What are employee responsibilities according to company policy?”

<img width="974" height="403" alt="image" src="https://github.com/user-attachments/assets/4b88b10d-2313-4c77-92cf-d9955728c092" />
Ticket Escalation Scenario
•	User asks an out-of-scope question
•	System suggests ticket creation
•	User confirms → GitHub Issue is created

<img width="974" height="474" alt="image" src="https://github.com/user-attachments/assets/7e6210f5-9ca5-4ac0-90b6-bb342cd80ab2" />


<img width="974" height="647" alt="image" src="https://github.com/user-attachments/assets/e831263c-5e0e-4747-9ff9-a9088e750aa9" />
8. Conclusion
This project successfully demonstrates:
•	A production-ready RAG-based customer support system
•	Safe AI behavior with hallucination avoidance
•	Real-world ticket escalation using function calling
•	Deployment on Hugging Face Spaces
All business and technical requirements of the practical task have been fully implemented.
________________________________________
9. Links
•	Hugging Face Space:
https://kuchkarovaziz77-rag-support-capstone.hf.space
•	GitHub Repository: https://github.com/azizkuchkarov/cap.stone-pr-1-adv.gen.ai
