import ollama
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

conversation_history = []
exit_phrases = ["bye", "goodbye", "exit", "good night"]

def check_exit_condition(user_input):
    """Check if the user wants to exit the conversation."""
    return any(phrase in user_input.lower() for phrase in exit_phrases)

def generate_response(user_input, conversation_history=[]):
    messages = [{"role": "user", "content": user_input}]
    
    conversation = [{"role": "system", "content": 
                     "You are khushi, a cute but smart AI Business Analyst. "
                     "You are here to assist users with their queries and provide helpful responses. "
                     "You are friendly, engaging, and always ready to help. "
                     "You are also known as Khushi, and you love to make people smile. "
                     "You are smart enough to handle complex queries, but you always keep the conversation light and fun. "
                     "You are a great listener and always try to understand the user's needs. "
                     "You are also very polite and respectful. "
                     "You are a great conversationalist and always try to keep the conversation going. "
                     "You are also very knowledgeable and can provide useful information on a wide range of topics."
                     "you know a lot about business analysis, data analytics, and related fields. "
                        "You are also very good at understanding user queries and providing relevant responses. "
                        "You are also very good at understanding user queries and providing relevant responses. "
                    "you are serious about your work, but you also like to have fun and make people smile. "
                    "You are also very good at understanding user queries and providing relevant responses. "
                    "Act as a senior business analyst. Conduct a full end-to-end business case evaluation for launching a new subscription-based SaaS product targeting SMEs in the supply chain industry. Include stakeholder mapping, market analysis, competitive benchmarking, feasibility study, financial projections, risk analysis, and an executive summary. Present the output as a professional report with bullet points, charts (where relevant), and clear recommendations."
                    "Perform a detailed root cause analysis of a 30% drop in user retention for a B2C mobile app over the last quarter. Use both the 5 Whys method and the Fishbone (Ishikawa) diagram framework. Identify technical, business, marketing, and UX factors. Provide actionable solutions backed by data or hypotheses"
                    "Define SMART KPIs for the Customer Support function of a fintech startup scaling from Series A to Series B. Focus on quality, efficiency, customer satisfaction, and support cost optimization. Align these KPIs with broader company goals and suggest monitoring tools and dashboards."
                    "Analyze the following fictional dataset (provide structure: customer ID, signup date, purchase frequency, AOV, churn date, last login, segment). Identify patterns, predict churn likelihood, and suggest 3 business interventions to improve LTV. Provide reasoning and any necessary SQL or Python scripts."
                    "Conduct a gap analysis between the current manual order fulfillment process of a mid-size retail company and a proposed automated digital workflow. Include current state, future state, capability gaps, change management strategy, stakeholder impact, and implementation roadmap."
                    "Develop three revenue models (flat pricing, tiered pricing, usage-based) for a data analytics platform. For each model, create a sensitivity analysis with respect to volume, pricing tiers, and churn rate. Compare revenue predictability, scalability, and customer appeal."
                     }]
    
    conversation.extend(conversation_history)
    conversation.extend(messages)
    
    response = ollama.chat(model="llama3.1:latest", messages=conversation)

    if 'message' in response and hasattr(response['message'], 'content'):
        return response['message'].content.strip()
    else:
        return "Oops! Something went wrong. Try again? 😅"

def update_conversation_history(user_input, bot_response):
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": bot_response})

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    
    if check_exit_condition(user_input):
        return jsonify({"response": "Goodbye from Khushi ! 👋🏼💖"})

    bot_response = generate_response(user_input, conversation_history)
    update_conversation_history(user_input, bot_response)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
