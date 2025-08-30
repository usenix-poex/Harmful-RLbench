from openai import OpenAI
import json
import re
import os


# OpenAI client
client = OpenAI(
    api_key=""
)

def iterative_prompting(initial_prompt, examples_prompt, llm_model, max_iterations=10):
    """
    Use the iterative_prompting function to input initial prompts and examples to the model, 
    then append the model's output to the end of the prompt and continue the interaction 
    until the maximum number of iterations is reached or the model produces no new valid output.
    :param initial_prompt: str, initial complete prompt content
    :param examples_prompt: str, example prompt content
    :param max_iterations: int, maximum number of conversation rounds
    :return: None
    """
    
    for i in range(max_iterations):
        print(f"--- Round {i+1} conversation ---")
        # Build user prompt
        user_prompt = initial_prompt + examples_prompt

        # Build conversation context
        conversation = [
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        # Call OpenAI API to generate model output
        response = client.chat.completions.create(
            model=llm_model,
            messages=conversation,
        )

        try:
            # Get model output text
            model_reply = response.choices[0].message.content.strip()
            
            print(f"--- Round {i+1} output ---")
            print(model_reply)
            
            # Filter content between ```json and ```
            model_reply = re.search(r"```json(.*)```", model_reply, re.DOTALL).group(1)
            # Concatenate model output with current examples_prompt
            examples_prompt = examples_prompt.strip("```json").strip("```")
            # Convert to JSON
            model_reply_json = json.loads(model_reply)
            examples_prompt_json = json.loads(examples_prompt)
            # Add content from model_reply_json to examples_prompt_json
            examples_prompt_json.extend(model_reply_json)

            # Convert merged content to formatted JSON string
            examples_prompt = json.dumps(examples_prompt_json, indent=4, ensure_ascii=False)

            # Add markdown-style JSON code block markers
            examples_prompt = "```json\n" + examples_prompt + "\n```"
        # If an error occurs, print the specific error and continue to next iteration
        except Exception as e:
            print(f"==== Error occurred ==== {e}")
            continue
    
    print("==== Iteration completed ====")
    return examples_prompt


if __name__ == "__main__":
    llm_model = "gpt-4o"
    scene = "office" # bathroom, bedroom, dining-room, factory, kitchen, lab, living-room, office (8 scenes)
    harmful_harmless = "harmful" # harmful, harmless
    max_iterations = 3
    os.makedirs(f"./assets/{llm_model}", exist_ok=True)

    initial_prompt = open(f"./prompts/{harmful_harmless}_prompt.txt", "r").read()
    initial_prompt = initial_prompt.replace("{SCENE}", scene)
    examples_prompt = open(f"./prompts/{harmful_harmless}_{scene}_examples.txt", "r").read()

    examples_prompt = iterative_prompting(initial_prompt, examples_prompt, llm_model, max_iterations)

    with open(f"./assets/{llm_model}/{llm_model}_{harmful_harmless}_{scene}_examples.txt", "w") as f:
        f.write(examples_prompt)