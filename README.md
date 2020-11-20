# An Dining Chatbot uses AWS services.
The dining chatbot is a web application hosted on AWS S3. The application components and structure is shown as blow:<br/>

<img src="https://github.com/YulongWang2020/AWSDiningChatbot/blob/main/architecture.jpg" alt="show" />


According to the answer from the chatbot, the backend will randomly search in the database for matching resturants.<br>
Then, the results will be SNS to the user phone.<br/>

#### Here is the demo:

<img src="https://github.com/YulongWang2020/AWSDiningChatbot/blob/main/demo.gif" alt="show" />

#### What I learned:
Let Api Gateway and CouldWatch Events trigger Lambda functions.<br>
Writing api using swager.<br>
Deploying api using Api Gateway.<br>
Building chatbot using Amazon Lex.<br>
Dynamodb data operations(boto3).<br>
ElasticSearch.<br>
S3 Static website hosting.<br>
Using SQS to decouple the application.<br>
SNS.<br>
  
