## 💡 Inspiration 💡
Peachy is the first Slack AI Assistant that implements Google’s latest PaLM 2 Model. Inspired by the PaLM 2 Model and its capabilities in doing complex tasks, we have created this tool to empower users to unleash the power of generative AI without leaving their Slack workspace. 

## 🍑 What Peachy does 🍑 
* Co-piloting Slack users in the completion of advanced reasoning tasks, from coding to drafting product roadmaps. 
* Being context-aware of user conversations. 
* Enabling users to customize the tonality of responses. 

## 🆕 NEW FEATURES (Aug 2023) 🆕
* Typing indicator
* Dynamic context awareness
* Automatic quit after inactivity

## Why integrate Google PaLM 2 on Slack?
* **Prospective user community**: We chose to build a Slack App because Slack is a popular all-in-one workplace communication tool. It is a chance to tap into a user population of business team collaborators that is tech-savvy, innovative, and value-conscious when it comes to productivity. 
* **Market Reach and Visibility for PaLM 2**: Existing generative AI assistants on Slack all implement ChatGPT. Integrating PaLM 2 into Slack potentially helps Google reach a broader user base and expand its market presence beyond existing products and services. 
* **Lab experiment for the new generation of search**: Peachy can become a segway into testing out generative AI-powered search engine features – in our project, we built a tone switch for users to receive responses in a more customized way. In a way, Peachy can be a good avenue to refine Google’s generative AI models and gain valuable insights into user preferences and interactions. 

## Why MongoDB?
* **Scalability and Performance**: MongoDB's horizontal scaling and document-based structure suited real-time chat interactions, ensuring smooth performance and accommodating data growth.
* **Schema Flexibility**: MongoDB's schema-less design allowed us to adapt quickly as features evolved, preventing database constraints from impeding our development progress.
* **Real-time Data Management**: MongoDB's fast read/write operations enabled us to maintain conversation context, providing timely AI responses within the dynamic Slack environment

## How we built it
Peachy was built using Google Generative AI and MongoDB, along with other technological components. The development process involved the following steps:

* Use Case Definition: We started the project by identifying the requirements and desired functionality of an AI Assistant within Slack. This included understanding the user needs, desired features, and integration points with Slack's APIs.

* Architecture Design: We designed an architecture that accommodates a three-tier app structure of Clients, Applications, and Build Processes. The Application tier consisted of a Slack app utilizing the Slack SDK for the frontend, Slack Event API and Google Generative AI API for middleware, and Slack App Socket for backend logic. MongoDB was chosen as the backend database to store user data for scalability and user analytics purposes in future development. 

* Integrating Generative AI: The Google Palm API, a generative AI product, was integrated into the Slack app to provide additional functionality and enhance the AI capabilities of the assistant. This integration allowed for intelligent responses, data analysis, or other AI-powered features within the assistant.

* CI/CD Pipeline Setup: A CI/CD pipeline was established using GitHub Actions. This pipeline included steps for code compilation, running tests, generating artifacts, and deploying the app to various environments. Secrets management was implemented using Dotenv to store sensitive information securely.

## Documentation Update
While our journey in ongoing development has been temporarily paused due to practical constraints, we are approaching this situation with proactive optimism. We had set ambitious goals for Peachy, and though we find ourselves on a temporary pause, we believe in the potential for future revival. Here's how we've adjusted our documentation to reflect our current status:

## Planned Next Steps (Original)
At the outset, our vision encompassed engaging in usability testing, enriching Peachy with more generative AI features, exploring the realm of Generative AI-powered search experiences, and meticulously addressing data governance in preparation for eventual app publishing.

## Adjusted Next Steps
Given the current context, our original roadmap for the future steps has been gracefully deferred. While our immediate momentum may be on hold, we remain actively engaged in shaping the path forward:

* **Usability Testing**: The invaluable step of usability testing has been temporarily deferred as we recalibrate our resources.
* **More Gen-AI Features**: Our fervor to elevate Peachy's AI capabilities and delve into the realm of generative AI-powered search experiences is temporarily in abeyance.
* **Data Governance & App Publishing**: Our efforts in ensuring data privacy and governance for future app publishing are presently paused.

As we navigate this phase, we're fueled by the belief that our journey with Peachy is far from over. We are exploring avenues for resurgence and are excited about the possibilities that lie ahead. While the current landscape has introduced a pause, we are dedicated to returning with renewed energy and creative solutions to bring Peachy's vision to fruition. Your support and interest have been invaluable, and we're committed to delivering a product that lives up to the excitement it has generated.

## Contact Us
Stay tuned for updates as we embrace the challenge to turn this pause into a launchpad for even greater achievements in the future.

Pamela Pan (pp452@cornell.edu)
Roman Chavex (rqc3@cornell.edu) 
