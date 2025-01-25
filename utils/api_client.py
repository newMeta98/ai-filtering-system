from openai import OpenAI
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def product_filterLLM(message, knowledge):
    print("AI generating response...\n")
    api_key = os.getenv('DEEPSEEK_API_KEY')
    model = "deepseek-chat"
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    personal_info = "You are 'Amazon Restricted/Prohibited Products filter Agent'. Your job is to look at the 'Products titles' and carefully filter them using 'filtering knowledge'."
    user_message = [{"role": "user", "content": message}]
    messages = [
        {
            "role": "system",
            "content": personal_info + f"\nHere is the filtering knowledge you need to use to filter titles, filtering knowledge: {knowledge} \n"
                      f"Look at the filtering knowledge, and product titles to provide accurate filtration of restricted_products.\n"
                      """
                      EXAMPLE JSON OUTPUT:
                        {
                            "thinking_proces": "concise step by step filtering thinking proces for each title (make sure to first understand the product based on title, then go true filtering proces)",
                            "restricted_products": ["product_title1","product_title2", "product_title3"...]
                        }
                      """
        },
    ] + user_message

    try:
        # Call the DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )

        # Log the raw response for debugging
        raw_response = response.choices[0].message.content
        logging.info(f"Raw API Response: {raw_response}")

        # Parse the JSON response
        response_json = json.loads(raw_response)
        logging.info(f"Parsed JSON Response: {response_json}")

        return response_json
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        logging.error(f"Invalid JSON: {raw_response}")
        return None
    except Exception as e:
        logging.error(f"Error in product_filterLLM: {e}")
        return None